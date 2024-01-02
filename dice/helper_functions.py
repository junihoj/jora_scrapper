from selenium.webdriver.common.by import By
def get_select_proxy(base_obj):
    us_proxies = base_obj.get_us_proxy()
    
    return us_proxies[0]

def get_element_attr_by_xpath(driver, xpath, attr):
    try:
        ele = driver.find_element(By.XPATH, xpath)
        return ele.get_attribute(attr)
        # return ele.text
    except:
        return ""
