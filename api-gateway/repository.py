import hazelcast

client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast"])
session_tokens_map = client.get_map("session-tokens-map").blocking()

def add_token(username: str, active_token: int):
    global session_tokens_map
    session_tokens_map.put(username, active_token)

def remove_token(username):
    session_tokens_map.remove(username)

def get_token(username):
    return session_tokens_map.get(username)

def get_active_tokens():
    return list(session_tokens_map.values())


add_token("admin", 1)
print(get_token("admin"))
print(get_active_tokens())
remove_token("admin")
print(get_active_tokens())
