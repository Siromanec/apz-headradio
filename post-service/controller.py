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




message_queue = None

@asynccontextmanager
async def lifespan(app):
    c = consul.Consul(host="consul")
    c.agent.service.register(name='post',
                         service_id='post',
                         address='post',
                         port=8080)
    
    cluster_name = (c.kv.get("hazelcast/cluster-name")[1]["Value"]).decode()
    client = hazelcast.HazelcastClient(cluster_name=cluster_name, cluster_members=["hazelcast"])

    global message_queue
    messages_queue_name = (c.kv.get("hazelcast/queue-name")[1]["Value"]).decode()
    message_queue = client.get_queue(messages_queue_name)

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/get-user-posts/")
async def get_user_posts(user: str, response: Response):

    posts = await service.get_user_posts(user)
    response.status_code = status.HTTP_200_OK
    print(f"post-service: posts of {user} - {posts}")
    message_queue.put(f"post-service: posts of {user} - {posts}")

    posts = list(map(lambda x: {"username": x["username"], "post_id": str(x["_id"]), "article": x["article"], "time": x["time"]}, posts))
    return {"posts": posts}


@app.post("/new-post/")
async def new_post(request: Request, response: Response):
    try:
        item = await request.json()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    try:
        await service.new_post(item["username"], item["article"], datetime.now())
        response.status_code = status.HTTP_200_OK
        print(f"post-service: User {item['username']} added a new post.")
        message_queue.put(f"post-service: User {item['username']} added a new post.")
    except KeyError:
        response.status_code = status.HTTP_400_BAD_REQUEST


@app.delete("/delete-post/")
async def delete_post(post: str, response: Response):
    await service.delete_post(post)
    response.status_code = status.HTTP_200_OK
    print(f"post-service: Post {post} deleted.")
    message_queue.put(f"post-service: Post {post} deleted.")
