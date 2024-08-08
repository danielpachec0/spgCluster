import os
import numpy as np


def flatten_and_convert(data):
    """Flattens nested lists and converts elements to numeric values."""
    flat_list = []
    for item in data:
        if isinstance(item, (list, tuple, np.ndarray)):
            flat_list.extend(flatten_and_convert(item))
        else:
            flat_list.append(item)
    return flat_list


# def remove_outliers(data):
#     # Ensure the data is a flat numpy array of numeric values
#     flat_data = flatten_and_convert(data)
#     numeric_data = np.array([x for x in flat_data if isinstance(x, (int, float))])
#
#     q1 = np.percentile(numeric_data, 25)
#     q3 = np.percentile(numeric_data, 75)
#     IQR = q3 - q1
#
#     lower_bound = q1 - 1.5 * IQR
#     upper_bound = q3 + 1.5 * IQR
#
#     filtered = numeric_data[(numeric_data >= lower_bound) & (numeric_data <= upper_bound)]
#     return filtered

def read_data(fileName):
    with open(fileName) as f:
        lns = f.readlines()
    data = np.array([float(i.split(',')[1].strip()) for i in lns[1:]])

    # Remove outliers from data
    # data = remove_outliers(data)
    return data


def get_all_metrics(path):
    data = {}
    metrics = ["cpu", "memSet", "mem", "netIn", "netOut", "fsRead", "fsWrite",]
    for m in metrics:
        d = read_data(os.path.join(path, m))
        data[m] = d
    return data


# dir = "./loki/load/loki"
# dir = "./loki/load/loki_no_cache"
# dir = "./opensearch/load"
dir = "./jaeger/load/v1"
# dir = "./tempo/load"
sub = []

for root, dirs, files in os.walk(dir):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        sub.append(dir_path)

allData = {
    "cpu": [],
    "memSet": [],
    "mem": [],
    "netIn": [],
    "netOut": [],
    "fsRead": [],
    "fsWrite": []
}

for exec_path in sub:
    metrics = ["cpu", "fsRead", "fsWrite", "memSet", "mem", "netIn", "netOut"]
    for m in metrics:
        r = read_data(os.path.join(exec_path, m))
        allData[m].append(r)


def calculate_statistics(numbers):
    # Flatten the list of arrays into a single array
    numbers = np.concatenate(numbers)
    mean = np.mean(numbers)
    median = np.median(numbers)
    std_deviation = np.std(numbers)

    return mean, median, std_deviation


def bytes_to_gigabytes(bytes_num):
    gigabytes = bytes_num / (1024 ** 3)  # Convert bytes to gigabytes
    return f"{gigabytes:.2f} GB"


def bytes_to_megabytes(bytes_num):
    gigabytes = bytes_num / (1024 ** 2)  # Convert bytes to gigabytes
    return f"{gigabytes:.2f} MB"


metrics = ["cpu", "fsRead", "fsWrite", "memSet", "mem", "netIn", "netOut"]

for m in metrics:
    mean, median, std_deviation = calculate_statistics(allData[m])
    if m == "cpu":
        mean = f"{mean:.2f}"
        median = f"{median:.2f}"
        std_deviation = f"{std_deviation:.2f}"
    elif m == "mem" or m == "memSet":
        mean = bytes_to_gigabytes(mean)
        median = bytes_to_gigabytes(median)
        std_deviation = bytes_to_gigabytes(std_deviation)
    else:
        mean = bytes_to_megabytes(mean)
        median = bytes_to_megabytes(median)
        std_deviation = bytes_to_megabytes(std_deviation)
    print(f"{m} -> Mean: {mean}, Median: {median}, \
Standard Deviation: {std_deviation}")
