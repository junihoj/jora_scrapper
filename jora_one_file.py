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
from get_location_time_zone import get_company_time_zone
import asyncio

BASE_DIR = pathlib.Path(__file__).parent.resolve()
skip_status = []


driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))
driver.maximize_window()


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def fetch_date(format="%d-%m-%Y-%H-%M-%S"):
    now = datetime.now()
    dt_string = now.strftime(format)
    return dt_string


dt_string = fetch_date("%d-%m-%Y")


def get_job_desc():
    try:
        job_desc_element = driver.find_element(
            By.XPATH, "//div[@class='job-description-container']")
        print('TAKING SCREENSHOT')
        job_desc_container = driver.find_element(By.XPATH, '//div[contains(@class,"jdv-panel") and @data-hidden="false"]')
        # job_desc_element.screenshot('screen_shot.png')
        job_desc_container.screenshot('screen_shoot_container.png')
        print(' FINISHED TAKING SCREENSHOT')
        all_child_elements = job_desc_element.find_elements(By.XPATH, ".//*")
        job_desc = '\n'.join([d.text.strip() for d in all_child_elements])
        return job_desc
    except Exception as e:
        return ""


def get_posted_date(posted_date):
    if posted_date:

        if "hour" in posted_date:
            posted_date = dt_string
        elif "day" in posted_date:
            day = posted_date.split(" day")[0]
            dt_str = dt_string.split("-")[0]
            exact_day = int(dt_str) - int(day)
            if exact_day < 0:
                exact_day = 30 + exact_day
                month = int(dt_string.split('-')[1]) - 1
            else:
                month = int(dt_string.split('-')[1])
            posted_date = str(exact_day) + \
                f"-{month}-" + dt_string.split("-")[2]
        if posted_date == "":
            posted_date = dt_string


def get_job_type(type_of_job):
    if type_of_job:
        if type_of_job == "Permanent" or type_of_job == "Employee" or type_of_job == "Nights" or type_of_job == "$55,000 - $75,000 a year" or type_of_job == "$60,000 - $70,000 a year" or type_of_job == "Full-time Contract Qualifications  Salesforce: 4 years (Required)  Certified Scrum Master (Required)  Work authorization (Required)" or type_of_job == "$60,000 - $70,000 a year" or type_of_job == "$100,000 - $140,000 a year" or type_of_job == "Full time, Permanent" or type_of_job == "Regular, Full time":
            type_of_job = "Full time"
        if type_of_job == "contract" or type_of_job == "Internship" or type_of_job == "Temporary" or type_of_job == "Third Party, Contract" or type_of_job == "Part-Time" or type_of_job == "Third Party" or type_of_job == "Casual/Temporary, Contract" or type_of_job == "Third Party, Contract" or type_of_job == "Contractor" or type_of_job == "Freelance":
            type_of_job = "Part time"
        if type_of_job == "Remote job" or type_of_job == "Remote Offsite" or type_of_job == "Remote Oppotunity":
            type_of_job = "Remote"
    if type_of_job == "":
        type_of_job = "contract"
    return type_of_job


def get_element_text_by_xpath(xpath):
    try:
        ele = driver.find_element(By.XPATH, xpath)
        return ele.text
    except:
        return ""

def get_element_attr_by_xpath(xpath, attr):
    try:
        ele = driver.find_element(By.XPATH, xpath)
        return ele.get_attribute(attr)
        # return ele.text
    except:
        return ""
    
def get_element_by_xpath(xpath):
    try:
        ele = driver.find_element(By.XPATH, xpath)
        return ele
    except:
        return false
    
def parse_job(cat_name, keyword, scrape_country, base_obj):
    print(f"PARSING JOB FOR {keyword}, {scrape_country}")
    job_title = get_element_text_by_xpath(
        '//h3[@class="job-title heading-xxlarge"]')
    # linkElement = driver.find_element(By.XPATH, '//a[@data-gtm="apply-job"]')
    # job_link = linkElement.get_attribute("href")
    job_link = get_element_attr_by_xpath('//a[@data-gtm="apply-job"]', "href")
    company = get_element_text_by_xpath('//span[@class="company"]')
    if not len(company):
        company = get_element_text_by_xpath("//a[contains(@class, 'company')]")
    location = get_element_text_by_xpath('//span[@class="location"]')
    location_container = get_element_text_by_xpath('//div[@id="company-location-container"]/span[3]')
    
    type_of_job = get_element_text_by_xpath(
        '//div[@class="badge -default-badge"]/div[@class="content"]')
    type_of_job = get_job_type(type_of_job)
    posted_at = get_element_text_by_xpath('//span[@class="listed-date"]')
    posted_date = get_posted_date(posted_at)

    # if not len(location):
    #     try:
    #         location = get_element_text_by_xpath(
    #         "//a[contains(@class, 'location')]")
    #     except:
    #         return
    print("HERE IS THE LOCATION", location)
    print("HERE IS THE LOCATION TEXT FROM LOCATION CONTAINER", location_container)
    if(location):
        get_company_time_zone(location)
    job_desc = get_job_desc()
    print(job_title, job_link, company, location, type_of_job)
    data = (
        dt_string, "Jora", job_title, cat_name, job_link, location, company, keyword, "",
        type_of_job, job_desc[0:5000], posted_date, scrape_country, posted_date,)
    # "scrape_job_post_date":data[13],
    #         "scrape_job_scrape_date":data[14],
    #         "scrape_timezone":data[15],
    #         "scrape_company_size":data[16],
    data_dict = {"dt_string": dt_string, "job board": "Jora", "JOB TITLE": job_title, "cat_name": cat_name, "job link": job_link, "company": company,
                 "keyword": keyword, "type_of_job": type_of_job, "job_desc": job_desc, "posted_date": posted_date, "scrape_country": scrape_country}
    print(f"INSERTING INTO DB {keyword} {scrape_country}")
    print("HERE IS THE DATA", data_dict)
    if(job_title=='' or company=='' or job_desc==''): return
    base_obj.db_insertion("temp_raw_leads", data)
    with open(f"scraped_data.csv", mode='a', encoding='utf-8',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow(list(data))
    time.sleep(20)


def getData(url, catgry, keyword, scrape_country, base_obj):
    # url = template_url.format(keyword, page)
    driver.get(url)

    def scrape_page():
        try:
            modal_close_btn = driver.find_elements(
                By.XPATH, '//div[@class="modal-header"]/div')
            # driver.execute_script("arguments[0].click();", modal_close_btn[1])
            modal_close_btn[0].click()
        except:
            pass
        # except NoSuchElementException:
        #     print("ELEMENT NOT FOUND")
        # except ElementNotInteractableException:
        #     print("NOT INTERACTABLE")

        wait_job_cards = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="job-card result organic-job -split-view"]'))
        )
        job_cards = driver.find_elements(
            By.XPATH, '//div[@class="job-card result organic-job -split-view"]')
        for job_card in job_cards: 
            try:
                modal_close_btn = driver.find_elements(
                    By.XPATH, '//div[@class="modal-header"]/div')
                # driver.execute_script("arguments[0].click();", modal_close_btn[1])
                modal_close_btn[0].click()
            except NoSuchElementException:
                print("ELEMENT NOT FOUND")
            except ElementNotInteractableException:
                print("NOT INTERACTABLE")
            except Exception  as e:
                pass

            try:
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable(job_card))
                job_card.click()

            except ElementClickInterceptedException:
                pass

            except TimeoutException:
                #TODO: CLICK USING TRY CLICKING USING JAVASCRIPT
                pass
            
            
            try:
                wait_apply_button = WebDriverWait(driver, 180).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//a[@data-gtm="apply-job"]'))
                )
                WebDriverWait(driver, 100).until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='job-description-container']")))
            except TimeoutException:
                return

            
            parse_job(catgry, keyword, scrape_country, base_obj)
            # time.sleep(100)

        # checking for next button
        try:
            next_button = driver.find_element(
                By.XPATH, '//a[@class="next-page-button"]')
            next_button.click()
            # parse_job(base_obj, catgry, keyword, scrape_country)
            scrape_page()
        except NoSuchElementException:
            print("NO SUCH ELEMENT NEXT BUTTON", "END FOR KEYWORD", keyword)
            return
        except ElementNotInteractableException:
            print("next button not interactable", "END FOR KEYWORD", keyword)
            return

    scrape_page()

    # driver.quit()
    time.sleep(30)


def write_file(new_data, filename):
    filename = f'{BASE_DIR}/{filename}.txt'
    with open(filename, 'a') as file_write:
        file_write.write(f"\n{new_data}")


# country_cities = {"us": us_cities, "uk": uk_cities, "au": au_cities, "ca": ca_cities, "nz": nz_cities}
# alternative https://us.jora.com/j?sp=search&trigger_source=serp&a=1&q={}&l=United+States
# https://us.jora.com/j?a=1&l=United+States&q=python+developer
# https://us.jora.com/j?sp=search&a=24h&&q={}&l=United+States
# https://us.jora.com/j?a=24h&l=United+States&q=python+developer
template_urls = {"us": "https://us.jora.com/j?a=24h&l=United+States&q={}",
                 "uk": "https://uk.jora.com/j?a=24h&l=United+Kingdom&q={}",
                 "au": "https://au.jora.com/j?a=24h&l=Australia&q={}",
                 "ca": "https://ca.jora.com/j?a=24h&l=Canada&q={}",
                 "nz": "https://nz.jora.com/j?a=24h&l=New+Zealand&q={}"
                 }
# read_file("keywords")


def main():
    getData(url, catgry, keyword, scrape_country, base_obj)


if __name__ == "__main__":
    base_obj = BASE("requests")
    session = requests.Session()
    session.trust_env = False
    base_obj.db_open_connection()
    dt_string = base_obj.fetch_date("%d-%m-%Y")
    countries = ["United States", "Canada",
                 "Australia", "United Kingdom", "New Zealand"]
    country_index = 0
    for country in template_urls:
        scrape_country = countries[country_index]
        country_index += 1
        for catgry in job_tiles_with_categories:
            cat_keywords = job_tiles_with_categories[catgry]
            for keyword in cat_keywords:
                print("starting another for", keyword)
                if f"{catgry} : {keyword}\n" in skip_status:
                    continue
                write_file(f"{catgry} : {keyword}", "keywords")
                url = template_urls[country].format(keyword.replace(' ', '+'))
                proxy_in = base_obj.get_proxy()
                getData(url, catgry, keyword, scrape_country, base_obj)
                print("starting for another end", keyword)
    base_obj.db_close_connection()
