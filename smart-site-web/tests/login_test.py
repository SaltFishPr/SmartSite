# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: login_test.py
# @date: 2020/12/15
import requests

if __name__ == "__main__":
    data = {"username": "saltfish", "password": "123", "description": "description"}
    response = requests.post("http://192.168.31.199:8000/auth/register", data=data)
    print(response.text)
