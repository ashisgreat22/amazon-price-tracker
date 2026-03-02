# 🕷️ Amazon Product Scraper & Price Tracker

A Python web scraping tool that extracts product data from Amazon search results and tracks prices over time. Outputs clean, structured data in CSV and JSON formats.

## Features

- 🔍 Scrape Amazon search results for any keyword
- 📊 Extract product name, price, rating, review count, and URL
- 💾 Export to CSV and JSON
- 📈 Price tracking with historical data logging
- ⏱️ Configurable delays to respect rate limits
- 🛡️ Rotating User-Agent headers
- 📋 Clean, well-documented code

## Installation

```bash
git clone https://github.com/ashie10/amazon-price-tracker.git
cd amazon-price-tracker
pip install -r requirements.txt
```

## Usage

### Basic Scraping

```bash
python scraper.py --query "wireless headphones" --pages 3
```

### With Price Tracking

```bash
python scraper.py --query "wireless headphones" --pages 3 --track
```

### Export Options

```bash
# CSV output (default)
python scraper.py --query "laptop stand" --output results.csv

# JSON output
python scraper.py --query "laptop stand" --output results.json --format json
```

## Output Example

| Product Name | Price | Rating | Reviews | URL |
|---|---|---|---|---|
| Sony WH-1000XM5 | $348.00 | 4.8 | 12,453 | amazon.com/dp/... |
| Bose QC Ultra | $299.00 | 4.3 | 8,291 | amazon.com/dp/... |
| Apple AirPods Pro 2 | $189.99 | 4.7 | 45,102 | amazon.com/dp/... |

## Project Structure

```
amazon-price-tracker/
├── scraper.py          # Main scraper script
├── tracker.py          # Price tracking module
├── utils.py            # Helper functions
├── config.py           # Configuration settings
├── requirements.txt    # Dependencies
├── data/               # Output directory
│   └── .gitkeep
└── README.md
```

## Configuration

Edit `config.py` to adjust:

- Request delays
- Number of retries
- Output directory
- User-Agent rotation list

## Disclaimer

This tool is for educational and personal use only. Always check and comply with a website's Terms of Service and robots.txt before scraping. Use responsibly.

## License

MIT License
