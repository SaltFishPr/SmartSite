# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: contract.py
# @date: 2020/12/13
from flask import Blueprint, request
import json

import db
from utils import page_size_convert

bp = Blueprint("contract", __name__, url_prefix="/contract")


@bp.route("/getList", methods=("POST",))
def get_all_contracts():
    data = json.loads(request.form["data"])
    page, size, search_key = data["page"], data["size"], data["searchKey"]
    table = db.ContractInfo()
    contract_list = table.get_all()
    length = len(contract_list)
    start, end = page_size_convert(page, size, length)
    data = {
        "resultTotal": length,
        "resultList": contract_list[start:end],
    }
    return data


@bp.route("/create", methods=("POST",))
def create_employee():
    data = json.loads(request.form["data"])
    table = db.ContractInfo()
    if table.insert(
        data["contractDescription"],
        data["clientId"],
    ):
        return {"message": "创建成功", "flag": True}
    return {"message": "创建失败", "flag": False}


@bp.route("/delete", methods=("POST",))
def delete_employee():
    data = json.loads(request.form["data"])
    table = db.ContractInfo()
    if table.delete(data["contractId"]):
        return {"message": "删除成功", "flag": True}
    return {"message": "删除失败", "flag": False}


@bp.route("/update", methods=("POST",))
def update_employee():
    data = json.loads(request.form["data"])
    table = db.ContractInfo()
    if table.update(
        data["contractId"],
        data["contractContent"],
        data["creationDate"],
        data["clientId"],
    ):
        return {"message": "更新成功", "flag": True}
    return {"message": "更新失败", "flag": False}
