# coding=utf-8
"""

"""

# @Time    :  2024-01-03 11:15:08
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  run


import os
import pytest
from common import ALLURE_REPORT_FOLDER, ALLURE_RESULT_FOLDER

if __name__ == '__main__':
    # """
    pytest.main(['-vs',
                 '--alluredir', ALLURE_RESULT_FOLDER, '--clean-alluredir'])
    os.system(f"allure generate {ALLURE_RESULT_FOLDER} -o {ALLURE_REPORT_FOLDER} --clean")
    # """
