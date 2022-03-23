#!/bin/bash
while true; do
    for ((i=0; i<6; i++))
    do
        echo `curl -H 'Cache-Control: no-cache' http://builders-frontendalb-1387412754.ap-northeast-2.elb.amazonaws.com/service` 1 > /dev/null ;
        sleep 0.2;
    done
done

