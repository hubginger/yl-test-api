# coding=utf-8
"""
    pytest 启动文件
    默认运行 test_case 下的所有用例

    Pytest 默认执行顺序:
        模块层面, 以 ASCII 码排序并加载,
        函数和方法层面, 以定义的先后顺序加载
"""

# @Time    :  2023-12-29 15:34:45
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  run


import os
import pytest
from common import ALLURE_REPORT_FOLDER, ALLURE_RESULT_FOLDER

if __name__ == '__main__':
    # main :
    # """
    pytest.main(['-s',
                 './test_cases',
                 '--alluredir', ALLURE_RESULT_FOLDER, '--clean-alluredir'])

    os.system(f"allure generate {ALLURE_RESULT_FOLDER} -o {ALLURE_REPORT_FOLDER} --clean")
    # """

    # local_debug :
    """
    pytest.main(['-vs',
                 './common/demo/test_demo',
                 '--alluredir', ALLURE_RESULT_FOLDER, '--clean-alluredir'])
    os.system(f"allure generate {ALLURE_RESULT_FOLDER} -o {ALLURE_REPORT_FOLDER} --clean")
    # """
