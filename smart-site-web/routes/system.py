# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: system.py
# @date: 2020/12/21
import json
from typing import List
from flask import Blueprint, request

import db
from routes.auth import login_required

bp = Blueprint("system", __name__, url_prefix="/system")


@bp.route("/getTree", methods=("POST",))
@login_required
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


@bp.route("/get_first_route", methods=("POST",))
def get_first_route():
    table = db.CheckSystemInfo()
    check_system_list = table.get_all()
    first_system = []
    id_list = []
    for system_item in check_system_list:
        if system_item["pre_id"] == "0":
            first_system.append(system_item["system_description"])
            id_list.append(system_item["system_id"])
    return json.dumps({"first_system": first_system, "id_list": id_list})


@bp.route("/get_second_route", methods=("POST",))
def get_send_route():
    data = json.loads(request.form["data"])
    first_id = str(data["first_id"])
    table = db.CheckSystemInfo()
    check_system_list = table.get_all()
    sencond_system = []
    id_list = []
    for system_item in check_system_list:
        if system_item["pre_id"] == first_id:
            sencond_system.append(system_item["system_description"])
            id_list.append(system_item["system_id"])
    return json.dumps({"sencond_system": sencond_system, "id_list": id_list})


@bp.route("/get_third_route", methods=("POST",))
def get_three_route():
    data = json.loads(request.form["data"])
    second_id = str(data["second_id"])
    table = db.CheckSystemInfo()
    check_system_list = table.get_all()
    third_system = []
    id_list = []
    for system_item in check_system_list:
        if system_item["pre_id"] == second_id:
            third_system.append(system_item["system_description"])
            id_list.append(system_item["system_id"])
    return json.dumps({"third_system": third_system, "id_list": id_list})


@bp.route("/get_check_info", methods=("POST",))
def get_check_info():
    data = json.loads(request.form["data"])
    check_info_id = str(data["check_info_id"])
    table = db.CheckSystemInfo()
    check_system_list = table.get_all()
    first_system = "该项目未匹配到相应检查体系"
    for system_item in check_system_list:
        if system_item["system_id"] == check_info_id:
            first_system = (system_item["system_description"])
    return json.dumps({"first_system": first_system})


if __name__ == '__main__':
    tmp = db.CheckSystemInfo()
    print(get_system())
