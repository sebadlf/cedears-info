from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sys

chrome_driver_path = './chromedriver'

if sys.platform == 'linux':
    chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def get_webdriver():
    wd = webdriver.Chrome(
    executable_path=chrome_driver_path, options=chrome_options
    )

    return wd