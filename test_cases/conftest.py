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


def pytest_collection_modifyitems(items):
    """ 编码转换 """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        if hasattr(item, 'callspec'):
            str(item.callspec.params.get('case_data')).encode("utf-8").decode("unicode_escape")


# 自动日志打印 :
# """
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    out = yield
    # yl_log.info(" *_* " * 20)
    res = out.get_result()
    if res.when == "call":
        yl_log.info(f"用例位置 : {res.nodeid}")
        if hasattr(item, 'callspec'):
            case_obj = tuple(item.callspec.params.values())[0]
            yl_log.info(f"数据位置 : Sheet: <{case_obj.sheet_name}> 第 row: <{case_obj.row}> 行")
            yl_log.info(f"请求地址 : {case_obj.url}")
            yl_log.info(f"请求方法 : {case_obj.method}")
            yl_log.info(f"请求参数 : {case_obj.data}")
        yl_log.info(f"测试结果 : {res.outcome}")
        yl_log.info(f"异常信息 : {call.excinfo}")
        yl_log.info(f"用例耗时 : {res.duration}")
        yl_log.info(" *¯* " * 20)
# """
