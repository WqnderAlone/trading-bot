from stocker import Stocker
import json

stocker = Stocker("less stocks.txt")

goodstocks = stocker.good_stocks()

print(json.dumps(stocker.json_data, indent = 2))
for stock in goodstocks:
    stocker.buy(stock.ticker, 90, 90)

print(json.dumps(stocker.json_data, indent = 2))
