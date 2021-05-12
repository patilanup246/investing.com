"""
    This script saves cookie to scrape data from investing.com
    First this script will open browser and wait for you to login
    After logged in from browser, Press enter so cookies will be saved.
    This cookies will be used next time instead of credentials.
"""

from selenium import webdriver
from afile import *

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
            "(KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 " \
            "Safari/537.36"

options = webdriver.ChromeOptions()
options.add_argument("--user-agent={0}".format(user_agent))
driver = webdriver.Chrome(options=options,executable_path='chromedriver')

########### Saving cookies for logged in users ###########

driver.get('https://www.investing.com')
foo = input("Please login through browser and then Press enter here : ")
save_cookie(driver, 'saved_cookies/client_cookie')
driver.quit()