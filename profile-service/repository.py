# data access idk

from pymongo import MongoClient

client = MongoClient("mongodb://root:root_pass@profile_db:27017/")

db = client["profile_db"]
collection = db["profile"]

def get_pfp(user):
    return collection.find_one({"username": user})['profile_picture']

def get_user_data(user):    
    return collection.find_one({"username": user})

def modify_profile_photo(user, user_data):
    collection.update_one({"username": user}, {"$set": {"profile_picture": user_data['profilePicture']}})

def set_music(user, song_name):
    collection.update_one({"username": user}, {"$set": {"selected_music": song_name}})

def create_profile(user):
    collection.insert_one({"username": user, "profile_picture": "", "selected_music": "", "motto": ""})

# create_profile("user")
# print(get_user_data("user"))
# set_music("user", "song_name")
# modify_profile_photo("user", {"profilePicture": "profile_picture"})
# print(get_user_data("user"))
# print(get_pfp("user"))

