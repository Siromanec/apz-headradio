import repository


async def get_following(username):
    return [followee[0] for followee in await repository.get_following(username)]

async def get_followers(username):
    return [follower[0] for follower in await repository.get_followers(username)]

async def get_friends(username):
    return [friend for username_friend, friend in await repository.get_friends(username)]

async def add_friend(user1, user2):
    await repository.add_friend(user1, user2)

async def remove_friend(user1, user2):
    await repository.remove_friend(user1, user2)