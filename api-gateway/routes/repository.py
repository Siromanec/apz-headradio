import hazelcast
import consul

c = consul.Consul(host="consul")

cluster_name = (c.kv.get("hazelcast/cluster-name")[1]["Value"]).decode()
client = hazelcast.HazelcastClient(cluster_name=cluster_name, cluster_members=["hazelcast"])

messages_queue_name = (c.kv.get("hazelcast/queue-name")[1]["Value"]).decode()
queue = client.get_queue(messages_queue_name)

map_name = (c.kv.get("hazelcast/map-name")[1]["Value"]).decode()
session_tokens_map = client.get_map(map_name).blocking()

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

