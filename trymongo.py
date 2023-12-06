from pymongo import MongoClient
from pandas import DataFrame

client = MongoClient('mongodb+srv://leadgenapp:bhglIbpYTJXCcxdO@cluster0.scrcs.mongodb.net/')
db = client['leadbackend']

domain = db.get_collection("api_continuousleadscrape").find({
    
})

df = DataFrame(list(domain))
