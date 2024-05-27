import consul
from fastapi import FastAPI, Response, Request, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
import httpx

from routes import repository

from routes.friend import router as friend_router
from routes.auth import router as auth_router
from routes.like import router as like_router
from routes.profile import router as profile_router
from routes.service_getter import service_getter

app = FastAPI()

app.include_router(friend_router)
app.include_router(auth_router)
app.include_router(like_router)
app.include_router(profile_router)


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




router = APIRouter()




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/feed")
async def feed(username : str, response: Response):
    hostport = service_getter.get_service_hostport('feed')
    url = f'http://{hostport}/feed/?user={username}'
    async with httpx.AsyncClient() as client:
        redirect_response = await client.get(url)
        message = redirect_response.json()
        code = redirect_response.status_code
        response.status_code = code
        return message



@app.post("/new-post")
async def new_post(request: Request, response: Response):
    hostport = service_getter.get_service_hostport('post')
    url = f'http://{hostport}/new-post/'
    async with httpx.AsyncClient() as client:
        redirect_response = await client.post(url, content=await request.body())
        message = redirect_response.json()
        code = redirect_response.status_code
        response.status_code = code
        return message


@app.post("/register/")
async def register(user: str, password: str, email: str, response: Response):
    auth_hostport = service_getter.get_service_hostport("auth")
    profile_hostport = service_getter.get_service_hostport("profile")
    auth_url = f'http://{auth_hostport}/register/?user={user}&password={password}&email={email}'
    profile_url = f'http://{profile_hostport}/create-profile/?user={user}'
    async with httpx.AsyncClient() as client:

        auth_promise = client.post(auth_url)
        profile_promise = client.post(profile_url)

        auth_response = await auth_promise
        auth_message = auth_response.json()
        code = auth_response.status_code
        response.status_code = code
        if code != status.HTTP_200_OK:
            await profile_promise # awaiting so the promise doesn't memory leak. todo Maybe there is a way to reject it
            print(f"failed to create account for {user} (auth)")
            return {"token": None}
        token = str(auth_message["token"])

        profile_response = await profile_promise
        code = profile_response.status_code
        response.status_code = code
        if code != status.HTTP_200_OK:
            print(f"failed to create profile for {user} (profile)")
            return {"token": None}

        repository.add_token(user, token)
        return {"token": token}