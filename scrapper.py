import sys
import os
import json

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append("../../base_scrapper/base_selenium")
from base_selenium import SELENIUM

sys.path.append("../../base_scrapper/base_requests")
from base_requests import REQUESTS

sys.path.append("../../base_scrapper/base_traceback")
from base_trace_back import TRACEBACK
import pathlib
from datetime import datetime
import csv
import requests
import random
# import psycopg2
# import pymysql.cursors
import traceback
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class BASE(SELENIUM, REQUESTS, TRACEBACK):
    def __init__(self, process="requests"):
        self.done_comps = {}
        TRACEBACK.__init__(self)
        self.tracking_obj = BASE
        if process.lower() == "selenium":
            SELENIUM.__init__(self)
        elif process.lower() == "requests":
            REQUESTS.__init__(self)


        else:
            self.process_error()

        self.proxies = []
        self.BASE_DIR = pathlib.Path(__file__).parent.resolve()
        self.initialize_proxies()
        self.conn = None
        self.cur = None
        self.zwilt_base_url = "http://127.0.0.1:8000/api{}"

    def fetch_date(self, format="%d-%m-%Y-%H-%M-%S"):
        now = datetime.now()
        dt_string = now.strftime(format)
        return dt_string

    def process_error(self):
        raise "ProcessModeError: mode not selected"

    def clean_data(self, data):
        try:
            if data and isinstance(data, str):
                data = data.encode('ascii', 'ignore').decode()
        except Exception as e:
            print(e)
            self.tracking_obj.tracebackError(self.clean_data.__name__, self.fetch_date())
            return ''
        return data

    def get_dict_value(self, data, key_list, default=''):
        try:
            for key in key_list:
                if data and isinstance(data, dict):
                    data = data.get(key, default)
                else:
                    return default
        except Exception as e:
            print(e)
            self.tracking_obj.tracebackError(self.get_dict_value.__name__, self.fetch_date())
            return default
        return self.clean_data(data)

    def get_list_index(self, lst, index, default=''):
        try:
            return lst[index] if len(lst) > index else default
        except Exception as e:
            print(e)
            self.tracking_obj.tracebackError(self.get_list_index.__name__, self.fetch_date())
            return default

    def file_write(self, name='file', mode='a', encoding='utf-8', data=[]):
        with open(f'{name}.csv', mode=mode, newline='', encoding=encoding) as file:
            writer = csv.writer(file)
            writer.writerow(data)
            file.close()

    def initialize_proxies(self):
        try:
            for page in range(1, 3):
                response = requests.get("https://proxy.webshare.io/api/proxy/list/?page=" + str(
                    page), headers={"Authorization": "Token 697bfb06a037cccc135419ceb1d08669b1f15384"})
                pr = response.json()
                print("Total Proxies: " + str(len(pr['results'])))
                self.proxies += pr['results']
        except Exception as e:
            self.tracking_obj.tracebackError(self.initialize_proxies.__name__, self.fetch_date())
            return "ProxyError: " + str(e)

    def get_proxy(self):
        if self.proxies:
            pr = random.randint(0, 9)
            proxy = self.proxies[pr]['proxy_address'].strip()
            port = self.proxies[pr]['ports']['http']
            user = self.proxies[pr]['username'].strip()
            password = self.proxies[pr]['password'].strip()
            proxy_in = {
                'http': 'http://{}:{}@{}:{}/'.format(user, password, proxy, port),
                'https': 'http://{}:{}@{}:{}/'.format(user, password, proxy, port)
            }
            return proxy_in

    def get_proxy_withcred(self):
        if self.proxies:
            pr = random.randint(0, 9)
            proxy = self.proxies[pr]['proxy_address'].strip()
            port = self.proxies[pr]['ports']['http']
            user = self.proxies[pr]['username'].strip()
            password = self.proxies[pr]['password'].strip()
            proxy_in = {
                'http': 'http://{}:{}@{}:{}/'.format(user, password, proxy, port),
                'https': 'http://{}:{}@{}:{}/'.format(user, password, proxy, port),
                'username':user,
                'password':password
            }
            return proxy_in

    def db_open_connection(self, db_name='punch_scrappers', user='user', host='localhost', password=''):
        # self.conn = pymysql.connect(host='localhost',
        #                             user='root',
        #                             password=password,
        #                             database=db_name,
        #                             cursorclass=pymysql.cursors.DictCursor)
        # with self.conn:
        #     with self.conn.cursor() as cursor:
        #         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        #         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        # self.conn = psycopg2.connect(dbname=db_name,
        #                              user=user,
        #                              host=host,
        #                              password=password)
        # self.cur = self.conn.cursor()
        pass

    def db_insertion(self, table, data):
        payload = {
            "scrape_source": data[1],
            "scrape_company_name": data[6],
            "scrape_company_domain": data[8],
            "scrape_job_title": data[2],
            "scrape_job_url": data[4],
            "scrape_job_location": data[5],
            "scrape_category": data[3],
            "scrape_keyword": data[7],
            "scrape_type_of_job": data[9],
            "scrape_job_description": data[10],
            "scrape_posted_time": data[11],
            "scrape_country": data[12]
        }
        scrape_data_upload = self.zwilt_base_url.format("/continuous-lead-scrape/")
        response = requests.post(scrape_data_upload, data=payload)
        print(response.text)
        # self.cur.execute(
        #
        #     f"INSERT INTO {table} (scrape_date, source, title, category, url, location, company, keyword, domain) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        #     data)
        # self.conn.commit()

    def db_close_connection(self):
        self.cur.close()
        self.conn.close()

    def check_company(self, title='', keyword='', company_name='', catgy=''):
        if (company_name.lower() not in self.done_comps) and (
                ((title.lower() in keyword.lower() or keyword.lower() in title.lower())
                 or (title.lower() in catgy.lower() or catgy.lower() in title.lower()))
                or ((fuzz.ratio(title.lower(), keyword.lower()) > 30) or
                    (fuzz.ratio(title.lower(), catgy.lower()) > 30))):
            self.done_comps[company_name.lower()] = True
            return True
    # def track_backError(self):
    #     error_type, error, tb = sys.exc_info()
    #     filename, lineno, func_name, line = traceback.extract_tb(tb)[-1]
    #     print(filename, lineno, func_name, line)
