# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: redis_test.py
# @date: 2020/12/15
import redis

pool = redis.ConnectionPool(host="localhost", port=6379, decode_responses=True)


if __name__ == "__main__":
    r = redis.Redis(connection_pool=pool)
    print(r.keys())
