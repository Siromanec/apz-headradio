# data access idk

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://root:root_pass@post_db_1:27017,post_db_2:27018,post_db_3:27019/?replicaSet=rs0")

db = client["post_db"]
collection = db["posts"]

async def get_user_posts(user):
    cursor = collection.find({"username": user})
    items = await cursor.to_list(length=100)
    return items

async def new_post(username, article, time):
    post = {"username": username,
            "time": time,
            "article": article}
    await collection.insert_one(post)

async def delete_post(post):
    await collection.delete_one({"post_id": post})


