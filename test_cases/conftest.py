# coding=utf-8
"""
    全局 conftest

        修改编码
        打印日志
        读取 Excel 全部数据, 如果是多个 Excel, 则可在这里将多个 Excel 数据进行合并

    file_name = Delivery_System_V1.5.xlsx
"""

# @Time    :  2024-01-02 00:03:36
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  conftest

import pytest

from common import yl_log
from common import all_data


def pytest_collection_modifyitems(items):
    """ 编码转换 """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        if hasattr(item, 'callspec'):
            str(item.callspec.params.get('case_data')).encode("utf-8").decode("unicode_escape")


# 自动日志打印:
# """
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # 自动日志打印
    # res = out.get_result()
    # case_data = item.callspec.params.get('case_data')

    k_v = item.callspec.params
    print('||' * 30)
    print(list(k_v.values())[0].case_id)
    print('||' * 30)

    out = yield
    res = out.get_result()
    if res.when == "call":
        yl_log.info(f"用例ID : {res.nodeid}")

        # 用例信息打印 :
        '''
        if hasattr(item, 'callspec'):
            case_data = item.callspec.params.get('case_data')
            sheet_name = case_data.get('sheet_name')
            row = case_data['id']
            url = case_data.get('url')
            method = case_data.get('method')
            _data = case_data.get('data')
            data = _data.encode("utf-8").decode("unicode_escape") if isinstance(_data, str) else _data

            yl_log.info(f"用例位置 : {sheet_name} 第 {row} 行")
            yl_log.info(f"请求地址 : {url}")
            yl_log.info(f"请求方法 : {method}")
            yl_log.info(f"请求参数 : {data}")
        # '''

        yl_log.info(f"测试结果 : {res.outcome}")
        yl_log.info(f"故障表示 : {res.longrepr}")
        yl_log.info(f"异常 : {call.excinfo}")
        yl_log.info(f"用例耗时 : {res.duration}")
        yl_log.info("**" * 20)
# """
