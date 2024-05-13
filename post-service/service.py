# logic
import repository

def get_user_posts(user):
    return repository.get_user_posts(user)

def new_post(items):
    repository.new_post(items)

def delete_post(post):
    repository.delete_post(post)