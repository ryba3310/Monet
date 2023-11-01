#!/usr/bin/python3
import socket
import requests
from scapy.all import arping
from time import sleep
from datetime import datetime

LOCALHOST = "127.0.0.1"


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("10.254.254.254", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = LOCALHOST
    finally:
        s.close()
    return IP

def get_hosts(network):
    ans, unans = arping(network, timeout=3, verbose=0)     # any send based function returns couple of answered ad unanswared pkts, and answared pkts are pairs of sent-recived
    return ans.res


def update_hosts(hosts):
    try:
        response = requests.post(f"http://{LOCALHOST}:5000/hosts", json=hosts)
        if response.status_code != 204:
            print("[INFO]Couldn't deliver hosts to server")
        else:
            print("[INFO]Delivered dicovered hosts to server")
    except requests.exceptions.HTTPError as errh:
        print ("[INFO]Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("[INFO]Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("[INFO]Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("[INFO]IDK wat is going on????\n",err)

def main():
    my_subnet = ".".join(get_my_ip().split(".")[0:3]) + ".0/24"

    while True:
        discovered = get_hosts(my_subnet)
        discovery_time = str(datetime.now())[0:-7]
        hosts = []
        for discovery in discovered:
            ip_addr = discovery[1].payload.psrc
            mac_addr = discovery[1].payload.hwsrc
            try:
                hostname = socket.gethostbyaddr(ip_addr)
            except (socket.error, socket.gaierror):
                hostname = (str(ip_addr), [], str(ip_addr))
            host = {
                "mac": mac_addr,
                "ip": ip_addr,
                "hostname": hostname[0],
                "time": discovery_time}
            hosts.append(host)
        update_hosts(hosts)     # Sending list of dicts as JSON
        sleep(10)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"Exiting host monitor")
        exit()
