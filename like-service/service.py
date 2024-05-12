# logic
import repository

def add_like(user, post):
    repository.add_like(user, post)
def has_liked(user, post):
    return repository.has_liked(user, post)
def remove_like(user, post):
    repository.remove_like(user, post)
def get_likes(post):
    return [like[0] for like in repository.get_likes(post)]
