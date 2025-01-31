#!/bin/bash

URL="http://localhost:8000/predict/"

trap 'echo "Terminating the script..."; exit 0' SIGINT

echo "Starting to send POST requests to FastAPI server..."

while true
do
    feature1=$(echo "scale=2; $RANDOM / 100" | bc)
    feature2=$(echo "scale=2; $RANDOM / 100" | bc)

    PAYLOAD="{\"features\": [$feature1, $feature2]}"

    echo "Sending request with features: $feature1, $feature2"

    curl -s -X POST "$URL" -H "Content-Type: application/json" -d "$PAYLOAD" > /dev/null

    echo "Request sent successfully!"

    SLEEP_TIME=$((RANDOM % 3 + 1))
    sleep $SLEEP_TIME
done
