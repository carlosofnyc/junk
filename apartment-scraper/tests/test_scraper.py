# FILE: /apartment-scraper/apartment-scraper/tests/test_scraper.py

import unittest
from src.scraper.apartment_scraper import ApartmentScraper

class TestApartmentScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = ApartmentScraper()

    def test_init_driver(self):
        driver = self.scraper.init_driver()
        self.assertIsNotNone(driver)

    def test_get_apartment_links(self):
        # This test would require a mock or a live test environment
        links = self.scraper.get_apartment_links()
        self.assertIsInstance(links, list)

    def test_extract_apartment_info(self):
        sample_data = {
            'props': {
                'pageProps': {
                    'listing': {
                        'apartmentName': 'Test Apartment',
                        'apartmentSize': '50m²',
                        'minPrice': 500,
                        'startingPrice': 500,
                        'totalRooms': 2,
                        'apartmentSuburb': 'Test Suburb',
                        'cityName': 'Test City',
                        'bookableUnits': [
                            {
                                'room': {'name': 'Room 1', 'roomAttributes': {'size': '25', 'furnished': True}},
                                'rent': 500,
                                'isAvailable': True,
                                'moveInDate': '2023-01-01'
                            }
                        ]
                    }
                }
            }
        }
        apartment_info = self.scraper.extract_apartment_info(sample_data)
        self.assertIsNotNone(apartment_info)
        self.assertEqual(apartment_info['Apartment Name'], 'Test Apartment')

    def tearDown(self):
        self.scraper.close_driver()

if __name__ == '__main__':
    unittest.main()