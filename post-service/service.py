# logic
import repository

def get_user_posts(user):
    return repository.get_user_posts(user)

def new_post(items):
    post = {"username": items["user"], "post_id": items["idpost"], "time": items["added"], "article": items["article"]}
    repository.new_post(post)

def delete_post(post):
    repository.delete_post(post)