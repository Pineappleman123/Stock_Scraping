# https://realpython.com/beautiful-soup-web-scraper-python/
# https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
# https://www.marketwatch.com/

import matplotlib.pyplot as plt
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

    x = []
    columns = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
    data = results2.find("tbody", class_="table__body row-hover")
    rows = data.find_all("tr", class_="table__row")
    row_data = {}
    for row in rows:
        date = row.find("div", class_="cell__content u-secondary").text.strip()
        x.append(date)
        values = list((columns[i], value.text.strip()) for (i, value) in enumerate(row.find_all("td", class_="overflow__cell")[1:]))
        row_data[date] = values

    x.reverse()

    for i in range(len(columns) - 1):
        y = []
        for date in x:      
            label = row_data[date][i][0]
            y.append(float(row_data[date][i][1][1:]))
        plt.plot(x, y, label=label)


    plt.xlabel("DATE")
    plt.ylabel("VALUE IN $")

    plt.legend()
    plt.show()

except:
    print("Incorrect stock symbol")
