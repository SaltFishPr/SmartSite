# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: employee.py
# @date: 2020/12/15
from flask import Blueprint, request
import db
import json

bp = Blueprint("employee", __name__, url_prefix="/employee")


@bp.route("/getList", methods=("GET", "POST"))
def get_all_employees():
    if request.method == "POST":
        data = json.loads(request.form["data"])
        page, size, search_key = data["page"], data["size"], data["searchKey"]
        employee_list = db.get_all_employees()
        start = (page - 1) * size
        end = page * size if page * size <= len(employee_list) else len(employee_list)
        data = {
            "resultTotal": len(employee_list),
            "resultList": employee_list[start:end],
        }
        return json.dumps(data)


@bp.route("/create", methods=("GET", "POST"))
def create_employee():
    if request.method == "POST":
        data = json.loads(request.form["data"])
        employee = db.EmployeeInfo(int(data["employeeId"]))
        if employee.insert(data["employeeName"], data["employeeGroup"]):
            return {"message": "创建成功"}
        return {"message": "创建失败"}


@bp.route("/delete", methods=("GET", "POST"))
def delete_employee():
    if request.method == "POST":
        data = json.loads(request.form["data"])
        employee = db.EmployeeInfo(data["employee_id"])
        if employee.delete():
            return {"message": "删除成功"}
        return {"message": "删除失败"}


@bp.route("/update", methods=("GET", "POST"))
def update_employee():
    if request.method == "POST":
        data = json.loads(request.form["data"])
        employee = db.EmployeeInfo(data["employee_id"])
        if employee.update(data["employee_name"], data["employee_age"]):
            return {"message": "更新成功"}
        return {"message": "更新失败"}
