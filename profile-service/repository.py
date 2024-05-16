# data access idk

from pymongo import MongoClient

client = MongoClient("mongodb://root:root_pass@profile_db:27017/")

db = client["profile_db"]
collection = db["profile"]

def get_user_data(user):
    if (user_data:=collection.find_one({"username": user})) is not None:
        print(user_data)
        return user_data
    raise KeyError

def modify_profile_photo(user, profile_photo):
    if collection.find_one({"username": user}) is None:
        print("no user")
        raise KeyError
    collection.update_one({"username": user}, {"$set": {"profile_picture": profile_photo}})

def set_music(user, song_name):
    if collection.find_one({"username": user}) is None:
        print("no user")
        raise KeyError
    collection.update_one({"username": user}, {"$set": {"selected_music": song_name}})

def create_profile(user):
    if collection.find_one({"username": user}) is None:
        collection.insert_one({"username": user})
        return
    raise KeyError

# create_profile("user")
# print(get_user_data("user"))
# set_music("user", "song_name")
# modify_profile_photo("user", {"profilePicture": "profile_picture"})
# print(get_user_data("user"))
# print(get_pfp("user"))

