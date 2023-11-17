import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time
import re
#driver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
def fetch_date(self, format="%d-%m-%Y-%H-%M-%S"):
        now = datetime.now()
        dt_string = now.strftime(format)
        return dt_string
dt_string = fetch_date("%d-%m-%Y")
def getPostedDate():
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
    
def parse_job(base_obj):
    job_title = driver.find_element(By.XPATH, '//h3[@class="job-title heading-xxlarge"]').text
    linkElement = driver.find_element(By.XPATH, '//a[@data-gtm="apply-job"]')
    job_link = "https://us.jora.com" + linkElement.get_attribute("href")
    company = driver.find_element(By.XPATH, '//span[@class="company"]').text
    location = driver.find_element(By.XPATH,'//span[@class="location"]').text
    type_of_job = driver.find_element(By.XPATH, '//div[@class="badge -default-badge"]/div[@class="content"]').text
    posted_at = driver.find_element(By.XPATH, '//span[@class="listed-date"]')
    print(job_title, job_link, company, location, type_of_job)
    data = ""
    base_obj.db_insertion("temp_raw_leads",data)
def getData(url, base_obj):
    driver.get(url)
    wait_drop_container = WebDriverWait(driver, 180).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="dropdown-container listed-date-facet-filter"]'))
    )

    drop_container =  driver.find_element(By.XPATH, '//div[@class="dropdown-container listed-date-facet-filter"]')
    drop_button =  driver.find_element(By.XPATH, '//div[@class="dropdown-container listed-date-facet-filter"]')
    drop_button.click()
    wait_drop_down = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="dropdown-container listed-date-facet-filter"]/ul/li[2]'))
    )
    drop_down = drop_container.find_element(By.XPATH, './ul/li[2]')
    drop_down.click()

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
        wait_apply_button = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-gtm="apply-job"]'))
        )
        parse_job(base_obj)
        time.sleep(100)

