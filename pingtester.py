import re
import socket
from ping3 import ping
from statistics import mean
from math import floor
from re import match
from datetime import datetime

dns_list = [
    '1.1.1.1',          # Cloudflare DNS (primary)
    '1.0.0.1',          # Cloudflare DNS (secondary)
    '8.8.8.8',          # Google DNS (primary)
    '8.8.4.4',          # Google DNS (secondary)
    '9.9.9.9',          # Quad9 DNS (primary)
    '149.112.112.112',  # Quad9 DNS (secondary)
    '208.67.222.222',   # OpenDNS (primary)
    '208.67.220.220'    # OpenDNS (secondary)
]
pings = []
max_pings = []
min_pings = []
ping_count = 128

print('Default DNS server list:')
for dns in dns_list:
    print(dns)
print()
custom = input(
    'Do you want to add custom DNS servers? [y/N] ').lower().strip() == 'y'


def valid_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except OSError:
        return False

if custom:
    while custom != 'done':
        custom = input(
            'DNS server IP or \'done\' to exit: [0.0.0.0 | done] ').strip()

        if valid_ip(custom):
            print(f'Adding server {custom} to list.')
            dns_list.append(custom)
        elif custom != 'done':
            print('Invalid DNS server IP.')

print('DNS server list:')
for dns in dns_list:
    print(dns)
print()

pings_per_address = input(
    'How many tests to you want to run on each DNS server? (Higher number = more accurate results) [128]').strip()

if match('^[0-9]+$', pings_per_address):
    print('Pings per address set to', pings_per_address)
    ping_count = int(pings_per_address)
else:
    print('Pings per address set to 128')
    ping_count = 128


def reduce_latency_size(latency: float) -> float:
    return floor(latency * 1000000) / 1000000


def format_latency(i: int, latency: float) -> str:
    return f'{i + 1} | \
Avg Latency: {latency:.6f} ms | \
Min Latency: {min_pings[i]:.6f} ms | \
Max Latency: {max_pings[i]:.6f} ms | \
DNS Server: {dns_list[pings.index(latency)]}'


print('Testing your list of DNS servers now...')

for dns in dns_list:
    print('Testing', dns)
    try:
        latency = [ping(dns) * 1000 for _ in range(ping_count)]
    except TypeError:
        print(f'{dns} timed out.')
    pings.append(reduce_latency_size(mean(latency)))
    max_pings.append(reduce_latency_size(max(latency)))
    min_pings.append(reduce_latency_size(min(latency)))


sorted_pings = sorted(pings)
min_ping = sorted_pings[0]
min_ping2 = sorted_pings[1]

print_entire_list = input(
    'Do you want to print out a comprehensive list of latencies? [y/N]').lower().strip()

if print_entire_list == 'y':
    for latency in sorted_pings:
        i = sorted_pings.index(latency)
        print(format_latency(i, latency))

export_csv = input(
    'Do you want to export this data to a csv file? [y/N]').lower().strip()

if export_csv == 'y':
    time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    with open('Test ' + time.replace(':', '') + '.csv', 'w+') as csv_file:
        csv_file.write('Time:,{}\n'.format(time))
        csv_file.write(
            'Ranking,Average Latency (ms),Minimum Latency (ms),Maximum Latency (ms),DNS Server Address\n')

        for latency in sorted_pings:
            i = sorted_pings.index(latency)
            min_latency = min_pings[i]
            max_latency = max_pings[i]
            server_address = dns_list[pings.index(latency)]
            csv_file.write(
                f'{i + 1},{latency},{min_latency},{max_latency},{server_address}\n')
