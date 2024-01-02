# coding=utf-8
"""

"""

# @Time    :  2023-12-30 18:04:07
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  demo_init
from common import yl_log

try:
    1 / 0
except ZeroDivisionError as e:
    yl_log.error(e)
    # yl_log.exception(e)
