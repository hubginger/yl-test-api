# coding=utf-8
"""
    通用提取封装
    场景:
        提取时, 可能是多层关系:
        比如:
            response = {"code": "OK", "result": {"user_info": {"name": "Admin"}}}
        取 Admin 时, 就是 $.result.user_info.name
        那我们定义提取方法, 以不定长参数接收 result, user_info, name, 根据顺序, 按照层级提取最后返回

    当前仅提供了层级字典提取, 如果是 jsonlist, 则需要根据下标提取, 下标提取需自行封装

    待封装:
        jsonlist 的下标提取
        jsonpath 表达式提取 ( 使用第 0 个结果, 使用列表两种)
        regular 正则表达式提取
"""
from typing import Dict

import allure
import jsonpath

from common.utils.do_conf import do_conf
from common.utils.do_log import yl_log


# @Time    :  2024-01-04 10:39:11
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  base_extract

@allure.step('写入')
def set2yml(key, value):
    do_conf.set(key, value)
    yl_log.debug(f'写入数据成功, 数据为: < {key}: {value} >')


@allure.step('提取')
def extract(target: Dict, *keys):
    """
        根据 keys 的顺序, 按照层级从 target 中提取
        提取出来直接存入 staticsss/data/extract.yml 文件中
    """
    _expression = 'target'
    for key in keys:
        _expression += f'["{key}"]'

    try:
        target = target if isinstance(target, dict) else eval(target)
        _target = eval(_expression)
    except (KeyError, TypeError, NameError):
        # 娶不到时, 就可能 KeyError, 还有下级时取到非 dict, 就可能 TypeError, 当异常时, 就让 _target 为 None
        _target = None
        yl_log.warning('提取失败, 请检提取相关信息')
    return _target


@allure.step('提写')
def extract_set(target: Dict, key, *keys):
    """
        提取并存储, 根据 keys 从 target 提取后
        存入 staticsss/data/extract.yml
    """
    _value = extract(target, *keys)
    if _value:
        do_conf.set(key, _value)
        yl_log.debug(f'extract.yml 写入数据: {key}:{_value}')
    else:
        yl_log.warning(f'extract.yml 未写入数据, 因为根据 {keys} 从 {target} 提取到 < None >')


@allure.step('提取')
def json_one(target: Dict, key):
    """
        jsonpath 提取, 如果仅传递一个 key, 比如 'name' , 则会转换为 $..name 进行提取
        对 target 应用 jsonpath 表达式进行提取
        如果没有提取到数据, 则返回 None
        如果提取到数据, 则返回第一个匹配到的数据
    """
    _target = target if isinstance(target, Dict) else eval(target)
    _expression = key if key.startswith('$') else f'$..{key}'
    _res_s = jsonpath.jsonpath(target, _expression)
    _res = _res_s[0] if _res_s else None
    yl_log.debug(f'Json提取__提取语句: {_expression}')
    yl_log.debug(f'Json提取__提取目标: {target}')
    yl_log.debug(f'Json提取__提取结果: {_res_s}')
    yl_log.debug(f'Json提取__使用结果: {_res}')
    return _res


@allure.step('提取')
def json_list():
    return


@allure.step('提取')
def extract_list():
    return


if __name__ == '__main__':
    # extract / extract_set
    """
    __target = {"code": "OK", "result": {"user_info": {"name": "Admin"}}}
    print('code : ', extract(__target, 'code'))
    print('result : ', extract(__target, 'result'))
    print('result.user_info : ', extract(__target, 'result', 'user_info'))
    print('result.user_info.name : ', extract(__target, 'result', 'user_info', 'name'))

    extract_set(__target, 'code', 'code')
    print(do_conf.get_all())
    """

    # json_one :
    # """
    __target = {"code": "OK", "result": {"user_info": {"name": "Admin"}, 'name': '法外狂徒'}}
    print(json_one(__target, '$..id'))
    # """

    # set2yml :
    """
    set2yml('demo_set', 'demo_set_value')
    print(do_conf.get_all())
    # """
