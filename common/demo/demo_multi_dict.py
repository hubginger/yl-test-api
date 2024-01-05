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
    di = {'a': {'b': ['00', '11', '22']}}
    li = ['a', 'b', 0]

    expr = 'di'
    express = ''
    for k in li:
        if isinstance(k, int) or k.isdigit():
            expr += f'[{k}]'
        else:
            expr += f'["{k}"]'
        express += f'["{k}"]'

    print(di)
    print(di['a']['b'][0])
    print(expr)
    print(express)
    print(eval(expr))


if __name__ == '__main__':
    _multi_key()
    print('----' * 20)
    get_by_multi_key()
