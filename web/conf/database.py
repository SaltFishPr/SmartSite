# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: database.py
# @date: 2020/12/2
import redis


pool = redis.ConnectionPool(host="localhost", port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
