# logic

def add_like(user, post):
    print(f"INSERT INTO likes (USERNAME, POST) VALUES ({user}, {post})")
    ...
def has_liked(user, post):
    print(f"SELECT EXISTS (SELECT 1 FROM likes WHERE POST = {post} AND USERNAME = {user})")
    ...
def remove_like(user, post):
    print(f"DELETE FROM likes WHERE POST = {post} AND USERNAME = {user}")
    ...
def get_likes(post):
    print(f"SELECT * FROM likes WHERE POST = {post}")
    ...
