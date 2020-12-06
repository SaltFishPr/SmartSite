# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: database.py
# @date: 2020/12/2
import redis


pool = redis.ConnectionPool(host="localhost", port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
if __name__ == "__main__":
    r.set("name", "saltfish")  # 设置 name 对应的值
    r.set("name1", "saltfish")  # 设置 name 对应的值
    a = r.delete("name", "name1")
    print(type(a), a)
    # print(r.get("name"))  # 取出键 name 对应的值
    # r.set("fruit", "watermelon", nx=True)  # nx - 如果设置为True，则只有name不存在时，当前set操作才执行（新建）
    # r.set("fruit", "watermelon", xx=True)  # xx - 如果设置为True，则只有name存在时，当前set操作才执行（修改）
    pass
