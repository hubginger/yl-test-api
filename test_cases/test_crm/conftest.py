# coding=utf-8
"""

"""
import pytest

from common import yl_log, all_data


# @Time    :  2024-01-03 12:25:59
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  conftest.py


@pytest.fixture(scope='session')
def _all():
    print()
    yl_log.info('----执行开始----')
    yield all_data
    yl_log.info('----执行完毕----')
    print()


@pytest.fixture(scope='function', params=all_data.get('登录模块', 'Login'), name='login')
# @pytest.fixture(scope='function', **all_data.fetch('登录模块', 'Login'), name='login')
def login(request, _all):
    datas = request.param
    yield datas


"""
    fixture 参数化
        1. fixture 会很庞大
        2. 不方便调试, 没法直接调试 fixture, 可以参数化之后, 调试用例, 也就达到了调试 fixture 的目的     
        3. 多人协作, 共同编辑 conftest, 合并代码容易有冲突
    没有 libs 了, 全放 conftest 中 , 每条用例对应一个参数化的 fixture.
"""
