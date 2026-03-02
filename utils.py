"""
Utility functions for Amazon Product Scraper
"""

import random
import time
import re
import os
from config import USER_AGENTS, REQUEST_DELAY_MIN, REQUEST_DELAY_MAX, OUTPUT_DIR


def get_random_headers():
    """Return request headers with a random User-Agent."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


def random_delay():
    """Sleep for a random duration to avoid rate limiting."""
    delay = random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
    time.sleep(delay)


def clean_price(price_text):
    """Extract numeric price from text.
    
    Args:
        price_text: Raw price string (e.g., '$34.99', '34.99')
    
    Returns:
        float or None: Cleaned price value
    """
    if not price_text:
        return None
    
    match = re.search(r'(\d+[.,]?\d*)', price_text.replace(',', ''))
    if match:
        return float(match.group(1))
    return None


def clean_rating(rating_text):
    """Extract numeric rating from text like '4.5 out of 5 stars'.
    
    Args:
        rating_text: Raw rating string
    
    Returns:
        float or None: Rating value (0-5)
    """
    if not rating_text:
        return None
    
    match = re.search(r'(\d+\.?\d*)', rating_text)
    if match:
        return float(match.group(1))
    return None


def clean_review_count(review_text):
    """Extract review count from text like '12,453'.
    
    Args:
        review_text: Raw review count string
    
    Returns:
        int or None: Number of reviews
    """
    if not review_text:
        return None
    
    cleaned = re.sub(r'[^\d]', '', review_text)
    if cleaned:
        return int(cleaned)
    return None


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_filename(query, extension="csv"):
    """Generate a timestamped filename based on the search query.
    
    Args:
        query: Search query string
        extension: File extension (csv, json)
    
    Returns:
        str: Generated filename
    """
    from datetime import datetime
    
    safe_query = re.sub(r'[^\w\s-]', '', query).strip().replace(' ', '_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{safe_query}_{timestamp}.{extension}"
