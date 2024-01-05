# coding=utf-8
"""

"""

# @Time    :  2023-12-31 15:13:16
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  demo_obj_str
from common import yl_log


class A:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


a = A('aa', 'bb', 'cc')
print(a)
b = A('aaa', 'bbb', 'ccc')
print(b)

yl_log.info(a)
yl_log.info(b)

di = {
    'a': a,
    'b': b,
}

print(di)

print(a.a)
print(a.b)
print(a.c)

print(b.a)
print(b.b)
print(b.c)
