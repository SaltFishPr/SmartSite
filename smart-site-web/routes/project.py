# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: project.py
# @date: 2020/12/17
from flask import Blueprint, request
import json

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
