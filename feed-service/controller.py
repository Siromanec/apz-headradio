import fastapi
import requests.status_codes
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
import uuid
import os

app = FastAPI()

@app.post("/feed/")
async def feed(user: str, response: Response):
    service.feed(user)
    response.status_code = status.HTTP_200_OK
