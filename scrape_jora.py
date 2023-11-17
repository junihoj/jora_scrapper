import pathlib
import csv
import os
import sys
import requests
from scrapper import BASE
from constants import job_tiles_with_categories
from constants import keywordfilter

BASE_DIR = pathlib.Path(__file__).parent.resolve()

skip_status = []

def read_file(filename):
    filename = f'{BASE_DIR}/{filename}.txt'
    with open(filename, 'r+') as file:
        for line in file:
            skip_status.append(line)
read_file("keywords")

if os.path.exists("scraped_data.csv"):
  os.remove("scraped_data.csv")
else:
  print("The file does not exist")

# assign header columns
headerList = ['Scrape_Date', 'Platform', 'Job_title', 'Job_Category','Job_Link','Job_Location','Company_Name','keyword',"","type_of_job","job_description","posted_time","scrape_country"]

# open CSV file and assign header
with open("scraped_data.csv", 'a') as file:
    dw = csv.DictWriter(file, delimiter=',',fieldnames=headerList)
    dw.writeheader()

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
print(scriptPath)


# if __name__== "__main__":
#     base_obj = BASE('requests')
#     session = requests.session()
#     session.trust_env=False
#     base_obj.db_open_connection()
#     dt_string = base_obj.fetch_date("%d-%m-%Y")
#     read_file("keywords")