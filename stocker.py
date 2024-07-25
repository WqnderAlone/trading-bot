import yfinance as yf
import json

class Stocker:
    def __init__(self, stockoptions = "stocks.txt", financeinfo = "finances.json"):
        # gather stock options
        f = open(stockoptions, "r+")
        self.ticker_options = []

        for l in f:
            l = l.strip()
            self.ticker_options.append(yf.Ticker(l))
        f.close()


        # gather finance information (stocks, buy price, etc)
        f = open(financeinfo)
        self.json_data = json.load(f)

        f.close()
        
    
    def get_investments(self):
        return self.json_data["investments"]


    def get_investment_tickers(self):
        out = set()
        for d in self.json_data["investments"]:
            out.add(d["symbol"])

        return out


    """
    Iterates through all stock Tickers in filename (from instantiation) and finds those with 50 day growth rate > 200 day growth rate

    Returns:
        list(yf.Ticker)
    """
    def good_stocks(self):
        out = []
        for ticker in self.ticker_options:
            if self.performing_well(ticker):
                out.append(ticker)

        return out


    def get_price(self, ticker):
        return yf.Ticker(ticker).info["currentPrice"]
    #       print(ticker, yf.Ticker(ticker).info["currentPrice"])
    #       print(json.dumps((yf.Ticker(ticker).info), indent = 2))

    """
    \"Buys\" a stock given a ticker

    Parameters:
        ticker:             str     -> the symbol of the stock
        share_count:        int     -> the number of shares being bought
        price_per_share:    float   -> price per share
    """
    def buy(self, ticker, share_count):
        price_per_share = self.get_price(ticker)

        if share_count*price_per_share > self.json_data["remaining balance"]:
            print("not enough money\n" * 5)
            raise OSError

        if ticker in self.get_investment_tickers():
            print("already bought this stock\nsell first to buy more\n" * 5)
            raise OSError



        new_purchase = {}
        
        new_purchase["symbol"] = ticker
        new_purchase["shares"] = share_count
        new_purchase["price_per_share"] = price_per_share
        
        self.json_data["investments"].append(new_purchase)

        self.json_data["remaining balance"] -= share_count*price_per_share

        self.json_data["initial invested balance"] += share_count*price_per_share

        j = json.dumps(self.json_data, indent = 4)
        with open("finances.json", "w+") as f:
            print(j, file = f)

    def sell(self, ticker, share_count):
        price_per_share = self.get_price(ticker)

        for d in self.json_data["investments"]:
            if d["symbol"] != ticker:
                continue

            del d
            pass

            break

        print("stock not found\n" * 5)


    """
    Checks whether 50 day growth > 200 day growth 

    Parameters:
        ticker:         yf.Ticker   -> ticker being checked

    Returns:
        boolean: whether the yf.Ticker is performing well
    """


    def performing_well(self, ticker):
        try:
            #calculating 6 mo avg growth rate
            hist_6mo = ticker.history(period = "6mo")["Close"]
            timePer = 182.5
            avg_growth_6mo = int(hist_6mo.iloc[-1] - hist_6mo.iloc[0]) / timePer
            
            # 1 mo avg growth rate
            hist_1mo = ticker.history(period = "1mo")["Close"]
            timePer = 30.42
            avg_growth_1mo = int(hist_1mo.iloc[-1] - hist_1mo.iloc[0]) / timePer

            print(f"{ticker.ticker}" + "\t\t {:.4f} \t\t {:.4f}".format(avg_growth_6mo, avg_growth_1mo))
        except:
            print(f"error with calculating average growth rates for {ticker.ticker}")
            return False
        return (avg_growth_1mo > avg_growth_6mo)

