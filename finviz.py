from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from datetime import datetime as dt

from utils import get_float

from get_webdriver import get_webdriver

import time
import sys

def get_result_dict():
    result = {
        "current_price": None,
        "one_year_target": None,
        "recommendation": None,
        "sma20": None,
        "sma50": None,
        "sma200": None,
    }

    return result
        
def get_finviz_data(ticker):
    result = get_result_dict()

    print(f"finviz start {dt.now().isoformat()}")

    try:
        result = get_finviz_raw_data(ticker)
        result["success"] = True
    except:
        print(f"{ticker} error yahoo")
        result["success"] = False
    
    result["datetime"] = dt.now().isoformat()

    print(f"finviz end {dt.now().isoformat()}")

    return result


def get_finviz_raw_data(ticker):

    wd = get_webdriver()

    url = f"https://finviz.com/quote.ashx?t={ticker}"

    #print(url)

    with wd as driver:
        # Set timeout time 
        wait = WebDriverWait(driver, 10)
        # retrive url in headless browser
        driver.get(url)

        wait.until(presence_of_element_located((By.CSS_SELECTOR, ".fullview-links")))

        current_price = driver.find_elements_by_css_selector(".snapshot-td2")[65].text
        current_price = get_float(current_price)

        one_year_target = driver.find_elements_by_css_selector(".snapshot-td2")[28].text
        one_year_target = get_float(one_year_target)        

        recommendation = driver.find_elements_by_css_selector(".snapshot-td2")[66].text
        recommendation = get_float(recommendation)        

        sma20 = None
        try:
            text = driver.find_elements_by_css_selector(".snapshot-td2")[67].text.replace("%", "")
            sma20 = current_price / (1 + get_float(text) / 100)
        except:
            pass    

        sma50 = None
        try:
            text = driver.find_elements_by_css_selector(".snapshot-td2")[68].text.replace("%", "")
            sma50 = current_price / (1 + get_float(text) / 100)
        except:
            pass    

        sma200 = None
        try:
            text = driver.find_elements_by_css_selector(".snapshot-td2")[69].text.replace("%", "")
            sma200 = current_price / (1 + get_float(text) / 100)
        except:
            pass   

        # must close the driver after task finished
        driver.close()

        # time.sleep(3)

        result = {
            "current_price": current_price,
            "one_year_target": one_year_target,
            "recommendation": recommendation,
            "sma20": sma20,
            "sma50": sma50,
            "sma200": sma200,
        }

        return result

#print(get_finviz_data("bidu"))
