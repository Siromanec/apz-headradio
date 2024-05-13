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
    c = consul.Consul(host="consul")
    c.agent.service.register(name='likes',
                         service_id='likes',
                         address='likes',
                         port=8079)

    yield
    repository.end_session()

app = FastAPI(lifespan=lifespan)

@app.get("/has-liked/")
async def has_liked(user: str, post: int, response: Response):
    liked = service.has_liked(user, post)
    response.status_code = status.HTTP_200_OK
    return {"has_liked": liked}


@app.post("/add-like/")
async def add_like(user: str, post: int, response: Response):
    service.add_like(user, post)
    response.status_code = status.HTTP_200_OK


@app.post("/remove-like/")
async def remove_like(user: str, post: int, response: Response):
    service.remove_like(user, post)
    response.status_code = status.HTTP_200_OK


@app.get("/get-likes/")
async def get_likes(post: int, response: Response):
    likes = service.get_likes(post)
    response.status_code = status.HTTP_200_OK
    return {"likes": likes}
