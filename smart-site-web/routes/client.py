# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: client.py
# @date: 2020/12/16
import json

from flask import Blueprint, request

import db
from utils import page_size_convert

bp = Blueprint("client", __name__, url_prefix="/client")


@bp.route("/getList", methods=("POST",))
def get_all_clients():
    data = json.loads(request.form["data"])
    page, size, search_key = data["page"], data["size"], data["searchKey"]
    table = db.ClientInfo()
    client_list = table.get_all()
    length = len(client_list)
    start, end = page_size_convert(page, size, length)
    data = {
        "resultTotal": length,
        "resultList": client_list[start:end],
    }
    return data


@bp.route("/create", methods=("POST",))
def create_client():
    data = json.loads(request.form["data"])
    table = db.ClientInfo()
    if table.insert(data["clientName"], data["clientDescription"]):
        return {"message": "创建成功", "flag": True}
    return {"message": "创建失败", "flag": False}


@bp.route("/delete", methods=("POST",))
def delete_client():
    data = json.loads(request.form["data"])
    table = db.ClientInfo()
    if table.delete(data["clientId"]):
        return {"message": "删除成功", "flag": True}
    return {"message": "删除失败", "flag": False}


@bp.route("/update", methods=("POST",))
def update_client():
    data = json.loads(request.form["data"])
    table = db.ClientInfo()
    if table.update(data["clientId"], data["clientName"], data["clientDescription"]):
        return {"message": "更新成功", "flag": True}
    return {"message": "更新失败", "flag": False}
