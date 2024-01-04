# coding=utf-8
"""
    crm conftest
"""
import pytest
from common import BaseLogin, do_conf


# @Time    :  2024-01-04 14:09:30
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  conftest

@pytest.fixture(scope='package')
def token():
    uri = do_conf.read_one('login')
    BaseLogin().login()
    yield
