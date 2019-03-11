#!/bin/bash

cmd="$1"

while true
do
    sleep 1;
    echo Check hub
    nc -z "hub" "4444" > /dev/null
    if ([[ $? -eq 0 ]]); then
        break
    fi
done

echo cmd "$cmd"

>&2 echo "App are up - executing command"
exec ${cmd}
