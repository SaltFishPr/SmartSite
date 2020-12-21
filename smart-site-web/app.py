# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: __init__.py.py
# @date: 2020/12/13
from flask import Flask
from flask_cors import *

from routes import auth, client, contract, employee, group, project, system, check


def create_app():
    """create and configure the app"""
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_mapping(SECRET_KEY="dev")

    app.register_blueprint(auth.bp)  # 注册认证蓝图
    app.register_blueprint(client.bp)  # 注册委托方蓝图
    app.register_blueprint(contract.bp)  # 注册合同蓝图
    app.register_blueprint(employee.bp)  # 注册员工蓝图
    app.register_blueprint(group.bp)  # 注册检查小组蓝图
    app.register_blueprint(project.bp)  # 注册项目蓝图
    app.register_blueprint(system.bp)  # 注册检查体系蓝图
    app.register_blueprint(check.bp)  # 注册接受检查信息蓝图

    @app.route("/")
    def index():
        return "index"

    app.add_url_rule("/", endpoint="index")

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=8000)
