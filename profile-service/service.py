# logic
import repository


async def get_user_data(user):
    return await repository.get_user_data(user)

async def modify_profile_photo(user, profile_photo):
    await repository.modify_profile_photo(user, profile_photo)

async def set_music(user, song_name):
    await repository.set_music(user, song_name)

async def create_profile(user):
    await repository.create_profile(user)
