import warnings
warnings.filterwarnings("ignore", message="Glyph.*missing from font")

import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from urllib.parse import urljoin
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.family'] = 'DejaVu Sans'

BASE_URL = "https://books.toscrape.com/catalogue/"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def get_book_links(page_url):
    soup = get_soup(page_url)
    book_links = []
    for article in soup.select('article.product_pod h3 a'):
        rel_url = article.get('href')
        full_url = urljoin(page_url, rel_url)
        book_links.append(full_url)
    return book_links

def parse_book_page(book_url):
    soup = get_soup(book_url)
    title = soup.h1.text.strip()
    price = soup.select_one("p.price_color").text.strip()
    availability = soup.select_one("p.instock.availability").text.strip()
    description_tag = soup.select_one("div#product_description")
    description_text = description_tag.find_next_sibling("p").text.strip() if description_tag else "No Description"
    category = soup.select("ul.breadcrumb li")[-2].text.strip()
    raiting = soup.select_one("p.star-rating")["class"][1]
    return {
        'title': title,
        'price': price,
        'availability': availability,
        'raiting': raiting,
        'description': description_text,
        'category': category,
        'url': book_url
    }

def scrap_all_books():
    all_books = []
    limit = int(input("Books from how many pages do you want to scrap? "))
    print("Scraping in progress...")
    for i in range(1, limit + 1):
        page_url = f"{BASE_URL}page-{i}.html"
        book_links = get_book_links(page_url)
        for link in book_links:
            all_books.append(parse_book_page(link))
            time.sleep(0.5)
    return all_books

def save_to_db_and_csv(books, dbname="books.db", csvname="books.csv"):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS books(
        title TEXT,
        price TEXT,
        availability TEXT,
        raiting TEXT,
        description TEXT,
        category TEXT,
        url TEXT
    )''')
    cur.execute("DELETE FROM books")
    for book in books:
        cur.execute('''INSERT INTO books VALUES(?,?,?,?,?,?,?)''',
                    (book['title'], book['price'], book['availability'],
                     book['raiting'], book['description'], book['category'], book['url']))
    conn.commit()
    conn.close()
    pd.DataFrame(books).to_csv(csvname, index=False)

def run_queries():
    conn = sqlite3.connect("books.db")
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()

    df['price'] = df['price'].str.replace(r'[^\d.]', '', regex=True).astype(float)

    top5_expensive = df.sort_values(by='price', ascending=False).head(5)
    avg_price = df['price'].mean()
    count_by_rating = df['raiting'].value_counts()
    count_by_category = df['category'].value_counts()
    python_books = df[df['title'].str.contains("Python", case=False, na=False)]
    in_stock_books = df[df['availability'].str.contains("In stock", case=False, na=False)]
    out_of_stock_books = df[~df['availability'].str.contains("In stock", case=False, na=False)]
    missing_desc_count = (df['description'].str.strip().str.lower() == 'no description').sum()
    most_common_rating = df['raiting'].mode()[0]
    unique_categories_count = df['category'].nunique()
    unique_categories_list = df['category'].unique()
    sorted_books = df.sort_values(by='title')
    df['desc_len'] = df['description'].str.len()
    longest_desc_books = df.sort_values(by='desc_len', ascending=False)
    cheapest_per_category = df.loc[df.groupby('category')['price'].idxmin()]
    top3_per_category = (
        df.groupby('category', group_keys=False)
          .apply(lambda x: x.loc[x['price'].nlargest(3).index], include_groups=False)
          .reset_index(drop=True)
    )
    long_title_books = df[df['title'].str.len() > 50]
    df['is_expensive'] = df['price'] > 40
    expensive_count_by_category = df[df['is_expensive']].groupby('category').size()
    in_stock_expensive = df[(df['is_expensive']) & (df['availability'].str.contains("In stock", case=False, na=False))]
    in_stock_expensive.to_csv("in_stock_expensive_books.csv", index=False)

    print("\n=== QUERY RESULTS ===")
    print("Top 5 Most Expensive:\n", top5_expensive[['title','price']])
    print("\nAverage Price:", avg_price)
    print("\nBooks by Rating:\n", count_by_rating)
    print("\nBooks by Category:\n", count_by_category)
    print("\nMissing Descriptions:", missing_desc_count)
    print("\nMost Common Rating:", most_common_rating)
    print("\nUnique Categories Count:", unique_categories_count)
    print("\nUnique Categories List:", unique_categories_list)

def run_plots():
    df = pd.read_csv("books.csv")
    df['price'] = df['price'].str.replace('[^0-9.]', '', regex=True).astype(float)

    df.groupby('category')['price'].mean().sort_values().plot(kind='bar', figsize=(10,5), title="Average Price per Category")
    plt.ylabel("Average Price (£)")
    plt.show()

    df['raiting'].value_counts().plot(kind='bar', title="Books by Rating")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.show()

    df['in_stock'] = df['availability'].str.contains("In stock", case=False, na=False)
    df['in_stock'].value_counts().plot(kind='bar', title="In Stock vs Out of Stock")
    plt.xticks([0,1], ['In Stock', 'Out of Stock'], rotation=0)
    plt.show()

    df.nlargest(10, 'price').set_index('title')['price'].plot(kind='barh', title="Top 10 Most Expensive Books")
    plt.xlabel("Price (£)")
    plt.show()

    df['category'].value_counts().head(10).plot(kind='bar', title="Top 10 Categories by Book Count")
    plt.ylabel("Count")
    plt.show()

    df['price'].plot(kind='hist', bins=20, title="Price Distribution")
    plt.xlabel("Price (£)")
    plt.show()

    df['title_length'] = df['title'].str.len()
    df['title_length'].plot(kind='hist', bins=20, title="Title Length Distribution")
    plt.xlabel("Title Length (characters)")
    plt.show()

    df.boxplot(column='price', by='raiting', grid=False)
    plt.title("Price by Rating")
    plt.suptitle("")
    plt.xlabel("Rating")
    plt.ylabel("Price (£)")
    plt.show()

    thresholds = [20, 40, 60]
    counts = {f">{t}": (df['price'] > t).sum() for t in thresholds}
    pd.Series(counts).plot(kind='bar', title="Books Over Price Thresholds")
    plt.ylabel("Count")
    plt.show()

    df[df['raiting'] == 'Five']['category'].value_counts().head(10).plot(kind='bar', title="Top Categories with Most 5-Star Books")
    plt.ylabel("Count")
    plt.show()

    df['desc_length'] = df['description'].str.len()
    df.nlargest(10, 'desc_length').set_index('title')['desc_length'].plot(kind='barh', title="Top 10 Longest Descriptions")
    plt.xlabel("Description Length")
    plt.show()

    df['category'].value_counts().head(6).plot(kind='pie', autopct='%1.1f%%', title="Top 6 Categories")
    plt.ylabel("")
    plt.show()

    df['raiting'].value_counts().sort_index().plot(kind='line', marker='o', title="Books per Rating")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.show()

    df.groupby('raiting')['price'].mean().plot(kind='bar', title="Average Price by Rating")
    plt.ylabel("Average Price (£)")
    plt.show()

if __name__ == "__main__":
    books = scrap_all_books()
    print("Scraping done. Saving data in DB and CSV...")
    save_to_db_and_csv(books)
    print("Data saved successfully.")

    run_queries()
    run_plots()
