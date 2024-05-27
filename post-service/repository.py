# data access idk

from pymongo import MongoClient

client = MongoClient("mongodb://root:root_pass@post_db:27017/")

db = client["post_db"]
collection = db["posts"]

def get_user_posts(user):
    return list(collection.find({"username": user}))

def new_post(username, article, time):
    post = {"username": username,
            "time": time,
            "article": article}
    collection.insert_one(post)

def delete_post(post):
    collection.delete_one({"post_id": post})


