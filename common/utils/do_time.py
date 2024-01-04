# coding=utf-8
"""
    时间处理
    有些查询的接口, 需要传时间
    在这里封装一些时间处理的逻辑
    方便调用
"""

import time
from typing import Text
from datetime import datetime


# @Time    :  2024-01-04 11:23:46
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  do_time

def now():
    return time.time()


def date2time(time_str: Text):
    """
        2024-01-04 11:32:56 ----> 1704339176000
    """
    try:
        datetime_format = datetime.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
        timestamp = int(
            time.mktime(datetime_format.timetuple()) * 1000.0
            + datetime_format.microsecond / 1000.0
        )
        return timestamp
    except ValueError as e:
        raise ValueError('日期格式错误, 需要传入得格式为 "%Y-%m-%d %H:%M:%S" ') from e


if __name__ == '__main__':
    n = datetime.now()
    print(str(n).split('.')[0])
    n1 = date2time('2024-01-04 11:32:56')
    print(n1)
