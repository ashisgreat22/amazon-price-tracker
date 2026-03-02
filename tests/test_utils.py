import pytest
from utils import clean_price, clean_rating, clean_review_count, generate_filename

def test_clean_price():
    assert clean_price("$34.99") == 34.99
    assert clean_price("34.99") == 34.99
    assert clean_price("1,234.56") == 1234.56
    assert clean_price("$1,234") == 1234.0
    assert clean_price("") is None
    assert clean_price(None) is None

def test_clean_rating():
    assert clean_rating("4.5 out of 5 stars") == 4.5
    assert clean_rating("4.5") == 4.5
    assert clean_rating("3 out of 5 stars") == 3.0
    assert clean_rating("") is None
    assert clean_rating(None) is None

def test_clean_review_count():
    assert clean_review_count("12,453") == 12453
    assert clean_review_count("12453 reviews") == 12453
    assert clean_review_count("0") == 0
    assert clean_review_count("") is None
    assert clean_review_count(None) is None

def test_generate_filename():
    filename = generate_filename("gaming mouse", "json")
    assert filename.startswith("gaming_mouse_")
    assert filename.endswith(".json")
    
    filename_complex = generate_filename("Wireless @ Headset!", "csv")
    assert "Wireless" in filename_complex
    assert "Headset" in filename_complex
    assert "@" not in filename_complex
    assert "!" not in filename_complex
