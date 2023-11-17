from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time
import re
import csv
#driver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
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
        job_desc_element = driver.find_element(By.XPATH, "//div[@class='job-description-container']")
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
            posted_date = str(exact_day) + f"-{month}-" + dt_string.split("-")[2]
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
    
def parse_job(cat_name, keyword, scrape_country, base_obj):
    job_title =get_element_text_by_xpath('//h3[@class="job-title heading-xxlarge"]')
    linkElement = driver.find_element(By.XPATH, '//a[@data-gtm="apply-job"]')
    job_link = linkElement.get_attribute("href")
    company = get_element_text_by_xpath('//span[@class="company"]')
    if not len(company):
        company = get_element_text_by_xpath("//a[contains(@class, 'company')]")
    location = get_element_text_by_xpath('//span[@class="location"]')
    type_of_job = get_element_text_by_xpath('//div[@class="badge -default-badge"]/div[@class="content"]')
    type_of_job = get_job_type(type_of_job)
    posted_at = driver.find_element(By.XPATH, '//span[@class="listed-date"]')
    posted_date = get_posted_date(posted_at)
    
    if not len(location):
        location = get_element_text_by_xpath("//a[contains(@class, 'location')]")
    job_desc = get_job_desc()
    print(job_title, job_link, company, location, type_of_job)
    data = (
            dt_string, "Jora", job_title, cat_name, job_link, location, company, keyword, "",
            type_of_job, job_desc, posted_date, scrape_country)
    base_obj.db_insertion("temp_raw_leads",data)
    with open(f"scraped_data.csv", mode='a', encoding='utf-8',
                    newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list(data))
    #checking for next button
    try:
        next_button = driver.find_element(By.XPATH, '//a[@class="next-page-button"]')
        next_button.click()
        # wait_apply_button = WebDriverWait(driver, 180).until(
        #     EC.presence_of_element_located((By.XPATH, '//a[@data-gtm="apply-job"]'))
        # )
        try:
            modal_close_btn = driver.find_elements(By.XPATH, '//div[@class="modal-header"]/div')
            # driver.execute_script("arguments[0].click();", modal_close_btn[1])
            modal_close_btn[0].click()
        except NoSuchElementException:
            print("ELEMENT NOT FOUND")
        except ElementNotInteractableException:
            print("NOT INTERACTABLE")
        wait_job_cards = WebDriverWait(driver, 180).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="job-card result organic-job -split-view"]'))
        ) 
        parse_job(base_obj, cat_name, keyword, scrape_country) 
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass

def getData(url, catgry, keyword, scrape_country, base_obj):
    # url = template_url.format(keyword, page)
    driver.get(url)
    try:
        modal_close_btn = driver.find_elements(By.XPATH, '//div[@class="modal-header"]/div')
        # driver.execute_script("arguments[0].click();", modal_close_btn[1])
        modal_close_btn[0].click()
    except NoSuchElementException:
        print("ELEMENT NOT FOUND")
    except ElementNotInteractableException:
        print("NOT INTERACTABLE")
    
    wait_job_cards = WebDriverWait(driver, 180).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="job-card result organic-job -split-view"]'))
    )
    job_cards = driver.find_elements(By.XPATH, '//div[@class="job-card result organic-job -split-view"]')
    for job_card in job_cards:
        job_card.click()
    try:
        modal_close_btn = driver.find_elements(By.XPATH, '//div[@class="modal-header"]/div')
        # driver.execute_script("arguments[0].click();", modal_close_btn[1])
        modal_close_btn[0].click()
    except NoSuchElementException:
        print("ELEMENT NOT FOUND")
    except ElementNotInteractableException:
        print("NOT INTERACTABLE")
        wait_apply_button = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-gtm="apply-job"]'))
        )
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@class='job-description-container']")))
        parse_job(catgry, keyword, scrape_country, base_obj)
        # time.sleep(100)
    