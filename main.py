from stocker import Stocker
import json

stocker = Stocker("less stocks.txt")

goodstocks = stocker.good_stocks()

print(stocker.json_data)
for stock in goodstocks:
    stocker.buy(stock.ticker, 20, 20)

print(json.dumps(stocker.json_data, indent = 2))
