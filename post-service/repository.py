# data access idk

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from bson import json_util
import json
import os
import datetime

client = MongoClient("mongodb://root:root_pass@localhost:27017/")

db = client["post_db"]
collection = db["posts"]

def get_user_posts(user):
    return list(collection.find({"username": user}))

def new_post(items):
    collection.insert_one(items)

def delete_post(post):
    collection.delete_one({"post_id": post})

print(get_user_posts("user1"))
print(new_post({"username": "user1", "post_id": 1, "time": datetime.datetime.now(), "article": "This is a post"}))
print(get_user_posts("user1"))
print(delete_post(1))
print(get_user_posts("user1"))
