# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: auth.py
# @date: 2020/12/13
"""
认证蓝图 Blueprint
认证蓝图将包括注册新用户、登录和注销视图。
"""
import functools

from flask import Blueprint, request, session, json, g

import db
from utils import random_id

bp = Blueprint("auth", __name__, url_prefix="/auth")  # url_prefix 会添加到所有与该蓝图关联的 URL 前面


@bp.route("/register", methods=("POST",))
def register():
    account = request.form["account"]
    password = request.form["password"]
    identity = request.form["identity"]
    table = db.UserInfo()
    error = None

    if not account:
        error = "Username is required."
    elif not password:
        error = "Password is required."
    elif table.is_exist(account):
        error = "User {} is already registered.".format(account)

    if error is None:
        table.insert(account, password, identity)
        return {"message": "Register successfully", "flag": True}

    return {"message": error, "flag": False}


@bp.route("/login", methods=("POST",))
def login():
    """
    进行登录验证
    :return:
    """
    data = json.loads(request.form["data"])
    account = data["account"]
    password = data["password"]
    table = db.UserInfo()
    error = None
    user = table.get(account)

    if not table.is_exist(account) or user == [] or user[1] != password:
        error = "Incorrect username or password."

    if user[2] != "admin":
        error = "Non administrator account"

    if error is None:
        session.clear()
        verification = random_id()
        verification_table = db.VerificationInfo()
        verification_table.insert(verification)
        return {
            "message": "Login successfully",
            "flag": True,
            "verification": verification,
        }

    return {"message": error, "flag": False}


@bp.route("/employee_login", methods=("POST",))
def employee_login():
    """
    安卓端的登陆或注册按钮，如果存在用户登陆，如果不存在则进行注册。
    """
    employee_id = request.form["employee_id"]
    employee_name = request.form["employee_name"]
    data = {
        "message": "未执行操作",
        "ret_code": -4,
    }

    table = db.EmployeeInfo()
    employee = table.get_data(employee_id)
    if table.is_exist(employee_id):  # 如果存在该用户ID则进行登陆操作
        if employee[1] == employee_name:
            data["message"] = "登陆成功"
            data["ret_code"] = 1
            return json.dumps(data)
        else:
            data["message"] = "用户名错误，请重新输入"
            data["ret_code"] = -1
            return json.dumps(data)
    else:  # 如果不存在该用户则进行提示
        data["message"] = "请联系管理员注册"
        data["ret_code"] = -2
        return json.dumps(data)


@bp.route("/logout")
def logout():
    verification_table = db.VerificationInfo()
    if verification_table.delete(request.form["verification"]):
        return {"message": "Logout successfully", "flag": True}
    else:
        return {"message": "Logout failed", "flag": False}


def login_required(view):
    """装饰器 用于身份验证"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        verification = request.form["verification"]
        verification_table = db.VerificationInfo()
        if not verification_table.is_exist(verification):
            return {"message": "请先登录", "flag": False}
        return view(**kwargs)

    return wrapped_view
