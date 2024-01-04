# coding=utf-8
"""

    使用 with 语句, 简化 try 语句
    其实没啥乱用, 哈哈哈
    可以实现异常记录, 就是后续代码还是会执行的

    适用于关闭连接这种操作, 即便关闭失败, 也不影响流程继续执行

│-----------------------------------------│
│    try:                                 │
│        1 / 0                            │
│    except ZeroDivisionError as e:       │
│        print(e)                         │
│-----------------------------------------│
│    with YLTry(ZeroDivisionError) as e:  │
│        1 / 0                            │
│-----------------------------------------│
"""


# @Time    :  2023-12-30 22:44:09
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  do_exception

class YLTry:
    """
    捕获到 with 中的异常, 则什么都不干
    捕获到其他异常, 则打印该异常的信息, 程序继续执行
    """

    def __init__(self, *args):
        self._exception_s = args

    def __enter__(self):
        return True

    def __exit__(self, _exception_type, _exception_value, _exception_trackback):
        """
        :param _exception_type:         错误类型, 代码实际执行时, 抛出的异常的 type
        :param _exception_value:        错误信息, 代码实际执行时, 抛出的异常的 message
        :param _exception_trackback:    错误详情
        """
        from common import yl_log
        if _exception_type and _exception_type in self._exception_s:
            return True
        elif _exception_type and issubclass(_exception_type, Exception):
            yl_log.exception(f'{_exception_value}')
            return True


class IgnoreError:
    """
    遇到任何异常都不打印, 只是返回 False
    """

    def __enter__(self):
        return self

    def __exit__(self, _exception_type, _exception_value, _exception_trackback):
        """
        该方法返回值为 "真值" 时, 不会抛出异常, 但是会将异常信息记录到日志中
        """
        if _exception_type:
            from common import yl_log
            yl_log.exception(f'{_exception_value}')
        return True


if __name__ == '__main__':
    # YLTry
    """
    try:
        v1 = 1 / 0
    except:
        pass

    with YLTry(ZeroDivisionError) as e:
        v2 = 1 / 0
    # """

    # IgnoreError
    # """
    with IgnoreError():
        var2 = {'a': 'aaa'}['b']
    with IgnoreError():
        var1 = 1 == 1
    # """
