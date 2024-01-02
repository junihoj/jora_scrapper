import os
import zipfile
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

# PROXY_HOST = '192.168.3.2'  # rotating proxy or host
# PROXY_PORT = 8080 # port
# PROXY_USER = 'proxy-user' # username
# PROXY_PASS = 'proxy-password' # password

PROXY_HOST = '38.170.190.247'  # rotating proxy or host
PROXY_PORT = 9598 # port
PROXY_USER = 'spmcbdkr' # username
PROXY_PASS = 'f2puv4moz6e1' # password

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    # chrome_options = webdriver.ChromeOptions()
    chrome_options = Options()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    # driver = webdriver.Chrome(
    #     os.path.join(path, 'chromedriver'),
    #     chrome_options=chrome_options)
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options)
    return driver

def main():
    driver = get_chromedriver(use_proxy=True)
    #driver.get('https://www.google.com/search?q=my+ip+address')
    # driver.get('https://httpbin.org/ip')
    driver.get("https://dice.com")
    time.sleep(30)

if __name__ == '__main__':
    main()