import fastapi
import requests.status_codes
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
import uuid
import os
import consul
from contextlib import asynccontextmanager
import socket
import hazelcast

message_queue = None


@asynccontextmanager
async def lifespan(app):
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    c = consul.Consul(host = "consul")
    c.agent.service.register(name='feed',
                         service_id=f'{ip_addr}-8085',
                         address='feed',
                         port=8085)
    
    cluster_name = (c.kv.get("hazelcast/cluster-name")[1]["Value"]).decode()
    client = hazelcast.HazelcastClient(cluster_name=cluster_name, cluster_members=["hazelcast"])
    global message_queue
    messages_queue_name = (c.kv.get("hazelcast/queue-name")[1]["Value"]).decode()
    message_queue = client.get_queue(messages_queue_name)

    yield

app = FastAPI(lifespan=lifespan)


@app.get("/feed/")
async def feed(user: str, response: Response):
    posts =  await service.feed(user)
    response.status_code = status.HTTP_200_OK   
    print(f"feed-service: feed for {user}")
    message_queue.put(f"feed-service: feed for {user}")
    return posts


