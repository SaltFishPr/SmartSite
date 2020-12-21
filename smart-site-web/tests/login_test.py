# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: login_test.py
# @date: 2020/12/15
import requests

if __name__ == "__main__":
    data = {"verification": "jl"}
    response = requests.post("http://192.168.31.177:8000/system/getTree", data=data)
    print(response.text)
