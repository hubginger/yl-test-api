# coding=utf-8
"""
    创建客户
    转合作客户
"""
import pytest


# @Time    :  2024-01-03 11:28:37
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  test_create_customer


class TestCRM:

    def test_create_customer(self, login):  # login 返回 3 条数据, 这个测试方法, 会执行 3 次
        # 0. 数据处理 , login 这个 fixture 中处理

        # 1. 发送请求

        # 2. 断言结果

        print()
        print(f'参数化的数据: {login}')

    def test_cooperation(self, login):
        print()
        print(f'参数化的数据: {login}')


if __name__ == '__main__':
    pytest.main([
        '-vs',
        'test_create_customer.py::TestCRM'
    ])
