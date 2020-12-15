# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: contract.py
# @date: 2020/12/13
from flask import Blueprint, request
import json
import db

bp = Blueprint("contract", __name__, url_prefix="/contract")


@bp.route("/getList", methods="POST")
def get_client_contract():
    if request.method == "POST":
        data = json.loads(request.form["data"])
        page, size, search_key = data["page"], data["size"], data["searchKey"]
        contract_list = db.get_all_contracts()
        length = len(contract_list)
        start = (page - 1) * size
        end = page * size if page * size <= length else length
        data = {
            "resultTotal": length,
            "resultList": contract_list[start:end],
        }
        print(data)
        return data
