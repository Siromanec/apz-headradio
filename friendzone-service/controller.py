from contextlib import asynccontextmanager

import fastapi
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
import repository
import consul

@asynccontextmanager
async def lifespan(app):
    repository.start_session()
    c = consul.Consul()
    c.agent.service.register(name='friendzone',
                            service_id='friendzone',
                            address='friendzone',
                            port=8084)
    yield
    repository.end_session()

app = FastAPI(lifespan=lifespan)

@app.get("/get-friends/")
async def get_friends(user: str, response: Response):
    friends = service.get_friends(user)
    response.status_code = status.HTTP_200_OK
    return {"friends": friends}


@app.post("/add-friend/")
async def add_friend(user1: str, user2: str, response: Response):
    service.add_friend(user1, user2)
    response.status_code = status.HTTP_200_OK


@app.post("/remove-friend/")
async def remove_friend(user1: str, user2: str, response: Response):
    service.remove_friend(user1, user2)
    response.status_code = status.HTTP_200_OK