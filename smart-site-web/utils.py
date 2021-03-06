# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: db.py
# @date: 2020/12/2
import random
import string
import pickle
import base64


def id_to_key(table_name: str, iid) -> str:
    return table_name + ":" + str(iid)


def key_to_id(key: str) -> str:
    return key.split(":")[-1]


def random_id():
    return "".join(random.sample(string.ascii_uppercase + string.digits, 16))


def random_employee_id():
    return "".join(random.sample(string.digits, 4))


def page_size_convert(page: int, size: int, length: int) -> (int, int):
    start = (page - 1) * size
    end = page * size if page * size <= length else length
    return start, end


def pic_to_str(f):
    return pickle.dumps(f)


def str_to_pic(pic_str):
    return pickle.loads(pic_str)


def pic_to_str64(f):
    return base64.b64encode(f)


def str_to_pic64(pic_str):
    return base64.b64decode(pic_str)
