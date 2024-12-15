from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import json
import logging
import time
from typing import List, Dict, Any, Optional
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def retry_on_exception(retries: int = 3, delay: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries - 1:
                        raise
                    logging.warning(f"Attempt {i + 1} failed: {e}. Retrying...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class ApartmentScraper:
    def __init__(self):
        self.driver = None
        self.deposit = 10000

    def init_driver(self):
        if not self.driver:
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        return self.driver

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    @retry_on_exception()
    def get_apartment_links(self) -> List[str]:
        driver = self.init_driver()
        links = []
        try:
            driver.get('https://joinlifex.com/copenhagen/homes')
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/copenhagen/homes/']"))
            )
            links = [elem.get_attribute('href') for elem in elements]
            logging.info(f"Found {len(links)} apartment links")
            return links
        except Exception as e:
            logging.error(f"Error getting apartment links: {e}")
            raise

    def extract_apartment_info(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            listing = data['props']['pageProps']['listing']
            rooms_info = []
            
            for unit in listing.get('bookableUnits', []):
                room = unit['room']
                rent = unit['rent']
                
                # Calculate move-in costs
                total_move_in = self.deposit + (2 * rent)  # Deposit + first and last month
                
                room_info = {
                    'Room Name': f"Room {room['name']}",
                    'Monthly Rent': rent,
                    'Deposit': self.deposit,
                    'First Month Rent': rent,
                    'Last Month Rent': rent,
                    'Total Move In Cost': total_move_in,
                    'Size': f"{room['roomAttributes']['size']}m²",
                    'Furnished': 'Yes' if room['roomAttributes'].get('furnished') else 'No',
                    'Desk': 'Yes' if room['roomAttributes'].get('desk') else 'No',
                    'TV': 'Yes' if room['roomAttributes'].get('tv') else 'No',
                    'Private Balcony': 'Yes' if room['roomAttributes'].get('privateBalcony') else 'No',
                    'Ensuite Bathroom': 'Yes' if room['roomAttributes'].get('ensuiteBathroom') else 'No',
                    'Available': 'Yes' if unit.get('isAvailable') else 'No',
                    'Move In Date': unit.get('moveInDate', 'Not specified')
                }
                rooms_info.append(room_info)
            
            # Calculate availability status
            has_available_rooms = any(room['Available'] == 'Yes' for room in rooms_info)
            available_rooms_count = sum(1 for room in rooms_info if room['Available'] == 'Yes')
            
            return {
                'Apartment Name': listing['apartmentName'],
                'Apartment Size': listing['apartmentSize'],
                'Min Price': listing['minPrice'],
                'Starting Price': listing['startingPrice'],
                'Total Rooms': listing['totalRooms'],
                'Suburb': listing['apartmentSuburb'],
                'City': listing['cityName'],
                'Availability': 'Available' if has_available_rooms else 'Not Available',
                'Available Rooms': available_rooms_count,
                'Deposit Required': self.deposit,
                'Rooms': rooms_info
            }
        except KeyError as e:
            logging.error(f"Error extracting apartment info: {e}")
            return None

def main():
    scraper = ApartmentScraper()
    try:
        apartment_links = scraper.get_apartment_links()
        all_apartments = []
        
        for url in apartment_links:
            try:
                scraper.driver.get(url)
                script_elem = WebDriverWait(scraper.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
                )
                data = json.loads(script_elem.get_attribute('innerHTML'))
                apartment_info = scraper.extract_apartment_info(data)
                if apartment_info:
                    all_apartments.append(apartment_info)
                    logging.info(f"Processed apartment: {apartment_info['Apartment Name']}")
            except Exception as e:
                logging.error(f"Error processing {url}: {e}")
                continue

        if all_apartments:
            # Create apartments DataFrame
            apartments_df = pd.DataFrame([
                {key: value for key, value in apt.items() if key != "Rooms"}
                for apt in all_apartments
            ])

            # Create rooms DataFrame
            rooms_data = []
            for apartment in all_apartments:
                for room in apartment["Rooms"]:
                    room_data = room.copy()
                    room_data["Apartment Name"] = apartment["Apartment Name"]
                    rooms_data.append(room_data)
            
            rooms_df = pd.DataFrame(rooms_data)

            # Sort and save to Excel
            apartments_df = apartments_df.sort_values('Apartment Name')
            rooms_df = rooms_df.sort_values(['Apartment Name', 'Monthly Rent'])

            with pd.ExcelWriter("lifex.xlsx", engine='openpyxl') as writer:
                apartments_df.to_excel(writer, sheet_name="Apartments", index=False)
                rooms_df.to_excel(writer, sheet_name="Rooms", index=False)
            
            logging.info("Data saved to lifex.xlsx")
        else:
            logging.warning("No apartments found")
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    main()