from fastapi import FastAPI, Response
import service

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login")
async def login(user: str, passw: str, response: Response):
    result = service.login(user, passw)
    response.status_code = result["status"]
    return result["message"]

@app.get("/main-page?{username}")
async def main_page(response: Response):
    result = service.main_page()
    response.status_code = result["status"]
    return result["message"]

@app.post("/new-post")
async def new_post(token: str, content: str, response: Response):
    result = service.new_post(token, content)
    response.status_code = result["status"]
    return result["message"]


@app.delete("/logout")
async def logout(token: str, response: Response):
    result = service.logout(token)
    response.status_code = result["status"]
    return result["message"]


@app.get("/show-user?{username}")
async def show_user(username: str, response: Response):
    result = service.show_user(username)
    response.status_code = result["status"]
    return result["message"]

@app.post("/register")
async def register(user: str, passw: str, mail: str, response: Response):
    result = service.register(user, passw, mail)
    response.status_code = result["status"]
    return result["message"]


@app.post("/friend-request?{friend1}&{friend2}")
async def add_friend(friend1: str, friend2: str, response: Response):
    result = service.add_friend(friend1, friend2)
    response.status_code = result["status"]
    return result["message"]


@app.post("/accept-request?{friend1}&{friend2}")
async def accept_request(friend1: str, friend2: str, response: Response):
    result = service.accept_request(friend1, friend2)
    response.status_code = result["status"]
    return result["message"]


@app.post("/like-post?{username}&{post_id}")
async def like_post(username: str, post_id: str, response: Response):
    result = service.like_post(username, post_id)
    response.status_code = result["status"]
    return result["message"]

@app.delete("/like-post?{username}&{post_id}")
async def unlike_post(username: str, post_id: str, response: Response):
    result = service.unlike_post(username, post_id)
    response.status_code = result["status"]
    return result["message"]

@app.get("/show-likes?{post_id}")
async def show_likes(post_id: str, response: Response):
    result = service.show_likes(post_id)
    response.status_code = result["status"]
    return result["message"]

@app.get("/has-liked?{username}&{post_id}")
async def has_liked(username: str, post_id: str, response: Response):
    result = service.has_liked(username, post_id)
    response.status_code = result["status"]
    return result["message"]

@app.post("/modify-profile-photo?${user}") 
async def modify_profile_photo(user: str, response: Response):
    result = service.modify_profile_photo(user)
    response.status_code = result["status"]
    return result["message"]


@app.post("/modify-music") 
async def modify_music(token: str, music: str, response: Response):
    result = service.modify_music(token, music)
    response.status_code = result["status"]
    return result["message"]