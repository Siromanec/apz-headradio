from typing import override

import consul
from fastapi import FastAPI, Response, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.cbv import cbv
import requests
import httpx
import asyncio

import service



app = FastAPI()
router = APIRouter()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

c = consul.Consul(host = "consul")
c.agent.service.register(name='api-gateway',
                         service_id='api-gateway',
                         address='api-gateway',
                         port=8084)

class ServiceGetter():
    def _get_services(self, service_name):
        list_services = []
        services = c.health.service(service_name)[1]
        for service in services:
            adder = {}
            adder['Address'] = service['Service']['Address']
            adder['Port'] = service['Service']['Port']
            list_services.append(adder)
        print(list_services)
        return list_services
    def get_service_hostport(self, service_name):
        raise NotImplemented

class FirstServiceGetter(ServiceGetter):
    def __init__(self):
        super().__init__()

    @override
    def get_service_hostport(self, service_name):
        service = self._get_services(service_name)[0]
        service_hostport = f"{service['Address']}:{service['Port']}"
        return service_hostport

service_getter = FirstServiceGetter()

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

@app.post("/register")
async def register(user: str, passw: str, mail: str, response: Response):
    result = await  service.register(user, passw, mail)
    response.status_code = result["status"]
    return result["message"]

# @app.get("/friends")
# async def friends(username: str, response: Response):
#     result = service.friends(username)
#     response.status_code = result["status"]
#     return result["message"]
# @app.post("/add-friend")
# async def add_friend(friend1: str, friend2: str, response: Response):
#     result = service.add_friend(friend1, friend2)
#     response.status_code = result["status"]
#     return result["message"]


# @app.post("/remove-friend")
# async def remove_friend(friend1: str, friend2: str, response: Response):
#     result = service.remove_friend(friend1, friend2)
#     response.status_code = result["status"]
#     return result["message"]


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login")
async def login(user: str, passw: str, response: Response):
    result = service.login(user, passw)
    response.status_code = result["status"]
    return result["message"]

@app.get("/main-page")
async def main_page(username : str, response: Response):
    result = service.main_page(username)
    response.status_code = result["status"]
    return result["message"]

@app.post("/new-post")
async def new_post(content: Request, response: Response):
    item = await content.json()
    result = service.new_post(item)
    response.status_code = result["status"]
    return result["message"]





@app.get("/show-user")
async def show_user(username: str, response: Response):
    result = service.show_user(username)
    response.status_code = result["status"]
    return result["message"]

@app.delete("/logout")
async def logout(token: str, response: Response):
    result = await service.logout(token)
    response.status_code = result["status"]
    return result["message"]





@app.post("/like-post")
async def like_post(username: str, post_id: str, response: Response):
    result = service.like_post(username, post_id)
    response.status_code = result["status"]
    return result["message"]

@app.delete("/like-post")
async def unlike_post(username: str, post_id: str, response: Response):
    result = service.unlike_post(username, post_id)
    response.status_code = result["status"]
    return result["message"]

@app.get("/show-likes")
async def show_likes(post_id: str, response: Response):
    result = service.show_likes(post_id)
    response.status_code = result["status"]
    return result["message"]

@app.get("/has-liked")
async def has_liked(username: str, post_id: str, response: Response):
    result = service.has_liked(username, post_id)
    response.status_code = result["status"]
    return result["message"]

@app.post("/modify-profile-photo") 
async def modify_profile_photo(request: Request, response: Response):
    item = await request.json()
    result = service.modify_profile_photo(item)
    response.status_code = result["status"]
    return result["message"]


@app.post("/modify-music") 
async def modify_music(user: str, music: str, response: Response):
    result = service.modify_music(user, music)
    response.status_code = result["status"]
    return result["message"]

app.include_router(router)
