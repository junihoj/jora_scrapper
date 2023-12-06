#python buitin
import sys
import time
#selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException,ElementClickInterceptedException

# driver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# proxy
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
#internal

sys.path.append("..")
from scrapper import BASE

# req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
# proxies = req_proxy.get_proxy_list() #this will create proxy list

# ind=[]
# def get_all_proxy():
#     # with open ('proxies.txt', "w+") as f:
    # for proxy in proxies:
    #     if proxy.country == 'India':
    #         ind.append(proxy)

base_obj = BASE("requests")
proxy_in = base_obj.get_us_proxy()
proxy_address = proxy_in[0]["proxy_address"]
port = proxy_in[0]["ports"]['http']
PROXY = f'{proxy_address}:{port}'
print("HERE IS THE PROXY", PROXY)      
webdriver.DesiredCapabilities.CHROME['proxy']={
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "proxyType":"MANUAL",   
}
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get('https://www.expressvpn.com/what-is-my-ip')

time.sleep(30)

if __name__ == "__main__":
    print("started")
    