from pymongo import MongoClient
import pandas as pd
from date_functions import get_data_from_server, get_n_days_before_date
client = MongoClient('mongodb+srv://leadgenapp:bhglIbpYTJXCcxdO@cluster0.scrcs.mongodb.net/')
db = client['leadbackend']
input_csv_file = '14-12-2023-14-05-31 Rawleads_final (1).csv'
input_dataframe = pd.DataFrame(input_csv_file)
input_to_dict = input_dataframe.to_dict(orient='records')
# get_data_from_server()

print(db.list_collection_names())
# api_continuousleadscrape
# api_companiesdata
companies_data_collection = db.get_collection('api_continuousleadscrape')
companies_data = companies_data_collection.find({})
companies_list = list(companies_data)
print("LIST LENGTH", len(companies_list))
companies_dataframe = pd.DataFrame(companies_list)
print(companies_dataframe.head())

# print(companies_data)
# print('there')
# print(list(companies_data)[0,5])
# data = pd.DataFrame(companies_data)
# print('data frame')
# print(data.head)