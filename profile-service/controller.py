from contextlib import asynccontextmanager

import fastapi
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
import uuid
import os
import repository
import consul

import hazelcast

message_queue = None

@asynccontextmanager
async def lifespan(app):

    c = consul.Consul(host="consul")
    c.agent.service.register(name='profile',
                         service_id='profile',
                         address='profile',
                         port=8081)
    
    client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast"])

    global message_queue
    messages_queue_name = "messages_queue"
    message_queue = client.get_queue(messages_queue_name).blocking()

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/get-pfp/")
async def get_pfp(user: str, response: Response):
    profile_picture = service.get_pfp(user)
    response.status_code = status.HTTP_200_OK
    print(f"profile-service: profile picture of {user} - {profile_picture}")
    message_queue.put(f"profile-service: profile picture of {user} - {profile_picture}")
    return {"get_pfp": profile_picture}

@app.get("/get-user-data/")
async def get_user_data(user: str, response: Response):
    user_data = service.get_user_data(user)
    response.status_code = status.HTTP_200_OK
    if user_data != None:
        print(f"profile-service: data of {user} - {user_data}")
        message_queue.put(f"profile-service: data of {user} - {user_data}")
        user_data = list(map(lambda x: {"username": user_data["username"], "profile_picture": user_data["profile_picture"], "selected_music": user_data["selected_music"], "motto": user_data["motto"]}, user_data))
        return {"get_user_data": user_data}
    else:
        print("profile-service: User not found.")
        message_queue.put("profile-service: User not found.")
        return {"get_user_data": "User not found."}

@app.post("/modify-profile-photo/")
async def modify_profile_photo(request: Request, response: Response):
    item = await request.json()
    filename = str(uuid.uuid4())
    try:
        while os.path.isfile("./data/" + filename):
            filename = str(uuid.uuid4())
        with open("./data/" + filename, "w") as file:
            file.write(item["image"])
        username = item["username"]
        service.modify_profile_photo("user", {"profilePicture": f"'{filename}'"}, f"`username`='{username}'")
        response.status_code = status.HTTP_200_OK
        print(f"profile-service: User {username} modified profile photo.")
        message_queue.put(f"profile-service: User {username} modified profile photo.")
    except FileNotFoundError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        print(f"profile-service: User failed to modify profile photo. There is no such file.")
        message_queue.put(f"profile-service: User failed to modify profile photo. There is no such file.")

@app.post("/set-music/")
async def set_music(user: str, song_name: str, response: Response):
    service.set_music(user, song_name)
    response.status_code = status.HTTP_200_OK
    print(f"profile-service: User {user} set music to {song_name}.")
    message_queue.put(f"profile-service: User {user} set music to {song_name}.")

@app.post("/create-profile/")
async def create_profile(user: str, response: Response):
    service.create_profile(user)
    response.status_code = status.HTTP_200_OK
    print(f"profile-service: User {user} created profile.")
    message_queue.put(f"profile-service: User {user} created profile.")