from typing import override

import consul
from fastapi import FastAPI, Response, Request, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.cbv import cbv
import requests
import httpx
import asyncio

import repository

from .service_getter import service_getter

router = APIRouter()


@cbv(router)
class AuthService():
    name = "auth"

    @router.post("/login/")
    async def login(self, user: str, password: str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/login/?user={user}&password={password}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.post(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            if code == status.HTTP_200_OK:
                token = str(message["token"])
                repository.add_token(user, token)
                return {"token": token}
            return {"token": None}

    @router.post("/logout/")
    async def logout(self, user: str, response: Response):
        repository.remove_token(user)
        response.status_code = status.HTTP_200_OK
