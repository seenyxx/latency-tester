from ping3 import ping
from statistics import mean
from math import floor
from re import match
from datetime import datetime

# 1.1.1.1 (Cloudflare), Google DNS, Quad9 DNS, OpenDNS
dns_list = ["1.1.1.1", "1.0.0.1", "8.8.8.8", "8.8.4.4", "9.9.9.9", "149.112.112.112", "208.67.222.222", "208.67.220.220"]
pings = []
max_pings = []
min_pings = []
ping_count = 128

pings_per_address = input("How many tests to you want to run on each DNS server? (Higher number = more accurate results) [128]").strip()

if match("^[0-9]+$", pings_per_address):
    print("Pings per address set to", pings_per_address)
    ping_count = int(pings_per_address)
else:
    print("Pings per address set to 128")
    ping_count = 128



def reduce_latency_size(latency):
    return floor(latency * 1000000) / 1000000

def format_latency(i, latency):
    return "{} | Avg Latency: {:.6f} ms | Min Latency: {:.6f} ms | Max Latency: {:.6f} ms | DNS Server: {}".format(i + 1, latency, min_pings[i], max_pings[i], dns_list[pings.index(latency)])

print("Testing your list of DNS servers now...")

for dns in dns_list:
    latency = []
    print("Testing", dns)
    for i in range(ping_count):
        latency.append(ping(dns) * 1000)
    pings.append(reduce_latency_size(mean(latency)))
    max_pings.append(reduce_latency_size(max(latency)))
    min_pings.append(reduce_latency_size(min(latency)))


sorted_pings = sorted(pings)
min_ping = sorted_pings[0]
min_ping2 = sorted_pings[1]

print(format_latency(0, min_ping))
print(format_latency(1, min_ping2))

print_entire_list = input("Do you want to print out a comprehensive list of latencies? [y/N]").lower().strip()

if print_entire_list == "y":
    for latency in sorted_pings:
        i = sorted_pings.index(latency)
        print(format_latency(i, latency))

export_csv = input("Do you want to export this data to a csv file? [y/N]").lower().strip()

if export_csv == "y":
    time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    csv_file = open("Test " + time.replace(":", "") + ".csv", "w+")
    csv_file.write("Time:,{}\n".format(time))
    csv_file.write("Ranking,Average Latency (ms),Minimum Latency (ms),Maximum Latency (ms),DNS Server Address\n")
    
    for latency in sorted_pings:
        i = sorted_pings.index(latency)
        min_latency = min_pings[i]
        max_lantecy = max_pings[i]
        server_address = dns_list[pings.index(latency)]
        csv_file.write("{},{},{},{},{}\n".format(i + 1, latency, min_latency, max_lantecy, server_address))
    
    csv_file.close()
    exit(0)
else:
    exit(0)

