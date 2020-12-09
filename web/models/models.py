# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: models.py
# @date: 2020/12/2
import redis
import json
from typing import List
from conf import database
from utils.db import id_to_key


class ClientContractInfo:
    """
    委托方合同信息表：委托方ID、委托方描述等
    """

    def __init__(self, client_id):
        """
        初始化该委托方
        :param client_id: 委托方ID
        """
        self.table_name = "ClientContractInfo"  # 表名
        self.client_id = client_id
        self.client_key = id_to_key(self.table_name, client_id)
        self.r = redis.Redis(connection_pool=database.pool)

    def __del__(self):
        self.r.close()

    def is_exist(self) -> bool:
        if self.r.exists(self.client_key) == 1:
            return True
        return False

    def insert(self, client_description: str) -> bool:
        """
        插入该委托人信息
        :param client_description: 委托人描述
        :return: 成功插入返回True，否则返回False
        """
        data = [self.client_id, client_description]
        return self.r.setnx(self.client_key, json.dumps(data))

    def delete(self) -> bool:
        """
        删除该委托人信息
        :return: 成功删除返回True，否则返回False
        """
        if self.r.delete(self.client_key) == 1:
            return True
        return False

    def get(self) -> List:
        """
        获取该委托人信息
        :return: [委托方ID, 委托人描述]
        """
        if not self.is_exist():
            return []
        return json.loads(self.r.get(self.client_key))


class ProjectInfo:
    """
    项目信息表：项目ID、委托方ID、检查体系ID、项目状态、项目风险值、项目创建时间、项目描述、项目负责人等
    """

    def __init__(self, project_id):
        """
        初始化该项目信息
        :param project_id: 项目ID
        """
        self.table_name = "ProjectInfo"  # 表名
        self.project_id = project_id
        self.project_key = id_to_key(self.table_name, project_id)
        self.r = redis.Redis(connection_pool=database.pool)

    def __del__(self):
        self.r.close()

    def is_exist(self) -> bool:
        if self.r.exists(self.project_key) == 1:
            return True
        return False

    def insert(
        self,
        client_id: int,
        check_system_id: int,
        project_status,
        project_risk_value,
        project_creation_time,
        project_description,
        project_manager,
    ) -> bool:
        """
        插入该项目信息
        :param client_id: 委托方ID
        :param check_system_id: 检查体系 ID
        :param project_status: 项目状态
        :param project_risk_value: 项目风险值
        :param project_creation_time: 项目创建时间
        :param project_description: 项目描述
        :param project_manager: 项目负责人
        :return: 成功插入返回 True，否则返回 False
        """
        data = [
            self.project_id,
            client_id,
            check_system_id,
            project_status,
            project_risk_value,
            project_creation_time,
            project_description,
            project_manager,
        ]
        return self.r.setnx(self.project_key, json.dumps(data))

    def delete(self) -> bool:
        """
        删除该委托人信息
        :return: 成功删除返回True，否则返回False
        """
        if self.r.delete(self.project_key) == 1:
            return True
        return False

    def get(self) -> List:
        """
        获取该委托人信息
        :return: [项目 ID, 委托方 ID, 检查体系 ID, 项目状态, 项目风险值, 项目创建时间, 项目描述, 项目负责人]
        """
        if not self.is_exist():
            return []
        return json.loads(self.r.get(self.project_key))


class CheckInfo:
    """
    检查信息表：检查ID、项目ID、检查体系第一级ID、第二级ID、检查员员工ID、问题描述等
    """

    def __init__(self, check_id):
        """
        初始化该检查条目
        :param check_id: 检查条目ID
        """
        self.table_name = "CheckInfo"  # 表名
        self.check_id = check_id
        self.check_key = id_to_key(self.table_name, check_id)
        self.r = redis.Redis(connection_pool=database.pool)

    def __del__(self):
        self.r.close()

    def is_exist(self) -> bool:
        if self.r.exists(self.check_key) == 1:
            return True
        return False

    def insert(
        self,
        project_id: int,
        check_system_lv_1: int,
        check_system_lv_2: int,
        employee_id: int,
        problem_description: str,
    ) -> bool:
        """
        插入一个检查条目
        :param project_id: 项目ID
        :param check_system_lv_1: 检查体系第一级ID
        :param check_system_lv_2: 检查体系第二级ID
        :param employee_id: 检查员员工ID
        :param problem_description: 问题描述
        :return: 成功返回 True，否则返回 False
        """
        data = [
            self.check_id,
            project_id,
            check_system_lv_1,
            check_system_lv_2,
            employee_id,
            problem_description,
        ]
        return self.r.setnx(self.check_key, json.dumps(data))

    def delete(self) -> int:
        """
        删除该检查信息
        :return: 成功返回 True，否则返回 False
        """
        if self.r.delete(self.check_key) == 1:
            return True
        return False

    def get(self) -> List:
        """
        获取该检查信息
        :return: [检查ID, 项目ID, 检查体系第一级ID, 第二级ID, 问题描述]
        """
        if not self.is_exist():
            return []
        return json.loads(self.r.get(self.check_key))


class CheckSystemInfo:
    """
    检查体系表：当前结点ID、前置结点ID（第一级改字段为0）等
    """

    def __init__(self, check_system_id):
        self.table_name = "CheckSystemInfo"  # 表名
        self.check_system_id = check_system_id
        self.check_system_key = id_to_key(self.table_name, check_system_id)
        self.r = redis.Redis(connection_pool=database.pool)

    def __del__(self):
        self.r.close()

    def is_exist(self) -> bool:
        if self.r.exists(self.check_system_key) == 1:
            return True
        return False

    def insert(self, front_id, check_system_describe):
        """
        插入该检查体系信息
        :param front_id: 前置检查体系ID
        :param check_system_describe: 检查体系描述
        :return:
        """
        data = [self.check_system_id, front_id, check_system_describe]
        return self.r.setnx(self.check_system_key, json.dumps(data))

    def delete(self):
        """
        删除该检查体系信息
        :return: 成功返回 True，否则返回 False
        """
        if self.r.delete(self.check_system_key) == 1:
            return True
        return False

    def get(self):
        """
        得到该检查体系信息
        :return: [当前结点ID, 前置结点ID, 节点描述]
        """
        if not self.is_exist():
            return []
        return json.loads(self.r.get(self.check_system_key))


class EmployeeInfo:
    """
    员工信息表：员工ID、员工姓名、员工年龄等
    """

    def __init__(self, employee_id):
        """
        初始化该员工信息
        :param employee_id: 员工ID
        """
        self.table_name = "EmployeeInfo"  # 表名
        self.employee_id = employee_id
        self.employee_key = id_to_key(self.table_name, employee_id)
        self.r = redis.Redis(connection_pool=database.pool)

    def __del__(self):
        self.r.close()

    def is_exist(self) -> bool:
        if self.r.exists(self.employee_key) == 1:
            return True
        return False

    def insert(self, employee_name: str, employee_age: int) -> bool:
        """
        插入该员工信息
        :param employee_name: 员工姓名
        :param employee_age: 员工年龄
        :return: 成功返回 True，否则返回 False
        """
        data = [self.employee_id, employee_name, employee_age]
        return self.r.hsetnx(
            self.employee_key, "data", json.dumps(data)
        ) and self.r.hsetnx(self.employee_key, "groups", json.dumps([]))

    def delete(self) -> bool:
        """
        删除该员工信息
        :return: 成功返回 True，否则返回 False
        """
        if self.r.delete(self.employee_key) == 1:
            return True
        return False

    def update(self) -> bool:
        pass

    def get_data(self) -> List:
        """
        获取该员工信息
        :return: [员工ID, 员工姓名, 员工年龄]
        """
        if not self.is_exist():
            return []
        data = self.r.hget(self.employee_key, "data")
        return json.loads(data)

    def get_groups(self) -> List:
        """
        获取该员工所在小组
        :return: 包含小组ID的列表
        """
        if not self.is_exist():
            return []
        return json.loads(self.r.hget(self.employee_key, "groups"))

    def join_group(self, group_id: int) -> bool:
        """
        员工加入小组
        :param group_id: 小组ID
        :return: 是否加入成功
        """
        if not self.is_exist():
            return False
        groups = self.get_groups()
        if group_id in groups:
            return False
        groups.append(group_id)
        self.r.hset(self.employee_key, "groups", json.dumps(groups))
        return True

    def leave_group(self, group_id: int) -> bool:
        """
        员工退出小组
        :param group_id: 小组ID
        :return: 是否退出成功
        """
        if not self.is_exist():
            return False
        groups = self.get_groups()
        if group_id in groups:
            groups.remove(group_id)
            return True
        return False


class GroupInfo:
    """
    小组成员表：小组ID、员工ID、组长标志等
    """

    def __init__(self, group_id):
        """
        初始化小组信息
        :param group_id: 小组ID
        """
        self.table_name = "GroupInfo"  # 表名
        self.group_id = group_id
        self.group_key = id_to_key(self.table_name, group_id)
        self.r = redis.Redis(connection_pool=database.pool)

    def __del__(self):
        self.r.close()

    def is_exist(self) -> bool:
        if self.r.exists(self.group_key) == 1:
            return True
        return False

    def delete_group(self) -> int:
        """
        删除小组
        :return: 成功返回 True，否则返回 False
        """
        if self.r.delete(self.group_key) == 1:
            return True
        return False

    def add_employee(self, employee_id: int, is_leader: bool) -> bool:
        """
        插入小组组员信息
        :param employee_id: 员工ID
        :param is_leader: 是否为组长
        :return: 成功插入信息返回True，否则返回False
        """
        data = {"is_leader": is_leader}
        # 如果是第一个员工加入则初始化leader_num为0
        self.r.hsetnx(self.group_key, "leader_num", 0)

        if is_leader:
            self.update_leader_num(1)

        employee_info = EmployeeInfo(employee_id)
        if employee_info.join_group(self.group_id) and self.r.hsetnx(
            self.group_key, employee_id, json.dumps(data)
        ):
            return True
        else:
            employee_info.leave_group(self.group_id)
            return False

    def remove_employee(self, employee_id):
        """
        删除组内某一员工
        :param employee_id: 员工ID
        :return: 删除成功返回True
        """
        employee = self.get_employee(employee_id)

        if employee["is_leader"]:
            self.update_leader_num(-1)

        employee_info = EmployeeInfo(employee_id)
        if employee_info.leave_group(self.group_id) and self.r.hdel(
            self.group_key, employee_id
        ):
            return True
        else:
            employee_info.join_group(self.group_id)
            return False

    def get_employee(self, employee_id) -> dict:
        """
        获取该组一个员工的信息
        :param employee_id: 员工ID
        :return: {"is_leader": True/False}
        """
        return json.loads(self.r.hget(self.group_key, employee_id))

    def get_all(self) -> List:
        """
        获取所有员工
        :return: 一个包含该组所有员工的员工ID的List
        """
        res = []
        data = self.r.hgetall(self.group_key)
        for k, v in data.items():
            res.append([int(k), json.loads(v)["is_leader"]])
        return res

    def update_leader_num(self, a):
        """
        更新组长数量
        :param a:
        :return:
        """
        leader_num = int(self.r.hget(self.group_key, "leader_num"))
        leader_num += a
        self.r.hset(self.group_key, "leader_num", leader_num)


if __name__ == "__main__":
    tmp = EmployeeInfo(1)
    # print(tmp.get_data())
    # print(tmp.insert("wws", 18))
    # print(tmp.get_data())
    # print(tmp.get_groups())
    # print(tmp.join_group(1))
    # print(tmp.get_groups())
    # print(tmp.delete())
    print(tmp.r.keys())
    # print(tmp.is_exist())
