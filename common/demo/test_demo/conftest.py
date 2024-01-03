# coding=utf-8
"""
    收集用例
    输出信息
"""


# @Time    :  2024-01-03 09:52:36
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  conftest.py

def pytest_collection_modifyitems(session, items):
    pass
    # print(items)
    # print(type(items))
    # for item in items:
    #     print(item)
    #     print(item.nodeid)
    #     print(type(item))


def pytest_runtest_call(item):
    print(item)
    print(type(item))
