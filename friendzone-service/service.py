import repository


def get_following(username):
    return [followee[0] for followee in repository.get_following(username)]

def get_followers(username):
    return [follower[0] for follower in repository.get_followers(username)]

def get_friends(username):
    return [friend for username_friend, friend in repository.get_friends(username)]

def add_friend(user1, user2):
    repository.add_friend(user1, user2)

def remove_friend(user1, user2):
    repository.remove_friend(user1, user2)