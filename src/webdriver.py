from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime, timedelta
import sys
from dotenv import load_dotenv
import os

load_dotenv()
chrome_driver_adress = os.environ.get("chromedadress")

tryCounter = 0

def GetWebdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('enable-automation')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_driver_adress,chrome_options=options)
    return driver

