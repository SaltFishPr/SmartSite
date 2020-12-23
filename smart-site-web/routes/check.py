# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: check.py
# @date: 2020/12/21
import json
from flask import Blueprint, request

import db

bp = Blueprint("check", __name__, url_prefix="/check")


@bp.route("/create", methods=("POST",))
def create_check_info():
    problem_description = request.form["problem_description"]
    project_id = request.form["project_id"]
    employee_id = request.form["employee_id"]
    check_system_route = request.form["check_system_route"]
    check_id = f"{project_id}-{check_system_route}"
    img = request.files["Image"]
    table = db.CheckInfo()
    if table.insert(
        check_id, project_id, check_system_route, employee_id, problem_description, img
    ):
        return json.dumps({"message": "上传服务器成功"})
    else:
        return json.dumps({"message": "上传服务器失败请重试"})
