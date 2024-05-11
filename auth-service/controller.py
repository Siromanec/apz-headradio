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

@app.post("/login/")
async def login(user: str, password: str, response: Response):
    service.login(user, password)
    response.status_code = status.HTTP_200_OK

@app.post("/register/")
async def register(user: str, password: str, email:str, response: Response):
    service.register(user, password, email)
    response.status_code = status.HTTP_200_OK