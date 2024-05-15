from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

import service


app = FastAPI()

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


@app.delete("/logout")
async def logout(token: str, response: Response):
    result = service.logout(token)
    response.status_code = result["status"]
    return result["message"]


@app.get("/show-user")
async def show_user(username: str, response: Response):
    result = service.show_user(username)
    response.status_code = result["status"]
    return result["message"]

@app.post("/register")
async def register(user: str, passw: str, mail: str, response: Response):
    result = service.register(user, passw, mail)
    response.status_code = result["status"]
    return result["message"]


@app.post("/add-friend")
async def add_friend(friend1: str, friend2: str, response: Response):
    result = service.add_friend(friend1, friend2)
    response.status_code = result["status"]
    return result["message"]


@app.post("/remove-friend")
async def remove_friend(friend1: str, friend2: str, response: Response):
    result = service.remove_friend(friend1, friend2)
    response.status_code = result["status"]
    return result["message"]

@app.get("/friends")
async def friends(username: str, response: Response):
    result = service.friends(username)
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

