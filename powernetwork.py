import socket
import requests
import json


def dns_lookup(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        return "DNS Lookup Failed"

def check_port(hostname, port=443):
    try:
        sock = socket.create_connection((hostname, port), timeout=3)
        sock.close()
        return "Open"
    except:
        return "Closed"

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json()["ip"]
    except:
        return "Unable to retrieve"

with open("hosts.txt", "r") as file:
    hostnames = [line.strip() for line in file if line.strip()]

results = []

for host in hostnames:
    result = {
        "hostname": host,
        "resolved_ip": dns_lookup(host),
        "port_443": check_port(host)
    }
    results.append(result)

output = {
    "public_ip": get_public_ip(),
    "hosts": results
}

with open("results.json", "w") as file:
    json.dump(output, file, indent=4)

print("Results exported to results.json")
