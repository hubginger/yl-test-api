# coding=utf-8
"""
    通用登录
    当前实现:
        PC
        APP
"""
import hashlib

# @Time    :  2024-01-03 10:33:42
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  base_login
from enum import Enum

import requests


class Terminal(Enum):
    PC = 'pc'
    APP = 'app'
    MINI = 'mini'


class Login:

    @staticmethod
    def __md5(pwd, salt):
        md5 = hashlib.md5()
        pwd = pwd + salt
        md5.update(pwd.encode('utf-8'))
        return md5.hexdigest()

    @staticmethod
    def get_verify_info(terminal: str = 'pc_a'):
        """ 根据 terminal 标记来获取验证码 """
        verify_code_url = ''
        response = requests.get(url=verify_code_url).json()
        result = {'verifyCode': response['result']['verifyCode'], 'verifyId': response['result']['verifyId']}
        return result

    def __init__(self, flag='pc', account=None, password=None):
        """
            flag 仅可传 pc / app / mini
        """
        pass

    def __get_verify_code(self):
        pass
