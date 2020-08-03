from datetime import datetime as dt

from yahoo import get_yahoo_data
from finviz import get_finviz_data
from marketwatch import get_marketwatch_data

from marketwatch import get_result_dict as get_marketwatch_empty_dict

from pyvirtualdisplay import Display

from multiprocessing import Process, Queue

import json
import time
import gspread
import sys

from logger import log

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
    #log(row, col, value)
    if (value):
        try:
            sh.sheet1.update_cell(row, col, value)
        except:
            log(f"Unable to write, {row}, {col}, {value}")

if __name__ == '__main__':
    while True:
        row = 3

        data = []
        importants = []

        for ticker in tickers:
            log(ticker)

            #ticker = ticker.replace('.', '')

            yahoo_result = Queue()
            finviz_result = Queue()
            marketwatch_result = Queue()

            all_data = []
            p_yahoo = Process(target=get_yahoo_data, args=(ticker, yahoo_result))
            p_yahoo.start()

            p_finviz = Process(target=get_finviz_data, args=(ticker, finviz_result))
            p_finviz.start()

            p_marketwatch = Process(target=get_marketwatch_data, args=(ticker, marketwatch_result))
            p_marketwatch.start()
            
            p_yahoo.join()
            p_finviz.join()
            p_marketwatch.join()        

            yahoo = yahoo_result.get()
            finviz = finviz_result.get()
            marketwatch = marketwatch_result.get()

            # yahoo = get_yahoo_data(ticker)
            # finviz = get_finviz_data(ticker)
            # marketwatch = get_marketwatch_data(ticker)  

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
                log(f"N/A: {ticker}")

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
