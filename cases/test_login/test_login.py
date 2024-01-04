# coding=utf-8
"""
    创建客户
    转合作客户
"""
import pytest
from common import BaseApi, ExcelData, BaseAssert, yl_log


# @Time    :  2024-01-03 11:28:37
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  test_create_customer


class TestLogin:

    def test_login(self, login: ExcelData):  # login 返回 3 条数据, 这个测试方法, 会执行 3 次
        # 0. 处理数据
        # 放在参数化中进行处理就好了

        # 1. 发送请求
        res = BaseApi().send(login.url, login.method, json=login.data)
        yl_log.debug(f'预期结果: {login.expected_response}')
        yl_log.debug(f'响应结果: {res}')

        # 2. 断言结果
        BaseAssert.assert_common(login.expected_response, res, 'message')


if __name__ == '__main__':
    pytest.main([
        'test_login.py::TestLogin'
    ])
