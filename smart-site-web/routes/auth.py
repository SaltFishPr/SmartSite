# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: auth.py
# @date: 2020/12/13
"""
认证蓝图 Blueprint
认证蓝图将包括注册新用户、登录和注销视图。
"""
import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    json
)

import db

bp = Blueprint("auth", __name__, url_prefix="/auth")  # url_prefix 会添加到所有与该蓝图关联的 URL 前面


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
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
            return redirect(url_for("auth.login"))

        flash(error)  # 用于储存在渲染模块时可以调用的信息

    return render_template("auth/register.html")  # 渲染一个包含 HTML 的模板


@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    进行登录验证
    :return:
    """
    if request.method == "POST":
        account = request.form["account"]
        password = request.form["password"]
        table = db.UserInfo()
        error = None
        user = table.get(account)

        if not table.is_exist(account) or user == [] or user[1] != password:
            error = "Incorrect username or password."

        if user[2] != "admin":
            error = "Non administrator account"

        if error is None:
            session.clear()
            session["account"] = user[0]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/login_or_register", methods=("POST",))
def login_or_register():
    """
    安卓端的登陆或注册按钮，如果存在用户登陆，如果不存在则进行注册。
    """
    username = request.form["username"]
    password = request.form["password"]
    data = {
        "message":"未执行操作",
        "ret_code":-4,
    }

    table = db.UserInfo()
    user = table.get(username)
    if table.is_exist(username):  #如果存在该用户则进行登陆操作
        if user[1] == password:
            data["message"] = "登陆成功"
            data["ret_code"] = 1
            return json.dumps(data)
        else:
            data["message"] = "密码错误，请重新输入"
            data["ret_code"] = -1
            return json.dumps(data)
    else:  #如果不存在该用户进行注册操作
        if table.insert(username, password, "Android端注册员工"):
            data["message"] = "为你注册成功"
            data["ret_code"] = 0
            return json.dumps(data)
        else:
            data["message"] = "注册失败，请重新注册"
            data["ret_code"] = -2
            return json.dumps(data)



@bp.before_app_request  # 注册一个在视图函数之前运行的函数，不论其 URL 是什么
def load_logged_in_user():
    """
    检查用户 id 是否已经储存在 session 中，并从数据库中获取用户数据，然后储存在 g.user 中。
    g.user 的持续时间比请求要长。如果没有用户 id ，或者 id 不存在，那么 g.user 将会是 None 。
    :return: Nothing
    """
    account = session.get("account")

    if account is None:
        g.user = None
    else:
        g.user = db.UserInfo().get(account)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    """装饰器 用于身份验证"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
