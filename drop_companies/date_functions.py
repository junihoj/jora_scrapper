from datetime import datetime, timedelta
import dateutil
import requests
import json

punch_base_url = "http://127.0.0.1:8000/api{}"

def get_n_days_before_date(date_format="%d %B %Y", days_before=120):
 date_n_days_ago = datetime.now() - timedelta(days=days_before)
 return date_n_days_ago.strftime(date_format)


def get_data_from_server():
    get_companies_url = punch_base_url.format('/companies/')
    response = requests.get(get_companies_url)
    results_dict = json.loads(response.content)
    result = results_dict['queryset']

def format_date(date, format='%Y-%m-%d'):
   return date.strftime(format)

get_n_days_before_date(date_format="%d %B %Y", days_before=30)

# dt = datetime.strptime("2016-04-15T08:27:18-0500", "%Y-%m-%dT%H:%M:%S%z")

# YYYY-MM-DD HH:MM:SS.ssssss
# dt = datetime.strptime("2022-06-01 16:42:22.880", "YYYY-MM-DD")
# dt = datetime.strptime("2022-06-01 16:42:22.880", "%Y-%m-%d HH:MM:SS.ssssss")
# date_string = "2022-06-01 16:42:22.880".split(" ")[0]
# date_object = datetime.strptime(date_string, "%Y-%m-%d")
# print(date_object)

