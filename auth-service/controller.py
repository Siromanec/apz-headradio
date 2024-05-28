from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
import repository
import consul
import hazelcast
import socket

message_queue = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    await repository.start_session()
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    c = consul.Consul(host="consul")
    c.agent.service.register(name='auth',
                             service_id=f'{ip_addr}-8082',
                             address='auth',
                             port=8082)

    cluster_name = (c.kv.get("hazelcast/cluster-name")[1]["Value"]).decode()
    client = hazelcast.HazelcastClient(cluster_name=cluster_name, cluster_members=["hazelcast"])
    global message_queue
    messages_queue_name = (c.kv.get("hazelcast/queue-name")[1]["Value"]).decode()
    message_queue = client.get_queue(messages_queue_name)
    yield
    await repository.end_session()


app = FastAPI(lifespan=lifespan)


@app.post("/login/")
async def login(user: str, password: str, response: Response):
    token = await service.login(user, password)
    response.status_code = status.HTTP_200_OK
    if token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        log = f"auth-service: some bruv tryna hack {user}. skibidi is generated."
        print(log)
        message_queue.put(log)
    else:
        log = f"auth-service: User {user} is logged in. Token ({token}) is generated."
        print(log)
        message_queue.put(log)
    return {"token": token}


@app.post("/register/")
async def register(user: str, password: str, email: str, response: Response):
    token = await service.register(user, password, email)
    response.status_code = status.HTTP_200_OK
    if token is None:
        response.status_code = status.HTTP_409_CONFLICT
        log = (f"auth-service: sheesh {user} failed the vibe check. iykyk took huge L. "
               f"the username is taken, big yikes, no cap. skibidi is generated.")
        print(log)
        message_queue.put(log)
    else:
        log = f"auth-service: User {user} is registered. Token ({token}) is generated."
        print(log)
        message_queue.put(log)
    return {"token": token}


