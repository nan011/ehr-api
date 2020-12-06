import re
from bs4 import BeautifulSoup
from requests_html import HTMLSession
browser = HTMLSession()

def load_page(url):
    # Fetch HTML page
    html_file = browser.get(url).text
    
    # Parse html and extract list of games
    return BeautifulSoup(html_file, 'html.parser')

tables = soup.select("h3 ~ table")
provinces = [value.text for value in soup.select("div.mw-parser-output > h3 > span:nth-of-type(1)")]
area = []
for i in range(len(tables)):
    cities = [value.text.replace('\n', '') for value in tables[i].select("tr > td:nth-of-type(2)")]
    area.append({
        'name': provinces[i],
        'cities': cities
    })

with open("area.json", 'w') as f:
    f.write(str(area))