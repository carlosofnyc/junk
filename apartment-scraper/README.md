# README.md

# Apartment Scraper

This project is a Python-based web scraper designed to extract apartment data from multiple URLs. It utilizes Selenium for web automation and pandas for data manipulation, and it can store the scraped data in a Snowflake database.

## Features

- Scrapes apartment listings from specified URLs.
- Extracts detailed information about each apartment, including rent, size, and availability.
- Supports multiple URLs for scraping in a single run.
- Saves the scraped data to a Snowflake database and exports it to Excel.

## Project Structure

```
apartment-scraper
├── src
│   ├── scraper
│   │   ├── __init__.py
│   │   ├── apartment_scraper.py
│   │   └── utils.py
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database
│   │   ├── __init__.py
│   │   └── snowflake_connector.py
│   └── main.py
├── tests
│   ├── __init__.py
│   └── test_scraper.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/apartment-scraper.git
   cd apartment-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the scraper, execute the following command in your terminal:

```
python src/main.py <url1> <url2> ...
```

Replace `<url1>`, `<url2>`, etc., with the URLs you want to scrape.

## Configuration

Configuration settings can be adjusted in `src/config/settings.py`. This includes web driver options and other constants used throughout the project.

## Testing

Unit tests for the scraper can be found in the `tests` directory. To run the tests, use:

```
pytest tests
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.