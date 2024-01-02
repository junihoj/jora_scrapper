import sys
import csv
import pathlib
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from initialize_proxy_driver import get_chromedriver
from helper_functions import get_select_proxy, get_element_attr_by_xpath
sys.path.append("..")
from constants import job_tiles_with_categories
from scrapper import BASE





headerList = ['Scrape_Date', 'Platform', 'Job_title', 'Job_Category', 'Job_Link', 'Job_Location',
              'Company_Name', 'keyword', "", "type_of_job", "job_description", "posted_time", "scrape_country"]
# open CSV file and assign header
with open("scraped_data.csv", 'a') as file:
    dw = csv.DictWriter(file, delimiter=',', fieldnames=headerList)
    dw.writeheader()
BASE_DIR = pathlib.Path(__file__).parent.resolve()


def write_file(new_data, filename):
    filename = f'{BASE_DIR}/{filename}.txt'
    with open(filename, 'a') as file_write:
        file_write.write(f"\n{new_data}")


template_urls = {"us": "https://www.dice.com/jobs?q={}&location=United%20States&filters.postedDate=ONE",
                 "uk": "https://www.dice.com/jobs?q={}&location=United%20Kingdom&filters.postedDate=ONE",
                 "au": "https://www.dice.com/jobs?q={}&location=Australia&filters.postedDate=ONE",
                 "ca": "https://www.dice.com/jobs?q={}&location=Canada&filters.postedDate=ONE",
                 "nz": "https://www.dice.com/jobs?q={}&location=New%20Zealand&filters.postedDate=ONE"
                 }


def get_job_links_for_keyword(url, category, keyword, country):
    links = []
    selected_proxy = get_select_proxy(base_obj)
    keyword_driver = get_chromedriver(
        selected_proxy=selected_proxy, use_proxy=True)
    keyword_driver.get(url)
    job_card_xpath = '//div[contains(@class,"search-card")]'
    try:
        WebDriverWait(keyword_driver, 180).until(
            EC.presence_of_element_located((By.XPATH, job_card_xpath)))
    except TimeoutException:
        print("ERROR OCCURRED SEARCH CARD TIMEOUT", e)
        return links
    except Exception as e:
        print("ERROR OCCURRED SEARCH CARD", e)
        return links

    job_cards = keyword_driver.find_elements(By.XPATH, job_card_xpath)
    # print('job cards', job_cards)
    for index, ele in enumerate(job_cards):
        try:
            # job_page_link_achor = job_card.find_element(By.XPATH, '//a[contains(@class,"card-title-link")]')
            anchorEle = keyword_driver.find_elements(By.XPATH, '//a[contains(@class,"card-title-link")]')[index]
            job_id = anchorEle.get_attribute("id")
            print("JOB ID", job_id)
            job_page_link_achor = "https://www.dice.com/job-detail/" + job_id
            print("JOB LINK", job_page_link_achor)
            links.append({"keyword": keyword, "category": category,
                         "job_link": job_page_link_achor})
        except Exception as e:
            print("JOB CARD ERROR", e)
            continue
    time.sleep(30)

    # check if there is next page
    try:
        next_page_x_path = '//li[contains(@class,"pagination-next")]'
        next_button = keyword_driver.find_element(By.XPATH, next_page_x_path)
        next_button.click()
    except TimeoutException:
        keyword_driver.quit()

    # keyword_driver.quit()
    return links


if __name__ == "__main__":
    base_obj = BASE("requests")
    countries = ["United States", "Canada",
                 "Australia", "United Kingdom", "New Zealand"]
    us_proxies = base_obj.get_us_proxy()
    all_job_links = []
    country_index = 0
    for country in template_urls:
        scrape_country = countries[country_index]
        country_index += 1
        for catgry in job_tiles_with_categories:
            cat_keywords = job_tiles_with_categories[catgry]
            for keyword in cat_keywords:
                print("starting for", keyword)
                # if f"{catgry} : {keyword}\n" in skip_status:
                #     continue
                write_file(f"{catgry} : {keyword}", "keywords")
                url = template_urls[country].format(
                    keyword.replace(' ', '%20'))
                proxy_in = base_obj.get_proxy()
                print("parsing page for", keyword, "...")

                keyword_links = get_job_links_for_keyword(url, catgry, keyword, scrape_country)
                print("KEYWORDS LINKS", keyword_links)

                print("end for ", keyword)

    base_obj.db_close_connection()
