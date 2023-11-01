#!/usr/bin/python3.10
from flask import Flask, request


app = Flask(__name__)

all_hosts = list()

@app.route("/hosts", methods=["GET", "POST"])
def hosts():
    global all_hosts
    if request.method == "GET":
        return all_hosts, 200
    elif request.method == "POST":
        all_hosts = request.get_json()
        print(f"[INFO] GOT HOSTS JSON")
        return "Got it mate", 204
    # ONLY FOR PYTHON3.10 BYEBYE : (((((
    # Gonna do venv or pipenv someday
    # match request.method:
    #     case "GET":
    #         return hosts
    #     case "POST":
    #         hosts = request.get_json()
    #         print(f"[INFO] GOT HOSTS JSON \n{hosts}")

