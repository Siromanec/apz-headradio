import fastapi
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
from datetime import datetime


app = FastAPI()

id = 0

@app.get("/get-user-posts/")
async def get_user_posts(user: str, response: Response):
    posts = service.get_user_posts(user)
    response.status_code = status.HTTP_200_OK
    return {"posts": posts} 


@app.post("/new-post/")
async def new_post(request: Request, response: Response):
    item = await request.json()
    global id
    id +=1 # todo have the db handle the ids (on service shutdown the last id is forgotten)
    items = {"idpost": id, "user": item["username"], "article": item["article"],  "added": datetime.now(
    ), "modified": datetime.now()}
    service.new_post(items)
    response.status_code = status.HTTP_200_OK


@app.post("/delete-post/")
async def delete_post(post: int, response: Response):
    service.delete_post(post)
    response.status_code = status.HTTP_200_OK
