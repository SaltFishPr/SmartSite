# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: employee.py
# @date: 2020/12/15
from flask import Blueprint, request
import db

bp = Blueprint("employee", __name__, url_prefix="/employee")


@bp.route("/", methods=("GET", "POST"))
def get_all_employees():
    data = {"data": db.get_all_employees(), "error": None}
    return data


@bp.route("/create", methods=("GET", "POST"))
def create_employee():
    if request.method == "POST":
        data = request.form["data"]
        employee = db.EmployeeInfo(data["employee_id"])
        if employee.insert(data["employee_name"], data["employee_age"]):
            return "创建成功"
        return "创建失败"


@bp.route("/delete", methods=("GET", "POST"))
def delete_employee():
    if request.method == "POST":
        data = request.form["data"]
        employee = db.EmployeeInfo(data["employee_id"])
        if employee.delete():
            return "删除成功"
        return "删除失败"


@bp.route("/update", methods=("GET", "POST"))
def update_employee():
    if request.method == "POST":
        data = request.form["data"]
        employee = db.EmployeeInfo(data["employee_id"])
        if employee.update(data["employee_name"], data["employee_age"]):
            return "更新成功"
        return "更新失败"
