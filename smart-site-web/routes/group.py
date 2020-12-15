# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: group.py
# @date: 2020/12/15
from flask import Blueprint, request, render_template, json

import db

bp = Blueprint("group", __name__, url_prefix="/group")


@bp.route("/create", methods=("GET", "POST"))
def create_group():
    data = {"flag": False,
            "message": "未执行创建"}
    if request.method == "POST":
        # print(json.loads(request.form["data"]))
        group_id = (json.loads(request.form["data"])["groupId"])
        group = db.GroupInfo(group_id)
        employee_string: str = json.loads(request.form["data"])["groupMember"]
        employee_list = employee_string.split("-")
        for employee in employee_list:
            group.add_employee(int(employee), False)
        leader_string: str = json.loads(request.form["data"])["groupLeader"]
        leader_list = leader_string.split("-")
        for leader in leader_list:
            if group.get_leader_num() == 3:
                data["flag"] = False
                data["message"] = "The number of group leaders in the group reaches the upper limit"
                return data
            group.add_employee(int(leader), True)
        data["flag"] = True
        data["message"] = "successfullyCreatedGroup"
        return json.dumps(data)
    return json.dumps(data)


@bp.route("/delete", methods=("GET", "POST"))
def delete_group():
    data = {"flag": False,
            "message": "未执行删除"}
    if request.method == "POST":
        group_id = (json.loads(request.form["data"]))["groupId"]
        group = db.GroupInfo(group_id)
        if group.delete_group():
            data["flag"] = True
            data["message"] = "groupDeletedSuccessfully"
            return json.dumps(data)
        else:
            data["flag"] = False
            data["message"] = "failedToDeleteGroup"
            return json.dumps(data)
    return json.dumps(data)


@bp.route("/update", methods=("GET", "POST"))
def update():
    data = {"flag": False,
            "message": "未执行更新小组"}
    if request.method == "POST":

        group_id = json.loads(request.form["data"])["groupId"]
        group = db.GroupInfo(group_id)
        for employee_id_delete in group.get_all():
            group.remove_employee(employee_id_delete[0])
        employee_string: str = json.loads(request.form["data"])["groupMember"]
        employee_list = employee_string.split("-")
        for employee in employee_list:
            group.add_employee(int(employee), False)
        leader_string: str = json.loads(request.form["data"])["groupLeader"]
        leader_list = leader_string.split("-")
        for leader in leader_list:
            if group.get_leader_num() == 3:
                data["flag"] = False
                data["message"] = "The number of group leaders in the group reaches the upper limit"
                return data
            group.add_employee(int(leader), True)
        data["flag"] = True
        data["message"] = "successfullyUpdateGroup"
        return json.dumps(data)
    return json.dumps(data)


if __name__ == "__main__":
    pass
