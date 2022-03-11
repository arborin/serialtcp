# sudo apt-get install python3-pymongo

import pymongo
from pymongo import MongoClient


client = MongoClient('mongodb://192.168.1.50:27017/')

print(client)

db = client['learning']

print(db)
#Creating a collection
coll = db['upwork']
book = db['books']
print(coll)

# coll.insert_one({
#     "name": "jemali",
#     "age": 20
# })
# doc = coll.find_one({'PartNo':'HHAR2502301'})
book_1 = book.find_one()

# book.update_one(book_1, {"$set": {"year" : 2000 }})
print(book_1)