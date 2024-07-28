from stocker import Stocker
import json
import time

stocker = Stocker("temp_stock.txt")

goodstocks = stocker.good_stocks()
badstocks = stocker.bad_stocks()
investments = stocker.get_investment_tickers()

print("good stocks:", goodstocks)
print("bad stocks: ", badstocks)

stocker.update_investments()


"""
for stock in goodstocks:
    if stock.ticker in investments:
        continue
    share_count = 1e-10 * stocker.json_data["remaining balance"]
    stocker.buy(stock.ticker, share_count)
    investments.add(stock.ticker)

for stock in badstocks:
    if stock.ticker in investments:
        stocker.sell(stock.ticker)
        investments.remove(stock.ticker)
"""

stocker.write_json()
