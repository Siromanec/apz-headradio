import json
from typing import override

import consul
from fastapi import FastAPI, Response, Request, APIRouter, status, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.cbv import cbv
import requests
import httpx
import asyncio
from .pechyvo import unauthorized
import repository

from .service_getter import service_getter

router = APIRouter()

@cbv(router)
class ProfileService():
    name = "profile"

    @router.get("/show-profile/")
    async def show_profile(self, username: str, response: Response, token: str):
        if (res := unauthorized(username, response, token)):
            repository.put_message(f"profile-service: show-profile of {username} with code {response.status_code}")
            return res
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/get-user-data/?user={username}'
        async with httpx.AsyncClient() as client:
            try:
                redirect_response = await client.get(url)
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                return None
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            repository.put_message(f"profile-service: show-profile of {username} with code {code}")
            return message

    @router.post("/set-profile-photo/")
    async def set_profile_photo(self, request: Request, response: Response, token: str):
        if (res := unauthorized(request["username"], response, token)):
            repository.put_message(f"profile-service: set-profile-photo of {request["username"]} with code {response.status_code}")
            return res
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/set-profile-photo/'
        async with httpx.AsyncClient() as client:
            try:
                redirect_response = await client.post(url, content=await request.body())
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                return None
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            repository.put_message(f"profile-service: set-profile-photo of {request["username"]} with code {code}")
            return message

    @router.post("/set-music/")
    async def set_music(self, user: str, music: str, response: Response, token: str):
        if (res := unauthorized(user, response, token)):
            repository.put_message(f"profile-service: set-music of {user} with code {response.status_code}")
            return res
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/set-music/?user={user}&music={music}'
        async with httpx.AsyncClient() as client:
            try:
                redirect_response = await client.post(url)
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                return None
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            repository.put_message(f"profile-service: set-music of {user} with code {code}")
            return message
