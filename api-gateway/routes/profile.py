import json
from typing import override

import consul
from fastapi import FastAPI, Response, Request, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.cbv import cbv
import requests
import httpx
import asyncio

from .service_getter import service_getter

router = APIRouter()

@cbv(router)
class ProfileService():
    name = "profile"

    @router.get("/show-profile/")
    async def show_profile(self, username: str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/get-user-data/?user={username}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.get(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message

    @router.post("/set-profile-photo/")
    async def set_profile_photo(self, request: Request, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/set-profile-photo/'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.post(url, data=request)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message

    @router.post("/set-music/")
    async def set_music(self, user: str, music: str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/set-music/?user={user}&music={music}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.post(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message
