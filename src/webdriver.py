from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime, timedelta
import sys
# from dotenv import load_dotenv
import os

# load_dotenv()
# chrome_driver_adress = os.environ.get("chromedadress")

tryCounter = 0

webdriver.ChromeOptions()
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
    
    # driver = webdriver.Chrome(chrome_driver_adress,chrome_options=options)
    selenium_server_url = 'http://localhost:4444/wd/hub'
    if "seleniumServer" in os.environ:
        selenium_server_url = os.getenv("seleniumServer")
    print("Driver 1")
    driver = webdriver.Remote(command_executor=selenium_server_url,options=options)
    # driver.set_timeout(30)
    print("Driver 2")

    return driver
def CloseWebdriver(driver : WebDriver):
    driver.close()
    driver.quit()

