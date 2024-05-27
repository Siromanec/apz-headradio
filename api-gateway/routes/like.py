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
class LikeService():
    name = "likes"
    @router.post("/add-like/")
    async def add_like(self, username: str, post_id: str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/add-like/?user={username}&post={post_id}'
        async with httpx.AsyncClient() as client:
            try:
                redirect_response = await client.post(url)
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                return None
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message

    @router.delete("/remove-like")
    async def remove_like(self, username: str, post_id: str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/remove-like/?user={username}&post={post_id}'
        async with httpx.AsyncClient() as client:
            try:
                redirect_response = await client.delete(url)
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                return None
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            return message

    @router.get("/get-likes")
    async def get_likes(self, post_id: str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/get-likes/?post={post_id}'
        async with httpx.AsyncClient() as client:
            try:
                redirect_response = await client.get(url)
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                return {"likes": []}
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            if code == status.HTTP_200_OK:
                return message
            return {"likes": []}

    @router.get("/has-liked")
    async def has_liked(self, username: str, post_id: str, response: Response):
        hostport = service_getter.get_service_hostport(self.name)
        url = f'http://{hostport}/has-liked/?user={username}&post={post_id}'
        async with httpx.AsyncClient() as client:
            try:
                redirect_response = await client.get(url)
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                return {"has_liked": None}
            message = redirect_response.json()
            code = redirect_response.status_code
            response.status_code = code
            if code == status.HTTP_200_OK:
                return message
            return {"has_liked": None}

