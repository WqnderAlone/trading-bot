import yfinance as yf

with open("temp_stock.txt", "r+") as fread:
    fwrite = open("full_stock.txt", "a")

    for l in fread:
        l = l.strip()
        try:
            yf.Ticker(l).history("6mo")
            fwrite.write(l)
        except:
            continue

