const Consul = require("consul");
// import {Consul} from "consul";
function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

export default class ConsulAgent{
    constructor(){
        this.consul = new Consul({host: "gateway-consul"})
    }

    async getService(serviceName){
        return this.consul.health.service(serviceName)
        .then(services => {
            if(services.length === 0) {
                throw new Error(`Service ${serviceName} not available`)
            }
            console.log("Services:", services)
            return services[getRandomInt(services.length)].Service
        })
        .then(service => {
            return {host: service.Address, port: service.Port}
        })

    }
}
