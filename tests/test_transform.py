import pandas as pd
import pytest
from utils.transform import clean_price, clean_rating, clean_colors, transform

def test_clean_price_basic():
    assert clean_price("$10") == 160000
    assert clean_price("USD 12.34") == int(12.34 * 16000)
    assert clean_price("7.5") == int(7.5 * 16000)

def test_clean_price_unavailable_and_invalid():
    assert clean_price("Unavailable") is None
    assert clean_price("") is None
    assert clean_price("no digits here") is None

def test_clean_rating_and_colors():
    assert clean_rating("4.5 out of 5") == 4.5
    assert clean_rating("5") == 5.0
    assert clean_rating("no rating") is None

    assert clean_colors("3 colors") == 3
    assert clean_colors("0") == 0
    assert clean_colors("n/a") is None

def test_transform_integration_and_dedup_dropna():
    data = [
        {"title": "A", "price": "$10", "rating": "4.5", "colors": "3 colors"},
        {"title": "B", "price": "Unavailable", "rating": "No rating", "colors": "N/A"},
        {"title": "A", "price": "$10.00", "rating": "4.5", "colors": "3"},
        {"title": "C", "price": "USD 7.5", "rating": "4", "colors": "2 colors"},
        {"title": "NoPrice", "price": "", "rating": "5", "colors": "1"},
        {"title": None, "price": "$1", "rating": "5", "colors": "1"},
    ]

    df = transform(data)
    assert isinstance(df, pd.DataFrame)

    # Rows with unavailable/empty price or missing title should be dropped.
    titles = set(df["title"].tolist())
    assert titles == {"A", "C"}

    # Duplicate (A with same price) should be removed; only one A remains
    assert df[df["title"] == "A"].shape[0] == 1

    # Prices converted and scaled correctly
    assert int(df.loc[df["title"] == "A", "price"].item()) == 160000
    assert int(df.loc[df["title"] == "C", "price"].item()) == int(7.5 * 16000)

    # Ratings and colors parsed correctly
    assert pytest.approx(float(df.loc[df["title"] == "A", "rating"].item())) == 4.5
    assert int(df.loc[df["title"] == "A", "colors"].item()) == 3