from typing import override

import consul

c = consul.Consul(host = "consul")

class ServiceGetter():
    def _get_services(self, service_name):
        list_services = []
        services = c.health.service(service_name)[1]
        for service in services:
            adder = {}
            adder['Address'] = service['Service']['Address']
            adder['Port'] = service['Service']['Port']
            list_services.append(adder)
        print(list_services)
        return list_services
    def get_service_hostport(self, service_name):
        raise NotImplemented

class FirstServiceGetter(ServiceGetter):
    def __init__(self):
        super().__init__()

    @override
    def get_service_hostport(self, service_name):
        service = self._get_services(service_name)[0]
        service_hostport = f"{service['Address']}:{service['Port']}"
        return service_hostport

service_getter = FirstServiceGetter()
