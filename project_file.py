

"""Google Maps Extractor using Python"""

# importing libraries
from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse

# Define a data class for holding information about each search result
@dataclass
class Search_Results:
    """holds the search results"""

    Name: str = None
    Address: str = None
    Latitude: float = None
    Longitude: float = None
    Website: str = None
    PhoneNumber: str = None
    ReviewsCount: int = None
    AverageRating: float = None   

# Define a data class to hold a list of Search_Results and provide utility methods
@dataclass
class SearchResultList:
    """holds list of Business objects,and save to excel file """

    search_list: list[Search_Results] = field(default_factory=list)

    def dataframe(self):
        """Converts search_list to pandas dataframe.
        Returns: pandas dataframe
        """
        return pd.json_normalize((asdict(business) for business in self.search_list), sep="_")

    def save_to_excel(self, filename):
        """saves pandas dataframe to excel (xlsx) file"""
        self.dataframe().to_excel(f"{filename}.xlsx", index=False)


# Function to extract latitude and longitude coordinates from a Google Maps URL
def extract_coordinates_from_url(url: str) -> tuple[float,float]:
    coordinates = url.split('/@')[-1].split('/')[0]    
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to Google Maps
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(5000)

        # Perform a search on Google Maps
        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        # Scroll to load more results
        page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

        # Loop to scrape results until the specified total is reached or no more results are available
        previously_counted = 0
        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)
            
            if (page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()>= total):

                # If the total number of results is reached, break from the loop
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()[:total]
                listings = [listing.locator("xpath=..") for listing in listings]
                print(f"Total Scraped: {len(listings)}")
                break
            else:
                # Logic to break from the loop if arrived at all available listings
                if (page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count() == previously_counted):

                    listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                    print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                    break
                else:
                    previously_counted = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()
                    print(f"Currently Scraped: ",page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count(),)

        # Initialize SearchResultList object to store scraped data
        searchlist = SearchResultList()

        # Loop through each listing and extract detailed information
        for listing in listings:
            try:
                listing.click()
                page.wait_for_timeout(5000)
                # Define XPaths for extracting search details
                name_xpath = '//div[contains(@class, "fontHeadlineSmall")]'
                address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                reviews_span_xpath = '//span[@role="img"]'

                # Create a Search_Results object to store extracted data                
                data_search = Search_Results()

                # Extract information from XPaths and populate the data_search object
                # Name
                if listing.locator(name_xpath).count() > 0:
                    data_search.Name = listing.locator(name_xpath).all()[0].inner_text()
                else:
                    data_search.Name = ""
                
                # Address
                if page.locator(address_xpath).count() > 0:
                    data_search.Address = page.locator(address_xpath).all()[0].inner_text()
                else:
                    data_search.Address = ""

                # Website
                if page.locator(website_xpath).count() > 0:
                    data_search.Website = page.locator(website_xpath).all()[0].inner_text()
                else:
                    data_search.Website = ""
                
                # Phone Number
                if page.locator(phone_number_xpath).count() > 0:
                    data_search.PhoneNumber = page.locator(phone_number_xpath).all()[0].inner_text()
                else:
                    data_search.PhoneNumber = ""

                # Average Rating & review Count
                if listing.locator(reviews_span_xpath).count() > 0:
                    data_search.AverageRating = float(
                        listing.locator(reviews_span_xpath).all()[0]
                        .get_attribute("aria-label")
                        .split()[0]
                        .replace(",", ".")
                        .strip()
                    )
                    data_search.ReviewsCount = int(
                        listing.locator(reviews_span_xpath).all()[0]
                        .get_attribute("aria-label")
                        .split()[2]
                        .replace(',','')
                        .strip()
                    )
                else:
                    data_search.AverageRating = ""
                    data_search.ReviewsCount = ""
                
                # Extract coordinates from the current page URL
                data_search.Latitude, data_search.Longitude = extract_coordinates_from_url(page.url)

                # Append the data_search object to the searchlist
                searchlist.search_list.append(data_search)

            except Exception as e:
                print(e) # Print any exceptions encountered during scraping

        # Save the scraped data to an Excel file
        searchlist.save_to_excel("google_maps_data")  

        # Close the Playwright browser
        browser.close()

 # Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()

    # Set the search query from command-line arguments or user input
    if args.search:
        search_for = args.search
    else:
        # in case no arguments passed,the scraper will search for user input
        search_for = input("Enter place to search : ")

    # total number of products to scrape. Default is 15
    if args.total:
        total = args.total
    else:
        total = 15

    main()
