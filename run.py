# coding=utf-8
"""
    pytest 启动文件
"""

# @Time    :  2023-12-29 15:34:45
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  run


import os
import sys
import pytest
from common import ALLURE_REPORT_FOLDER, ALLURE_RESULT_FOLDER

if __name__ == '__main__':
    pytest.main(['-s',
                 './test_cases/',
                 '--alluredir', ALLURE_RESULT_FOLDER, '--clean-alluredir'])

    os.system(f"allure generate {ALLURE_RESULT_FOLDER} -o {ALLURE_REPORT_FOLDER} --clean")
