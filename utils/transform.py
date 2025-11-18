import pandas as pd
import re

USD_TO_IDR = 16000

def clean_price(price):
    if "Unavailable" in price:
        return None
    match = re.search(r"(\d+(\.\d+)?)", price)
    if not match:
        return None
    usd = float(match.group(1))
    return int(usd * USD_TO_IDR)


def clean_rating(rating):
    match = re.search(r"(\d+(\.\d+)?)", rating)
    if not match:
        return None
    return float(match.group(1))


def clean_colors(colors):
    match = re.search(r"(\d+)", colors)
    return int(match.group(1)) if match else None


def transform(data: list):
    df = pd.DataFrame(data)

    df["price"] = df["price"].apply(clean_price)
    df["rating"] = df["rating"].apply(clean_rating)
    df["colors"] = df["colors"].apply(clean_colors)

    df = df.dropna(subset=["title", "price"])

    df = df.drop_duplicates(subset=["title", "price"], keep="first")

    return df
