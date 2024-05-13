import hazelcast
import consul

consul_service = consul.Consul(host="consul")
consul_service.agent.service.register(name="logging", service_id="logging", address="logging", port=8082)
client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast"])

messages_queue_name = "messages_queue"
messages_queue = client.get_queue(messages_queue_name).blocking()

while True:
    message = messages_queue.take()
    print(message)
