#!/usr/bin/python3

import requests
from time import sleep


WHITE = "\033[0m"
OKGREEN = "\033[92m"


def request_hosts():
    hosts = []
    try:
        response = requests.get(f"http://localhost:5000/hosts")
        if response.status_code != 200:
            print("[INFO]Couldn't retrive hosts from server")
        else:
            print("[INFO]Got the hosts")
            hosts = response.json()
            return hosts
    except requests.exceptions.HTTPError as errh:
        print ("[INFO]Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("[INFO]Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("[INFO]Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("[INFO]IDK wat is going on????\n",err)
    return hosts

def print_hosts():
    while True:
        hosts = request_hosts()
        print("\t\tMac Address\t\tIP address\t\tHostname\t\tDate")
        for host in hosts:
            print(f"{host['mac']:<17}{host['ip']:<16}{host['hostname'][:15]}{host['time']:>16}")
        sleep(10)


if __name__ == "__main__":
    try:
        print_hosts()
    except KeyboardInterrupt:
        print(f"Exiting host display")
        exit()
