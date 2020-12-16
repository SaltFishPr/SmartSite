# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: employee.py
# @date: 2020/12/15
from flask import Blueprint, request
import db
import json

bp = Blueprint("employee", __name__, url_prefix="/employee")


@bp.route("/getList", methods=("POST",))
def get_all_employees():
    data = json.loads(request.form["data"])
    page, size, search_key = data["page"], data["size"], data["searchKey"]
    table = db.EmployeeInfo()
    employee_list = table.get_all()
    start = (page - 1) * size
    end = page * size if page * size <= len(employee_list) else len(employee_list)
    data = {
        "resultTotal": len(employee_list),
        "resultList": employee_list[start:end],
    }
    return data


@bp.route("/create", methods=("POST",))
def create_employee():
    data = json.loads(request.form["data"])
    table = db.EmployeeInfo()
    if table.insert(data["employeeName"], data["employeeAge"]):
        return {"message": "创建成功"}
    return {"message": "创建失败"}


@bp.route("/delete", methods=("POST",))
def delete_employee():
    data = json.loads(request.form["data"])
    table = db.EmployeeInfo()
    if table.delete(data["employeeId"]):
        return {"message": "删除成功"}
    return {"message": "删除失败"}


@bp.route("/update", methods=("POST",))
def update_employee():
    data = json.loads(request.form["data"])
    table = db.EmployeeInfo()
    if table.update_data(data["employeeId"], data["employeeName"], data["employeeAge"]):
        return {"message": "更新成功"}
    return {"message": "更新失败"}
