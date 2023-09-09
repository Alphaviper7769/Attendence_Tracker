from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") 

db = client["Hack24"]  


collection = db["Teacher"]  
