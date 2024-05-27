import hazelcast
import consul

consul_service = consul.Consul(host="consul")
consul_service.agent.service.register(name="logging", service_id="logging", address="logging", port=8082)

cluster_name = (consul_service.kv.get("hazelcast/cluster-name")[1]["Value"]).decode()
client = hazelcast.HazelcastClient(cluster_name=cluster_name, cluster_members=["hazelcast"])

messages_queue_name = (consul_service.kv.get("hazelcast/queue-name")[1]["Value"]).decode()
messages_queue = client.get_queue(messages_queue_name).blocking()

while True:
    message = messages_queue.take()
    print(message)
