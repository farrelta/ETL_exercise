import requests
from bs4 import BeautifulSoup

BASE_URL = "https://fashion-studio.dicoding.dev"

def get_page_url(page_number: int):
    """Return correct URL depending on page number."""
    if page_number == 1: 
        return BASE_URL                     
    return f"{BASE_URL}/page{page_number}"  


def extract_page(page_number: int):
    """
    Extract product data from one page.
    """
    url = get_page_url(page_number)
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.select(".collection-card")
    products = []

    for card in cards:

        # TITLE
        title = card.select_one(".product-title").text.strip()

        # PRICE
        price_tag = card.select_one(".price")
        price = price_tag.text.strip() if price_tag else "Price Unavailable"

        # RATING
        rating_tag = card.find(string=lambda t: "Rating" in t)
        rating = rating_tag.strip() if rating_tag else "Not Rated"

        # COLORS
        colors_tag = card.find(string=lambda t: "Colors" in t)
        colors = colors_tag.strip() if colors_tag else "0 Colors"

        # SIZE
        size_tag = card.find(string=lambda t: "Size:" in t)
        size = size_tag.replace("Size: ", "").strip() if size_tag else "Unknown"

        # GENDER
        gender_tag = card.find(string=lambda t: "Gender:" in t)
        gender = gender_tag.replace("Gender: ", "").strip() if gender_tag else "Unknown"

        products.append({
            "title": title,
            "price": price,
            "rating": rating,
            "colors": colors,
            "size": size,
            "gender": gender,
        })

    return products


def extract_all(start_page=1, end_page=50):
    """Extract multiple pages."""
    all_data = []

    for page in range(start_page, end_page + 1):
        try:
            print(f"Extracting page {page}...")
            data = extract_page(page)
            all_data.extend(data)
        except Exception as e:
            print(f"Error at page {page}: {e}")

    return all_data
