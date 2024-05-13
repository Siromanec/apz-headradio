import fastapi
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
from datetime import datetime
import hazelcast
import consul

app = FastAPI()

id = 0


message_queue = None

@asynccontextmanager
async def lifespan(app):
    c = consul.Consul()
    c.agent.service.register(name='posts',
                         service_id='posts',
                         address='posts',
                         port=8080)
    client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast"])

    global message_queue
    messages_queue_name = "messages_queue"
    message_queue = client.get_queue(messages_queue_name).blocking()

    yield


@app.get("/get-user-posts/")
async def get_user_posts(user: str, response: Response):
    posts = service.get_user_posts(user)
    response.status_code = status.HTTP_200_OK
    print(f"post-service: posts of {user} - {posts}")
    message_queue.put(f"post-service: posts of {user} - {posts}")
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
    print(f"post-service: User {item['username']} added a new post.")
    message_queue.put(f"post-service: User {item['username']} added a new post.")


@app.post("/delete-post/")
async def delete_post(post: int, response: Response):
    service.delete_post(post)
    response.status_code = status.HTTP_200_OK
    print(f"post-service: Post {post} deleted.")
    message_queue.put(f"post-service: Post {post} deleted.")
