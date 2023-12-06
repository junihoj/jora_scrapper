# Import Dependencies
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys  
from bs4 import BeautifulSoup  
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService  
from webdriver_manager.chrome import ChromeDriverManager  
from datetime import date, datetime  
import time  
import sys  
from datetime import datetime 
 

# sys.path.append("../../base_scrapper/leadgeneration")
# from scrapper import BASE  # Import BASE class from a custom module (if available)
import pathlib  # Import pathlib for working with file paths

# Define the base directory
#  = pathlib.Path(__file__).parent.resolve()

# Initialize the Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Define a function to click an element by its XPath
def ClickByXPATH(NameOfObject):
    try:
        item = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, NameOfObject)))
        item.click()
    except Exception as e:
        pass

# Define a function to scrape job page data
def scrape_job_page(data_complete):
    
    # Define global variables
    today = datetime.utcnow()
    scrape_date = today.strftime("%m/%d/%Y")
    platform = "GlassDoor"
    jobtitle = ''
    company = ''
    company_domain = ''
    job_category = data_complete[0]['category']  # Get job category from the function
    job_link = ''
    job_location = ''
    keyword = data_complete[0]['keywords']  # Get keywords from the function
    job_type = data_complete[0]['jobtype']  # Get job type from the function
    job_description = ''
    posted_date = scrape_date
    scrape_country = data_complete[0]['scrape_country']  # Get scrape country from the function

    # Read URL links

    # Set up the browser
    # options = Options()
    # options.add_experimental_option("detach", True)
    # driver = webdriver.Chrome(options=options)
    # base_obj = BASE("selenium")

  
    i = 1

    # Iterate through the data links
    for link in data_complete:
        #base_obj = BASE("requests")
        #base_obj.db_open_connection()
        # driver = base_obj.driver_initialize()
        

        dict = link
        i += 1
        job_link = dict["job_link"]
        driver.get(job_link)

        # Enter job search criteria
        time.sleep(1)
        
        try:
            # Check for job title elements and get the job title
            if driver.find_elements(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]'):
                jobtitle = driver.find_element(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]')
                jobtitle = jobtitle.text
                

            # Check for alternative job title elements and get the job title
            elif driver.find_elements(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]'):
                jobtitle = driver.find_element(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]')
                jobtitle = jobtitle.text
                
            else:
                jobtitle = "N/A"
        except NoSuchElementException:
            pass
                

        try:
            
            # Check for company elements and get the company name
            if driver.find_elements(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div'):
                company = driver.find_element(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div')
                company = (company.text)
                separator = '\n'
                company = company.split(separator, 1)[0]
               
            elif driver.find_elements(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div'):
                company = driver.find_element(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div')
                company = (company.text)
                separator = '\n'
                company = company.split(separator, 1)[0]
             
            else:
                company = ""
        except NoSuchElementException:
            pass

        
        
        try:
            # Check for job location elements and get the job location
            if driver.find_elements(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[3]/span'):
                job_location = driver.find_element(By.XPATH, '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[3]/span')
                job_location = (job_location.text)
            else:
                job_location = "N/A"  
        except NoSuchElementException:
            pass
        

        # job_location_element = job_element.find_element(By.XPATH, "//*[contains(@id,'job-location-')]" )
      
        try:
            # Check for job type elements and get the job type
            if driver.find_elements(By.XPATH, '//*[contains(@id, "JobDesc")]/div/p[4]'):
                job_type = driver.find_element(By.XPATH, '//*[contains(@id, "JobDesc")]/div/p[4]')
                job_type = (job_type.text)
                if ":" in job_type:
                    job_type = job_type.split(":")[1].strip()
            else:
                job_type = "N/A"
        except NoSuchElementException:
            pass

        time.sleep(2)
        
        
        """ # Check if job location is 'Lahore' and continue to the next iteration if true
        if job_location == 'Lahore' or job_location == 'lahore':
            continue
        """
        
        
        # Click the job description element to expand it
        try:
            if driver.find_elements(By.XPATH, '//*[@id="JobDescriptionContainer"]/div[1]'):
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="JobDescriptionContainer"]/div[1]'))).click()

            # Get the job description
            if driver.find_element(By.XPATH, '//*[@id="JobDescriptionContainer"]/div[1]'):
                job_description = driver.find_element(By.XPATH, '//*[@id="JobDescriptionContainer"]/div[1]')
                job_description = job_description.text
                #job_description = job_description[:-16]
            

                # Truncate job description if it's too long
                if len(job_description) > 5000:
                    job_description = job_description[:5000]
            else:
                job_description = "N/A"
                
            
        except NoSuchElementException:
            pass
            
        

        #Get the Date posted X-Path
        
        try:
            date_posted = driver.find_element(By.XPATH , '/html/body/div[2]/div[1]/div[3]/div[1]/div[4]')    
            date_posted = date_posted.text
        except NoSuchElementException:
            pass
        

        #Get the last day job posted X-path
        
        try:
            last_day = driver.find_element(By.XPATH , '/html/body/div[2]/div[1]/div[3]/div[1]/div[4]/div[2]/ul/li[2]/button/div')
            last_day = last_day.text
        except NoSuchElementException:
            pass
        

        """
        #Get show more jobs links
        if driver.find_element(By.XPATH , '/html/body/div[2]/div[1]/div[3]/div[2]/div[1]/div[2]'):
            show_more_jobs_links = driver.find_element(By.XPATH , '/html/body/div[2]/div[1]/div[3]/div[2]/div[1]/div[2]')
            show_more_job_links = (show_more_jobs_links.text)
        """
    
    
        # Click the company domain element to get the company domain
        try:
            if driver.find_elements(By.XPATH, '//*[@id="PageContent"]/div[1]/div[2]/header/div/div/div[3]'):
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="PageContent"]/div[1]/div[2]/header/div/div/div[3]'))).click()
                if driver.find_elements(By.XPATH, '//*[@id="PageContent"]/div[1]/div[2]/div/div/div/div/div[2]/div/span/a'):
                    company_domain = driver.find_element(By.XPATH, '//*[@id="PageContent"]/div[1]/div[2]/div/div/div/div/div[2]/div/span/a').get_attribute('href') or "N/A"
           

            # Get the current time and set it as the posted date
            current_time = datetime.now()
            current_time = current_time.strftime('%m/%d/%Y')
            posted_date = current_time
        
        except NoSuchElementException:
            pass

        # Define the data to be inserted into the database
        data = (today, platform, jobtitle, job_category, job_link, job_location, company,
                keyword.replace("+", " "), company_domain, job_type, job_description, posted_date, scrape_country)
        
       
        
        # Insert the data into the database
        # base_obj.db_insertion("temp_raw_leads", data)
        
        time.sleep(1)
    

    #Quit the web driver
    driver.quit()



    
