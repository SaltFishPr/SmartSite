# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: project.py
# @date: 2020/12/17
import json

from flask import Blueprint, request

import db
from utils import page_size_convert

bp = Blueprint("project", __name__, url_prefix="/project")


@bp.route("/getList", methods=("POST",))
def get_all_projects():
    data = json.loads(request.form["data"])
    page, size, search_key = data["page"], data["size"], data["searchKey"]
    table = db.ProjectInfo()
    project_list = table.get_all()
    length = len(project_list)
    start, end = page_size_convert(page, size, length)
    data = {
        "resultTotal": length,
        "resultList": project_list[start:end],
    }
    return data


@bp.route("/create", methods=("POST",))
def create_project():
    data = json.loads(request.form["data"])
    table = db.ProjectInfo()
    if table.insert(
        data["clientId"],
        data["projectCheckSystemId"],
        data["projectStatus"],
        data["projectRiskValue"],
        data["projectDescription"],
        data["projectManager"],
        data["projectCheckGroupId"],
    ):
        return {"message": "创建成功", "flag": True}
    return {"message": "创建失败", "flag": False}


@bp.route("/delete", methods=("POST",))
def delete_project():
    data = json.loads(request.form["data"])
    table = db.ProjectInfo()
    if table.delete(data["projectId"]):
        return {"message": "删除成功", "flag": True}
    return {"message": "删除失败", "flag": False}


@bp.route("/update", methods=("POST",))
def update_project():
    data = json.loads(request.form["data"])
    table = db.ProjectInfo()
    if table.update(
        data["projectId"],
        data["clientId"],
        data["projectCheckSystemId"],
        data["projectStatus"],
        data["projectRiskValue"],
        data["projectCreationTime"],
        data["projectDescription"],
        data["projectManager"],
        data["projectCheckGroupId"],
    ):
        return {"message": "更新成功", "flag": True}
    return {"message": "更新失败", "flag": False}


@bp.route("/get_by_group", methods=("POST",))
def get_by_group():
    data = json.loads(request.form["data"])
    table = db.ProjectInfo()
    projects = table.get_all()
    rev_id = data["group_id"]
    description_list = []
    id_list = []
    check_id_list = []
    for project in projects:
        if rev_id == project["projectCheckGroupId"]:
            description_list.append(project["projectDescription"])
            id_list.append(project["projectId"])
            check_id_list.append(project["projectCheckSystemId"])
    return json.dumps(
        {
            "project_list": description_list,
            "id_list": id_list,
            "check_id_list": check_id_list,
        }
    )


@bp.route("/getCheckInfo", methods=("POST",))
def get_check_info():
    data = json.loads(request.form["data"])
    project_id = data["projectId"]
    system_id = data["systemId"]
    check_system_table = db.CheckSystemInfo()
    check_table = db.CheckInfo()

    checks = []
    system_list = check_system_table.get_children(system_id)
    for system in system_list:
        check_id = f"{project_id}-{system_id}-{system['system_id']}"
        check_info = check_table.get(check_id)
        if check_info:
            employee_name = db.EmployeeInfo().get_data(check_info[3])[1]
            description = check_info[4]
            checks.append(
                {
                    "title": system["system_name"],
                    "pic": f"{db.checkfiles_path}/{check_id}.jpg",
                    "employeeName": employee_name,
                    "description": description,
                }
            )
        else:
            checks.append(
                {
                    "title": system["system_name"],
                    "pic": "",
                    "employeeName": "",
                    "description": "",
                }
            )
    return {"checks": checks, "flag": True}
