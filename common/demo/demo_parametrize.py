# coding=utf-8
"""

"""

# @Time    :  2023-12-31 14:39:37
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  demo_parapetrize
import pytest


@pytest.mark.parametrize('a,b,c', [('a1', 'b1', 'c1',), ('a2', 'b2', 'c2',)])
def test_parametrize(a, b, c):
    print()
    print(a)
    print(b)
    print(c)


@pytest.mark.parametrize('a,b,c', [('a1', 'b1', 'c1', 'd1'), ('a2', 'b2', 'c2', 'd2')])
def test_parametrize_error(a, b, c):
    print()
    print(a)
    print(b)
    print(c)


if __name__ == '__main__':
    pytest.main([
        '-vs',
    ])
