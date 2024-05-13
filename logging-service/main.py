import hazelcast
import consul

consul_service = consul.Consul()
client_name = consul_service.kv.get('cluster-name')[1]['Value'].decode()
client = hazelcast.HazelcastClient(cluster_name=client_name)

messages_queue_name = consul_service.kv.get("messages_queue_name")[1]["Value"].decode()
messages_queue = client.get_queue(messages_queue_name).blocking()

while True:
    message = messages_queue.take()
    print(message)
