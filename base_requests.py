import requests
from lxml import html
import sys
import os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append("../../base_scrapper/base_traceback")
from base_trace_back import TRACEBACK
from datetime import datetime


class REQUESTS:
    def __init__(self):
        self.tracking_obj = TRACEBACK
        pass

    def get_list_index(self, lst, index, default=''):
        try:
            return lst[index] if len(lst) > index else default
        except Exception as e:
            print(e)
            self.tracking_obj.tracebackError(self.get_list_index.__name__, self.fetch_date())
            return default

    def fetch_date(self, format="%d-%m-%Y-%H-%M-%S"):
        now = datetime.now()
        dt_string = now.strftime(format)
        return dt_string

    def get_text_by_xpath(self, element, xpath, index):
        if not element and not xpath:
            return None
        ele = self.get_list_index(element.xpath(f'{xpath}//text()'), index)
        return ele.strip() if ele else ''

    def get_attribute_by_xpath(self, element, xpath, attr, index):
        if not element and not xpath:
            return None
        ele = self.get_list_index(element.xpath(f"{xpath}//@{attr}"), index)
        return ele if ele else ''
