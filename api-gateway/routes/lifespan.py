import hazelcast
import consul
import socket 
from contextlib import asynccontextmanager

queue = None

@asynccontextmanager
async def lifespan(app):
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    print(ip_addr)
    c = consul.Consul(host="gateway-consul")
    c.agent.service.register(name='api-gateway',
                         service_id=f'{ip_addr}-8084',
                         address=ip_addr,
                         port=8084)
    
    client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast"])

    global queue
    messages_queue_name = "messages_queue"
    queue = client.get_queue(messages_queue_name)
    yield



