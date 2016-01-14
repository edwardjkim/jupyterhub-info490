#!/bin/bash

hosts=(
    jupyterhub_node3
    jupyterhub_node4
    jupyterhub_node5
    jupyterhub_node6
    jupyterhub_node7
    jupyterhub_node8
    jupyterhub_node9
    jupyterhub_node10
    jupyterhub_node11
    jupyterhub_node12
)

KEYMASTER="sudo docker run --rm -v $(pwd)/certificates/:/certificates/ cloudpipe/keymaster"

for a in "${hosts[@]}"
do
    line=$(cat inventory | grep -v "#" | grep "$a")
    if [[ -z "${line// }" ]]
    then
        continue
    fi
    array=($line)
    name="${array[0]}"
    ansible_host="${array[2]}"
    hostname="$(echo $ansible_host | awk -F= '{print $2}')"
    private_ip="${array[3]}"
    ip="$(echo $private_ip | awk -F= '{print $2}')"
    
    ${KEYMASTER} signed-keypair -n "$name" -h "$hostname" -p both -s IP:"$ip"
done
