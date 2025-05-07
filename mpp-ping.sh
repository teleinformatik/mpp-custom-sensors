#!/bin/bash

HOST="$1"
COUNT=3

if [[ -z "$HOST" ]]; then
  echo '{"prtg": {"error": 1, "text": "No host specified"}}'
  exit 1
fi

PING_RESULT=$(ping -c "$COUNT" -W 1 "$HOST")

if [[ $? -ne 0 ]]; then
  echo '{"prtg": {"error": 1, "text": "Ping failed"}}'
  exit 1
fi

# Extrahiere Latenz (avg) und Packet Loss
LATENCY=$(echo "$PING_RESULT" | grep rtt | awk -F'/' '{print $5}')
LOSS=$(echo "$PING_RESULT" | grep -oP '\d+(?=% packet loss)')

echo '{
  "prtg": {
    "result": [
      {
        "channel": "Latency",
        "value": '"$LATENCY"',
        "unit": "ms",
        "float": 1,
        "limitmaxwarning": 100,
        "limitmaxerror": 200,
        "limitmode": 1
      },
      {
        "channel": "Packet Loss",
        "value": '"$LOSS"',
        "unit": "Percent",
        "limitmaxwarning": 20,
        "limitmaxerror": 50,
        "limitmode": 1
      }
    ],
    "text": "Ping to '"$HOST"' OK"
  }
}'
