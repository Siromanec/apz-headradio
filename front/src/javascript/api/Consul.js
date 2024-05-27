const Consul = require("consul")
const {json} = require("express");

class Consul{
    constructor(){
        this.consul = new Consul({host: "gateway-consul"})
    }

    async function getService(serviceName){
        
    }
}