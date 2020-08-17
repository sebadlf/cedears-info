import yfinance as yf

cedears = 

usa = yf.download("AAPL GGAL", period="1d")['Adj Close'].head(1)
arg = yf.download("AAPL.BA GGAL.BA", period="1d")['Adj Close'].head(1)

print(arg)

print(arg.iloc[0]["AAPL"])
print(usa.iloc[0]["AAPL"])

