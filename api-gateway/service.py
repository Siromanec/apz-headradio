import requests
import json
import consul

c = consul.Consul(host = "consul")
c.agent.service.register(name='api-gateway',
                         service_id='api-gateway',
                         address='api-gateway',
                         port=8003)

def get_services(service_name):
    list_services = []
    services = c.health.service(service_name)[1]
    for service in services:
        service = {}
        service['Address'] = service['Service']['Address']
        service['Port'] = service['Service']['Port']
        list_services.append(service)
    return services

def login(user, passw):
    auth = get_services('auth_service')[0]
    address, port = auth['Address'], auth['Port']
    url = f'http://{address}:{port}/login?{user}&{passw}'
    response = requests.post(url)
    code, message = response.status_code, response.text
    return {"status": code, "message": message}


def logout(token):
    auth = get_services('auth_service')[0]
    address, port = auth['Address'], auth['Port']
    url = f'http://{address}:{port}/logout?{token}'
    response = requests.delete(url)
    code, message = response.status_code, response.text
    return {"status": code, "message": message}

def show_user(username):
    user = get_services('user_service')[0]
    address, port = user['Address'], user['Port']
    url = f'http://{address}:{port}/show-user?{username}'
    response = requests.get(url)
    code, message = response.status_code, response.text
    return {"status": code, "message": message}

def register(user, passw, mail):
    user = get_services('user_service')[0]
    address, port = user['Address'], user['Port']
    url = f'http://{address}:{port}/register?{user}&{passw}&{mail}'
    response = requests.post(url)
    code, message = response.status_code, response.text
    return {"status": code, "message": message} 

def add_friend(friend1, friend2):
    friend = get_services('friendzone_service')[0]
    address, port = friend['Address'], friend['Port']
    url = f'http://{address}:{port}/add-friend?{friend1}&{friend2}'
    response = requests.post(url)
    code, message = response.status_code, response.text
    return {"status": code, "message": message}

def accept_request(friend1, friend2):
    ...

def like_post(username, post_id):
    likes = get_services('like_service')
    address, port = likes[0]['Address'], likes[0]['Port']
    url = f'http://{address}:{port}/add-like?{username}&{post_id}'
    response = requests.post(url)
    code, message = response.status_code, response.text
    return {"status": code, "message": message}

def unlike_post(username, post_id):
    likes = get_services('like_service')
    address, port = likes[0]['Address'], likes[0]['Port']
    url = f'http://{address}:{port}/remove-like?{username}&{post_id}'
    response = requests.post(url)
    code, message = response.status_code, response.text
    return {"status": code, "message": message}

def show_likes(post_id):
    likes = get_services('like_service')
    address, port = likes[0]['Address'], likes[0]['Port']
    url = f'http://{address}:{port}/get-likes?{post_id}'
    response = requests.get(url)
    code, message = response.status_code, response.text
    return {"status": code, "message": message}

def has_liked(username, post_id):
    likes = get_services('like_service')
    address, port = likes[0]['Address'], likes[0]['Port']
    url = f'http://{address}:{port}/has-liked?{username}&{post_id}'
    response = requests.get(url)
    code, message = response.status_code, response.text
    return {"status": code, "message": message}