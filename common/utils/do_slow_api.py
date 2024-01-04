# coding=utf-8
"""
    慢接口记录到日志

    加载 slow_api.yml 中定义的 maximum_time, 该值表示接口响应的最大允许时间, 实际响应耗时超过该值则会被记录到 yljk_slow_log.out 文件中

    这是一个类装饰器, 带参数, 使用时可以通过给装饰器传参来自定义 maximum_time,
    一般不需要传参, 不传参时使用的是配置文件中定义的 maximum_time

    记录时, 会重复记录,
        比如一个接口 A, 执行过程中被调用过 10 次, 其中 8 次慢于 maximum_time
        则在日志文件中记录时, 会记录 8 次数
        可使用如下 linux 命令来对日志记录进行排序和去重
    sh:
        awk '{print $2,$3,$6,$8}' slow_api_log.out | sort -k 4 -nr | sort -k 3,3 -u
"""
from time import time

from common.utils.do_conf import do_conf
from common.utils.do_log import slow_log


# @Time    :  2023-12-29 17:58:26
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  do_slow_api

class AnswerTime:
    """
        将慢接口记录到日志文件中
    """

    maximum_time = int(do_conf.read_one('slow_api', 'maximum_time'))

    def __init__(self, maximum_time=maximum_time):
        """
            响应大于 maximum_time 的接口会被记录 maximum_time : millisecond
        """

        self._maximum_time = maximum_time

    def __call__(self, target_func):
        def inner(*args, **kwargs):
            start_time = time() * 1000
            res = target_func(*args, **kwargs)
            end_time = time() * 1000

            consume_time = int(end_time - start_time)

            url = kwargs.get('uri') if kwargs.get('uri') else kwargs.get('url')

            if consume_time > self._maximum_time:
                slow_log.error(f'api_url: {url} consume_time: {consume_time} ms, maximum_time: {self._maximum_time} ms.')
            return res

        return inner


if __name__ == '__main__':
    from time import sleep


    @AnswerTime()
    def send_slow(url):
        sleep(1)


    @AnswerTime()
    def send_quick(url):
        pass


    send_slow(url='http://www.baidu.com')
    send_quick(url='http://www.yljk.com')
