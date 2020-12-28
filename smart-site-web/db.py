# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: db.py
# @date: 2020/12/2
import json
import os
import time
from typing import List

import redis

import config
from utils import id_to_key, key_to_id, random_id, random_employee_id

# decode_responses设置取出为字符串
pool = redis.ConnectionPool(
    host=config.redis_host,
    port=config.redis_port,
    decode_responses=True,
    password=config.redis_password,
)

print(os.getcwd())

checkfiles_path = os.path.join(os.getcwd(), "checkfiles")


if not os.path.exists(checkfiles_path):
    os.makedirs(checkfiles_path)


class UserInfo:
    """用户信息表：用户名，密码，用户身份"""

    def __init__(self):
        """初始化表信息"""
        self.__table_name = "UserInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, account: str) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, account)) == 1:
            return True
        return False

    def insert(self, account: str, password: str, identity: str) -> bool:
        """
        插入用户信息
        :param account: 用户名
        :param password: 密码
        :param identity: 用户身份
        :return: 成功返回 True，否则返回 False
        """
        data = [account, password, identity]
        return self.__r.setnx(id_to_key(self.__table_name, account), json.dumps(data))

    def update(self, account: str, password: str, identity: str) -> bool:
        """
        更新用户信息
        :param account: 用户名
        :param password: 密码
        :param identity: 用户身份
        :return: 成功返回 True，否则返回 False
        """
        data = [account, password, identity]
        if not self.is_exist(account):
            return False
        self.__r.set(id_to_key(self.__table_name, account), json.dumps(data))
        return True

    def delete(self, account: str) -> bool:
        """
        删除用户信息
        :param account: 用户名
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(id_to_key(self.__table_name, account)) == 1:
            return True
        return False

    def get(self, account: str) -> List:
        """
        获取用户信息
        :param account: 用户名
        :return: [用户名, 密码, 用户身份]
        """
        if not self.is_exist(account):
            return []
        return json.loads(self.__r.get(id_to_key(self.__table_name, account)))


class ClientInfo:
    """委托方信息表：委托方ID、委托方名称、委托方描述等"""

    def __init__(self):
        """初始化表信息"""
        self.__table_name = "ClientInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, client_id: str) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, client_id)) == 1:
            return True
        return False

    def insert(self, client_name: str, client_description: str) -> bool:
        """
        插入委托方信息
        :param client_name: 委托方名称
        :param client_description: 委托方描述
        :return: 成功返回 True，否则返回 False
        """
        client_id = random_id()  # 生成委托方ID
        while self.is_exist(client_id):
            client_id = random_id()

        data = [client_id, client_name, client_description]
        return self.__r.setnx(id_to_key(self.__table_name, client_id), json.dumps(data))

    def update(self, client_id: str, client_name: str, client_description: str) -> bool:
        """
        插入委托方信息
        :param client_id: 委托方ID
        :param client_name: 委托方名称
        :param client_description: 委托方描述
        :return: 成功返回 True，否则返回 False
        """
        data = [client_id, client_name, client_description]
        if not self.is_exist(client_id):
            return False
        self.__r.set(id_to_key(self.__table_name, client_id), json.dumps(data))
        return True

    def delete(self, client_id: str) -> bool:
        """
        删除委托方信息
        :param client_id: 委托方ID
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(id_to_key(self.__table_name, client_id)) == 1:
            return True
        return False

    def get(self, client_id: str) -> List:
        """
        获取委托方信息
        :param client_id: 委托方ID
        :return: [委托方ID, 委托方名称, 委托方描述]
        """
        if not self.is_exist(client_id):
            return []
        return json.loads(self.__r.get(id_to_key(self.__table_name, client_id)))

    def get_all(self):
        clients = self.__r.keys(pattern="ClientInfo:*")
        res = []
        for client in clients:
            data = self.get(key_to_id(client))
            res.append(
                {
                    "clientId": data[0],
                    "clientName": data[1],
                    "clientDescription": data[2],
                }
            )
        return res


class ProjectInfo:
    """项目信息表：项目ID、委托方ID、检查体系ID、项目状态、项目风险值、项目创建时间、项目描述、项目负责人等"""

    def __init__(self):
        """初始化表信息"""
        self.__table_name = "ProjectInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, project_id: str) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, project_id)) == 1:
            return True
        return False

    def insert(
        self,
        client_id: str,
        check_system_id: str,
        project_status: str,
        project_risk_value: int,
        project_description: str,
        project_manager: str,
        project_check_group_id: str,
    ) -> bool:
        """
        插入项目信息
        :param client_id: 委托方ID
        :param check_system_id: 检查体系 ID
        :param project_status: 项目状态
        :param project_risk_value: 项目风险值
        :param project_description: 项目描述
        :param project_manager: 项目负责人
        :param project_check_group_id: 检查小组ID
        :return: 成功返回 True，否则返回 False
        """
        project_id = random_id()  # 生成项目ID
        while self.is_exist(project_id):
            project_id = random_id()

        data = [
            project_id,
            client_id,
            check_system_id,
            project_status,
            project_risk_value,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  # 项目创建时间
            project_description,
            project_manager,
            project_check_group_id,
        ]
        return self.__r.setnx(
            id_to_key(self.__table_name, project_id), json.dumps(data)
        )

    def update(
        self,
        project_id,
        client_id,
        check_system_id,
        project_status,
        project_risk_value,
        creation_time,
        project_description,
        project_manager,
        project_check_group_id,
    ):
        """
        更新合同信息
        :param project_id: 项目ID
        :param client_id: 委托方ID
        :param check_system_id: 检查体系ID
        :param project_status: 项目状态
        :param project_risk_value: 项目风险值
        :param creation_time: 项目创建时间
        :param project_description: 项目描述
        :param project_manager: 项目管理人
        :param project_check_group_id: 检查小组ID
        :return: 成功返回 True，否则返回 False
        """
        data = [
            project_id,
            client_id,
            check_system_id,
            project_status,
            project_risk_value,
            creation_time,
            project_description,
            project_manager,
            project_check_group_id,
        ]
        if not self.is_exist(project_id):
            return False
        self.__r.set(id_to_key(self.__table_name, project_id), json.dumps(data))
        return True

    def delete(self, project_id: str) -> bool:
        """
        删除项目信息
        :param project_id: 项目ID
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(id_to_key(self.__table_name, project_id)) == 1:
            return True
        return False

    def get(self, project_id: str) -> List:
        """
        获取项目信息
        :param project_id: 项目ID
        :return: [项目 ID, 委托方 ID, 检查体系 ID, 项目状态, 项目风险值, 项目创建时间, 项目描述, 项目负责人]
        """
        if not self.is_exist(project_id):
            return []
        return json.loads(self.__r.get(id_to_key(self.__table_name, project_id)))

    def get_all(self):
        projects = self.__r.keys(pattern="ProjectInfo:*")
        res = []
        for project in projects:
            data = self.get(key_to_id(project))
            res.append(
                {
                    "projectId": data[0],
                    "clientId": data[1],
                    "projectCheckSystemId": data[2],
                    "projectStatus": data[3],
                    "projectRiskValue": data[4],
                    "projectCreationTime": data[5],
                    "projectDescription": data[6],
                    "projectManager": data[7],
                    "projectCheckGroupId": data[8],
                }
            )
        return res


class ContractInfo:
    """合同信息表：合同ID、合同内容、合同创建日期、委托方ID"""

    def __init__(self):
        """初始化表信息"""
        self.__table_name = "ContractInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, contract_id: str) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, contract_id)) == 1:
            return True
        return False

    def insert(
        self,
        contract_content: str,
        client_id: str,
    ) -> bool:
        """
        插入合同信息
        :param contract_content: 合同内容
        :param client_id: 委托方ID
        :return: 成功返回 True，否则返回 False
        """
        contract_id = random_id()  # 生成合同ID
        while self.is_exist(contract_id):
            contract_id = random_id()

        data = [
            contract_id,
            contract_content,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  # 合同创建日期
            client_id,
        ]
        return self.__r.setnx(
            id_to_key(self.__table_name, contract_id), json.dumps(data)
        )

    def update(
        self,
        contract_id: str,
        contract_content: str,
        contract_creation_date: str,
        client_id: str,
    ) -> bool:
        """
        更新合同信息
        :param contract_id: 合同ID
        :param contract_content: 合同内容
        :param contract_creation_date: 合同创建时间
        :param client_id: 委托方ID
        :return: 成功返回 True，否则返回 False
        """
        data = [contract_id, contract_content, contract_creation_date, client_id]
        if not self.is_exist(contract_id):
            return False
        self.__r.set(id_to_key(self.__table_name, contract_id), json.dumps(data))
        return True

    def delete(self, contract_id: str) -> bool:
        """
        删除合同信息
        :param contract_id: 合同ID
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(id_to_key(self.__table_name, contract_id)) == 1:
            return True
        return False

    def get(self, contract_id: str) -> List:
        """
        获取合同信息
        :param contract_id: 合同ID
        :return: [合同ID, 合同内容, 合同创建时间, 委托方ID]
        """
        if not self.is_exist(contract_id):
            return []
        return json.loads(self.__r.get(id_to_key(self.__table_name, contract_id)))

    def get_all(self) -> List:
        contracts = self.__r.keys(pattern="ContractInfo:*")
        res = []
        for contract in contracts:
            data = self.get(key_to_id(contract))
            res.append(
                {
                    "contractId": data[0],
                    "contractDescription": data[1],
                    "createTime": data[2],
                    "clientId": data[3],
                }
            )
        return res


class CheckInfo:
    """检查信息表：检查ID、项目ID、检查体系第一级ID、第二级ID、检查员员工ID、问题描述等"""

    def __init__(self):
        """初始化信息表"""
        self.__table_name = "CheckInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, check_id: str) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, check_id)) == 1:
            return True
        return False

    def insert(
        self,
        check_id: str,
        project_id: str,
        check_system_route: str,
        employee_id: str,
        problem_description: str,
        picture,
    ) -> bool:
        """
        插入一个检查信息
        :param check_id: 检查信息ID
        :param project_id: 项目ID
        :param check_system_route: 检查体系（例：安全检查->人员安全检查）
        :param employee_id: 检查员员工ID
        :param problem_description: 问题描述
        :param picture: 序列化后的图片
        :return: 成功返回 True，否则返回 False
        """

        data = [
            check_id,
            project_id,
            check_system_route,
            employee_id,
            problem_description,
        ]
        picture.save(f"{checkfiles_path}/{check_id}.jpg")
        return self.__r.set(id_to_key(self.__table_name, check_id), json.dumps(data))

    def delete(self, check_id: str) -> bool:
        """
        删除检查信息
        :param check_id: 检查信息ID
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(id_to_key(self.__table_name, check_id)) == 1:
            return True
        return False

    def get(self, check_id: str) -> List:
        """
        获取检查信息
        :param check_id: 检查信息ID
        :return: [检查信息ID, 项目ID, 检查体系, 用户ID, 问题描述]
        """
        if not self.is_exist(check_id):
            return []
        return json.loads(self.__r.get(id_to_key(self.__table_name, check_id)))

    def search(self, search_key):
        check_keys = self.__r.keys(pattern=f"CheckInfo:{search_key}*")
        res = []
        for check_key in check_keys:
            tmp = self.get(check_key)
            res.append(tmp)
        return res


class CheckSystemInfo:
    """检查体系表：当前结点ID、前置结点ID（第一级改字段为0）等"""

    def __init__(self):
        """初始化信息表"""
        self.__table_name = "CheckSystemInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, check_system_id: str) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, check_system_id)) == 1:
            return True
        return False

    def insert(
        self, system_id: str, system_name: str, pre_id: str, system_description: str
    ):
        """
        向检查体系树中插入一个节点
        :param system_id: 当前检查体系ID
        :param system_name: 当前检查体系名称
        :param pre_id: 前置检查体系ID
        :param system_description: 检查体系描述
        :return: 成功返回 True，否则返回 False
        """
        data = [system_id, system_name, pre_id, system_description]
        return self.__r.setnx(id_to_key(self.__table_name, system_id), json.dumps(data))

    def update(
        self,
        system_id: str,
        system_name: str,
        pre_id: str,
        system_description: str,
    ) -> bool:
        """
        更新合同信息
        :param system_id: 当前检查体系ID
        :param system_name: 当前检查体系名称
        :param pre_id: 前置检查体系ID
        :param system_description: 检查体系描述
        :return: 成功返回 True，否则返回 False
        """
        data = [system_id, system_name, pre_id, system_description]
        if not self.is_exist(system_id):
            return False
        self.__r.set(id_to_key(self.__table_name, system_id), json.dumps(data))
        return True

    def delete(self, system_id: str) -> bool:
        """
        删除检查信息
        :param system_id: 检查体系ID
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(id_to_key(self.__table_name, system_id)) == 1:
            return True
        return False

    def get(self, system_id: str) -> List:
        """
        获取一个检查体系信息
        :param system_id: 检查体系ID
        :return: [当前检查体系ID, 当前检查体系名称, 前置检查体系ID, 检查体系描述]
        """
        if not self.is_exist(system_id):
            return []
        return json.loads(self.__r.get(id_to_key(self.__table_name, system_id)))

    def get_all(self):
        check_system_keys = self.__r.keys(pattern="CheckSystemInfo:*")
        res = []
        table = CheckSystemInfo()
        for check_system_key in check_system_keys:
            tmp_data = table.get(key_to_id(check_system_key))
            res.append(
                {
                    "system_id": tmp_data[0],  # 当前检查体系ID
                    "system_name": tmp_data[1],  # 当前检查体系名称
                    "pre_id": tmp_data[2],  # 前置检查体系ID
                    "system_description": tmp_data[3],  # 检查体系描述
                }
            )
        return res

    def get_children(self, pre_id: str):
        res = []
        for d in self.get_all():
            if d["pre_id"] == pre_id:
                res.append(d)
        return res


class EmployeeInfo:
    """员工信息表：员工ID、员工姓名、员工年龄等"""

    def __init__(self):
        """初始化信息表"""
        self.__table_name = "EmployeeInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, employee_id: str) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, employee_id)) == 1:
            return True
        return False

    def insert(self, employee_name: str, employee_age: int) -> bool:
        """
        插入员工信息
        :param employee_name: 员工姓名
        :param employee_age: 员工年龄
        :return: 成功返回 True，否则返回 False
        """
        employee_id = random_employee_id()  # 生成员工信息ID
        while self.is_exist(employee_id):
            employee_id = random_employee_id()

        data = [employee_id, employee_name, employee_age]
        return self.__r.hsetnx(
            id_to_key(self.__table_name, employee_id), "data", json.dumps(data)
        ) and self.__r.hsetnx(
            id_to_key(self.__table_name, employee_id), "groups", json.dumps([])
        )

    def delete(self, employee_id: str) -> bool:
        """
        删除该员工信息
        :param employee_id: 员工ID
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(id_to_key(self.__table_name, employee_id)) == 1:
            return True
        return False

    def update_data(
        self, employee_id: str, employee_name: str, employee_age: int
    ) -> bool:
        """
        更新员工信息
        :param employee_id: 员工ID
        :param employee_name: 员工姓名
        :param employee_age: 员工年龄
        :return: 成功返回 True，否则返回 False
        """
        data = [employee_id, employee_name, employee_age]
        if not self.is_exist(employee_id):
            return False
        self.__r.hset(
            id_to_key(self.__table_name, employee_id), "data", json.dumps(data)
        )
        return True

    def get_data(self, employee_id: str) -> List:
        """
        获取员工信息
        :param employee_id: 员工ID
        :return: [员工ID, 员工姓名, 员工年龄]
        """
        if not self.is_exist(employee_id):
            return []
        data = self.__r.hget(id_to_key(self.__table_name, employee_id), "data")
        return json.loads(data)

    def update_groups(self, employee_id: str, groups: List) -> bool:
        """
        更新小组信息
        :param employee_id: 员工ID
        :param groups: 小组列表
        :return:
        """
        if not self.is_exist(employee_id):
            return False
        self.__r.hset(
            id_to_key(self.__table_name, employee_id), "groups", json.dumps(groups)
        )
        return True

    def get_groups(self, employee_id: str) -> List:
        """
        获取员工所在小组
        :param employee_id: 员工ID
        :return: 包含小组ID的列表
        """
        if not self.is_exist(employee_id):
            return []
        return json.loads(
            self.__r.hget(id_to_key(self.__table_name, employee_id), "groups")
        )

    def get_all(self) -> List:
        """
        获取所有员工信息
        :return: [{"employeeId": ,"employeeName": ,"employeeAge": ,"employeeGroups":[]}]
        """
        employee_keys = self.__r.keys(pattern="EmployeeInfo:*")
        res = []
        table = EmployeeInfo()
        for employee_key in employee_keys:
            tmp_data = table.get_data(key_to_id(employee_key))
            res.append(
                {
                    "employeeId": tmp_data[0],
                    "employeeName": tmp_data[1],
                    "employeeAge": tmp_data[2],
                    "employeeGroups": ",".join(
                        table.get_groups(key_to_id(employee_key))
                    ),
                }
            )
        return res


class GroupInfo:
    """小组成员表：小组ID、员工ID、组长标志等"""

    def __init__(self, group_id: int):
        """
        初始化小组信息
        :param group_id: 小组ID
        """
        self.__table_name = "GroupInfo"  # 表名
        self.__group_id = group_id
        self.__group_key = id_to_key(self.__table_name, group_id)
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self) -> bool:
        if self.__r.exists(self.__group_key) == 1:
            return True
        return False

    def delete_group(self) -> int:
        """
        删除小组
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(self.__group_key) == 1:
            return True
        return False

    def add_employee(self, employee_id: str, is_leader: bool) -> bool:
        """
        插入小组组员信息
        :param employee_id: 员工ID
        :param is_leader: 是否为组长
        :return: 成功返回 True，否则返回 False
        """
        data = {"is_leader": is_leader}
        # 如果是第一个员工加入则初始化leader_num为0
        self.__r.hsetnx(self.__group_key, "leader_num", 0)

        employee_info = EmployeeInfo()
        joined_groups = employee_info.get_groups(employee_id)

        if self.__r.hsetnx(self.__group_key, employee_id, json.dumps(data)):
            if is_leader:
                self.update_leader_num(1)
            joined_groups.append(self.__group_id)
            employee_info.update_groups(employee_id, joined_groups)
            return True
        return False

    def remove_employee(self, employee_id: str):
        """
        删除组内某一员工
        :param employee_id: 员工ID
        :return: 成功返回 True，否则返回 False
        """
        employee = self.get_employee(employee_id)

        employee_info = EmployeeInfo()
        joined_groups = employee_info.get_groups(employee_id)
        if self.__r.hdel(self.__group_key, employee_id):
            if employee["is_leader"]:
                self.update_leader_num(-1)
            joined_groups.remove(self.__group_id)
            employee_info.update_groups(employee_id, joined_groups)
            return True
        return False

    def get_employee(self, employee_id: str) -> dict:
        """
        获取该组一个员工的信息
        :param employee_id: 员工ID
        :return: {"is_leader": True/False}
        """
        if self.__r.hexists(self.__group_key, employee_id):
            return json.loads(self.__r.hget(self.__group_key, employee_id))
        return {}

    def get_all(self) -> List:
        """
        获取所有员工
        :return: 一个包含该组所有员工的员工ID的List
        """
        res = []
        data = self.__r.hgetall(self.__group_key)
        for k, v in data.items():
            if k == "leader_num":
                continue
            res.append([int(k), json.loads(v)["is_leader"]])
        return res

    def update_leader_num(self, a: int):
        """更新组长数量"""
        leader_num = int(self.__r.hget(self.__group_key, "leader_num"))
        leader_num += a
        self.__r.hset(self.__group_key, "leader_num", leader_num)

    def get_leader_num(self):
        """得到组长的数量"""
        return int(self.__r.hget(self.__group_key, "leader_num"))

    def get_group_dict(self):
        """
        获取改组内的数据字典列表
        :return: [{"groupID":int,"groupMember":list,"groupLeader":list}]
        """
        res = []
        group_member = []
        group_leader = []
        data = self.__r.hgetall(self.__group_key)
        for k, v in data.items():
            if k == "leader_num":
                continue
            if json.loads(v)["is_leader"]:
                group_leader.append(k)
            else:
                group_member.append(k)
        res.append(
            {
                "groupId": self.__group_id,
                "groupMember": "-".join(group_member),
                "groupLeader": "-".join(group_leader),
            }
        )
        return res


class VerificationInfo:
    def __init__(self):
        """初始化表信息"""
        self.__table_name = "VerificationInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, verification: str) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, verification)) == 1:
            return True
        return False

    def insert(self, verification) -> bool:
        return self.__r.set(
            id_to_key(self.__table_name, verification), verification, ex=86400, nx=True
        )

    def delete(self, verification: str) -> bool:
        if self.__r.delete(id_to_key(self.__table_name, verification)) == 1:
            return True
        return False


def get_all_groups():
    r = redis.Redis(connection_pool=pool)
    contracts = r.keys(pattern="GroupInfo:*")
    r.close()
    res = []
    for contract in contracts:
        group_id = int(key_to_id(contract))
        tmp = GroupInfo(group_id)
        group_member = []
        group_leader = []
        for tmp_group in tmp.get_all():
            if tmp_group[1] is True:
                group_leader.append(str(tmp_group[0]))
            else:
                group_member.append(str(tmp_group[0]))
        res.append(
            {
                "groupId": group_id,
                "groupMember": "-".join(group_member),
                "groupLeader": "-".join(group_leader),
            }
        )
    return res
