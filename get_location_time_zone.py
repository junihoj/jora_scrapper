from threading import Thread
import pathlib
import requests
from scrapper import BASE
# from helpers import us_cities, uk_cities, au_cities, ca_cities, nz_cities
from constants import job_tiles_with_categories
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException,ElementClickInterceptedException
import time
import re
import csv
# driver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import asyncio


driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))
driver.maximize_window()

def get_element_by_xpath(xpath):
    try:
        WebDriverWait(driver, 120).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath))
        )
        ele = driver.find_element(By.XPATH, xpath)
        return ele
    except TimeoutException:
        print("unable to locate element", xpath)
        return False
    except:
        return False

def get_company_time_zone(location):
    print("GETING LOCATION STARTED")
    driver.get('https://www.google.com/')
    
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located(
                (By.XPATH, '//textarea[@title="Search"]'))
        )
        google_search_box = driver.find_element(By.XPATH, '//textarea[@title="Search"]')
        country_f_string = "{} timezone"
        search_term = country_f_string.format(location)
        google_search_box.send_keys(location + "timezone")
        google_search_box.send_keys(Keys.RETURN)
    except TimeoutException:
        print("Unable to get search box")
        return
    timezone_text = get_element_by_xpath('//div[contains(@class, "dDoNo")]')
    timezone_text.text
    print("HERE IS THE TEXT")
    driver.quit()