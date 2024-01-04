# coding=utf-8
"""
    全局 conftest

        修改编码
        打印日志
        allure 报告 title

"""
import allure
import pytest

from common import yl_log, ExcelData


# @Time    :  2024-01-02 00:03:36
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  conftest


def pytest_collection_modifyitems(items):
    """ 编码转换 """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


# 用例执行前后分别打印分割日志 :
@pytest.fixture(scope='function', autouse=True)
def auto_log():
    """
    每条用例执行之前 , 先打印一行日志
        执行前 : *_*  *_*  *_*  *_*  *_*  *_*  *_*
        执行完 : *¯*  *¯*  *¯*  *¯*  *¯*  *¯*  *¯*
    分割每条用例的日志, 方便查看
    """
    yl_log.info("*_*  " * 20)
    yield
    yl_log.info("*¯*  " * 20)


# """
# 详细日志打印 :
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    out = yield
    res = out.get_result()
    if res.when == "call":
        yl_log.info(f"用例位置 : {res.nodeid}")
        if hasattr(item, 'callspec'):
            case_obj = tuple(item.callspec.params.values())[0]
            if hasattr(case_obj, 'title'):
                allure.dynamic.title(case_obj.case_id + case_obj.title)
            if isinstance(case_obj, ExcelData):
                yl_log.info(f"数据位置 : Sheet: < {case_obj.sheet_name} > RowNumber: < {case_obj.row} >")
                yl_log.info(f"请求地址 : {case_obj.url}")
                yl_log.info(f"请求方法 : {case_obj.method}")
                yl_log.info(f"请求参数 : {case_obj.data}")
        yl_log.info(f"测试结果 : {res.outcome}")
        yl_log.info(f"异常信息 : {call.excinfo}")
        yl_log.info(f"用例耗时 : {res.duration}")
# """
