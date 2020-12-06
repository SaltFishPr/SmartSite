# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: db.py
# @date: 2020/12/2


def id_to_key(table_name: str, iid: int) -> str:
    return table_name + ":" + str(iid)


def key_to_id(key: str) -> int:
    return int(key.split(":")[-1])


if __name__ == "__main__":
    print(id_to_key("client", 1))
    print(key_to_id("client:1"))
