# Importing necessary modules
from playwright.sync_api import sync_playwright  # For web scraping with Playwright
from bs4 import BeautifulSoup  # For HTML parsing
import pandas as pd  # For data manipulation
from playwright._impl._errors import TimeoutError  # For handling timeouts

# Function to scrape table data from a page
def scrape_table_data(page):
    # Extracting HTML content from the page
    html = page.inner_html("body")
    # Parsing HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    # Selecting table rows from the HTML content
    rows = soup.select("tbody.Crom_body__UYOcU tr")
    # Extracting data from each row and storing in a list of lists
    data = [[td.get_text() for td in row.find_all("td")] for row in rows]
    return data

# Main function to execute the scraping process
def main():
    # Setting up Playwright
    with sync_playwright() as p:
        # Launching a Chromium browser
        browser = p.chromium.launch(headless=False)
        # Creating a new browsing context
        context = browser.new_context()
        # Creating a new page within the context
        page = context.new_page()
        # Navigating to the NBA stats website
        page.goto("https://www.nba.com/stats/players/boxscores",timeout=60000)

        # List to store scraped data
        data = []
        # Variable to track page number
        page_number = 1

        # Looping through pages until there are no more next buttons
        while True:
            try:
                # Scraping data from the current page
                data += scrape_table_data(page)
                print(f"Scraped data from page {page_number}.")

                # Finding the next button
                next_button = page.query_selector("button[data-track='click'][data-type='controls'][data-pos='next']")
                # If no next button found, exit loop
                if not next_button:
                    print("No next button found. Exiting loop.")
                    break

                # Clicking the next button
                next_button.click(timeout=5000)
                # Waiting for table data to load on the next page
                page.wait_for_selector("tbody.Crom_body__UYOcU tr")
                # Incrementing page number
                page_number += 1
            except TimeoutError as e:
                # Handling timeout error
                print(f"Failed to navigate to the next page: {e}")
                print("Saving the DataFrame and exiting.")
                break
            except Exception as e:
                # Handling other exceptions
                print(f"An error occurred: {e}")
                break

        # Column names for the DataFrame
        columns = [
            "Player", "Team", "Opponent", "Date", "Result", "Minutes", "Points", 
            "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", 
            "OREB", "DREB", "REB", "AST", "TO", "STL", "BLK", "PF", "+/-", "SPI"
        ]
        # Creating a DataFrame from the scraped data
        df = pd.DataFrame(data, columns=columns) 
        # Saving DataFrame to a CSV file
        df.to_csv("nba_player_boxscores_2023-2024.csv", index=False)
        print("Scraping completed.")

# Call the main function to start the scraping process
main()
