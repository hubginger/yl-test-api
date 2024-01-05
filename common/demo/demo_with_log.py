# coding=utf-8
"""

"""

# @Time    :  2023-12-30 22:41:29
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  demo_with_log
# -*- coding: utf-8 -*-
import json


class A(object):

    def __init__(self, exception_type=None):
        self.exception_type = exception_type

    def __enter__(self):
        return self.exception_type

    def __exit__(self, exc_type, exc_val, exc_trackback):
        # 也是可以在这里捕捉任何错误
        print(exc_type, exc_val, exc_tb)
        # 如果不走 就会返回错误信息,就是报错
        if self.exception_type and exc_type is self.exception_type:
            # 判断单个
            return self

        elif self.exception_type is None and issubclass(exc_type, Exception):
            pass


try:
    json.loads({'a'})
except Exception as e:
    print(e)
finally:
    print(1)

with A(TypeError) as a:
    json.loads({'a'})
