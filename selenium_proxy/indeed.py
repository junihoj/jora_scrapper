import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from constants import job_title_categories
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.alert import Alert
from datetime import date
from datetime import datetime
from datetime import datetime, timedelta
import os
from PIL import Image
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pytz
from datetime import datetime
from timezonefinder import TimezoneFinder

timezone_finder = TimezoneFinder()

def click_by_xpath(driver, xpath):
    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        return True
    except TimeoutException as e:
        print("Couldn't Click by XPATH on:", xpath)
        return False
    
    
# Mapping of time zone abbreviations to standardized formats
time_zone_mapping = {
    "AST": "Alaska Standard Time",
    "PST": "Pacific Standard Time",
    "MST": "Mountain Standard Time",
    "CST": "Central Standard Time",
    "EST": "Eastern Standard Time",
    "GMT": "Greenwich Mean Time",
    "AWST": "Australian Western Standard Time",
    "ACDT": "Australian Central Daylight Time",
    "AEDT": "Australia Eastern Daylight Time",
    "NST": "New Zealand Standard Time",
}


def get_standardized_time_zone(time_zone_abbreviation):
    return time_zone_mapping.get(time_zone_abbreviation, time_zone_abbreviation)


def get_time_zone(location):
    geolocator = Nominatim(user_agent="your_app_name")
    try:
        location_info = geolocator.geocode(location, timeout=10)
        if location_info:
            latitude, longitude = location_info.latitude, location_info.longitude
            time_zone_str = timezone_finder.timezone_at(lng=longitude, lat=latitude)
            return pytz.timezone(time_zone_str) if time_zone_str else None
        else:
            return None
    except GeocoderTimedOut as e:
        print(f"Error getting time zone for {location}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_time_zone_abbreviation(time_zone):
    if time_zone:
        return datetime.now(time_zone).strftime('%Z')
    else:
        return None
    
def scrape_job_details(driver, Job_Post_URL, csv_writer, catgry , webpage_folder="webpages" , expired_folder="expired_webpages"):
    driver.get(Job_Post_URL)
    time.sleep(0)
    
    
    # Extract job details
    Job_Post_Title = ""
    Company_Name = ""
    Company_Size = "N/A" 

    # Extract job details
    if driver.find_elements(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/h1/span'):
        Job_Post_Title = driver.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/h1/span').text
    else:
        Job_Post_Title = driver.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[3]/div[1]/div[1]/h1/span').text
        
    if driver.find_elements(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]/div[1]/span/a'):
        Company_Name = driver.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]/div[1]/span/a').text
    elif driver.find_elements(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/span'):
        Company_Name = driver.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/span').text
    else:
        Company_Name = driver.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/div/div/div/div[1]/div[1]/span/a').text
        
        
    if driver.find_elements(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div'):
        Job_Location = driver.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div').text
        if "Remote" in Job_Location:
            time_zone = None  # Set time zone to None for remote jobs
            print(f"Job is remote, Time Zone: N/A")
        else:
            # Get time zone based on location
            time_zone = get_time_zone(Job_Location)
            print(f"Time Zone: {time_zone}")

            # Get time zone abbreviation
            time_zone_abbreviation = get_time_zone_abbreviation(time_zone)
            print(f"Time Zone Abbreviation: {time_zone_abbreviation}")
    else:
        Job_Location = driver.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/div/div/div/div[2]/div').text
        if "Remote" in Job_Location:
            time_zone = None  # Set time zone to None for remote jobs
            print(f"Job is remote, Time Zone: N/A")
        else:
            # Get time zone based on location
            time_zone = get_time_zone(Job_Location)
            print(f"Time Zone: {time_zone}")

            # Get time zone abbreviation
            time_zone_abbreviation = get_time_zone_abbreviation(time_zone)
            print(f"Time Zone Abbreviation: {time_zone_abbreviation}")    
        

    if driver.find_elements(By.XPATH, '//*[@id="salaryInfoAndJobType"]'):
        Job_Type = driver.find_element(By.XPATH, '//*[@id="salaryInfoAndJobType"]').text 
    else:
        Job_Type = "N/A"
        
    # Check if the company button is clickable
    company_button_xpath = '//*[@id="ifl-Tabs-3-ifl-Tab-1"]/span/span'
    company_button = driver.find_elements(By.XPATH, company_button_xpath)

    if company_button:
        # Company button is clickable, click it to go to the company page
        if click_by_xpath(driver, company_button_xpath):
            # Extract employee details from the company page (modify this part accordingly)
            # Extract company size from the company page
            time.sleep(3)
            Company_Size_xpath = '//*[@id="jobInsightsTab"]/div/div/div/div[2]/div[3]/span'
            Company_Size = driver.find_element(By.XPATH, Company_Size_xpath).text
            print(f"Company Size: {Company_Size}")

        else:
            print("Couldn't click on the company button.")
    else:
        print("No company button found for", Company_Name)
        
        
    # Save the page source to a file
    try:
        # Create the webpage folder if it doesn't exist
        if not os.path.exists(webpage_folder):
            os.makedirs(webpage_folder)

        # Extract the job ID from the URL to use as the filename
        job_id = Job_Post_URL.split("/")[-1].split("?")[0]
        filename = f"{webpage_folder}/{Job_Post_Title}_{Company_Name}_{datetime.now().strftime('%d%m%Y')}_{datetime.now().strftime('%H%M%S')}.html"

        # Save the page source to the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        print(f"Saved webpage for job {job_id} to {filename}")
    except Exception as e:
        print(f"Error saving webpage for job {job_id}: {e}")    
        
        
    #search_location = "United States"
    today = date.today()
    Job_Scrap_Date = today.strftime("%m/%d/%Y")
    # Add time zone to data
    #current_time = datetime.now(time_zone) if time_zone else None
    current_time = datetime.now(time_zone) if time_zone else None
    standardized_time_zone = get_standardized_time_zone(time_zone_abbreviation)
    
    data = ('Indeed' , Job_Post_Title , Job_Type , posted_day ,Job_Post_Date , Job_Scrap_Date , catgry , Job_Post_URL , Job_Location, standardized_time_zone ,Company_Name , Company_Size ) 
    csv_writer.writerow(data)

# Create an empty list to store job links
#links = []

# Create a CSV file to save job details
csv_file_path = "job_details.csv"
#csv_header = ["Job Source", "Job Post Title", "Job Type", "Posted Day", "Job Post Date", 'Job Scrap Date','Category', 'Job Post URL', 'Job Location', 'Time Zone' , 'Company Name', 'Company Size']

csv_header = ["Job Source", "Job Post Title", "Job Type", "Posted Day", "Job Post Date", 'Job Scrap Date',
              'Category', 'Job Post URL', 'Job Location', 'Time Zone', 'Company Name', 'Company Size']

with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(csv_header)  # Write the header to the CSV file
    
    # Create a set to store unique job URLs
    processed_job_urls = set()

    for catgry in job_title_categories:
        print(catgry)
        cat_keywords = job_title_categories[catgry]
        
        # Create an empty list to store job links
        links = []
        for keyword in cat_keywords:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            driver.get(f"https://www.indeed.com/q-{keyword.replace(' ', '-')}-jobs.html?vjk=96df6ffb06544ede")
            print(keyword)
            keyword = keyword.replace(".", " ")
            time.sleep(1)
            
            # Find the checkbox element with explicit wait
            checkbox_xpath = '//*[@id="challenge-stage"]/div'
            
            try:
                # Explicitly wait for the checkbox to be present
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, checkbox_xpath)))
                # Find the checkbox element
                checkbox = driver.find_element(By.XPATH, checkbox_xpath)

                # Check if the checkbox is not already selected
                if checkbox.is_displayed() and not checkbox.is_selected():
                    # If not selected, click on it to select it
                    checkbox.click()
                    print("Checkbox selected successfully")
                    time.sleep(3)  # Adjust the sleep duration as needed
                else:
                    print("Checkbox is already selected")

            except TimeoutException:
                print(f"Timeout waiting for the checkbox element to be present: {checkbox_xpath}")

            # Find and fill the location search input
            search_location = driver.find_element(By.XPATH, '//*[@id="text-input-where"]')
            search_location.send_keys("United States")
            search_location.send_keys(Keys.ENTER)
            time.sleep(1)

            # Click on the "Date Posted" filter
            date_posted_xpath = '//*[@id="filter-dateposted"]/div[1]'
            click_by_xpath(driver, date_posted_xpath)

            click_by_xpath(driver, '//*[@id="filter-dateposted-menu"]/li[1]')
            time.sleep(2)
            
            check = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[5]/div[1]/div[4]').text
            if 'did not match any' in check:
                print("No jobs found")
                continue
            else:
                print("found")
                
                
            job_page = driver.find_element(By.ID, 'mosaic-jobResults')
            jobs = job_page.find_elements(By.CLASS_NAME, 'job_seen_beacon')
            days_ago = 1
            posted_day = ''

            for job in jobs:
                soup = BeautifulSoup(driver.page_source, 'html.parser')  # Create BeautifulSoup object
                Job_Post_Date = soup.select_one('.date').get_text().strip()

                if Job_Post_Date.startswith("Posted"):
                    # Extract the part of the string after "Posted"
                    relative_date = Job_Post_Date[len("Posted"):].strip()

                    if "Today" in relative_date:
                        posted_day = "Today"
                        actual_date = datetime.now()
                    else:
                        actual_date = datetime.now() - timedelta(days=days_ago)
                        posted_day = "Posted " + str(days_ago) + " day ago"

                formatted_date = actual_date.strftime("%m-%d-%Y")
                Job_Post_Date = formatted_date
                print("Posted Date:", Job_Post_Date)

                Job_Post_URL = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
                links.append(Job_Post_URL)
                print("https://www.indeed.com/" + Job_Post_URL)

            # Now, you have all the links. You can loop through them and open each link
            for link in links:
                Job_Post_URL = "" + link  # Construct the full URL

                # Check if the job URL has already been processed
                if Job_Post_URL in processed_job_urls:
                    print(f"Skipping already processed job: {Job_Post_URL}")
                    continue

                # Add the URL to the set to mark it as processed
                processed_job_urls.add(Job_Post_URL)

                driver.get(Job_Post_URL)  # Open the job listing page
                time.sleep(2)  # Wait for the page to load
                print("Opened job listing URL:", Job_Post_URL)

                # Add your code to extract job details here
                scrape_job_details(driver, Job_Post_URL, csv_writer, catgry, webpage_folder="webpages", expired_folder="expired_webpages")

    # No need to close the CSV file here, as the 'with' statement will take care of it.

# # Close the CSV file
# csvfile.close()

# Quit the driver
driver.quit()
