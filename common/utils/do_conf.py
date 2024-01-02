# coding=utf-8
"""
    配置文件操作
        .yaml / .yml
"""

# @Time    :  2023-12-29 17:50:59
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  do_conf
import os
import yaml

from common.utils.do_path import CONF_FOLDER, DATA_FOLDER
from common.utils.do_try import IgnoreError


class DoConf(object):
    __instance = False

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            return cls
        else:
            cls.__instance = True
            return cls

    @classmethod
    def _file(cls, file_name, postfix='yml'):
        """
            因为 extract.yml 存储的是提取出来的数, 放在 data 目录下, 而其他 yml 文件放在 conf 目录下
            所以根据 file_name.postfix 是否为 extract.yml 来决定目录用 conf 还是 data
            返回文件绝对路径
        """
        _folder = DATA_FOLDER if file_name == 'extract' and postfix == 'yml' else CONF_FOLDER
        _file = os.sep.join([_folder, f'{file_name}.{postfix}'])
        return _file

    @classmethod
    def get(cls, _keys):
        """
            _keys 可传 str 或 list / tuple
                str :            返回顶层 key 对应的 value
                list / tuple :   list 中的顺序与 yaml 中的 key 顺序保持一致, 任意一个 key 未匹配到时, 返回 None
        """
        _file = os.sep.join([DATA_FOLDER, 'extract.yml'])
        with open(_file, encoding='utf8') as _f:
            _datas: dict = yaml.safe_load(_f)
            if isinstance(_keys, str):
                _keys = [_keys]
            for _key in _keys:
                _datas = _datas.get(_key)
                if not _datas:
                    return None
            return _datas

    @classmethod
    def set(cls, key, value):
        """
            写入数据到 extract.yml
            先加载 extract.yml 中的所有数据
            新增/更新 key: value 进去
        """
        _file = os.sep.join([DATA_FOLDER, 'extract.yml'])
        _datas = cls.read_all('extract')
        _datas = _datas if _datas else dict()

        _datas[key] = value
        with open(_file, encoding='utf8', mode='w') as _f:
            yaml.dump(_datas, _f)

    @classmethod
    def set_multi(cls, _keys, value):
        """
            加载 extract.yml 文件中的数据
            遍历 keys, 依次根据 key 取值, 更新/新增最后一个 key 值为 value

            更新:
                最后一个 key 存在时, 进行更新
            新增:
                最后一个 key 不存在, 前一个 key 存在, 且前一个 key 值为 dict 类型时, 进行新增
        例:
            extract.yml 取出来为: {'a': {'b': {'c': 'xxxx'}}}
            keys 为 ('a', 'b', 'c'), value 为 'cccc' 时, 更新为: {'a': {'b': {'c': 'cccc'}}}
            keys 为 ('a', 'b', 'd'), value 为 'dddd' 时, 更新为: {'a': {'b': {'c': 'xxxx', 'd': 'dddd'}}}
            keys 为 ('a','b','c','d'), 返回 False, 因为配置文件中, c 已经是 xxxx 了, 为 str, 不支持将 c 改为 dict

        :param _keys:        依次取值的 key, 可以是列表或者元组, 程序一层一层根据 keys 顺序取值
        :param value:       将 keys 的最后一个 key 对应的值更新为 value
        :return:            True / False, 更新成功, 返回 True, 更新失败, 返回 False
        """

        _file = _file = os.sep.join([DATA_FOLDER, 'extract.yml'])
        _keys = [_keys] if isinstance(_keys, str) else _keys
        data_s = cls.read_all(file_name='extract')
        data_s = data_s if data_s else dict()

        expression = 'data_s'
        for key in _keys[:-1]:
            expression += f'["{key}"]'
        try:
            res = eval(expression)
            res[_keys[-1]] = value
        except (KeyError, TypeError):
            # 可能的异常:
            # 配置文件只有 a:b:c, 但是 keys 传递了 a:x:y, a 取 x 娶不到, 就会 KeyError
            # 配置文件只有 a:b:c, 但是 keys 传递了 a:b:c:d, b 取 c 取到 str 之后, 执行 c[key]=value 就会 TypeError
            from common import yl_log
            yl_log.warning(f'更新失败, 请检查 extract.yml 内容和 keys: {_keys} 参数是否对应')
            return False

        with open(_file, encoding='utf8', mode='w') as _f:
            yaml.dump(data_s, _f)
            return True

    @classmethod
    def read_one(cls, file_name, _keys, postfix='yml', ):
        """
            读取部分数据

            yaml 文件存在, 获取 file_name.postfix 文件中的所有数据后, 根据 _keys 中的 key, 依次取值
            任意 key 娶不到时, 返回 None
            yaml 文件不存在, 则直接返回 None

            extract.yml 在 data 目录下, 其他在 conf 目录下

            _keys 可传 str 或 list / tuple
                str :            返回顶层 key 对应的 value
                list / tuple :   list 中的顺序与 yaml 中的 key 顺序保持一致, 任意一个 key 未匹配到时, 返回 None
        """
        _file = cls._file(file_name, postfix)
        try:
            with open(_file, encoding='utf8') as _f:
                _datas: dict = yaml.safe_load(_f)
                if isinstance(_keys, str):
                    _keys = [_keys]
                for _key in _keys:
                    _datas = _datas.get(_key)
                    if not _datas:
                        return None
                return _datas
        except FileNotFoundError:
            return None

    @classmethod
    def read_all(cls, file_name, postfix='yml', ):
        """
            读取全部数据

            yaml 文件存在, 获取 file_name.postfix 文件中的所有数据并返回
            yaml 文件不存在, 则直接返回 None

            extract.yml 在 data 目录下, 其他在 conf 目录下
        """
        _file = cls._file(file_name, postfix)
        try:
            with open(_file, encoding='utf8') as _f:
                _datas: dict = yaml.safe_load(_f)
                return _datas
        except FileNotFoundError:
            return None

    @classmethod
    def update(cls, _keys, value, file_name, postfix='yml', ):
        """
        循环方式
            加载 file_name.postfix ( 默认为 data 目录下的 : extract:yml) 文件中的数据
            遍历 keys, 依次根据 key 取值, 更新/新增最后一个 key 值为 value

            更新:
                最后一个 key 存在时, 进行更新
            新增:
                最后一个 key 不存在, 前一个 key 存在, 且前一个 key 值为 dict 类型时, 进行新增
        例:
            extract.yml 取出来为: {'a': {'b': {'c': 'xxxx'}}}
            keys 为 ('a', 'b', 'c'), value 为 'cccc' 时, 更新为: {'a': {'b': {'c': 'cccc'}}}
            keys 为 ('a', 'b', 'd'), value 为 'dddd' 时, 更新为: {'a': {'b': {'c': 'xxxx', 'd': 'dddd'}}}
            keys 为 ('a','b','c','d'), 返回 False, 因为配置文件中, c 已经是 xxxx 了, 为 str, 不支持将 c 改为 dict
        :param _keys:        依次取值的 key, 可以是列表或者元组, 程序一层一层根据 keys 顺序取值
        :param value:       将 keys 的最后一个 key 对应的值更新为 value
        :param file_name:   提取该配置文件中的数据
        :param postfix:     配置文件后缀, 一般就是 yml
        :return:            True / False, 更新成功, 返回 True, 更新失败, 返回 False
        """

        _file = cls._file(file_name, postfix)
        _keys = [_keys] if isinstance(_keys, str) else _keys
        data_s = cls.read_all(file_name=file_name, postfix=postfix, )
        data_s = data_s if data_s else dict()

        _data = data_s
        try:
            # for 循环可能抛 AttributeError
            for key in _keys[:-1]:
                _data = _data.get(key)
                if not _data:
                    return False
            # 字典增改, 可能抛 TypeError
            _data[_keys[-1]] = value
        except (AttributeError, TypeError):
            # 可能是配置文件只有 a:b 层级
            # 配置文件只有 a:b:c, 但是 keys 传递了 a:x:y, a 取 x 娶到 None, None 调用 get() 就会 AttributeError
            # 配置文件只有 a:b:c, 但是 keys 传递了 a:b:c:d, c 取到 str 之后, 执行 c[key]=value 就会 TypeError
            return False
        with open(_file, encoding='utf8', mode='w') as _f:
            yaml.dump(data_s, _f)
        return True

    @classmethod
    def update_multi(cls, keys, value, file_name='extract', postfix='yml', ):
        """
        eval 方式
            加载 file_name.postfix ( 默认为 data 目录下的 : extract:yml) 文件中的数据
            遍历 keys, 依次根据 key 取值, 更新/新增最后一个 key 值为 value

            更新:
                最后一个 key 存在时, 进行更新
            新增:
                最后一个 key 不存在, 前一个 key 存在, 且前一个 key 值为 dict 类型时, 进行新增
        例:
            extract.yml 取出来为: {'a': {'b': {'c': 'xxxx'}}}
            keys 为 ('a', 'b', 'c'), value 为 'cccc' 时, 更新为: {'a': {'b': {'c': 'cccc'}}}
            keys 为 ('a', 'b', 'd'), value 为 'dddd' 时, 更新为: {'a': {'b': {'c': 'xxxx', 'd': 'dddd'}}}
            keys 为 ('a','b','c','d'), 返回 False, 因为配置文件中, c 已经是 xxxx 了, 为 str, 不支持将 c 改为 dict
        :param keys:        依次取值的 key, 可以是列表或者元组, 程序一层一层根据 keys 顺序取值
        :param value:       将 keys 的最后一个 key 对应的值更新为 value
        :param file_name:   提取该配置文件中的数据
        :param postfix:     配置文件后缀, 一般就是 yml
        :return:            True / False, 更新成功, 返回 True, 更新失败, 返回 False
        """
        _file = cls._file(file_name, postfix)
        if isinstance(keys, str):
            keys = [keys]

        data_s = cls.read_all(file_name=file_name, postfix=postfix, )
        data_s = data_s if data_s else dict()
        expression = 'data_s'

        # 构造层级取值表达式 , keys: ['log_level','log_collection'] ----> expression: data_s['log_level']['log_collection']
        for key in keys[:-1]:
            expression += f'["{key}"]'
        try:
            res = eval(expression)
            res[keys[-1]] = value
        except (KeyError, TypeError):
            # 配置文件只有 a:b:c, 但是 keys 传递了 a:x:y, a 取 x 娶不到, 就会 KeyError
            # 配置文件只有 a:b:c, 但是 keys 传递了 a:b:c:d, c 取到 str 之后, 执行 c[key]=value 就会 TypeError
            from common import yl_log
            yl_log.warning(f'更新失败, 请检查 {file_name}.{postfix} 内容和 keys: {keys} 参数是否对应')
            return False

        with open(_file, encoding='utf8', mode='w') as _f:
            yaml.dump(data_s, _f)
            return True

    @classmethod
    def update_practice(cls, keys, value, file_name='extract', postfix='yml', ):
        """
            with 表达式简化 try/except,
            存在一个问题就是不知道表达式是对的还是错的
        """
        _file = cls._file(file_name, postfix)
        if isinstance(keys, str):
            keys = [keys]

        data_s = cls.read_all(file_name=file_name, postfix=postfix, )
        data_s = data_s if data_s else dict()
        expression = 'data_s'

        for key in keys[:-1]:
            expression += f'["{key}"]'
        with IgnoreError():
            res = eval(expression)
            res[keys[-1]] = value
        with open(_file, encoding='utf8', mode='w') as _f:
            yaml.dump(data_s, _f)

    @classmethod
    def __clear(cls, file_name='extract', postfix='yml'):
        _file = cls._file(file_name=file_name, postfix=postfix)
        with open(_file, encoding='utf-8', mode='w') as _f:
            _f.truncate()


do_conf = DoConf()

if __name__ == '__main__':
    # _file
    """
    # 对类的受保护成员文件的访问: 
    print(do_conf._file('extract'))
    print(do_conf._file('db'))
    # """

    # read_all
    """
    print(do_conf.read_all('extract'))
    print(do_conf.read_all('db'))
    print(do_conf.read_all('not_exist_file'))
    # """

    # read_one
    """
    print('文件不存在时:', do_conf.read_one('not_exist_file', 'not_exist_key'))
    print('extract.yml 键存在时:', do_conf.read_one('extract', 'demo_key'))
    print('extract.yml 键不存在时:', do_conf.read_one('extract', 'not_exist_key'))
    print('db.yml 键存在时:', do_conf.read_one('db', 'host'))
    print('db.yml 键不存在时:', do_conf.read_one('db', 'not_exist_key'))
    print('log.yml 取层级, 键存在时:', do_conf.read_one('log', ('log_level', 'log_collection')))
    print('log.yml 取层级, 后一个键不存在时:', do_conf.read_one('log', ('log_level', 'not_exist_key')))
    print('log.yml 取层级, 第一个键不存在时:', do_conf.read_one('log', ('not_exist_key', 'log_collection')))
    # """

    # get
    """
    print(do_conf.get('demo_key'))
    print(do_conf.get('not_exist_key'))
    print(do_conf.get(('', '')))
    # """

    # set
    """
    do_conf.set('demo_key_set', 'demo_value_set')
    print(do_conf.read_all('extract'))
    do_conf.set('demo_key', 'demo')
    print(do_conf.read_all('extract'))
    do_conf.set('demo_key', 'demo_value')
    print(do_conf.read_all('extract'))
    # """

    # update
    """
    print(do_conf.read_all('extract'))
    print(do_conf.update('demo_key', 'demo', 'extract'))
    print(do_conf.read_all('extract'))
    print(do_conf.update('demo_key', 'demo_value', 'extract'))
    print(do_conf.read_all('extract'))
    print(do_conf.update(('a', 'b', 'c'), 'xxx', 'extract'))
    print(do_conf.read_all('extract'))
    print(do_conf.update(('a', 'b'), 'xxx', 'extract'))
    print(do_conf.read_all('extract'))
    print(do_conf.update(('a', 'b', 'c'), 'xxx', 'extract'))
    print(do_conf.read_all('extract'))
    print(do_conf.update(('a',), 'xxx', 'extract'))
    print(do_conf.read_all('extract'))
    # """

    # update_mulit
    """
    with open(os.sep.join([DATA_FOLDER, 'extract.yml']), encoding='utf-8', mode='w') as f:
        f.truncate()
    print(do_conf.read_all('extract'))
    print(do_conf.update_multi(['demo_key'], 'demo_val'))
    print(do_conf.read_all('extract'))
    print(do_conf.update_multi(['demo_key'], 'demo_value'))
    print(do_conf.read_all('extract'))
    print(do_conf.update_multi(['a'], {'b': {'c': 'oooo'}}))
    print(do_conf.read_all('extract'))
    print(do_conf.update_multi('demo', 'demo'))
    print(do_conf.read_all('extract'))
    print(do_conf.update_multi(['a', 'b', 'c'], 'cccc'))
    print(do_conf.read_all('extract'))
    print(do_conf.update_multi(['a', 'b', 'd'], 'dddd'))
    print(do_conf.read_all('extract'))
    print(do_conf.update_multi(['a', 'b', 'c', 'd', 'e'], 'eeee'))
    print(do_conf.read_all('extract'))
    print(do_conf.update_multi(['x', 'y', 'z'], 'zzzz'))
    print(do_conf.read_all('extract'))
    # """

    # update_practice
    """
    print(do_conf.read_all('extract'))
    print(do_conf.update_practice(['a', 'b', 'c'], 'c'))
    print(do_conf.read_all('extract'))
    print(do_conf.update_practice(['a', 'b', 'c', 'd', 'e'], 'e'))
    print(do_conf.read_all('extract'))
    print(do_conf.update_practice(['a', 'b', 'c'], 'cccc'))
    print(do_conf.read_all('extract'))
    # """
