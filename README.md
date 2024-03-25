# NBA Player Box Scores Web Scraping

## Overview
This project aims to scrape NBA player box score data from the official NBA stats website using web scraping techniques. The data includes player statistics from various games, such as points scored, assists, rebounds, etc.

## Features
- Utilizes Playwright for browser automation to navigate through web pages.
- Parses HTML content using BeautifulSoup for extracting relevant data.
- Stores scraped data in a Pandas DataFrame for further analysis.
- Saves the scraped data to a CSV file for easy access and manipulation.

## Requirements
- Python 3.x
- Playwright
- BeautifulSoup
- Pandas

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Ebube45/NBA-BoxScores.git
   cd NBA-BoxScores
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the main script to start scraping:
   ```bash
   python main.py
   ```
2. The script will navigate through pages of NBA player box scores, scrape the data, and save it to a CSV file.

## Customization
- Adjust the timeout values in the script based on your internet speed and website responsiveness.
- Modify the column names in the `columns` list according to the data structure of the website being scraped.
- Explore additional data processing and analysis techniques using the Pandas library.

## License
This project is licensed under the [MIT License](LICENSE).

## Author
- [Nnaji David](https://github.com/Ebube45)

## Acknowledgments
Special thanks to the NBA for providing the box score data on their website.

