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

inps = [
    ("2024-07-11T13:02:49.595Z", "2024-07-11T13:32:49.620Z"),
    ("2024-07-11T13:45:24.580Z", "2024-07-11T14:15:24.627Z"),
    ("2024-07-11T14:28:00.147Z", "2024-07-11T14:58:00.215Z"),
    ("2024-07-11T15:10:36.095Z", "2024-07-11T15:40:36.146Z"),
    ("2024-07-11T15:53:09.587Z", "2024-07-11T16:23:09.633Z"),
    ("2024-07-11T16:35:40.225Z", "2024-07-11T17:05:40.244Z"),
    ("2024-07-11T17:18:25.602Z", "2024-07-11T17:48:25.650Z"),
    ("2024-07-11T18:00:59.794Z", "2024-07-11T18:30:59.861Z"),
    ("2024-07-11T18:43:38.109Z", "2024-07-11T19:13:38.152Z"),
    ("2024-07-11T19:26:12.743Z", "2024-07-11T19:56:12.772Z"),
    ("2024-07-11T20:08:32.441Z", "2024-07-11T20:38:32.485Z"),
    ("2024-07-11T20:51:09.572Z", "2024-07-11T21:21:09.626Z"),
    ("2024-07-11T21:33:28.599Z", "2024-07-11T22:03:28.620Z"),
    ("2024-07-11T22:16:00.644Z", "2024-07-11T22:46:00.722Z"),
    ("2024-07-11T22:58:19.654Z", "2024-07-11T23:28:19.688Z"),
    ("2024-07-11T23:40:29.991Z", "2024-07-12T00:10:30.055Z"),
    ("2024-07-12T00:23:02.916Z", "2024-07-12T00:53:02.951Z"),
    ("2024-07-12T01:05:11.447Z", "2024-07-12T01:35:11.464Z"),
    ("2024-07-12T01:47:21.785Z", "2024-07-12T02:17:21.803Z"),
    ("2024-07-12T02:29:30.751Z", "2024-07-12T02:59:30.804Z"),
    ("2024-07-12T03:11:38.472Z", "2024-07-12T03:41:38.517Z"),
    ("2024-07-12T03:54:09.871Z", "2024-07-12T04:24:09.909Z"),
    ("2024-07-12T04:36:19.156Z", "2024-07-12T05:06:19.208Z"),
    ("2024-07-12T05:18:28.243Z", "2024-07-12T05:48:28.262Z"),
    ("2024-07-12T06:00:57.211Z", "2024-07-12T06:30:57.231Z"),
    ("2024-07-12T06:43:08.903Z", "2024-07-12T07:13:08.979Z"),
    ("2024-07-12T07:25:40.022Z", "2024-07-12T07:55:40.084Z"),
    ("2024-07-12T08:07:58.927Z", "2024-07-12T08:37:58.976Z"),
    ("2024-07-12T08:50:08.193Z", "2024-07-12T09:20:08.255Z"),
    ("2024-07-12T09:32:35.158Z", "2024-07-12T10:02:35.200Z"),
]

qCpu = 'sum(rate(container_cpu_usage_seconds_total{namespace=~"loki|minio", container!="", container!="POD"}[5m]))'
IqCpu = 'sum(irate(container_cpu_usage_seconds_total{namespace=~"loki|minio", container!="", container!="POD"}[5m]))'
qmem = 'sum(container_memory_usage_bytes{namespace=~"loki|minio", container!="", image!="", container!="POD"})'
qmemSet = 'sum(container_memory_working_set_bytes{namespace=~"loki|minio", container!="", image!="", container!="POD"})'
netOutquery = 'sum(rate(container_network_receive_bytes_total{namespace=~"loki|minio"}[5m]))'
InetOutquery = 'sum(irate(container_network_receive_bytes_total{namespace=~"loki|minio"}[5m]))'
netInQuery = 'sum(rate(container_network_transmit_bytes_total{namespace=~"loki|minio"}[5m]))'
InetInQuery = 'sum(irate(container_network_transmit_bytes_total{namespace=~"loki|minio"}[5m]))'
fsWriteQuery = 'sum(rate(container_fs_writes_bytes_total{namespace=~"loki|minio", container!="", container!="POD"}[5m]))'
IfsWriteQuery = 'sum(irate(container_fs_writes_bytes_total{namespace=~"loki|minio", container!="", container!="POD"}[5m]))'
fsReadQuery = 'sum(rate(container_fs_reads_bytes_total{namespace=~"loki|minio", container!="", container!="POD"}[5m]))'
IfsReadQuery = 'sum(irate(container_fs_reads_bytes_total{namespace=~"loki|minio", container!="", container!="POD"}[5m]))'

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
