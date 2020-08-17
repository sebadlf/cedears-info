from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from get_webdriver import get_webdriver

from logger import log

from utils import get_float

import requests
import time
import sys

import traceback

from datetime import datetime as dt

def get_result_dict():
    result = {
        "current_price": None,
        "one_year_target": None,
        "price_type": None,
        "est_return": None,
        "recommendation": None,
        "one_year_target_low": None,
        "one_year_target_high":None        
    }

    return result
        
def get_yahoo_data(ticker, q = None):
    result = get_result_dict()

    #log(f"yahoo start {dt.now().isoformat()}")

    try:
        result = get_yahoo_raw_data(ticker)
        result["success"] = True
    except:
        log(f"{ticker} error yahoo")
        traceback.print_stack()
        result["success"] = False
    
    result["datetime"] = dt.now().isoformat()

    #log(f"yahoo end {dt.now().isoformat()}")

    if q != None:
        q.put(result)

    return result

def get_yahoo_raw_data(ticker):

    wd = get_webdriver()

    url = f"https://finance.yahoo.com/quote/{ticker}"

    #log(url)

    with wd as driver:
        # Set timeout time 
        #wait = WebDriverWait(driver, 60)
        # retrive url in headless browser
        driver.get(url)

        WebDriverWait(driver, 60).until(presence_of_element_located((By.CSS_SELECTOR, "#quote-header-info>div>div>div>span")))

        current_price = driver.find_elements_by_css_selector("#quote-header-info>div>div>div>span")[1].text

        current_price = get_float(current_price)

        one_year_target = driver.find_element_by_css_selector("[data-test='ONE_YEAR_TARGET_PRICE-value']").text

        one_year_target = get_float(one_year_target)

        analisys = driver.find_elements_by_css_selector("#fr-val-mod>div>div")

        price_type = analisys[1].text

        est_return = analisys[2].text.replace(" Est. Return", "")

        #log(current_price, one_year_target, price_type, est_return)
        
        recommendation = None
        try:    
            driver.execute_script("window.scrollTo(0, 600)")
            WebDriverWait(driver, 60).until(presence_of_element_located((By.CSS_SELECTOR, '[data-yaft-module="tdv2-applet-similarCompanies"]')))
        
            driver.execute_script("window.scrollTo(0, 1200)")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 1800)")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 2400)")
            time.sleep(1)                

            WebDriverWait(driver, 60).until(presence_of_element_located((By.CSS_SELECTOR, '[data-test="price-targets"]')))

            recommendation = driver.find_element_by_css_selector('[data-test="rec-rating-txt"]').text        
            recommendation = get_float(recommendation)
        except:
            sys.exc_info()

        one_year_target_low = None
        one_year_target_high = None
        try:
            analisys = driver.find_elements_by_css_selector('[data-test="price-targets"]>div>div>div>span')

            one_year_target_low = get_float(analisys[1].text)
            one_year_target_high = get_float(analisys[3].text)      
        except:
            pass

        driver.close()

    result = {
        "current_price": current_price,
        "one_year_target": one_year_target,
        "price_type": price_type,
        "est_return": est_return,
        "recommendation": recommendation,
        "one_year_target_low": one_year_target_low,
        "one_year_target_high":one_year_target_high
    }

    return result

#log(get_yahoo_data("amzn"))


def get_current_value(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"

    #log(url)

    r = requests.get(url)

    data = r.json()

    value = data['chart']['result'][0]['meta']['regularMarketPrice']

    # time.sleep(3)

    return value        