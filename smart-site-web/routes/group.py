# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: group.py
# @date: 2020/12/15
from flask import Blueprint, request, json

import db
from utils import page_size_convert

bp = Blueprint("group", __name__, url_prefix="/group")


@bp.route("/create", methods=("GET", "POST"))
def create_group():
    data = {"flag": False, "message": "未执行创建"}
    if request.method == "POST":
        rev_data = json.loads(request.form["data"])
        group_id = rev_data["groupId"]
        group = db.GroupInfo(group_id)
        if group.is_exist():
            data["flag"] = False
            data["message"] = "theGroupAlreadyExists"
            return json.dumps(data)

        print(rev_data)

        employee_string: str = rev_data["groupMember"]
        employee_list = employee_string.split("-")
        for employee in employee_list:
            group.add_employee(employee, False)

        leader_string: str = rev_data["groupLeader"]
        leader_list = leader_string.split("-")
        for leader in leader_list:
            if group.get_leader_num() == 3:
                data["flag"] = False
                data[
                    "message"
                ] = "The number of group leaders in the group reaches the upper limit"
                return json.dumps(data)
            group.add_employee(leader, True)

        data["flag"] = True
        data["message"] = "successfullyCreatedGroup"
        return json.dumps(data)
    return json.dumps(data)


@bp.route("/delete", methods=("GET", "POST"))
def delete_group():
    data = {"flag": False, "message": "未执行删除"}
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
def update_group():
    data = {"flag": False, "message": "未执行更新小组"}
    if request.method == "POST":
        rev_data = json.loads(request.form["data"])
        group_id = rev_data["groupId"]
        group = db.GroupInfo(group_id)

        for employee_id_delete in group.get_all():
            group.remove_employee(employee_id_delete[0])

        employee_string: str = rev_data["groupMember"]
        employee_list = employee_string.split("-")
        for employee in employee_list:
            group.add_employee(employee, False)

        leader_string: str = rev_data["groupLeader"]
        leader_list = leader_string.split("-")
        for leader in leader_list:
            if group.get_leader_num() == 3:
                data["flag"] = False
                data[
                    "message"
                ] = "The number of group leaders in the group reaches the upper limit"
                return json.dumps(data)
            group.add_employee(leader, True)

        data["flag"] = True
        data["message"] = "successfullyUpdateGroup"
        return json.dumps(data)
    return json.dumps(data)


@bp.route("/getList", methods=("GET", "POST"))
def get_all_groups():
    if request.method == "POST":
        rev_data = json.loads(request.form["data"])
        page, size, search_key = (
            rev_data["page"],
            rev_data["size"],
            rev_data["searchKey"],
        )
        if search_key == "":
            group_list = db.get_all_groups()
            length = len(group_list)
            start, end = page_size_convert(page, size, length)
            data = {
                "resultTotal": length,
                "resultList": group_list[start:end],
            }
            return json.dumps(data)
        else:
            search_key = int(search_key)
            group = db.GroupInfo(search_key)
            if group.is_exist():
                data = {"resultTotal": 1, "resultList": group.get_group_dict()}
                return json.dumps(data)
            else:
                data = {"resultTotal": 0, "resultList": None}
                return json.dumps(data)
