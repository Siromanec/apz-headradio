# logic
import repository

def get_user_posts(user):
    return repository.get_user_posts(user)

def new_post(username, article, time):
    repository.new_post(username, article, time)

def delete_post(post):
    repository.delete_post(post)