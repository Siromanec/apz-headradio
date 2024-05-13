import repository


def get_friends(user):
    return [friend[0] for friend in repository.get_friends(user)]

def add_friend(user1, user2):
    repository.add_friend(user1, user2)

def remove_friend(user1, user2):
    repository.remove_friend(user1, user2)