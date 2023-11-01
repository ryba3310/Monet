#!/usr/bin/python3
from flask import Flask, request


app = Flask(__name__)


@app.route("/hosts", methods=["GET", "POST"])
def hosts():
    hosts = {}
    print(request.method)
    if request.method == "POST":
        hosts = request.get_json()
        print(f"[INFO] GOT HOSTS JSON \n{hosts}")
        return "Got it mate", 204
    # match request.method:
    #     case "GET":
    #         return hosts
    #     case "POST":
    #         hosts = request.get_json()
    #         print(f"[INFO] GOT HOSTS JSON \n{hosts}")

