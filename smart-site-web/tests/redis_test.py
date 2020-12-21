# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: redis_test.py
# @date: 2020/12/15
import db

if __name__ == "__main__":
    # r = redis.Redis(connection_pool=db.pool)
    # print(r.keys())
    tmp = db.CheckSystemInfo()
    print(tmp.insert("1", "检查1", "0", "jiancha1"))
    print(tmp.insert("2", "检查2", "0", "jiancha2"))
    print(tmp.insert("3", "检查3", "0", "jiancha3"))
    print(tmp.insert("4", "检查4", "1", "jiancha4"))
    print(tmp.insert("5", "检查5", "1", "jiancha5"))
    print(tmp.insert("6", "检查6", "2", "jiancha6"))
    print(tmp.insert("7", "检查7", "3", "jiancha7"))
