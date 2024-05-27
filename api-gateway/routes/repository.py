import hazelcast

messages_queue_name = "messages_queue"
client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast"])
session_tokens_map = client.get_map("session-tokens-map").blocking()
queue = client.get_queue(messages_queue_name)

def add_token(username: str, active_token: str):
    global session_tokens_map
    session_tokens_map.put(username, active_token)

def remove_token(username):
    session_tokens_map.remove(username)

def get_token(username):
    return session_tokens_map.get(username)
    

def get_active_tokens():
    return list(session_tokens_map.values())

def put_message(message: str):
    global queue
    queue.put(message)

