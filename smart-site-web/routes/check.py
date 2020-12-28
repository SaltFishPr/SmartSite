# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: check.py
# @date: 2020/12/21
import json
from flask import Blueprint, request

import db

bp = Blueprint("check", __name__, url_prefix="/check")


@bp.route("/get_check_info", methods=("POST",))
def get_check_info():
    problem_description = request.form["problem_description"]
    project_id = request.form["project_id"]
    risk_value = request.form["risk_value"]
    print(risk_value)
    employee_id = request.form["employee_id"]
    check_system_route = request.form["check_system_route"]
    check_id = f"{project_id}-{check_system_route}"
    img = request.files["Image"]
    table = db.CheckInfo()
    if table.insert(
        check_id,
        project_id,
        check_system_route,
        employee_id,
        risk_value,
        problem_description,
        img,
    ):
        return json.dumps({"message": "上传服务器成功"})
    else:
        return json.dumps({"message": "上传服务器失败请重试"})
