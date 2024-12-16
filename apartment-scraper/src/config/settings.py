# Configuration settings for the Apartment Scraper

# Web driver options
WEBDRIVER_OPTIONS = {
    'headless': True,  # Run in headless mode for faster scraping
    'timeout': 10      # Timeout for web driver operations
}

# Constants
DEPOSIT_AMOUNT = 10000  # Default deposit amount for apartments
BASE_URL = 'https://joinlifex.com'  # Base URL for apartment listings