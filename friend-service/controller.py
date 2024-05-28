from contextlib import asynccontextmanager

import fastapi
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
import repository
import consul
import hazelcast
import socket

message_queue = None

@asynccontextmanager
async def lifespan(app):
    await repository.start_session()
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    c = consul.Consul(host="consul")
    c.agent.service.register(name='friend',
                            service_id=f'{ip_addr}-8083',
                            address='friend',
                            port=8083)
    
    cluster_name = (c.kv.get("hazelcast/cluster-name")[1]["Value"]).decode()
    client = hazelcast.HazelcastClient(cluster_name=cluster_name, cluster_members=["hazelcast"])
    global message_queue
    messages_queue_name = (c.kv.get("hazelcast/queue-name")[1]["Value"]).decode()
    message_queue = client.get_queue(messages_queue_name)
    yield
    await repository.end_session()

app = FastAPI(lifespan=lifespan)


@app.get("/get-following/")
async def get_following(username: str, response: Response):
    friends = await service.get_following(username)
    response.status_code = status.HTTP_200_OK
    print(f"friends-service: followings of {username} - {friends}")
    message_queue.put(f"friends-service: followings of {username} - {friends}")
    return {"following": friends}

@app.get("/get-followers/")
async def get_followers(username: str, response: Response):
    friends = await service.get_followers(username)
    response.status_code = status.HTTP_200_OK
    print(f"friends-service: followers of {username} - {friends}")
    message_queue.put(f"friends-service: followers of {username} - {friends}")
    return {"followers": friends}


@app.get("/get-friends/")
async def get_friends(username: str, response: Response):
    friends = await service.get_friends(username)
    response.status_code = status.HTTP_200_OK
    log = f"friends-service: mutual friends of {username} - {friends}"
    print(log)
    message_queue.put(log)
    return {"friends": friends}

@app.post("/add-friend/")
async def add_friend(username_follows: str, username: str, response: Response):
    await service.add_friend(username_follows, username)
    response.status_code = status.HTTP_200_OK
    print(f"friends-service: {username_follows} and {username} are now friends.")
    message_queue.put(f"friends-service: {username_follows} and {username} are now friends.")


@app.post("/remove-friend/")
async def remove_friend(username_follows: str, username: str, response: Response):
    await service.remove_friend(username_follows, username)
    response.status_code = status.HTTP_200_OK
    print(f"friends-service: {username_follows} and {username} are no longer friends.")
    message_queue.put(f"friends-service: {username_follows} and {username} are no longer friends.")