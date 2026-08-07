import pandas as pd
import requests
from bs4 import BeautifulSoup


URL = "https://books.toscrape.com/"


def extract_books():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    books = []

    for item in soup.select("article.product_pod"):
        title = item.select_one("h3 a")["title"]
        price_text = item.select_one(".price_color").get_text(strip=True)
        availability = item.select_one(".availability").get_text(strip=True)

        books.append({
            "title": title,
            "price": price_text,
            "availability": availability,
        })

    return pd.DataFrame(books)


def clean_data(df):
    cleaned = df.copy()

    cleaned["price"] = (
        cleaned["price"]
        .str.replace("£", "", regex=False)
        .astype(float)
    )

    cleaned["title"] = cleaned["title"].str.strip()
    cleaned["availability"] = cleaned["availability"].str.strip()

    return cleaned


def main():
    print("Starting extraction...")

    books = extract_books()
    books = clean_data(books)

    books.to_csv("books.csv", index=False)
    books.to_excel("books_report.xlsx", index=False)

    print(f"{len(books)} books extracted.")
    print("Files created: books.csv and books_report.xlsx")


if __name__ == "__main__":
    main()