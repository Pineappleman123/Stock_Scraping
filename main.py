# https://realpython.com/beautiful-soup-web-scraper-python/
# https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
# https://www.marketwatch.com/

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import numpy as np

symbol = input("Enter stock symbol: ").lower()
URL = "https://www.marketwatch.com/investing/stock/" + symbol + "?mod=search_symbol"
URL2 = "https://www.marketwatch.com/investing/stock/" + symbol + "/download-data?mod=mw_quote_tab"
page = requests.get(URL)
historical = requests.get(URL2)

close_y = []

soup = BeautifulSoup(page.content, "html.parser")
soup2 = BeautifulSoup(historical.content, "html.parser")

results = soup.find(id="maincontent")
results2 = soup2.find(id="maincontent")
figure, axis = plt.subplots(1, 2)

# try:
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
        if label == "CLOSE":
            close_y.append(float(row_data[date][i][1][1:]))
        y.append(float(row_data[date][i][1][1:]))
    axis[0].plot(x, y, label=label)
    plt.xticks(rotation=45)


close_x = [i for i in range(len(close_y))]
coef = np.polyfit(close_x, close_y, 1)
poly1d_fn = np.poly1d(coef) 
# poly1d_fn is now a function which takes in x and returns an estimate for y
line_len = [i for i in range(len(close_x) + 5)]
axis[1].plot(x, close_y, 'yo', line_len, poly1d_fn(line_len), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker
plt.xticks(rotation=45)
# axis[1].xlim(0, close_x[len(close_x - 1)])
# axis[1].ylim(0, close_y[len(close_y - 1)])
# plt.xlim(0, close_x[len(close_x) - 1] + 100)

plt.xlabel("DATE")
plt.ylabel("VALUE IN $")
axis[0].legend()
plt.show()

# except:
#     print("Incorrect stock symbol")
