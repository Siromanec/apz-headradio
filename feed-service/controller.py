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


@asynccontextmanager
async def lifespan(app):
    c = consul.Consul(host = "consul")
    c.agent.service.register(name='feed',
                         service_id='feed',
                         address='feed',
                         port=8085)

    yield

app = FastAPI(lifespan=lifespan)


@app.get("/feed/")
async def feed(user: str, response: Response):
    service.feed(user)
    response.status_code = status.HTTP_200_OK
