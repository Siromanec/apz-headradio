from contextlib import asynccontextmanager

import fastapi
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
import repository
import consul
import hazelcast

message_queue = None

@asynccontextmanager
async def lifespan(app):
    repository.start_session()
    c = consul.Consul(host="consul")
    c.agent.service.register(name='likes',
                         service_id='likes',
                         address='likes',
                         port=8079)
    client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast"])

    global message_queue
    messages_queue_name = "messages_queue"
    message_queue = client.get_queue(messages_queue_name)

    yield
    repository.end_session()

app = FastAPI(lifespan=lifespan)

@app.get("/has-liked/")
async def has_liked(user: str, post: int, response: Response):
    liked = service.has_liked(user, post)
    response.status_code = status.HTTP_200_OK
    print(f"like-service: User {user} has liked post {post}: {liked}")
    message_queue.put(f"like-service: User {user} has liked post {post}: {liked}")
    return {"has_liked": liked}


@app.post("/add-like/")
async def add_like(user: str, post: int, response: Response):
    service.add_like(user, post)
    response.status_code = status.HTTP_200_OK
    print(f"like-service: User {user} liked post {post}.")
    message_queue.put(f"like-service: User {user} liked post {post}.")


@app.post("/remove-like/")
async def remove_like(user: str, post: int, response: Response):
    service.remove_like(user, post)
    response.status_code = status.HTTP_200_OK
    print(f"like-service: User {user} unliked post {post}.")
    message_queue.put(f"like-service: User {user} unliked post {post}.")


@app.get("/get-likes/")
async def get_likes(post: int, response: Response):
    likes = service.get_likes(post)
    response.status_code = status.HTTP_200_OK
    print(f"like-service: Post {post} has {likes} likes.")
    message_queue.put(f"like-service: Post {post} has {likes} likes.")
    return {"likes": likes}
