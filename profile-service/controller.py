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
    message_queue = client.get_queue(messages_queue_name)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/get-pfp/")
async def get_pfp(user: str, response: Response):
    try:
        profile_picture = service.get_user_data(user)
    except KeyError:
        response.status_code = status.HTTP_409_CONFLICT
        log = f"profile-service: no such user {user}"
        print(log)
        message_queue.put(log)
        return

    try:
        profile_picture = profile_picture["profile_picture"]
    except KeyError:
        profile_picture = None

    response.status_code = status.HTTP_200_OK
    print(f"profile-service: profile picture of {user} - {profile_picture}")
    message_queue.put(f"profile-service: profile picture of {user} - {profile_picture}")
    return {"profile_picture": profile_picture}

@app.get("/get-user-data/")
async def get_user_data(user: str, response: Response):
    try:
        user_data = service.get_user_data(user)
    except KeyError:
        response.status_code = status.HTTP_409_CONFLICT
        log = f"profile-service: no such user {user}"
        print(log)
        message_queue.put(log)
        return
    response.status_code = status.HTTP_200_OK
    print(f"profile-service: data of {user} - {user_data}")
    message_queue.put(f"profile-service: data of {user} - {user_data}")
    del user_data["_id"]
    return user_data

@app.post("/set-profile-photo/")
async def modify_profile_photo(request: Request, response: Response):
    item = await request.json()
    username = item["username"]
    try:
        service.modify_profile_photo(username, item["image"])
    except KeyError:
        response.status_code = status.HTTP_409_CONFLICT
        log = f"profile-service: no such user {username}"
        print(log)
        message_queue.put(log)
        return
    response.status_code = status.HTTP_200_OK
    print(f"profile-service: User {username} modified profile photo.")
    message_queue.put(f"profile-service: User {username} modified profile photo.")


@app.post("/set-music/")
async def set_music(user: str, song_name: str, response: Response):
    try:
        service.set_music(user, song_name)
    except KeyError:
        response.status_code = status.HTTP_409_CONFLICT
        log = f"profile-service: no such user {user}"
        print(log)
        message_queue.put(log)
        return
    response.status_code = status.HTTP_200_OK
    print(f"profile-service: User {user} set music to {song_name}.")
    message_queue.put(f"profile-service: User {user} set music to {song_name}.")

@app.post("/create-profile/")
async def create_profile(user: str, response: Response):
    try:
        service.create_profile(user)
    except KeyError:
        response.status_code = status.HTTP_409_CONFLICT
        log = f"profile-service: user {user} already exists"
        print(log)
        message_queue.put(log)
        return
    response.status_code = status.HTTP_200_OK
    print(f"profile-service: User {user} created profile.")
    message_queue.put(f"profile-service: User {user} created profile.")