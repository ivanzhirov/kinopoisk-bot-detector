#!/bin/bash

cmd="$1"
# todo: add checking status: True intead simple nc to hub server
while true
do
    sleep 1;
    nc -z "hub" "4444" > /dev/null
    if ([[ $? -eq 0 ]]); then
        break
    fi
done

exec ${cmd}
