from ping3 import ping
from statistics import mean
from math import floor

# 1.1.1.1 (Cloudflare), Google DNS, Quad9 DNS, OpenDNS
dns_list = ["1.1.1.1", "1.0.0.1", "8.8.8.8", "8.8.4.4", "9.9.9.9", "149.112.112.112", "208.67.222.222", "208.67.220.220"]
pings = []
max_pings = []
min_pings = []
ping_count = 64



def reduce_latency_size(latency):
    return floor(latency * 1000000) / 1000000

print("Testing your list of DNS servers now...")

for dns in dns_list:
    latency = []
    for i in range(ping_count):
        latency.append(ping(dns) * 1000)
    pings.append(reduce_latency_size(mean(latency)))
    max_pings.append(reduce_latency_size(max(latency)))
    min_pings.append(reduce_latency_size(min(latency)))


sorted_pings = sorted(pings)
min_ping = sorted_pings[0]
min_ping2 = sorted_pings[1]

print("1 | Latency:", min_ping, "ms | DNS Server:", dns_list[pings.index(min_ping)])
print("2 | Latency:", min_ping2, "ms | DNS Server:", dns_list[pings.index(min_ping2)])

print_entire_list = input("Do you want to print out a comprehensive list of latencies? [y/N]").lower().strip()

if print_entire_list == "y":
    for latency in sorted_pings:
        i = sorted_pings.index(latency)
        print(i + 1, "| Avg Latency:", latency, "ms | Min Latency:", min_pings[i], "ms | Max Latency:", max_pings[i], "ms | DNS Server:", dns_list[pings.index(latency)])
else:
    exit(0)
