import requests
import consul

c = consul.Consul(host = "consul")


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


def get_all_friends(username):
    friend = get_services('friendzone')[0]
    address, port = friend['Address'], friend['Port']
    url = f'http://{address}:{port}/get-friends/?user={username}'
    response = requests.get(url).json()
    print("friends of user")
    response = response['friends']
    friends = []
    for friend in response:
        friends.append(friend['username_follows'])
    print(friends)
    return friends

def get_friend_posts(username):
    post = get_services('post')[0]
    address, port = post['Address'], post['Port']
    url = f'http://{address}:{port}/get-user-posts/?user={username}'
    response = requests.get(url).json()
    print("posts from friends")
    print(response)
    return response

def get_friends_pfp(username):
    profile = get_services('profile')[0]
    address, port = profile['Address'], profile['Port']
    url = f'http://{address}:{port}/get-pfp/?user={username}'
    response = requests.get(url).json()
    print("pfp of friends")
    print(response)
    return response
    
def feed(user):
    friends = get_all_friends(user)
    posts = []
    for friend in friends:
        posts.extend(get_friend_posts(friend)["posts"])
    print(posts)
    posts.sort(key=lambda x: x['time'], reverse=True)
    num = len(posts) if len(posts) < 50  else 50
    for post in posts:
        post['profile_picture'] = get_friends_pfp(post['username'])['get_pfp']
    return posts[:num]