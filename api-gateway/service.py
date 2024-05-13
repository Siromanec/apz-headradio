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
                         port=8003)

def get_services(service_name):
    list_services = []
    services = c.health.service(service_name)[1]
    for service in services:
        adder = {}
        adder['Address'] = service['Service']['Address']
        adder['Port'] = service['Service']['Port']
        list_services.append(adder)
    print(list_services)
    return list_services

def login(user, passw):
    auth = get_services('auth')[0]
    address, port = auth['Address'], auth['Port']
    url = f'http://{address}:{port}/login?user={user}&password={passw}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    token = str(message["token"])
    if code == status.HTTP_200_OK:
        repository.add_token(token)
    return {"status": code, "message": message}


def logout(token):
    repository.remove_token(token)    
    return {"status": status.HTTP_200_OK, "message": {"message" : f"removed {token} from active sessions"}}

def show_user(username):
    user = get_services('profile')[0]
    address, port = user['Address'], user['Port']
    url = f'http://{address}:{port}/get-user-data?user={username}'
    response = requests.get(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def register(user, passw, mail):
    auth = get_services('auth')[0]
    address, port = auth['Address'], auth['Port']
    url = f'http://{address}:{port}/register/?user={user}&password={passw}&email={mail}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    token = str(message["token"])
    if code == status.HTTP_200_OK:
        repository.add_token(token)
    return {"status": code, "message": message} 

def friends(username):
    friend = get_services('friendzone')[0]
    address, port = friend['Address'], friend['Port']
    url = f'http://{address}:{port}/get-friends/?user={username}'
    response = requests.get(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def add_friend(friend1, friend2):
    friend = get_services('friendzone')[0]
    address, port = friend['Address'], friend['Port']
    url = f'http://{address}:{port}/add-friend/?user1={friend1}&user2={friend2}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def remove_friend(friend1, friend2):
    friend = get_services('friendzone')[0]
    address, port = friend['Address'], friend['Port']
    url = f'http://{address}:{port}/remove-friend/?user1={friend1}&user2={friend2}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def like_post(username, post_id):
    likes = get_services('likes')
    address, port = likes[0]['Address'], likes[0]['Port']
    url = f'http://{address}:{port}/add-like/?user={username}&post={post_id}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def unlike_post(username, post_id):
    likes = get_services('likes')
    address, port = likes[0]['Address'], likes[0]['Port']
    url = f'http://{address}:{port}/remove-like/?user={username}&post={post_id}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def show_likes(post_id):
    likes = get_services('likes')
    address, port = likes[0]['Address'], likes[0]['Port']
    url = f'http://{address}:{port}/get-likes/?post={post_id}'
    response = requests.get(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def has_liked(username, post_id):
    likes = get_services('likes')
    address, port = likes[0]['Address'], likes[0]['Port']
    url = f'http://{address}:{port}/has-liked/?user={username}&post={post_id}'
    response = requests.get(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def main_page(username):
    feed = get_services('feed')
    address, port = feed[0]['Address'], feed[0]['Port']
    url = f'http://{address}:{port}/feed/?user={username}'
    response = requests.get(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def modify_music(user, music):
    profile = get_services('profile')
    address, port = profile[0]['Address'], profile[0]['Port']
    url = f'http://{address}:{port}/set-music/?user={user}&music={music}'
    response = requests.post(url)
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def modify_profile_photo(request):
    profile = get_services('profile')
    address, port = profile[0]['Address'], profile[0]['Port']
    url = f'http://{address}:{port}/modify-profile-photo'
    response = requests.post(url, data=json.dumps(request))
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}

def new_post(post):
    feed = get_services('post')
    address, port = feed[0]['Address'], feed[0]['Port']
    url = f'http://{address}:{port}/new-post'
    response = requests.post(url, data=json.dumps(post))
    code, message = response.status_code, response.json()
    return {"status": code, "message": message}