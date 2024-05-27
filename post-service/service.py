# logic
import repository

async def get_user_posts(user):
    return await repository.get_user_posts(user)

async def new_post(username, article, time):
    await repository.new_post(username, article, time)

async def delete_post(post):
    await repository.delete_post(post)