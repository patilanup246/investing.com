"""

    Created on Thu May 02 14:58:11 2019

    @author: keyur-r

    Description: This is a main scraper which will scrape data by fetching urls in './data/URLslist.txt'.
    It will prompt for Start and End date in YYYYMMDD and saves csv file into data folder.

    Run :
    python script1.py

"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from afile import load_cookie
import time
import os
import datetime


class InvestingScraper():

    def __init__(self, startDate, endDate, urls_file='./data/URLslist.txt'):
        self.urls_file = urls_file
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
            "(KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 " \
            "Safari/537.36"
        self.startDate = startDate # "02/01/2019"
        self.endDate = endDate # "03/01/2019"
        self.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    def init_driver(self):
        """
            Initializing selenium web driver in headless mode
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--user-agent={0}".format(self.user_agent))
        options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        prefs = {'download.default_directory' : self.ROOT_PATH+'/data'}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=options,executable_path=self.ROOT_PATH+'/chromedriver')
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.ROOT_PATH+'/data'}}
        command_result = self.driver.execute("send_command", params)

    def load_saved_login(self,file_name='saved_cookies/client_cookie'):
        """
            Loading saved cookies for login
        """
        self.driver.get('https://www.google.com/')
        load_cookie(self.driver, file_name)

    def read_urls(self):
        """
            Getting all target urls from text file
        """
        self.target_urls = [line.rstrip('\n') for line in open(self.urls_file)]

    def click_element(self, xpath):
        """
            This clicks the WebElement found by given xpath
            :param: xpath: str
        """
        try:
            WebDriverWait(self.driver, 30, poll_frequency=1).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element_by_xpath(xpath).click()
        except TimeoutException:
            time.sleep(5)
            self.driver.find_element_by_xpath(xpath).click()
        except NoSuchElementException:
            raise NoSuchElementException("Element not present with the given xpath")
        except StaleElementReferenceException:
            time.sleep(5)
            self.driver.find_element_by_xpath(xpath).click()
        except ElementNotVisibleException:
            pass

    def start_scraper(self):
        """
            It will start the actual scraping.
        """
        print ("Starting the scraper ... ")
        self.init_driver()
        self.load_saved_login()
        print ("Logged in to the investing.com")
        self.read_urls()
        f = open("failedURLslist.txt","w+")
        for url in self.target_urls:
            try :
                self.driver.get(url)
            except :
                if url != '' or url != " " or url is not None:
                    f.write(url+"\n")
                continue

            try :
                print ("Downloading data for {} ".format(url))
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, 400)")
                time.sleep(2)
                try :
                    self.click_element('//*[@id="widgetFieldDateRange"]')
                except :
                    self.driver.execute_script("window.scrollTo(0, 400)")
                    self.click_element('//*[@id="widgetFieldDateRange"]')

                WebDriverWait(self.driver, 10, poll_frequency=1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="applyBtn"]')))

                self.driver.find_element_by_id("startDate").clear()
                self.driver.find_element_by_id("startDate").send_keys(self.startDate)
                self.driver.find_element_by_id("endDate").clear()
                self.driver.find_element_by_id("endDate").send_keys(self.endDate)
                self.click_element('//*[@id="applyBtn"]')
                WebDriverWait(self.driver, 10, poll_frequency=1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="curr_table"]')))
                self.click_element('//*[@title="Download Data"]')
                # self.downloadads_done()
                time.sleep(5)
            except :
                f.write(url+"\n")
        f.close()
        self.driver.quit()

def validate_and_format(date_text):
    """
        Validating date string from prompted by user
    """
    try:
        date_obj = datetime.datetime.strptime(date_text, '%Y%m%d')
        formatted_date = '{:02d}'.format(date_obj.month) + "/" + '{:02d}'.format(date_obj.day) + "/" + '{:02d}'.format(date_obj.year)
        return formatted_date
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYYMMDD {}".format(date_text))


if __name__ == '__main__':

    startDate = input("Enter start date (YYYYMMDD) : ")
    endDate = input("Enter end date (YYYYMMDD) : ")

    startDate = validate_and_format(startDate)
    endDate = validate_and_format(endDate)

    Crawler = InvestingScraper(startDate, endDate)
    Crawler.start_scraper()