# ScrapeTheBooks

A Python-based web scraping project that extracts book information from a website, processes the collected data, and stores the results in CSV and SQLite database formats.

## About the Project

ScrapeTheBooks is a web scraping application developed using Python. It collects book-related information from web pages and processes the extracted data using Python libraries.

The project demonstrates:

- Web scraping
- HTML parsing
- Data extraction
- Data filtering
- CSV file handling
- SQLite database storage

## Features

- Extracts book information from web pages
- Parses HTML content using BeautifulSoup
- Processes scraped data using Python
- Stores scraped data in CSV format
- Stores data in an SQLite database
- Filters books based on selected conditions
- Generates a separate CSV file for filtered results

## Technologies Used

- Python
- BeautifulSoup
- Pandas
- SQLite
- CSV

## Project Structure

```text
ScrapeTheBooks/
│
├── BookScraper.py
├── books.csv
├── in_stock_expensive_books.csv
├── books.db
├── .gitignore
└── .idea/
```

## Files Description

| File | Description |
|------|-------------|
| `BookScraper.py` | Main Python script for web scraping and data processing |
| `books.csv` | CSV file containing the scraped book data |
| `in_stock_expensive_books.csv` | Filtered book data based on availability and price |
| `books.db` | SQLite database containing stored book data |
| `.gitignore` | Specifies files and directories ignored by Git |

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/saikollu2006-crypto/ScrapeTheBooks.git
```

### 2. Navigate to the Project Directory

```bash
cd ScrapeTheBooks
```

### 3. Install Required Libraries

```bash
pip install requests beautifulsoup4 pandas
```

### 4. Run the Scraper

```bash
python BookScraper.py
```

## Output

After running the program, the extracted data can be stored in:

- `books.csv`
- `books.db`

Filtered results are stored in:

- `in_stock_expensive_books.csv`

## Learning Outcomes

This project helped in understanding:

- Python web scraping techniques
- HTML and DOM structure
- Data extraction using BeautifulSoup
- Data processing using Pandas
- Working with CSV files
- SQLite database operations
- Automating data collection from websites

## Future Improvements

- Add support for scraping multiple pages automatically
- Add error handling for network failures
- Add logging for scraping activities
- Add more filtering and sorting options
- Export data to additional formats
- Create a graphical user interface for the scraper

## Author

**Kollu Phani Sai Ganesh**

B.Tech – Computer Science and Information Technology

Presidency University, Bengaluru

## License

This project is created for educational and learning purposes.
