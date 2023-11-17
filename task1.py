from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()

driver.get("https://www.glassdoor.com/Job/index.htm")
element = driver.find_element(By.ID,"searchBar-jobTitle")
element.send_keys("python developer")
element = driver.find_element(By.ID,"searchBar-location")
element.send_keys("United States")
driver.implicitly_wait(100)
element.send_keys(Keys.RETURN)
driver.implicitly_wait(100)



