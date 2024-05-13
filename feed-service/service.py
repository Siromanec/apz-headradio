import requests
import consul

c = consul.Consul(host = "consul")

def get_services(service_name):
    list_services = []
    services = c.health.service(service_name)[1]
    for service in services:
        service = {}
        service['Address'] = service['Service']['Address']
        service['Port'] = service['Service']['Port']
        list_services.append(service)
    return services

def get_all_friends(username):
    friend = get_services('friendzone')[0]
    address, port = friend['Address'], friend['Port']
    url = f'http://{address}:{port}/get-friends?user={username}'
    response = requests.get(url).json()
    return response['friends']

def get_friend_posts(username):
    friend = get_services('post')[0]
    address, port = friend['Address'], friend['Port']
    url = f'http://{address}:{port}/get-posts?user={username}'
    response = requests.get(url).json()
    return response
    
def feed(user):
    friends = get_all_friends(user)
    posts = []
    for friend in friends:
        posts.append(get_friend_posts(friend))
    posts.sort(key=lambda x: x['time'], reverse=True)
    num = len(posts) if len(posts) < 50  else 50
    return posts[:num]