# logic
import repository
import asyncio


async def add_like(user, post):
    await repository.add_like(user, post)
async def has_liked(user, post):
    return await repository.has_liked(user, post)
async def remove_like(user, post):
    await repository.remove_like(user, post)
async def get_likes(post):
    return await repository.get_likes(post)
    # return likes
