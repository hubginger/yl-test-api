# coding=utf-8
"""

"""

# @Time    :  2023-12-31 00:02:54
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  demo_enum

from enum import Enum


class Fix(Enum):
    yml = 'yml'
    yaml = 'yaml'


def func(a: Fix = 'yml'):
    print(a)


func()
func(a='yaml')
func(a='ini')
