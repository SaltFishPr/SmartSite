# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: system.py
# @date: 2020/12/21
import json
from typing import List
from flask import Blueprint, request

import db

bp = Blueprint("system", __name__, url_prefix="/system")


@bp.route("/getTree", methods=("POST",))
def get_system():
    table = db.CheckSystemInfo()
    check_system_list = table.get_all()

    def get_special(llist: List, pre_id: str):
        res = []
        for d in llist:
            if d["pre_id"] == pre_id:
                res.append(d)
        return res

    def get_children(system_id: str):
        children = get_special(check_system_list, system_id)
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
    return {"tree": data}


@bp.route("/create", methods=("POST",))
def create_system():
    data = json.loads(request.form["data"])
    table = db.CheckSystemInfo()
    if table.insert(
        data["systemId"], data["systemName"], data["preId"], data["systemDescription"]
    ):
        return {"message": "创建成功", "flag": True}
    return {"message": "创建失败", "flag": False}


@bp.route("/delete", methods=("POST",))
def delete_system():
    data = json.loads(request.form["data"])
    table = db.CheckSystemInfo()
    if table.delete(data["systemId"]):
        return {"message": "删除成功", "flag": True}
    return {"message": "删除失败", "flag": False}


@bp.route("/update", methods=("POST",))
def update_system():
    data = json.loads(request.form["data"])
    table = db.CheckSystemInfo()
    if table.update(
        data["systemId"], data["systemName"], data["preId"], data["systemDescription"]
    ):
        return {"message": "更新成功", "flag": True}
    return {"message": "更新失败", "flag": False}
