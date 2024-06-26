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
import socket
import hazelcast

message_queue = None

@asynccontextmanager
async def lifespan(app):
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    c = consul.Consul(host="consul")
    c.agent.service.register(name='profile',
                         service_id=f'{ip_addr}-8081',
                         address='profile',
                         port=8081)
    
    cluster_name = (c.kv.get("hazelcast/cluster-name")[1]["Value"]).decode()
    client = hazelcast.HazelcastClient(cluster_name=cluster_name, cluster_members=["hazelcast"])

    global message_queue
    messages_queue_name = (c.kv.get("hazelcast/queue-name")[1]["Value"]).decode()
    message_queue = client.get_queue(messages_queue_name)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/get-pfp/")
async def get_pfp(user: str, response: Response):
    try:
        profile_picture = await service.get_user_data(user)
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
        user_data = await service.get_user_data(user)
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
async def set_profile_photo(request: Request, response: Response):
    try:
        item = await request.json()
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
    username = item["username"]
    try:
        await service.modify_profile_photo(username, item["image"])
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
async def set_music(user: str, music: str, response: Response):
    try:
        await service.set_music(user, music)
    except KeyError:
        response.status_code = status.HTTP_409_CONFLICT
        log = f"profile-service: no such user {user}"
        print(log)
        message_queue.put(log)
        return
    response.status_code = status.HTTP_200_OK
    print(f"profile-service: User {user} set music to {music}.")
    message_queue.put(f"profile-service: User {user} set music to {music}.")

@app.post("/create-profile/")
async def create_profile(user: str, response: Response):
    try:
        await service.create_profile(user)
    except KeyError:
        response.status_code = status.HTTP_409_CONFLICT
        log = f"profile-service: user {user} already exists"
        print(log)
        message_queue.put(log)
        return
    response.status_code = status.HTTP_200_OK
    print(f"profile-service: User {user} created profile.")
    message_queue.put(f"profile-service: User {user} created profile.")