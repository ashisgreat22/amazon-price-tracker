import pytest
import requests_mock
from bs4 import BeautifulSoup
from scraper import parse_product, scrape_page
from config import BASE_URL, SELECTORS

def test_parse_product():
    # Mocking Amazon's HTML structure based on config.SELECTORS
    html = f"""
    <div data-component-type="s-search-result" data-asin="B00X1Y2Z3">
        <h2>
            <a href="/product-link">
                <span>Test Product Name</span>
            </a>
        </h2>
        <span class="a-price-whole">49.</span>
        <span class="a-price-fraction">99</span>
        <span class="a-icon-alt">4.5 out of 5 stars</span>
        <span class="a-size-base s-underline-text">12,345</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    item = soup.select_one(SELECTORS["product_container"])
    
    product = parse_product(item)
    
    assert product["name"] == "Test Product Name"
    assert product["price"] == 49.99
    assert product["asin"] == "B00X1Y2Z3"
    assert product["rating"] == 4.5
    assert product["reviews"] == 12345
    assert "amazon.com/product-link" in product["url"]

def test_scrape_page_success():
    with requests_mock.Mocker() as m:
        # Mock HTML response with one product following config.SELECTORS
        html_response = f"""
        <html>
            <body>
                <div data-component-type="s-search-result" data-asin="B00TEST">
                    <h2>
                        <a href="/test-url">
                            <span>Test Scrape Page Product</span>
                        </a>
                    </h2>
                    <span class="a-price-whole">10.</span>
                    <span class="a-price-fraction">00</span>
                </div>
            </body>
        </html>
        """
        m.get(BASE_URL, text=html_response)
        
        products = scrape_page("test query", page=1)
        
        assert len(products) == 1
        assert products[0]["name"] == "Test Scrape Page Product"
        assert products[0]["price"] == 10.0
        assert products[0]["asin"] == "B00TEST"

def test_scrape_page_empty():
    with requests_mock.Mocker() as m:
        m.get(BASE_URL, text="<html><body>No products here</body></html>")
        products = scrape_page("test query", page=1)
        assert len(products) == 0
