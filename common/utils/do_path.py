# coding=utf-8
"""
    路径通用化处理
"""

# @Time    :  2023-12-29 17:52:06
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  do_path
import os

# 项目绝对路径
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# 目录
CONF_FOLDER = os.sep.join([PROJECT_PATH, 'static', 'conf'])
DATA_FOLDER = os.sep.join([PROJECT_PATH, 'static', 'data'])
LOG_FOLDER = os.sep.join([PROJECT_PATH, 'static', 'log'])
ALLURE_RESULT_FOLDER = os.sep.join([PROJECT_PATH, 'static', 'allure_result'])
ALLURE_REPORT_FOLDER = os.sep.join([PROJECT_PATH, 'static', 'allure_report'])
CASE_FOLDER = os.sep.join([PROJECT_PATH, 'cases'])

# 文件
LOG_FILE = os.sep.join([LOG_FOLDER, 'yljk_test_api.out'])
SLOW_LOG_FILE = os.sep.join([LOG_FOLDER, 'yljk_slow_log.out'])

if __name__ == '__main__':
    def show(_path):
        print(os.path.exists(_path), _path)


    print('路径是否存在, 与路径本身 : ')
    show(PROJECT_PATH)
    show(CASE_FOLDER)
    show(CONF_FOLDER)
    show(DATA_FOLDER)
    show(LOG_FOLDER)
    show(ALLURE_RESULT_FOLDER)
    show(ALLURE_REPORT_FOLDER)

    print('文件是否存在, 与文件路径 : ')
    show(LOG_FILE)
    show(SLOW_LOG_FILE)
