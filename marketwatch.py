import requests
import traceback
from bs4 import BeautifulSoup

from datetime import datetime as dt

from logger import log

from utils import get_float

def get_result_dict():
    result = {
        'current_price': None,
        'recommendation': None,
        'one_year_target': None,
        'recommendation_str': None,
        'recommendation_calc_str': None
    }

    return result
        
def get_marketwatch_data(ticker, q = None):
    ticker = ticker.replace("-", '.')

    result = get_result_dict()

    #log(f"marketwatch start {dt.now().isoformat()}")

    try:
        result = get_marketwatch_raw_data(ticker)
        result["success"] = True
    except:
        log(f"{ticker} error marketwatch")
        log(traceback.format_exc())
        result["success"] = False
    
    result["datetime"] = dt.now().isoformat()

    #log(f"marketwatch end {dt.now().isoformat()}")

    if q != None:
        q.put(result)

    return result

def get_marketwatch_raw_data(ticker):
    URL = f'https://www.marketwatch.com/investing/stock/{ticker}/analystestimates'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    current_price = soup.select('.intraday__price')[0].text.replace("$", "").strip()
    current_price = get_float(current_price)

    recommendation_str = soup.select('.region--primary div:nth-child(1) table tr td.w25')[0].text.strip()

    recomendation_values = [
        (1 + 1.24) / 2,
        (1.25 + 1.74) / 2,
        (1.75 + 2.24) / 2,
        (2.25 + 2.74) / 2,
        (2.75 + 3) / 2
    ]

    # recomendation_values = [
    #     1,
    #     2,
    #     3,
    #     4,
    #     5
    # ]

    recomendation_array = soup.select(".analyst-ratings td:nth-child(4)")
    sum = 0
    count = 0

    for pos in range(5):
        amount = 0

        try:
            amount = float(recomendation_array[pos].text)
        except:
            pass

        value = recomendation_values[pos]

        sum = sum + amount * value
        count = count + amount

    recommendation = None
    recommendation_calc = None
    recommendation_calc_str = None

    if (count):
        recommendation_calc = (sum / count) - 0.01

        if 1 <= recommendation_calc < 1.25:
            recommendation_calc_str = 'Buy'
        elif 1.25 <= recommendation_calc < 1.75:
            recommendation_calc_str = 'Overweight'
        elif 1.75 <= recommendation_calc < 2.25:
            recommendation_calc_str = 'Hold'
        elif 2.25 <= recommendation_calc < 2.75:
            recommendation_calc_str = 'Underweight'
        elif 2.75 <= recommendation_calc <= 3:
            recommendation_calc_str = 'Sell'

        recommendation = (recommendation_calc + 0.01 - 1) * 2 + 1

    one_year_target = soup.select('.region--primary div:nth-child(1) table tr td.w25')[1].text.strip()
    one_year_target = get_float(one_year_target)

    result = {
        'current_price': current_price,
        'recommendation_str': recommendation_str,
        'recommendation': recommendation,
        'recommendation_calc': recommendation_calc,
        'recommendation_calc_str': recommendation_calc_str,
        'one_year_target': one_year_target
    }

    return result


#log(get_marketwatch_data("bidu"))