# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: redis_test.py
# @date: 2020/12/15
import db


if __name__ == "__main__":
    e1 = db.EmployeeInfo(1)
    e2 = db.EmployeeInfo(2)
    e3 = db.EmployeeInfo(3)
    e1.insert("e1", 25)
    e2.insert("e1", 22)
    e3.insert("e1", 21)

    print(db.get_all_employees())
