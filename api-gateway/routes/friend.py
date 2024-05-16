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
class FriendService():
    name = 'friendzone'
    @router.get("/get-following/")
    async def get_following(self, username:str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/get-following/?user={username}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.get(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message

    @router.get("/get-followers/")
    async def get_followers(self, username:str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/get-followers/?username={username}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.get(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message

    @router.get("/get-friends/")
    async def get_followers(self, username:str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/get-friends/?username={username}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.get(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message

    @router.post("/add-friend/")
    async def add_friend(self, username_follows:str, username:str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/add-friend/?username_follows={username_follows}&username={username}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.post(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message

    @router.post("/remove-friend/")
    async def remove_friend(self, username_follows:str, username:str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/remove-friend/?username_follows={username_follows}&username={username}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.post(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message