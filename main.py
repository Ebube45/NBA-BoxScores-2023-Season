from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from playwright._impl._errors import TimeoutError

def scrape_table_data(page):
    html = page.inner_html("body")
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tbody.Crom_body__UYOcU tr")
    data = [[td.get_text() for td in row.find_all("td")] for row in rows]
    return data

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.nba.com/stats/players/boxscores",timeout=60000)

        data = []
        page_number = 1

        while True:
            try:
                data += scrape_table_data(page)
                print(f"Scraped data from page {page_number}.")

                next_button = page.query_selector("button[data-track='click'][data-type='controls'][data-pos='next']")
                if not next_button:
                    print("No next button found. Exiting loop.")
                    break

                next_button.click(timeout=5000)
                page.wait_for_selector("tbody.Crom_body__UYOcU tr")
                page_number += 1
            except TimeoutError as e:
                print(f"Failed to navigate to the next page: {e}")
                print("Saving the DataFrame and exiting.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        columns = [
            "Player", "Team", "Opponent", "Date", "Result", "Minutes", "Points", 
            "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", 
            "OREB", "DREB", "REB", "AST", "TO", "STL", "BLK", "PF", "+/-", "SPI"
        ]
        df = pd.DataFrame(data, columns=columns) 
        df.to_csv("nba_player_boxscores_2023-2024.csv", index=False)
        print("Scraping completed.")

# Call the main function
main()
