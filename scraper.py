"""
Amazon Product Scraper
Extracts product data from Amazon search results.
"""

import argparse
import csv
import json
import sys
import os
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime

from config import BASE_URL, SELECTORS, MAX_RETRIES, TIMEOUT, OUTPUT_DIR, DEFAULT_FORMAT
from utils import (
    setup_logging,
    get_random_headers,
    random_delay,
    clean_price,
    clean_rating,
    clean_review_count,
    ensure_output_dir,
    generate_filename,
)

logger = logging.getLogger(__name__)


def scrape_page(query, page=1):
    """Scrape a single page of Amazon search results.
    
    Args:
        query: Search query string
        page: Page number to scrape
    
    Returns:
        list: List of product dictionaries
    """
    params = {
        "k": query,
        "page": page,
    }
    
    products = []
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                BASE_URL,
                params=params,
                headers=get_random_headers(),
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select(SELECTORS["product_container"])
            
            if not items:
                logger.warning(f"No products found on page {page} (attempt {attempt + 1})")
                if attempt < MAX_RETRIES - 1:
                    random_delay()
                    continue
                break
            
            for item in items:
                product = parse_product(item)
                if product and product["name"]:
                    products.append(product)
            
            logger.info(f"Page {page}: Found {len(products)} products")
            break
            
        except requests.RequestException as e:
            logger.error(f"Page {page}: Request failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                random_delay()
    
    return products


def parse_product(item):
    """Parse a single product element from the search results.
    
    Args:
        item: BeautifulSoup element for a single product
    
    Returns:
        dict: Product data with name, price, rating, reviews, url, asin
    """
    product = {
        "name": None,
        "price": None,
        "rating": None,
        "reviews": None,
        "url": None,
        "asin": None,
        "scraped_at": datetime.now().isoformat(),
    }
    
    # Product name
    title_el = item.select_one(SELECTORS["title"])
    if title_el:
        product["name"] = title_el.get_text(strip=True)
    
    # Price
    price_whole = item.select_one(SELECTORS["price_whole"])
    price_fraction = item.select_one(SELECTORS["price_fraction"])
    if price_whole:
        price_text = price_whole.get_text(strip=True)
        if price_fraction:
            price_text += price_fraction.get_text(strip=True)
        product["price"] = clean_price(price_text)
    
    # Rating
    rating_el = item.select_one(SELECTORS["rating"])
    if rating_el:
        product["rating"] = clean_rating(rating_el.get_text(strip=True))
    
    # Review count
    review_el = item.select_one(SELECTORS["review_count"])
    if review_el:
        product["reviews"] = clean_review_count(review_el.get_text(strip=True))
    
    # URL and ASIN
    url_el = item.select_one(SELECTORS["url"])
    if url_el and url_el.get("href"):
        href = url_el["href"]
        if href.startswith("/"):
            href = f"https://www.amazon.com{href}"
        product["url"] = href
    
    asin = item.get(SELECTORS["asin"])
    if asin:
        product["asin"] = asin
    
    return product


def scrape_amazon(query, pages=1):
    """Scrape multiple pages of Amazon search results.
    
    Args:
        query: Search query string
        pages: Number of pages to scrape
    
    Returns:
        list: All scraped products
    """
    logger.info(f"Searching Amazon for: '{query}'")
    logger.info(f"Pages to scrape: {pages}")
    
    all_products = []
    
    for page in range(1, pages + 1):
        products = scrape_page(query, page)
        all_products.extend(products)
        
        if page < pages:
            random_delay()
    
    logger.info(f"Total products scraped: {len(all_products)}")
    return all_products


def save_csv(products, filepath):
    """Save products to a CSV file.
    
    Args:
        products: List of product dictionaries
        filepath: Output file path
    """
    if not products:
        logger.warning("No products to save")
        return
    
    fieldnames = ["name", "price", "rating", "reviews", "url", "asin", "scraped_at"]
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    
    logger.info(f"Saved {len(products)} products to {filepath}")


def save_json(products, filepath):
    """Save products to a JSON file.
    
    Args:
        products: List of product dictionaries
        filepath: Output file path
    """
    if not products:
        logger.warning("No products to save")
        return
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(products)} products to {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Amazon Product Scraper - Extract product data from Amazon search results"
    )
    parser.add_argument(
        "--query", "-q",
        required=True,
        help="Search query (e.g., 'wireless headphones')"
    )
    parser.add_argument(
        "--pages", "-p",
        type=int,
        default=1,
        help="Number of pages to scrape (default: 1)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output filename (auto-generated if not specified)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["csv", "json"],
        default=DEFAULT_FORMAT,
        help="Output format (default: csv)"
    )
    parser.add_argument(
        "--track",
        action="store_true",
        help="Enable price tracking (appends to existing data)"
    )
    
    args = parser.parse_args()
    
    setup_logging()
    ensure_output_dir()
    
    # Scrape products
    products = scrape_amazon(args.query, args.pages)
    
    if not products:
        logger.error("No products found. Try a different search query.")
        sys.exit(1)
    
    # Determine output path
    if args.output:
        filepath = os.path.join(OUTPUT_DIR, args.output)
    else:
        filepath = os.path.join(OUTPUT_DIR, generate_filename(args.query, args.format))
    
    # Save results
    if args.format == "json":
        save_json(products, filepath)
    else:
        save_csv(products, filepath)
    
    # Price tracking
    if args.track:
        from tracker import update_price_history
        update_price_history(products, args.query)
    
    logger.info("Done!")


if __name__ == "__main__":
    main()
