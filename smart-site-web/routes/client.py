# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: client.py
# @date: 2020/12/16
from flask import Blueprint, request
import json
import db

bp = Blueprint("client", __name__, url_prefix="/client")
