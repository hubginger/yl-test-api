# coding=utf-8
"""

"""


# @Time    :  2023-12-31 10:35:30
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  demo_multi_dict


def _multi_key():
    """
    a,b,c cccc
    a,b,d dddd
    """
    di = {'a': {'b': {'c': 'xxxx'}}}
    li = ['a', 'b', 'c']

    expr = 'di'
    express = ''
    for k in li:
        expr += f'["{k}"]'
        express += f'["{k}"]'
    print(di)
    print(di['a']['b']['c'])
    print(expr)
    print(express)
    print(eval(expr))


def get_by_multi_key():
    pass


if __name__ == '__main__':
    _multi_key()
