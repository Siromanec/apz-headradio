from typing import override

import requests
import json
import consul
from hashlib import sha256
import repository
from fastapi import status


c = consul.Consul(host = "consul")
c.agent.service.register(name='api-gateway',
                         service_id='api-gateway',
                         address='api-gateway',
                         port=8084)

class ServiceGetter():
    def _get_services(self, service_name):
        list_services = []
        services = c.health.service(service_name)[1]
        for service in services:
            adder = {}
            adder['Address'] = service['Service']['Address']
            adder['Port'] = service['Service']['Port']
            list_services.append(adder)
        print(list_services)
        return list_services
    def get_service_hostport(self, service_name):
        raise NotImplemented

class FirstServiceGetter(ServiceGetter):
    def __init__(self):
        super().__init__()

    @override
    def get_service_hostport(self, service_name):
        service = self._get_services(service_name)[0]
        service_hostport = f"{service['Address']}:{service['Port']}"
        return service_hostport








service_getter = FirstServiceGetter()

async def login(user, passw):
    hostport = service_getter.get_service_hostport('auth')
    url = f'http://{hostport}/login?user={user}&password={passw}'

    response = requests.post(url)
    code = response.status_code
    message = await response.json()
    if code == status.HTTP_200_OK:
        token = str(message["token"])
        repository.add_token(token)
    return {"status": code, "message": message}


def logout(token):
    repository.remove_token(token)    
    return {"status": status.HTTP_200_OK, "message": {"message" : f"removed {token} from active sessions"}}

def show_user(username):
    hostport = service_getter.get_service_hostport('profile')
    url = f'http://{hostport}/get-user-data?user={username}'
    response = requests.get(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}


async def register(username, password, email):
    hostport = service_getter.get_service_hostport('auth')
    url = f'http://{hostport}/register/?user={username}&password={password}&email={email}'
    response = requests.post(url)

    code = response.status_code
    message = await response.json()
    if code == status.HTTP_200_OK:
        token = str(message["token"])
        repository.add_token(token)
    return {"status": code, "message": message} 



def like_post(username, post_id):
    hostport = service_getter.get_service_hostport('likes')
    url = f'http://{hostport}/add-like/?user={username}&post={post_id}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def unlike_post(username, post_id):
    hostport = service_getter.get_service_hostport('likes')
    url = f'http://{hostport}/remove-like/?user={username}&post={post_id}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def show_likes(post_id):
    hostport = service_getter.get_service_hostport('likes')
    url = f'http://{hostport}/get-likes/?post={post_id}'
    response = requests.get(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def has_liked(username, post_id):
    hostport = service_getter.get_service_hostport('likes')
    url = f'http://{hostport}/has-liked/?user={username}&post={post_id}'
    response = requests.get(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def main_page(username):
    hostport = service_getter.get_service_hostport('feed')
    url = f'http://{hostport}/feed/?user={username}'
    response = requests.get(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def modify_music(user, music):
    hostport = service_getter.get_service_hostport('profile')
    url = f'http://{hostport}/set-music/?user={user}&music={music}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def modify_profile_photo(request):
    hostport = service_getter.get_service_hostport('profile')
    url = f'http://{hostport}/modify-profile-photo'
    response = requests.post(url, data=json.dumps(request))
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def new_post(post):
    hostport = service_getter.get_service_hostport('post')
    url = f'http://{hostport}/new-post'
    response = requests.post(url, data=json.dumps(post))
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}