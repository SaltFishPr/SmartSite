# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: models.py
# @date: 2020/12/2
import redis
import json
from typing import List
from conf import database
from utils.db import id_to_key, key_to_id


class ClientContractInfo:
    """
    委托方合同信息表：委托方 ID、委托方描述等
    """

    def __init__(self):
        self.table_name = "ClientContractInfo"  # 表名
        self.r = redis.Redis(connection_pool=database.pool)

    def __del__(self):
        self.r.close()

    def insert(self, client_id: int, client_description: str) -> bool:
        """
        插入一个委托人信息
        :param client_id: 委托人ID
        :param client_description: 委托人描述
        :return: 成功返回True，否则返回False
        """
        data = [client_id, client_description]
        return self.r.setnx(id_to_key(self.table_name, client_id), json.dumps(data))

    def delete(self, client_id: int) -> int:
        """
        删除一个委托人信息
        :param client_id: 委托人ID
        :return: 成功删除的数量(成功删除为1，未成功为0)
        """
        return self.r.delete(id_to_key(self.table_name, client_id))

    def get(self, client_id: int) -> List:
        """
        获取key为client_id的委托人信息
        :param client_id: 委托人ID
        :return: [委托人描述]
        """
        return json.loads(self.r.get(id_to_key(self.table_name, client_id)))


class ProjectInfo:
    """
    项目信息表：项目 ID、委托方 ID、检查体系 ID、项目状态、项目风险值、项目创建时间、项目描述、项目负责人等
    """

    def __init__(self):
        self.table_name = "ProjectInfo"  # 表名
        self.r = redis.Redis(connection_pool=database.pool)

    def __del__(self):
        self.r.close()

    def insert(
        self,
        project_id: int,
        client_id: int,
        check_system_id: int,
        project_status,
        project_risk_value,
        project_creation_time,
        project_description,
        project_manager,
    ) -> bool:
        """
        插入项目信息
        :param project_id: 项目ID
        :param client_id: 委托方ID
        :param check_system_id: 检查体系 ID
        :param project_status: 项目状态
        :param project_risk_value: 项目风险值
        :param project_creation_time: 项目创建时间
        :param project_description: 项目描述
        :param project_manager: 项目负责人
        :return: 成功返回True，否则返回False
        """
        data = [
            project_id,
            client_id,
            check_system_id,
            project_status,
            project_risk_value,
            project_creation_time,
            project_description,
            project_manager,
        ]
        return self.r.setnx(id_to_key(self.table_name, project_id), json.dumps(data))

    def delete(self, project_id: int) -> int:
        """
        删除一个委托人信息
        :param project_id: 项目ID
        :return: 成功删除的数量(成功删除为1，未成功为0)
        """
        return self.r.delete(id_to_key(self.table_name, project_id))

    def get(self, project_id: int) -> List:
        """
        获取key为client_id的委托人信息
        :param project_id: 项目ID
        :return: [项目 ID, 委托方 ID, 检查体系 ID, 项目状态, 项目风险值, 项目创建时间, 项目描述, 项目负责人]
        """
        return json.loads(self.r.get(id_to_key(self.table_name, project_id)))


# 检查信息表：检查 ID、项目 ID、检查体系第一级 ID、第二级 ID、问题描述等
class CheckInfo:
    pass


# 检查体系表：当前结点 ID、前置结点 ID（第一级改字段为 0）等
class CheckSystem:
    pass


# 员工信息表：员工 ID、员工姓名等
class EmployeeInfo:
    pass


# 小组成员表：小组 ID、员工 ID、组长标志等
class GroupInfo:
    pass


if __name__ == "__main__":
    tmp = ProjectInfo()
    print(tmp.insert(1, 1, 1, "test", "test", "test", "test", "test"))
    # print(tmp.insert(1, "test"))
    print(tmp.get(1))
    print(tmp.delete(1))
    print(tmp.r.keys())
