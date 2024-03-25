from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from playwright._impl._errors import TimeoutError

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.nba.com/stats/players/boxscores",timeout=60000)
    
    # Extracting data from the first page
    html = page.inner_html("body")
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tbody.Crom_body__UYOcU tr")
    data = []
    for row in rows:
        row_data = [td.get_text() for td in row.find_all("td")]
        data.append(row_data)

    # Navigating through multiple pages
    for _ in range(456):  
        try:
            page.get_by_role("button", name="Next Page Button").click(timeout=5000) 
            page.wait_for_selector("tbody.Crom_body__UYOcU tr")
            html = page.inner_html("body")
            soup = BeautifulSoup(html, "html.parser")
            rows = soup.select("tbody.Crom_body__UYOcU tr")
            for row in rows:
                row_data = [td.get_text() for td in row.find_all("td")]
                data.append(row_data)
        except TimeoutError as e:
            print(f"Failed to navigate to the next page: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Create a DataFrame from the list of lists
columns = [
    "Player", "Team", "Opponent", "Date", "Result", "Minutes", "Points", 
    "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", 
    "OREB", "DREB", "REB", "AST", "TO", "STL", "BLK", "PF", "+/-", "SPI"
]
df = pd.DataFrame(data, columns=columns) 
df.to_csv("nba_player_boxscores_test2.csv", index=False)
# Display the DataFrame
# print(df)
