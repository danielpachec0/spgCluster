#!/bin/bash

while true; do
    echo Deleting k6
    #kubectl delete -f /scripts/logging.yaml
    kubectl delete -f /scripts/tracing.yaml
    sleep 120
    
    echo "Creating k6"

    export TEST_IDENTIFIER=$(uuidgen)
    #BASE_YAML="/scripts/logging.yaml"
    BASE_YAML="/scripts/tracing.yaml"
    
    envsubst < $BASE_YAML | kubectl apply -f -
    
    echo "Sleeping for 35 minutes..."
    sleep 2220
done
