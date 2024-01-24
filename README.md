# **Google Maps Extractor using Python**

## Project Overview

The project involves scraping information from Google Maps search results based on user input for city names and places to search. The user can provide the city name either through a command-line argument or by choosing from a list of cities stored in a CSV file (`city.csv`). The information is then scraped from Google Maps for the specified place within the chosen city.

## Project Components

### Data Classes

1. **Search_Results:**
   A data class that holds information about each search result, including Name, Address, Latitude, Longitude, Website, Phone Number, Reviews Count, and Average Rating.
   
2. **SearchResultList:**
   A data class that holds a list of `Search_Results` objects and provides utility methods for saving the data to an Excel file.

### Helper Functions

3. **extract_coordinates_from_url:**
   A function that extracts latitude and longitude coordinates from a Google Maps URL.

### Main Functionality

4. **main Function:**
   The main function that orchestrates the entire scraping process. It performs the following steps:
   - Takes user input for the city name and the place to search.
   - Launches a Playwright browser and navigates to Google Maps.
   - Performs a search on Google Maps using the specified city name and place.
   - Scrolls to load more results and scrapes detailed information for each listing.
   - Saves the scraped data to both a CSV file and an Excel file.

## Usage Instructions

### Command-line Arguments

The script can be executed from the command line with the following optional arguments:

- `-s` or `--search:` Specifies the place to search.
- `-t` or `--total:` Specifies the total number of results to scrape.

If these arguments are not provided, the script prompts the user for input.

### Choosing a City

If the user does not provide a city name through the command line, the script displays a list of cities from `city.csv` and prompts the user to choose a city.

## Error Handling

The code includes error handling mechanisms. For example:

- If the Playwright browser encounters issues during scraping, the script prints the exception.
- If the entered city is not in the list of cities, the script prints an error message and exits.

## Saving Data

The scraped data is saved in both CSV and Excel formats. The CSV file is named based on the search query, and the Excel file is saved using the `xlsxwriter` library.

## Potential Improvements

- Enhancements could be made to handle more complex scenarios, such as handling different types of data on Google Maps.
- The script could be extended to include additional information or refine the scraping logic.

## Dependencies

The script relies on external libraries, such as `playwright`, `pandas`, and `xlsxwriter`, which should be installed before running the script.

## Execution

To execute the script, run it from the command line, providing optional arguments for the search query and total results, or simply follow the prompts.

## Future Work

As the Google Maps website structure may change over time, it's essential to adapt the script accordingly to maintain its functionality. Additionally, feedback from users can help identify areas for improvement and new features.

