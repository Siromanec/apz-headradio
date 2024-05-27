import consul
from fastapi import status
import asyncio
import httpx
import random
c = consul.Consul(host = "consul")


async def get_services(service_name):
    list_services = []
    services = c.health.service(service_name)[1]
    for service in services:
        adder = {}
        adder['Address'] = service['Service']['Address']
        adder['Port'] = service['Service']['Port']
        list_services.append(adder)
    return list_services


async def get_all_friends(username):
    friend = random.choice(await get_services('friend'))
    address, port = friend['Address'], friend['Port']
    url = f'http://{address}:{port}/get-friends/?username={username}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            return []
        response = response.json()
        friends = response['friends']
        return friends

async def get_friend_posts(username, client):
    post = random.choice(await get_services('post'))
    address, port = post['Address'], post['Port']
    url = f'http://{address}:{port}/get-user-posts/?user={username}'
    return await client.get(url)


async def get_friends_pfp(username, client):
    profile =  random.choice(await get_services('profile'))
    address, port = profile['Address'], profile['Port']
    url = f'http://{address}:{port}/get-pfp/?user={username}'
    return await client.get(url)

async def get_like_count(post_id, client) -> int:
    profile = random.choice(await get_services('likes'))
    address, port = profile['Address'], profile['Port']
    url = f'http://{address}:{port}/get-like-count/?post={post_id}'
    return await client.get(url)

async def feed(user):
    async with httpx.AsyncClient() as client:
        friends = await get_all_friends(user)
        posts_tasks = [get_friend_posts(friend, client) for friend in friends]
        posts_responses = await asyncio.gather(*posts_tasks)
        all_posts = []
        for response in posts_responses:
            if response.status_code != status.HTTP_200_OK:
                continue
            posts = response.json()
            posts = posts['posts']
            all_posts.extend(posts)

        all_posts.sort(key=lambda x: x['time'], reverse=True)
        num = min(len(all_posts), 50)
        all_posts = all_posts[:num]


        selected_friends = set()
        like_tasks = [get_like_count(post['post_id'], client) for post in all_posts]
        like_counts = await asyncio.gather(*like_tasks)

        likes = []
        for response in like_counts:
            if response.status_code != status.HTTP_200_OK:
                continue
            likes.append(response.json()["like_count"])

        for i, post in enumerate(all_posts):
            post["likeCount"] = likes[i]
            post["postID"] = post.pop('post_id')
            selected_friends.add(post['username'])


        profile_picture_tasks = [get_friends_pfp(friend, client) for friend in selected_friends]
        profile_picture_responses = await asyncio.gather(*profile_picture_tasks)
    
        profile_pictures = {}
        for response in profile_picture_responses:
            if response.status_code != status.HTTP_200_OK:
                continue
            profile_pictures[response.json()["username"]] = response.json()["profile_picture"]
        

    return {"posts": all_posts, "profilePictures": profile_pictures}
