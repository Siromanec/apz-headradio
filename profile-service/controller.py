import fastapi
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
import uuid
import os

app = FastAPI()

@app.get("/get-pfp/")
async def get_pfp(user: str, response: Response):
    liked = service.get_pfp(user)
    response.status_code = status.HTTP_200_OK
    return {"get_pfp": liked}

@app.get("/get-user-data/")
async def get_user_data(user: str, response: Response):
    user_data = service.get_user_data(user)
    response.status_code = status.HTTP_200_OK
    return {"get_user_data": user_data}

@app.post("/modify-profile-photo/")
async def modify_profile_photo(request: Request, response: Response):
    item = await request.json()
    filename = str(uuid.uuid4())
    while os.path.isfile("./data/" + filename):
        filename = str(uuid.uuid4())
    with open("./data/" + filename, "w") as file:
        file.write(item["image"])
    username = item["username"]
    service.modify_profile_photo("user", {"profilePicture": f"'{filename}'"}, f"`username`='{username}'")
    response.status_code = status.HTTP_200_OK

@app.post("/set-music/")
async def set_music(user: str, song_name: str, response: Response):
    service.set_music(user, song_name)
    response.status_code = status.HTTP_200_OK

@app.post("/create-profile/")
async def create_profile(user: str, response: Response):
    service.create_profile(user)
    response.status_code = status.HTTP_200_OK