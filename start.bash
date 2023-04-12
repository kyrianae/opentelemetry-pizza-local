#!/bin/bash
# export OTEL_SERVICE_NAME=customer; opentelemetry-instrument python3 customer.py &

for i in "customer" "freezer" "hoover" "guichet" "pizzaiolo" "recipes"  ; do
echo Launch $i
export OTEL_SERVICE_NAME=$i; opentelemetry-instrument python3 $i.py 2>$i.err >$i.log &

done

watch curl 127.0.0.1:8082/ask_for_pizza