# logic
import repository


def get_user_data(user):
    return repository.get_user_data(user)

def modify_profile_photo(user, profile_photo):
    repository.modify_profile_photo(user, profile_photo)

def set_music(user, song_name):
    repository.set_music(user, song_name)

def create_profile(user):
    repository.create_profile(user)
