# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: redis_test.py
# @date: 2020/12/15
import db
import redis
import os

if __name__ == "__main__":
    r = redis.Redis(connection_pool=db.pool)
    check_keys = r.keys(pattern="CheckInfo:*")
    for check_key in check_keys:
        r.delete(check_key)
    # print(tmp.insert("1", "检查1", "0", "jiancha1"))
    # print(tmp.insert("2", "检查2", "0", "jiancha2"))
    # print(tmp.insert("3", "检查3", "0", "jiancha3"))
    # print(tmp.insert("4", "检查4", "1", "jiancha4"))
    # print(tmp.insert("5", "检查5", "1", "jiancha5"))
    # print(tmp.insert("6", "检查6", "2", "jiancha6"))
    # print(tmp.insert("7", "检查7", "3", "jiancha7"))
    # print(tmp.insert("8", "检查8", "4", "jiancha8"))
    # print(tmp.insert("9", "检查9", "4", "jiancha9"))
