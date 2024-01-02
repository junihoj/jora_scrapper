# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import sys
sys.path.append("..")
from scrapper import BASE

base_obj = BASE("requests")
proxy_in = base_obj.get_us_proxy()

proxy_address = proxy_address = proxy_in[0]["proxy_address"]
port = proxy_in[0]["ports"]['http']
proxy_username = proxy_in[0]['username']
proxy_password = proxy_in[0]['password']
is_valid = proxy_in[0]['valid']

options = Options()

# free proxy server URL
proxy_server_url = "157.245.97.60"
options.add_argument(f'--proxy-server={proxy_server_url}')
seleniumwire_options = {
    'proxy': {
        'http': f'http://{proxy_username}:{proxy_password}@{proxy_address}:{port}',
        'https': f'http://{proxy_username}:{proxy_password}@{proxy_address}:{port}',
        'verify_ssl': False,
    },
}
# create the ChromeDriver instance with custom options
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options,
    seleniumwire_options=seleniumwire_options
)

# driver.get('http://httpbin.org/ip')
driver.get('https://whatismyipaddress.com/')
time.sleep(30)