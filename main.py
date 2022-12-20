# https://realpython.com/beautiful-soup-web-scraper-python/
# https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
# https://www.marketwatch.com/

import matplotlib as plt
import requests
from bs4 import BeautifulSoup

symbol = input("Enter stock symbol: ").lower()
URL = "https://www.marketwatch.com/investing/stock/" + symbol + "?mod=search_symbol"
URL2 = "https://www.marketwatch.com/investing/stock/" + symbol + "/download-data?mod=mw_quote_tab"
page = requests.get(URL)
historical = requests.get(URL2)

soup = BeautifulSoup(page.content, "html.parser")
soup2 = BeautifulSoup(historical.content, "html.parser")

results = soup.find(id="maincontent")
results2 = soup2.find(id="maincontent")

try:
    current_price = results.find("h2", class_="intraday__price").find("bg-quote").text

    info = results.find("div", class_="group group--elements left").find_all("li", class_="kv__item")
    print("Useful info: \n")
    for info in info:
        print(info.text.strip())
        print()

    print("Current price: $" + current_price)
except:
    print("Incorrect stock symbol")

data = results2.find("tbody", class_="table__body row-hover")
rows = data.find_all("tr", class_="table__row")
row_data = {}
for row in rows:
    date = row.find("div", class_="cell__content u-secondary").text.strip()
    values = list(value.text.strip() for value in row.find_all("td", class_="overflow__cell")[1:])
    row_data[date] = values

print(row_data)