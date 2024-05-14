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

import hazelcast

message_queue = None


@asynccontextmanager
async def lifespan(app):
    c = consul.Consul(host = "consul")
    c.agent.service.register(name='feed',
                         service_id='feed',
                         address='feed',
                         port=8085)
    
    client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast"])
    global message_queue
    messages_queue_name = "messages_queue"
    message_queue = client.get_queue(messages_queue_name)

    yield

app = FastAPI(lifespan=lifespan)


@app.get("/feed/")
async def feed(user: str, response: Response):
    posts = service.feed(user)
    response.status_code = status.HTTP_200_OK
    print(f"feed-service: feed of {user}")
    message_queue.put(f"feed-service: feed of {user}")
    return {"posts": posts}
