# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: contract.py
# @date: 2020/12/13
from flask import Blueprint, request

bp = Blueprint("contract", __name__)


@bp.route("/")
def index():
    return "index"


@bp.route("/getList")
def get_client_contract():
    if request.method == "POST":
        data = request.form["data"]
        # data = request.values.get("data")
        print(data)
    return "123"
