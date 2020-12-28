# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: redis_test.py
# @date: 2020/12/15
import db
import redis
import os

if __name__ == "__main__":
    # r = redis.Redis(connection_pool=db.pool)
    # # print(r.keys())
    # check_system_keys = r.keys(pattern="CheckInfo:*")
    # print(check_system_keys)

    table = db.CheckInfo()
    print(table.get("CheckInfo:BSWGJPZO6CD5X8R2-1-4"))
