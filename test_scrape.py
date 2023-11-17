from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time
#driver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://us.jora.com/")

input_title = driver.find_element(By.XPATH, '//input[@placeholder="Job title, company, keyword"]')
city_district_state = driver.find_element(By.XPATH, '//input[@placeholder="City, district, state"]')

input_title.send_keys("python developer")
input_title.send_keys(Keys.RETURN)

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
# //div[@class="modal-header"]/div
# time.sleep(100)
wait_job_cards = WebDriverWait(driver, 180).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="job-card result organic-job -split-view"]'))
    )
job_cards = driver.find_elements(By.XPATH, '//div[@class="job-card result organic-job -split-view"]')
driver.execute_script("arguments[0].click();", job_cards[0])
job_cards[0].click()


# wait_apply_button = WebDriverWait(driver, 180).until(
#         EC.presence_of_element_located((By.XPATH, '//a[@data-gtm="apply-job"]'))
#     )
# job type //div[@class="badge -default-badge"]/div[@class="content"]
# job title //h3[@class="job-title heading-xxlarge"]
# company //span[@class="company"]
# location //span[@class="location"]
time.sleep(100)

driver.quit()

# job_cards = driver.find_elements(By.XPATH, '//div[@class="job-card result organic-job -split-view"]')
# job_cards[0].click()
# us_button[0].click()


