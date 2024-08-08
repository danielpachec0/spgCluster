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


namespace = "opensearch"
prometheus_url = 'http://localhost:9090'

inps = [
    ("2024-07-13T02:04:59.283Z", "2024-07-13T11:47:48.325Z"),
]

qCpu = 'sum(rate(container_cpu_usage_seconds_total{namespace=~"opensearch", container!="", container!="POD"}[5m]))'
IqCpu = 'sum(irate(container_cpu_usage_seconds_total{namespace=~"opensearch", container!="", container!="POD"}[5m]))'
qmem = 'sum(container_memory_usage_bytes{namespace=~"opensearch", container!="", image!="", container!="POD"})'
qmemSet = 'sum(container_memory_working_set_bytes{namespace=~"opensearch", container!="", image!="", container!="POD"})'
netOutquery = 'sum(rate(container_network_receive_bytes_total{namespace=~"opensearch"}[5m]))'
InetOutquery = 'sum(irate(container_network_receive_bytes_total{namespace=~"opensearch"}[5m]))'
netInQuery = 'sum(rate(container_network_transmit_bytes_total{namespace=~"opensearch"}[5m]))'
InetInQuery = 'sum(irate(container_network_transmit_bytes_total{namespace=~"opensearch"}[5m]))'
fsWriteQuery = 'sum(rate(container_fs_writes_bytes_total{namespace=~"opensearch", container!="", container!="POD"}[5m]))'
IfsWriteQuery = 'sum(irate(container_fs_writes_bytes_total{namespace=~"opensearch", container!="", container!="POD"}[5m]))'
fsReadQuery = 'sum(rate(container_fs_reads_bytes_total{namespace=~"opensearch", container!="", container!="POD"}[5m]))'
IfsReadQuery = 'sum(irate(container_fs_reads_bytes_total{namespace=~"opensearch", container!="", container!="POD"}[5m]))'

queries = [(qCpu, "cpu"), (IqCpu, "Icpu"), (qmem, "mem"), (qmemSet, "memSet"),
           (netOutquery, "netOut"), (InetOutquery, "InetOut"),
           (netInQuery, "netIn"), (InetInQuery, "InetIn"),
           (fsWriteQuery, "fsWrite"), (IfsWriteQuery, "IfsWrite"),
           (fsReadQuery, "fsRead"), (IfsReadQuery, "IfsRead")
           ]

for a in ["05s"]:
    for i in inps:
        print(".")
        os.system(f'mkdir -p {namespace}{a}/{i[0]}')
        for j in queries:
            output_file = namespace + a + "/"+i[0]+"/"+j[1]
            data = prom_query(prometheus_url, j[0], i[0], i[1], a)
            prom_to_csv(data, output_file)
