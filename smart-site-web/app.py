# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: __init__.py.py
# @date: 2020/12/13
from flask import Flask, request

from routes import auth, client


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.register_blueprint(auth.bp)  # 注册认证蓝图
    app.register_blueprint(client.bp)  # 注册博客蓝图

    # 关联端点名称 'index' 和 / URL
    # 这样 url_for('index') 或 url_for('blog.index') 都会有效
    # 会生成同样的 / URL
    app.add_url_rule("/", endpoint="index")

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=8000)
