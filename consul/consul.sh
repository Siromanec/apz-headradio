#!/bin/sh

consul agent -server -ui -node=server-1 -client=0.0.0.0 -bootstrap-expect=1 -data-dir=/tmp/consul &
while [ true ]; do
    sleep 1
    curl -f http://localhost:8500/v1/status/leader
    if [ "$?" -eq "0" ]; then
        break
    fi
done

consul kv put hazelcast/cluster-name dev
consul kv put hazelcast/queue-name queue
consul kv put hazelcast/map-name map

wait