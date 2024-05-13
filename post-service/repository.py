# data access idk

from pymongo import MongoClient

client = MongoClient("mongodb://root:root_pass@post_db:27017/")

db = client["post_db"]
collection = db["posts"]

def get_user_posts(user):
    return list(collection.find({"username": user}))

def new_post(items):
    collection.insert_one(items)

def delete_post(post):
    collection.delete_one({"post_id": post})


