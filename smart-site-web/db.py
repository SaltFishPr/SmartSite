# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: db.py
# @date: 2020/12/2
import json
import redis
from typing import List

import config
from utils import id_to_key, key_to_id, random_id, random_employee_id

# decode_responses设置取出为字符串
pool = redis.ConnectionPool(
    host=config.redis_host,
    port=config.redis_port,
    decode_responses=True,
    password=config.redis_password,
)


class UserInfo:
    """用户信息表：用户名，密码，用户身份"""

    def __init__(self):
        """初始化表信息"""
        self.__table_name = "ClientContractInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, administrator_username) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, administrator_username)) == 1:
            return True
        return False

    def insert(self, administrator_username, password: str, identity: str) -> bool:
        """
        插入管理员信息
        :param administrator_username: 用户名
        :param password: 密码
        :param identity: 用户身份
        :return: 成功插入返回True，否则返回False
        """
        data = [administrator_username, password, identity]
        return self.__r.setnx(
            id_to_key(self.__table_name, administrator_username), json.dumps(data)
        )

    def delete(self, administrator_username) -> bool:
        """
        删除用户信息
        :param administrator_username: 用户名
        :return: 成功删除返回True，否则返回False
        """
        if self.__r.delete(id_to_key(self.__table_name, administrator_username)) == 1:
            return True
        return False

    def get(self, administrator_username) -> List:
        """
        获取用户信息
        :param administrator_username: 用户名
        :return: [用户名, 密码, 用户身份]
        """
        if not self.is_exist(administrator_username):
            return []
        return json.loads(
            self.__r.get(id_to_key(self.__table_name, administrator_username))
        )


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

    def insert(self, client_name, client_description: str) -> bool:
        """
        插入委托方信息
        :param client_name: 委托方名称
        :param client_description: 委托方描述
        :return: 成功插入返回True，否则返回False
        """
        client_id = random_id()  # 生成委托方ID
        while self.is_exist(client_id):
            client_id = random_id()

        data = [client_id, client_name, client_description]
        return self.__r.setnx(id_to_key(self.__table_name, client_id), json.dumps(data))

    def update(self, client_id, client_name, client_description) -> bool:
        """
        插入委托方信息
        :param client_id: 委托方ID
        :param client_name: 委托方名称
        :param client_description: 委托方描述
        :return: 成功插入返回True，否则返回False
        """
        data = [client_id, client_name, client_description]
        if not self.is_exist(client_id):
            return False
        self.__r.set(id_to_key(self.__table_name, client_id), json.dumps(data))
        return True

    def delete(self, client_id) -> bool:
        """
        删除委托方信息
        :param client_id: 委托方ID
        :return: 成功删除返回True，否则返回False
        """
        if self.__r.delete(id_to_key(self.__table_name, client_id)) == 1:
            return True
        return False

    def get(self, client_id) -> List:
        """
        获取委托方信息
        :param client_id: 委托方ID
        :return: [委托方ID, 委托方名称, 委托方描述]
        """
        if not self.is_exist(client_id):
            return []
        return json.loads(self.__r.get(id_to_key(self.__table_name, client_id)))


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
        client_id,
        check_system_id,
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
        project_id = random_id()  # 生成项目ID
        while self.is_exist(project_id):
            project_id = random_id()

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
        return self.__r.setnx(
            id_to_key(self.__table_name, project_id), json.dumps(data)
        )

    def delete(self, project_id) -> bool:
        """
        删除项目信息
        :param project_id: 项目ID
        :return: 成功删除返回True，否则返回False
        """
        if self.__r.delete(id_to_key(self.__table_name, project_id)) == 1:
            return True
        return False

    def get(self, project_id) -> List:
        """
        获取项目信息
        :param project_id: 项目ID
        :return: [项目 ID, 委托方 ID, 检查体系 ID, 项目状态, 项目风险值, 项目创建时间, 项目描述, 项目负责人]
        """
        if not self.is_exist(project_id):
            return []
        return json.loads(self.__r.get(id_to_key(self.__table_name, project_id)))


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
        contract_creation_date: str,
        client_id: int,
    ) -> bool:
        """
        插入合同信息
        :param contract_content: 合同内容
        :param contract_creation_date: 合同创建日期
        :param client_id: 委托方ID
        :return: 成功插入返回True，否则返回False
        """
        contract_id = random_id()  # 生成合同ID
        while self.is_exist(contract_id):
            contract_id = random_id()

        data = [contract_id, contract_content, contract_creation_date, client_id]
        return self.__r.setnx(
            id_to_key(self.__table_name, contract_id), json.dumps(data)
        )

    def update(
        self,
        contract_id: str,
        contract_content: str,
        contract_creation_date: str,
        client_id: int,
    ) -> bool:
        """
        更新合同信息
        :param contract_id: 合同ID
        :param contract_content: 合同内容
        :param contract_creation_date: 合同创建时间
        :param client_id: 委托方ID
        :return: 成功插入返回True，否则返回False
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
        :return: 成功删除返回True，否则返回False
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

    def get_all(self):
        contracts = self.__r.keys(pattern="ClientContractInfo:*")
        res = []
        for contract in contracts:
            res.append(self.get(key_to_id(contract)))
        return res


class CheckInfo:
    """检查信息表：检查ID、项目ID、检查体系第一级ID、第二级ID、检查员员工ID、问题描述等"""

    def __init__(self):
        """初始化信息表"""
        self.__table_name = "CheckInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, check_id) -> bool:
        if self.__r.exists(id_to_key(self.__table_name, check_id)) == 1:
            return True
        return False

    def insert(
        self,
        project_id: int,
        check_system_route: str,
        employee_id: int,
        problem_description: str,
    ) -> bool:
        """
        插入一个检查信息
        :param project_id: 项目ID
        :param check_system_route: 检查体系（例：安全检查->人员安全检查）
        :param employee_id: 检查员员工ID
        :param problem_description: 问题描述
        :return: 成功返回 True，否则返回 False
        """
        check_id = random_id()  # 生成检查信息ID
        while self.is_exist(check_id):
            check_id = random_id()

        data = [
            check_id,
            project_id,
            check_system_route,
            employee_id,
            problem_description,
        ]
        return self.__r.setnx(id_to_key(self.__table_name, check_id), json.dumps(data))

    def delete(self, check_id) -> int:
        """
        删除检查信息
        :param check_id: 检查信息ID
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(id_to_key(self.__table_name, check_id)) == 1:
            return True
        return False

    def get(self, check_id) -> List:
        """
        获取检查信息
        :param check_id: 检查信息ID
        :return: [检查ID, 项目ID, 检查体系, 问题描述]
        """
        if not self.is_exist(check_id):
            return []
        return json.loads(self.__r.get(id_to_key(self.__table_name, check_id)))


class CheckSystemInfo:
    """检查体系表：当前结点ID、前置结点ID（第一级改字段为0）等"""

    def __init__(self, check_system_id):
        self.__table_name = "CheckSystemInfo"  # 表名
        self.__check_system_id = check_system_id
        self.__check_system_key = id_to_key(self.__table_name, check_system_id)
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self) -> bool:
        if self.__r.exists(self.__check_system_key) == 1:
            return True
        return False

    def insert(self, front_id, check_system_describe):
        """
        插入该检查体系信息
        :param front_id: 前置检查体系ID
        :param check_system_describe: 检查体系描述
        :return:
        """
        data = [self.__check_system_id, front_id, check_system_describe]
        return self.__r.setnx(self.__check_system_key, json.dumps(data))

    def delete(self):
        """
        删除该检查体系信息
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(self.__check_system_key) == 1:
            return True
        return False

    def get(self):
        """
        得到该检查体系信息
        :return: [当前结点ID, 前置结点ID, 节点描述]
        """
        if not self.is_exist():
            return []
        return json.loads(self.__r.get(self.__check_system_key))


class EmployeeInfo:
    """员工信息表：员工ID、员工姓名、员工年龄等"""

    def __init__(self):
        """初始化信息表"""
        self.__table_name = "EmployeeInfo"  # 表名
        self.__r = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.__r.close()

    def is_exist(self, employee_id) -> bool:
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

    def delete(self, employee_id) -> bool:
        """
        删除该员工信息
        :param employee_id: 员工ID
        :return: 成功返回 True，否则返回 False
        """
        if self.__r.delete(id_to_key(self.__table_name, employee_id)) == 1:
            return True
        return False

    def update_data(self, employee_id, employee_name, employee_age) -> bool:
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

    def get_data(self, employee_id) -> List:
        """
        获取员工信息
        :param employee_id: 员工ID
        :return: [员工ID, 员工姓名, 员工年龄]
        """
        if not self.is_exist(employee_id):
            return []
        data = self.__r.hget(id_to_key(self.__table_name, employee_id), "data")
        return json.loads(data)

    def update_groups(self, employee_id, groups: List):
        """
        更新小组信息
        :param employee_id: 员工ID
        :param groups: 小组列表
        :return:
        """
        self.__r.hset(
            id_to_key(self.__table_name, employee_id), "groups", json.dumps(groups)
        )

    def get_groups(self, employee_id) -> List:
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

    def get_all(self):
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

    def __init__(self, group_id):
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

    def add_employee(self, employee_id: int, is_leader: bool) -> bool:
        """
        插入小组组员信息
        :param employee_id: 员工ID
        :param is_leader: 是否为组长
        :return: 成功插入信息返回True，否则返回False
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

    def remove_employee(self, employee_id):
        """
        删除组内某一员工
        :param employee_id: 员工ID
        :return: 删除成功返回True
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

    def get_employee(self, employee_id) -> dict:
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

    def update_leader_num(self, a):
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


def get_all_group():
    r = redis.Redis(connection_pool=pool)
    contracts = r.keys(pattern="GroupInfo:*")
    r.close()
    res = []
    for contract in contracts:
        group_id = key_to_id(contract)
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
