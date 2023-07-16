import json
import time

import requests
from crontabs import Cron, Tab
from ping import send_ping


def get_servers():
    result = requests.get("http://127.0.0.1:5000/api/servers").json()
    return result


def send_metrics(host, response):
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


def monitor():
    servers = get_servers()

    if servers:
        for server in servers:
            response = send_ping(server["host"])
            send_metrics(server["host"], response)
    else:
        print("No hay servidores para monitorear.")


Cron().schedule(Tab(name="monitor").every(seconds=60).run(monitor)).go()
