#!/bin/bash
while true; do
    for ((i=0; i<6; i++))
    do
     ## put your alb dns name to the below line
        echo `curl -H 'Cache-Control: no-cache' http://<YOUR_ALB_DNS_NAME>/service` 1 > /dev/null ;
        sleep 0.2;
    done
done

