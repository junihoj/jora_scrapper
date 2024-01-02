from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
chrome_options = Options()
chrome_options.add_extension("proxy.zip")
# executable_path='chromedriver.exe', chrome_options=chrome_options
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get("http://httpbin.org/ip")
time.sleep(30)
driver.close()