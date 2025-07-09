import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Wikipedia base URL
base_url = "https://en.wikipedia.org/wiki/"

# Categories (54 pages total)
categories = {
    "Books": [
        "To_Kill_a_Mockingbird", "1984_(novel)", "Pride_and_Prejudice", "The_Great_Gatsby",
        "Moby-Dick", "The_Catcher_in_the_Rye", "Lord_of_the_Flies", "Jane_Eyre",
        "Wuthering_Heights", "The_Hobbit", "Fahrenheit_451", "Brave_New_World",
        "Animal_Farm", "The_Alchemist", "Catch-22", "The_Outsiders", "Charlotte's_Web",
        "The_Da_Vinci_Code", "Gone_with_the_Wind", "The_Lord_of_the_Rings",
        "A_Clockwork_Orange", "The_Color_Purple", "The_Handmaid's_Tale", "Dune_(novel)",
        "The_Bell_Jar", "Slaughterhouse-Five", "The_Giver"
    ],
    "Movies": [
        "The_Godfather", "Pulp_Fiction", "The_Shawshank_Redemption", "Inception",
        "Forrest_Gump", "The_Dark_Knight", "Fight_Club", "The_Matrix", "Titanic_(1997_film)",
        "Schindler's_List", "The_Empire_Strikes_Back", "Good_Will_Hunting",
        "The_Lion_King", "Saving_Private_Ryan", "Gladiator_(2000_film)", "Braveheart",
        "The_Departed", "No_Country_for_Old_Men", "The_Prestige", "Avatar_(2009_film)",
        "The_Avengers_(2012_film)", "Django_Unchained", "Interstellar_(film)",
        "Parasite_(2019_film)", "Joker_(2019_film)", "Mad_Max:_Fury_Road", "La_La_Land"
    ]
}

# Create folder for HTML files
if not os.path.exists("wiki_pages"):
    os.makedirs("wiki_pages")

# Data storage
data = []

# Set up requests with retries
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

# Crawl pages
for category, pages in categories.items():
    for page in pages:
        try:
            url = base_url + page
            response = session.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()

            # Save HTML
            html_file = f"wiki_pages/{category}_{page}.html"
            with open(html_file, "w", encoding="utf-8") as file:
                file.write(response.text)

            # Extract title and main text
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find("h1", {"id": "firstHeading"}).get_text(strip=True)
            main_text = soup.find("div", {"id": "mw-content-text"}).get_text(strip=True)

            # Store metadata
            data.append({
                "Category": category,
                "Page": page,
                "URL": url,
                "Title": title,
                "Main_Text": main_text,
                "HTML_File": html_file
            })
            print(f"Crawled: {page} ({category})")
            time.sleep(1)  # Delay to avoid overwhelming the server
        except Exception as e:
            print(f"Error crawling {page}: {e}")

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("wiki_data.csv", index=False, encoding="utf-8")
print(f"Data saved to wiki_data.csv ({len(data)} pages)")