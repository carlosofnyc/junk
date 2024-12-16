from scraper.apartment_scraper import ApartmentScraper

def main():
    urls = [
        'https://joinlifex.com/berlin/homes',
        'https://joinlifex.com/other-location/homes'  # Add more URLs as needed
    ]
    
    scraper = ApartmentScraper()
    
    try:
        all_apartments = []
        
        for url in urls:
            try:
                scraper.driver.get(url)
                apartment_links = scraper.get_apartment_links()
                for apartment_url in apartment_links:
                    scraper.driver.get(apartment_url)
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

        # Further processing and saving of all_apartments can be done here

    finally:
        scraper.close_driver()

if __name__ == "__main__":
    main()