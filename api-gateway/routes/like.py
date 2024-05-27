from typing import override

import consul
from fastapi import FastAPI, Response, Request, APIRouter, status, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.cbv import cbv
import requests
import httpx
import asyncio
from .pechyvo import unauthorized

from .service_getter import service_getter



router = APIRouter()

@cbv(router)
class LikeService():
    name = "likes"
    @router.post("/add-like/")
    async def add_like(self, username: str, post_id: str, response: Response, token: str):
        if (res := unauthorized(username, response, token)):
            repository.put_message(f"like-service: add-like of {username} with code {response.status_code}")
            return res
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/add-like/?user={username}&post={post_id}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.post(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            repository.put_message(f"like-service: add-like of {username} with code {code}")
            return message

    @router.delete("/remove-like")
    async def remove_like(self, username: str, post_id: str, response: Response,token: str ):
        if (res := unauthorized(username, response, token)):
            repository.put_message(f"like-service: remove-like of {username} with code {response.status_code}")
            return res
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/remove-like/?user={username}&post={post_id}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.delete(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            repository.put_message(f"like-service: remove-like of {username} with code {code}")
            return message

    @router.get("/get-likes")
    async def get_likes(self, post_id: str, response: Response):            
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/get-likes/?post={post_id}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.get(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            repository.put_message(f"like-service: get-likes of {post_id} with code {code}")
            return message

    @router.get("/has-liked")
    async def has_liked(self, username: str, post_id: str, response: Response, token: str ):
        if (res := unauthorized(username, response, token)):
            repository.put_message(f"like-service: has-liked of {username} with code {response.status_code}")
            return res
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/has-liked/?user={username}&post={post_id}'
        async with httpx.AsyncClient() as client:
            redirect_response = await client.get(url)
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            repository.put_message(f"like-service: has-liked of {username} with code {code}")
            return message

