# https://realpython.com/beautiful-soup-web-scraper-python/
# https://www.marketwatch.com/

import requests
from bs4 import BeautifulSoup

URL = "https://www.marketwatch.com/investing/stock/" + input("Enter stock symbol: ").lower() + "?mod=search_symbol"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="maincontent")

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