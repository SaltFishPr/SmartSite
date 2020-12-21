# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: system.py
# @date: 2020/12/21
import json
from typing import List
from flask import Blueprint, request

import db
from utils import page_size_convert

bp = Blueprint("system", __name__, url_prefix="/system")


@bp.route("/getList", methods=("POST",))
def get_system():
    table = db.CheckSystemInfo()
    client_list = table.get_all()

    def get_special(l: List, pre_id: str):
        res = []
        for d in l:
            if d["pre_id"] == pre_id:
                res.append(d)
        return res

    def get_children(system_id: str):
        children = get_special(client_list, system_id)
        if not children:
            return []
        res = []
        for child in children:
            res.append(
                {
                    "systemId": child["system_id"],
                    "systemName": child["system_name"],
                    "systemDescription": child["system_description"],
                    "children": get_children(child["system_id"]),
                }
            )
        return res

    data = get_children("0")
    return data
