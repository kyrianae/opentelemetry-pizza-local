#!/bin/bash
# export OTEL_SERVICE_NAME=customer; opentelemetry-instrument python3 customer.py &

for i in "customer" "freezer" "hoover" "guichet" "pizzaiolo" "recipes"  ; do
echo kill $i 
pkill -f $i.py 
done
