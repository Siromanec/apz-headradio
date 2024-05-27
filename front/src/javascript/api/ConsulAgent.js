const Consul = require("consul")

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

class ConsulAgent{
    constructor(){
        this.consul = new Consul({host: "gateway-consul"})
    }

    async getService(serviceName){
        return this.consul.health.service(this.serviceName)
        .then(services => {
            if(services.length === 0) {
                throw new Error(`Service ${this.serviceName} not available`)
            }
            console.log("Services:", services)
            return services[getRandomInt(services.length)].Service
        })
        .then(service => {
            return {host: service.Address, port: service.Port}
        })

    }
}

module.exports = ConsulAgent