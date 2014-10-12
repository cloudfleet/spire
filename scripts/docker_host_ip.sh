#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    /sbin/ifconfig docker0 | grep "inet addr" | awk -F: '{print $2}' | awk '{print $1}'
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo $DOCKER_HOST
fi
