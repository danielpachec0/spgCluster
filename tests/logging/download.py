import requests
import csv
import json
import os
from datetime import datetime


def prom_query(prometheus_url, query, start_time, end_time, step):
    params = {
        'query': query,
        'start': start_time,
        'end': end_time,
        'step': step
    }
    response = requests.get(
        f'{prometheus_url}/api/v1/query_range', params=params)
    response.raise_for_status()
    return response.json()


def prom_to_csv(json_data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in json_data['data']['result']:
            for value in result['values']:
                writer.writerow({'timestamp': datetime.utcfromtimestamp(
                    value[0]).isoformat(), 'value': value[1]})


namespace = "loki"
prometheus_url = 'http://localhost:9090'
# inps = [("2024-02-14T17:14:46.668Z", "2024-02-14T17:44:47.695Z"),
#         ("2024-02-14T18:47:45.575Z", "2024-02-14T19:17:46.293Z"),
#         ("2024-02-14T19:54:16.144Z", "2024-02-14T20:24:16.719Z"),
#         ("2024-02-14T20:31:57.313Z", "2024-02-14T21:01:57.313Z"),
#         ("2024-02-14T21:37:00.385Z", "2024-02-14T22:07:00.560Z"),
#         ("2024-02-14T22:29:48.097Z", "2024-02-14T22:59:48.920Z"),
#         ("2024-02-14T23:19:31.772Z", "2024-02-14T23:49:32.109Z"),
#         ("2024-02-15T00:05:49.837Z", "2024-02-15T00:35:50.098Z"),
#         ("2024-02-15T00:55:26.315Z", "2024-02-15T01:25:26.945Z"),
#         ("2024-02-15T01:51:53.667Z", "2024-02-15T02:21:54.220Z")
#         ]

inps = [("2024-02-14T17:04:46.668Z", "2024-02-15T02:38:54.220Z")]


qCpu = 'sum(rate(container_cpu_usage_seconds_total{namespace="loki", container!="", container!="POD"}[5m])) by (namespace)'
IqCpu = 'sum(irate(container_cpu_usage_seconds_total{namespace="loki", container!="", container!="POD"}[5m])) by (namespace)'
qmem = 'sum(container_memory_usage_bytes{namespace="loki", container!="", image!="", container!="POD"})'
qmemSet = 'sum(container_memory_working_set_bytes{namespace="loki", container!="", image!="", container!="POD"})'
netOutquery = 'sum(rate(container_network_receive_bytes_total{namespace="loki"}[5m]))'
InetOutquery = 'sum(irate(container_network_receive_bytes_total{namespace="loki"}[5m]))'
netInQuery = 'sum(rate(container_network_transmit_bytes_total{namespace="loki"}[5m]))'
InetInQuery = 'sum(irate(container_network_transmit_bytes_total{namespace="loki"}[5m]))'
fsWriteQuery = 'sum(rate(container_fs_writes_bytes_total{namespace="loki", container!="", container!="POD"}[5m]))'
IfsWriteQuery = 'sum(irate(container_fs_writes_bytes_total{namespace="loki", container!="", container!="POD"}[5m]))'
fsReadQuery = 'sum(rate(container_fs_reads_bytes_total{namespace="loki", container!="", container!="POD"}[5m]))'
IfsReadQuery = 'sum(irate(container_fs_reads_bytes_total{namespace="loki", container!="", container!="POD"}[5m]))'

queries = [(qCpu, "cpu"), (IqCpu, "Icpu"), (qmem, "mem"), (qmemSet, "memSet"),
           (netOutquery, "netOut"), (InetOutquery, "InetOut"),
           (netInQuery, "netIn"), (InetInQuery, "InetIn"),
           (fsWriteQuery, "fsWrite"), (IfsWriteQuery, "IfsWrite"),
           (fsReadQuery, "fsRead"), (IfsReadQuery, "IfsRead")
           ]

for i in inps:
    print(".")
    os.system(f'mkdir -p lokiDay1/{i[0]}')
    for j in queries:
        output_file = "lokiDay1"+"/"+i[0]+"/"+j[1]
        data = prom_query(prometheus_url, j[0], i[0], i[1], '5s')
        prom_to_csv(data, output_file)
