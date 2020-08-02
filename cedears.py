from datetime import datetime as dt

from yahoo import get_yahoo_data
from finviz import get_finviz_data
from marketwatch import get_marketwatch_data

from marketwatch import get_result_dict as get_marketwatch_empty_dict

from pyvirtualdisplay import Display

from multiprocessing import Pool

import json
import time
import gspread
import sys

if sys.platform == 'linux':
    display = Display(visible=0, size=(1980, 1200))
    display.start()

gc = gspread.oauth()

sh = gc.open("Cedears")

tickers = ["AAPL", "ABEV", "ABT", "ACH", "ADBE", 
# "ADGO", 
"AGRO",
"AIG", "AMD", "AMX", "AMZN", "ARCO", "AUY", 
#"AVP", 
"AVY", "AXP", "AZN", "BA", 
#"BA.C", 
"BAC",
"BABA", 
#"BAYN", 
"BBD", "BBVA", "BCS", "BHP", "BIDU", "BIIB", 
#"BNG",
"BG",  
"BP", "BSBR", "C", "CAT", "CDE", "CHL", "CRM", "CSCO", "CVX", "CX", 
#"DAI", 
"DD", "DE", "DEO", "DESP", 
#"DISN"
"DIS", 
"EBAY", "ERIC", "ERJ", "FB", "FCX", "FDX", "FMX", "GE", "GGB", "GILD", 
#GLNT
"GLOB", 
"GLW", "GOLD", "GOOGL", "GSK", "HD", "HL", "HMC", "HMY", "HON", "IBM", "IBN", "ING", "INTC", "ITUB", "JNJ", "JPM", "KMB", "KO", 
#"KOFM", 
"KOF",
"LLY", "LMT", "LVS", "LYG", "MCD", "MELI", "MMM", "MO", "MRK", "MSFT", "NEM", "NFLX", "NGG", "NKE", 
#"NOKA", 
"NOK",
"NUE", "NVDA", "NVS", 
#"OGZD", 
"ORCL", "PBR", "PEP", "PFE", "PG", "PTR", "PYPL", "QCOM"]
tickers += [
#"RDS", 
"RDS-A",
"RIO", "SAP", "SBUX", "SCCO", "SLB", "SNA", "SNE", "T", 
#"TEFO", 
"TEN", "TGT", 
#"TI", 
"TM", "TOT", "TRIP", "TSLA", "TSM", "TWTR", "TXN", 
#"TXR", 
"TX", 
"UGP", "UN", 
#"UTX", 
"V", "VALE", "VIST", "VOD", "VZ", "WFC", "WMT", "X", "XOM", 
#"XROX"
"XRX"
]

#tickers = ["bidu"]

def write_data(data):
    with open("info.json", "w") as file:
        json.dump(data, file, indent=4)

def write_cell(row, col, value):
    #print(row, col, value)
    if (value):
        try:
            sh.sheet1.update_cell(row, col, value)
        except:
            print("Unable to write", row, col, value)

row = 3

data = []
importants = []

def get_data(params):
    ticker = params[0]
    provider = params[1]

    result = None

    if provider == 'yahoo':
        result = get_yahoo_data(ticker)
    elif provider == 'finviz':
        result = get_finviz_data(ticker)
    else:
        result = get_marketwatch_data(ticker)

    return result

if __name__ == '__main__':
    for ticker in tickers:
        print(ticker)

        #ticker = ticker.replace('.', '')

        all_data = []
        with Pool(3) as p:
            all_data = p.map(get_data, [(ticker, 'yahoo'), (ticker, 'finviz'), (ticker, 'marketwatch')])

        # yahoo = get_yahoo_data(ticker)
        # finviz = get_finviz_data(ticker)
        # marketwatch = get_marketwatch_data(ticker)  
        yahoo = all_data[0]
        finviz = all_data[1]
        marketwatch = all_data[2]

        yahoo_target = yahoo["one_year_target"] if yahoo["one_year_target"] else 0
        marketwatch_target = marketwatch["one_year_target"] if marketwatch["one_year_target"] else 0
        target_ratio = 1

        if (yahoo_target != marketwatch_target):
            if (yahoo_target > marketwatch_target):
                target_ratio = marketwatch_target / yahoo_target

            if (marketwatch_target > yahoo_target):
                target_ratio = yahoo_target / marketwatch_target

        if (target_ratio < 0.5):
            marketwatch = get_marketwatch_empty_dict()

        current = {
            "ticker": ticker,
            "finviz": finviz,
            "yahoo": yahoo,
            "marketwatch": marketwatch,
            "last_update": dt.now().isoformat()
        }

        ratio = 0

        try:
            ratio = yahoo["one_year_target"] / yahoo["current_price"]
        except:
            print(f"N/A: {ticker}")

        row_values = []

        row_values.append(ticker)
        row_values.append(yahoo["current_price"])
        row_values.append(yahoo["price_type"])
        row_values.append(yahoo["est_return"])
        row_values.append(yahoo["one_year_target_low"])
        row_values.append(yahoo["one_year_target"])
        row_values.append(yahoo["one_year_target_high"])
        row_values.append(yahoo["recommendation"])

        row_values.append(finviz["sma20"])
        row_values.append(finviz["sma50"])
        row_values.append(finviz["sma200"])

        row_values.append(finviz["one_year_target"])
        row_values.append(yahoo["recommendation"])

        row_values.append(marketwatch["one_year_target"])
        row_values.append(marketwatch["recommendation"])
        row_values.append(marketwatch["recommendation_str"])
        row_values.append(marketwatch["recommendation_calc_str"])

        col = 1
        for value in row_values:
            write_cell(row, col, value)
            col += 1

        row = row + 1

        data.append(current)
        write_data(data)

        # if ratio > 1:
        #     importants.append(current)
        #     write_important(importants)
