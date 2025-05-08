#!/usr/bin/env python3
import json
import subprocess
import sys

def ping(host, count=3):
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", "1", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True
        )
        output = result.stdout

        if result.returncode == 0:
            # Extract latency
            lines = output.splitlines()
            stats_line = [line for line in lines if "rtt min" in line or "round-trip" in line]
            loss_line = [line for line in lines if "packet loss" in line]

            latency = 0.0
            loss = 0.0

            if stats_line:
                parts = stats_line[0].split("=")[1].strip().split("/")
                latency = float(parts[1])  # average

            if loss_line:
                loss_text = loss_line[0].split(",")[2].strip()
                loss = float(loss_text.split("%")[0])

            return latency, loss, True
        else:
            return 0, 100, False
    except Exception:
        return 0, 100, False

def main():
    if len(sys.argv) < 2:
        print("Usage: mpp-ping.py <host>")
        sys.exit(1)

    host = sys.argv[1]
    latency, loss, success = ping(host)

    data = {
        "prtg": {
            "result": [
                {
                    "channel": "Latency",
                    "value": latency,
                    "unit": "ms",
                    "float": 1,
                    "limitmaxwarning": 100,
                    "limitmaxerror": 200,
                    "limitmode": 1
                },
                {
                    "channel": "Packet Loss",
                    "value": loss,
                    "unit": "Percent",
                    "limitmaxwarning": 20,
                    "limitmaxerror": 50,
                    "limitmode": 1
                }
            ],
            "text": f"Ping to {host} {'OK' if success else 'FAILED'}"
        }
    }

    print(json.dumps(data))

if __name__ == "__main__":
    main()
