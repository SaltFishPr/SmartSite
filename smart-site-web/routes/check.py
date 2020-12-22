# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: check.py
# @date: 2020/12/21

import json

from flask import Blueprint, request

import db, utils
from utils import page_size_convert

bp = Blueprint("check", __name__, url_prefix="/check")


@bp.route("/getPic", methods=("POST",))
def get_pic():
    data = request.files["Image"]
    data.save('C:/Users/QiQi/Pictures/Saved Pictures/demo.jpg')
    print(data)
    return '图片测试'


@bp.route("/getText", methods=("POST",))
def get_text():
    problem_description = request.form["problem_description"]
    project_id = request.form["project_id"]
    employee_id = request.form["employee_id"]
    check_system_route = request.form["check_system_route"]
    print(project_id,employee_id,problem_description,check_system_route)
    return '文本测试'


if __name__ == '__main__':
    from PIL import Image
    img = Image.open(utils.str_to_pic(utils.pic_to_str('C:/Users/QiQi/Pictures/Saved Pictures/demo.jpg')))
    img.show()


