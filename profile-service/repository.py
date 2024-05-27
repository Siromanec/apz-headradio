# data access idk

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://root:root_pass@profile_db:27017/")

db = client["profile_db"]
collection = db["profile"]

async def get_user_data(user):
    user_data = await collection.find_one({"username": user})
    if user_data is not None:
        return user_data
    raise KeyError

async def modify_profile_photo(user, profile_photo):
    if await collection.find_one({"username": user}) is None:
        print("no user")
        raise KeyError
    await collection.update_one({"username": user}, {"$set": {"profile_picture": profile_photo}})

async def set_music(user, song_name):
    if await collection.find_one({"username": user}) is None:
        print("no user")
        raise KeyError
    await collection.update_one({"username": user}, {"$set": {"selected_music": song_name}})

async def create_profile(user):
    if await collection.find_one({"username": user}) is None:
        await collection.insert_one({"username": user})
        return
    raise KeyError

# create_profile("user")
# print(get_user_data("user"))
# set_music("user", "song_name")
# modify_profile_photo("user", {"profilePicture": "profile_picture"})
# print(get_user_data("user"))
# print(get_pfp("user"))

