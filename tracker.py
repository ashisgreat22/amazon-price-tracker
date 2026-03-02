"""
Price Tracking Module
Logs historical price data for trend analysis.
"""

import os
import csv
import json
import logging
from datetime import datetime
from config import OUTPUT_DIR

logger = logging.getLogger(__name__)


HISTORY_FILE = os.path.join(OUTPUT_DIR, "price_history.csv")


def update_price_history(products, query):
    """Append current prices to the history file for tracking over time.
    
    Args:
        products: List of product dictionaries from scraper
        query: Original search query
    """
    file_exists = os.path.exists(HISTORY_FILE)
    
    fieldnames = ["date", "query", "asin", "name", "price", "rating", "reviews"]
    
    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for product in products:
            writer.writerow({
                "date": timestamp,
                "query": query,
                "asin": product.get("asin", ""),
                "name": product.get("name", ""),
                "price": product.get("price", ""),
                "rating": product.get("rating", ""),
                "reviews": product.get("reviews", ""),
            })
    
    logger.info(f"Price history updated: {HISTORY_FILE}")
    logger.info(f"Tracked {len(products)} products for query '{query}'")


def get_price_history(asin=None, query=None):
    """Read price history from the tracking file.
    
    Args:
        asin: Filter by ASIN (optional)
        query: Filter by search query (optional)
    
    Returns:
        list: Historical price records
    """
    if not os.path.exists(HISTORY_FILE):
        logger.warning(f"No price history found at {HISTORY_FILE}. Run scraper with --track first.")
        return []
    
    records = []
    
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if asin and row.get("asin") != asin:
                continue
            if query and row.get("query") != query:
                continue
            records.append(row)
    
    return records


def print_price_summary(query):
    """Print a summary of price changes for a query.
    
    Args:
        query: Search query to summarize
    """
    records = get_price_history(query=query)
    
    if not records:
        logger.warning(f"No history found for query: '{query}'")
        return
    
    # Group by ASIN
    products = {}
    for record in records:
        asin = record.get("asin", "unknown")
        if asin not in products:
            products[asin] = {
                "name": record["name"],
                "prices": [],
            }
        
        price = record.get("price")
        if price:
            try:
                products[asin]["prices"].append(float(price))
            except ValueError:
                pass
    
    print(f"\n📊 Price Summary for '{query}'")
    print("=" * 60)
    
    for asin, data in products.items():
        if data["prices"]:
            current = data["prices"][-1]
            lowest = min(data["prices"])
            highest = max(data["prices"])
            
            name = data["name"][:40] + "..." if len(data["name"]) > 40 else data["name"]
            
            print(f"\n  {name}")
            print(f"    Current: ${current:.2f} | Low: ${lowest:.2f} | High: ${highest:.2f}")
            
            if len(data["prices"]) > 1:
                change = current - data["prices"][0]
                direction = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                print(f"    Trend: {direction} ${abs(change):.2f} ({len(data['prices'])} data points)")
    
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        print_price_summary(sys.argv[1])
    else:
        print("Usage: python tracker.py <search_query>")
        print("Example: python tracker.py 'wireless headphones'")
