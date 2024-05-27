import hazelcast
import consul
 
from contextlib import asynccontextmanager

queue = None

@asynccontextmanager
async def lifespan(app):
    c = consul.Consul(host="gateway-consul")
    c.agent.service.register(name='api-gateway',
                         service_id='api-gateway',
                         address='api-gateway',
                         port=8084)
    
    client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast"])

    global queue
    messages_queue_name = "messages_queue"
    queue = client.get_queue(messages_queue_name)
    yield



