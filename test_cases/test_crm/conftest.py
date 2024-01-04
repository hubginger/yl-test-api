# coding=utf-8
"""
    crm conftest
"""
import pytest
from common import BaseLogin


# @Time    :  2024-01-04 14:09:30
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  conftest

@pytest.fixture(scope='package')
def token():
    token = BaseLogin(host='c').simple_login('gingerqgyy', device='pc_c')
    yield token


@pytest.fixture(scope='function', params=[{'pageSize': '10'}, {'pageSize': '20'}], name='page')
def page(request):
    _data = request.param
    _data['pageNo'] = '1'
    _data['clientStatus'] = 'PROSPECTIVE_CUSTOMER'
    yield _data
