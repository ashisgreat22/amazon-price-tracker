"""
Configuration settings for Amazon Product Scraper
"""

# Request settings
REQUEST_DELAY_MIN = 2  # Minimum delay between requests (seconds)
REQUEST_DELAY_MAX = 5  # Maximum delay between requests (seconds)
MAX_RETRIES = 3        # Maximum retry attempts per page
TIMEOUT = 15           # Request timeout in seconds

# Output settings
OUTPUT_DIR = "data"
DEFAULT_FORMAT = "csv"

# User-Agent rotation list
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# Amazon base URL
BASE_URL = "https://www.amazon.com/s"

# CSS Selectors for parsing
SELECTORS = {
    "product_container": "div[data-component-type='s-search-result']",
    "title": "h2 a span",
    "price_whole": "span.a-price-whole",
    "price_fraction": "span.a-price-fraction",
    "rating": "span.a-icon-alt",
    "review_count": "span.a-size-base.s-underline-text",
    "url": "h2 a",
    "asin": "data-asin",
}
