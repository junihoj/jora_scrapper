from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import sys
import os

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append("../../base_scrapper/base_traceback")
from base_trace_back import TRACEBACK


class SELENIUM:
    def __init__(self):
        self.driver = None
        self.options = None
        self.add_chrome_options()
        self.chromedriver = ChromeDriverManager().install()
        self.tracking_obj = TRACEBACK

    def add_chrome_options(self):

        self.options = Options()
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument("start-maximized")
        self.options.add_argument('incognito')
        self.options.add_argument('disable-geolocation')
        self.options.add_argument('ignore-certificate-errors')
        self.options.add_argument('disable-popup-blocking')
        self.options.add_argument('disable-web-security')
        self.options.add_argument('disable-infobars')
        self.options.add_argument('disable-translate')
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")

    def fetch_date(self, format="%d-%m-%Y-%H-%M-%S"):
        now = datetime.now()
        dt_string = now.strftime(format)
        return dt_string

    def driver_initialize(self):
        self.driver = webdriver.Chrome(self.chromedriver, options=self.options)
        return self.driver

    def get_element_text_by_xpath(self, element=None, xpath=None):
        if not element:
            element = self.driver
        try:
            return element.find_element(By.XPATH, xpath).text.strip()
        except Exception as e:

            self.tracking_obj.tracebackError(self.get_element_text_by_xpath.__name__, self.fetch_date())
            return ''

    def get_element_attribute_by_xpath(self, element=None, xpath=None, attr=None):
        if not element:
            element = self.driver
        try:
            return element.find_element(By.XPATH, xpath).get_attribute(attr)
        except Exception as e:
            self.tracking_obj.tracebackError(self.get_element_attribute_by_xpath.__name__,
                                             self.fetch_date())
            return ''

    def get_elements_by_xpath(self, element=None, xpath=None):
        if not element:
            element = self.driver
        try:
            return element.find_elements(By.XPATH, xpath)
        except Exception as e:
            self.tracking_obj.tracebackError(self.get_elements_by_xpath.__name__, self.fetch_date())
            return []


if __name__ == "__main__":
    SELENIUM()
