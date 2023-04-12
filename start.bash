#!/bin/bash
# export OTEL_SERVICE_NAME=customer; opentelemetry-instrument python3 customer.py &

for i in "customer" "freezer" "hoover" "guichet" "pizzaiolo" "recipes"  ; do
echo Launch $i
echo "export OTEL_SERVICE_NAME=$i; opentelemetry-instrument python3 $i.py > $i.log &"
#export OTEL_SERVICE_NAME=$i; opentelemetry-instrument python3 $i.py > $i.log &
done

echo watch curl 127.0.0.1:8082/ask_for_pizza