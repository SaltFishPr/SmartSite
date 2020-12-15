# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: redis_test.py
# @date: 2020/12/15
import db
import redis

if __name__ == "__main__":
    r = redis.Redis(connection_pool=db.pool)
    print(r.keys())
