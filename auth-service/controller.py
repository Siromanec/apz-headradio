from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Response, status
import service
import repository
import consul

@asynccontextmanager
async def lifespan(app):
    repository.start_session()
    c = consul.Consul(host="consul")
    c.agent.service.register(name='auth',
                            service_id='auth',
                            address='auth',
                            port=8082)
    yield
    repository.end_session()

app = FastAPI(lifespan=lifespan)

@app.post("/login/")
async def login(user: str, password: str, response: Response):
    token = service.login(user, password)
    response.status_code = status.HTTP_200_OK
    return {"token": token}


@app.post("/register/")
async def register(user: str, password: str, email:str, response: Response):
    service.register(user, password, email)
    response.status_code = status.HTTP_200_OK