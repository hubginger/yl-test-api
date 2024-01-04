# coding=utf-8
"""
    通用断言封装
        只封装断言相等的这一种情况
            actual == expected

    其他:
        大概率还会遇到 : 包含关系 : actual in expected
        小概率还会遇到 : '>', '<', '!=', 'not', 'in'

    其他断言场景, 需自行封装, 封装时参考相等的断言
"""
import json

from jsonpath import jsonpath

from common.utils.do_log import yl_log


# @Project : yljk_test_api
# @File : base_assert
# @Time : 2024-01-02 18:01:59
# @Author : JiangTong


class BaseAssert:
    """
        基础断言类
        断言是否相等, 实现了 dict 层级断言和 json 取值断言两种方式

        实际中也会有其他断言场景出现, 届时就需要自行封装断言方法了
    """

    @staticmethod
    def assert_by_dict(expected, actual, keys):
        """
        该断言方法仅适用于接口响应为 json 的场景
        断言时候注意数据格式, 当从 actual 中根据 keys 取值取出来是 dict 时, 调用该方法传递 expected 也需要传递 dict

        方法作用 :
            根据 keys , 按照顺序, 从 actual 中找结果,
            找到最终结果和 expected 进行断言

        断言逻辑 :
            expected == actual.get('key_01').get('key_02').get('key_03')  # keys : ['key_01', 'key_02', 'key_03', ]

        参数说明 :
            :param expected:   预期结果
            :param actual:     实际结果
            :param keys:       取值
        """
        _expression = 'actual'
        for key in keys:
            _expression += f'["{key}"]'

        try:
            actual = actual if isinstance(actual, dict) else eval(actual)
            _actual = eval(_expression)
        except (KeyError, TypeError, NameError):
            # 娶不到时, 就可能 KeyError, 还有下级时取到非 dict, 就可能 TypeError, 当异常时, 就让 _actual 为 None
            _actual = None

        try:
            assert expected == _actual
        except AssertionError:
            yl_log.error(f'断言不通过 : {expected} != {_actual}')
            raise
        else:
            yl_log.info(f'断言通过 : {expected} == {_actual}')

    @staticmethod
    def assert_common(expected, actual, *keys):
        """
            该断言方法仅适用于接口响应为 json 的场景
            断言时候注意数据格式, 当从 actual 中根据 keys 取值取出来是 dict 时, 调用该方法传递 expected 也需要传递 dict

            方法作用 :
                根据 keys , 按照顺序, 从 actual 中找结果,
                找到最终结果和 expected 进行断言

            断言逻辑 :
                expected == actual.get('key_01').get('key_02').get('key_03')  # keys : ['key_01', 'key_02', 'key_03', ]

            参数说明 :
                :param expected:   预期结果
                :param actual:     实际结果
                :param keys:       不定长参数, 简化调用时的传参
        """
        _expr_actual = 'actual'
        _expr_expect = 'expected'

        for key in keys:
            _expr_actual += f'["{key}"]'
            _expr_expect += f'["{key}"]'

        try:
            actual = actual if isinstance(actual, dict) else eval(actual)
            expected = expected if isinstance(expected, dict) else eval(expected)
            _actual = eval(_expr_actual)
            _expected = eval(_expr_expect)
        except (KeyError, TypeError, NameError):
            # 娶不到时, 就可能 KeyError, 还有下级时取到非 dict, 就可能 TypeError, 当异常时, 就让 _actual 为 None, 让 _expected 为 ''
            _actual = None
            _expected = ''

        try:
            assert _expected == _actual
        except AssertionError:
            yl_log.error(f'断言不通过 : {_expected} != {_actual}')
            raise
        else:
            yl_log.info(f'断言通过 : {_expected} == {_actual}')

    @staticmethod
    def assert_by_json(expected, actual, expression):
        """
        该断言方法仅适用于接口响应为 json 的场景
        断言时候注意数据格式, 当从 actual 中根据 expression 取值取出来是 dict 时, 调用该方法传递 expected 也需要传递 dict

        方法作用 :
            expression 为 jsonpath 表达式
            根据 expression 从 actual 中取值, 然后和 expected 进行断言

        断言逻辑 :
            expected == jsonpath(actual, expression)

        参数说明 :
            :param expected:     预期结果
            :param actual:       实际结果
            :param expression:   取值表达式
        """

        try:
            actual = json.loads(str(actual))
        except json.decoder.JSONDecodeError:
            actual = str(actual).replace('\'', '\"')
            actual = json.loads(str(actual))

        try:
            _res = jsonpath(actual, expression)
            _actual = _res[0]
        except (json.JSONDecodeError, TypeError,):
            _actual = None

        try:
            assert expected == _actual
        except AssertionError:
            yl_log.error(f'断言不通过 : {expected} != {_actual}')
            raise
        else:
            yl_log.info(f'断言通过 : {expected} == {_actual}')


if __name__ == '__main__':
    # dict :
    # """
    exp = 'd'
    act = {'a': 'a', 'b': 'b', 'c': {'c': {'d': 'd'}}}
    ks = ['c', 'c', 'd']
    BaseAssert.assert_by_dict(exp, act, ks)

    exp = 'dd'
    act = str({'a': {'b': {'c': {'d': 'd'}}}})
    ks = ('a', 'b', 'c', 'd')
    BaseAssert.assert_by_dict(exp, act, ks)

    exp = 'dd'
    act = str('苟苟营')
    ks = ('a', 'b', 'c', 'd')
    BaseAssert.assert_by_dict(exp, act, ks)
    # """

    # json :
    # """
    exp = {"cd": {"d": "d"}}
    act = {"a": "a", "b": "b", "c": {"cd": {"d": "d"}}}
    js = '$..c'
    BaseAssert.assert_by_json(exp, act, js)

    exp = {"cd": {"d": "d"}}
    act = '{"a": "a", "b": "b", "c": {"cd": {"d": "d"}}}'
    js = '$..c'
    BaseAssert.assert_by_json(exp, act, js)
    # """
