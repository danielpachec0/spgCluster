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

# inps = [
#     ("2024-02-15T13:15:54.009Z", "2024-02-15T13:45:54.859Z"),
#     ("2024-02-15T14:03:41.654Z", "2024-02-15T14:33:42.147Z"),
#     ("2024-02-15T14:42:40.544Z", "2024-02-15T15:12:41.617Z"),
#     ("2024-02-15T15:21:38.545Z", "2024-02-15T15:51:39.564Z"),
#     ("2024-02-15T16:06:44.459Z", "2024-02-15T16:36:45.228Z"),
#     ("2024-02-15T16:59:53.540Z", "2024-02-15T17:29:53.720Z"),
#     ("2024-02-15T17:42:43.699Z", "2024-02-15T18:12:44.463Z"),
#     ("2024-02-15T18:30:14.981Z", "2024-02-15T19:00:15.366Z"),
#     ("2024-02-15T19:08:16.952Z", "2024-02-15T19:38:17.525Z"),
#     ("2024-02-15T19:48:54.546Z", "2024-02-15T20:18:55.203Z"),
#     ("2024-02-15T20:29:00.742Z", "2024-02-15T20:59:01.326Z"),
#     ("2024-02-15T21:10:31.033Z", "2024-02-15T21:40:31.380Z"),
# ]

# inps = [
#     ("2024-02-16T12:53:59.105Z", "2024-02-16T13:23:59.394Z"),
#     ("2024-02-16T13:39:59.236Z", "2024-02-16T14:09:59.285Z"),
#     ("2024-02-16T14:24:18.506Z", "2024-02-16T14:54:18.925Z"),
#     ("2024-02-16T15:05:39.825Z", "2024-02-16T15:35:40.091Z"),
#     ("2024-02-16T15:49:43.344Z", "2024-02-16T16:19:43.644Z"),
#     ("2024-02-16T16:27:22.139Z", "2024-02-16T16:57:22.520Z"),
#     ("2024-02-16T17:16:37.026Z", "2024-02-16T17:46:37.166Z"),
#     ("2024-02-16T18:02:17.491Z", "2024-02-16T18:32:18.179Z")
# ]

inps = [
    ("2024-02-16T11:53:59.105Z", "2024-02-16T19:32:18.179Z")
]



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
    os.system(f'mkdir -p lokiDay3/{i[0]}')
    for j in queries:
        output_file = "lokiDay3"+"/"+i[0]+"/"+j[1]
        data = prom_query(prometheus_url, j[0], i[0], i[1], '5s')
        prom_to_csv(data, output_file)
