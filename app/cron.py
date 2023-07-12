import json
import time

import requests
from crontabs import Cron, Tab
from ping import send_ping


def send_metric(host):
    response = send_ping(host)
    data = {
        "host": host,
        "response": response,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    headers = {"Content-Type": "application/json"}
    payload = json.dumps(data)
    result = requests.post(
        "http://127.0.0.1:5000/api/storage", data=payload, headers=headers
    )
    if result.ok:
        print(f"{host} - {result.status_code} - {data}")
        print(f"{host} - Se enviaron los datos correctamente.")
    else:
        print(f"{host} - {result.status_code} - {data}")
        print(f"{host} - No se enviaron los datos.")


servers = requests.get("http://127.0.0.1:5000/api/servers").json()
# print(servers.json())

if servers:
    Cron().schedule(
        *[
            Tab(name=server["name"]).every(seconds=15).run(send_metric, server["host"])
            for server in servers
        ]
    ).go()
