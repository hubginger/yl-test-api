# coding=utf-8
"""
    conftest 文件
    前后置
    参数化
"""
import pytest

from common import yl_log, all_data, ExcelData, get_verify_info, md5


# @Time    :  2024-01-03 12:25:59
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  conftest.py

@pytest.fixture(scope='function', params=all_data.get('登录模块', 'Login'), name='login')
def login(request):
    """
        参数化 fixture
        test_case 应用时, 只需要接参数即可
        先将数据初始化完毕, 然后再 yield 返回
    """
    datas: ExcelData = request.param
    yl_log.debug(f'参数化读取到数据: {datas}')
    datas.data.update(get_verify_info())
    datas.data['password'] = md5(datas.data['password'])
    yield datas


"""
    fixture 参数化
        1. fixture 会很庞大
        2. 不方便调试, 没法直接调试 fixture, 可以参数化之后, 调试用例, 也就达到了调试 fixture 的目的     
        3. 多人协作, 共同编辑 conftest, 合并代码容易有冲突
    没有 libs 了, 全放 conftest 中 , 每条用例对应一个参数化的 fixture.
"""
