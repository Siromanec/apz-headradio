import requests
import consul
from fastapi import status

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
    friend = get_services('friend')[0]
    address, port = friend['Address'], friend['Port']
    url = f'http://{address}:{port}/get-friends/?username={username}'
    response = requests.get(url).json()
    print("friends of user")
    friends = response['friends']
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
    response = requests.get(url)
    data = response.json()
    print("pfp of friends")
    print(data)
    print(response.status_code)
    if response.status_code == status.HTTP_409_CONFLICT:
        print(f"no user {username}")
        raise KeyError
    return data

def get_like_count(post_id) -> int:
    profile = get_services('likes')[0]
    address, port = profile['Address'], profile['Port']
    url = f'http://{address}:{port}/get-like-count/?post={post_id}'
    response = requests.get(url)
    data = response.json()
    print(data)
    print(response.status_code)
    return data["like_count"]


def feed(user):
    friends = get_all_friends(user)
    posts: list[dict] = []
    for friend in friends:
        posts.extend(get_friend_posts(friend)["posts"])
    print(posts)
    posts.sort(key=lambda x: x['time'], reverse=True)
    num = min(len(posts), 50)
    posts = posts[:num]

    selected_friends = set()
    for post in posts:
        post["likeCount"] = get_like_count(post['post_id'])
        post["postID"] = post.pop('post_id')

        selected_friends.add(post['username'])

    profile_pictures = dict()
    for friend in selected_friends:
        try:
            profile_pictures[friend] = get_friends_pfp(friend)['profile_picture']
        except KeyError:
            # ignore imaginary friends
            profile_pictures[friend] = None
            ...


    return {"posts": posts, "profilePictures": profile_pictures}
