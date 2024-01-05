# coding=utf-8
"""
    logging 封装
    支持多线程单例

    YLLog       用于项目日志打印
    SlowApiLog  用于记录较慢接口
"""

# @Time    :  2023-12-29 17:51:45
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  do_log


import logging
import threading
import colorlog
import os
from common.utils.do_path import LOG_FILE, LOG_FOLDER, SLOW_LOG_FILE as SLOW_API_LOG_FILE
from logging.handlers import TimedRotatingFileHandler
from common.utils.do_conf import do_conf


class YLLog(object):
    _logger = None
    _lock = threading.Lock()

    @classmethod
    def _acquire_lock(cls):
        cls._lock.acquire()

    @classmethod
    def _release_lock(cls):
        cls._lock.release()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not hasattr(cls, '_logger') or not cls._logger:

                # 日志收集器 :
                _logger = logging.getLogger('yljk_logger')
                _logger.setLevel(do_conf.read_one('log', ['log_level', 'log_collection'], ).upper())

                # 输出到控制台 (带颜色) :
                console_handler = logging.StreamHandler()
                console_handler.setLevel(do_conf.read_one('log', ('log_level', 'out_to_console')).upper())
                fmt = do_conf.read_one('log', ('format', 'console'))
                log_colors = do_conf.read_one('log', 'color')
                color_format = colorlog.ColoredFormatter(fmt=fmt, log_colors=log_colors)
                console_handler.setFormatter(color_format)

                # 输出到文件 , 按时间切割 :
                if not os.path.exists(LOG_FOLDER):
                    os.mkdir(LOG_FOLDER)
                filehandler = TimedRotatingFileHandler(LOG_FILE, when='W1', backupCount=3, encoding='utf8')
                filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"
                filehandler.setFormatter(logging.Formatter(do_conf.read_one('log', ('format', 'file'))))
                filehandler.setLevel(do_conf.read_one('log', ('log_level', 'out_to_file')).upper())

                if not _logger.handlers:
                    _logger.addHandler(console_handler)
                    _logger.addHandler(filehandler)
                console_handler.close()
                filehandler.close()
                # 绑定到类属性 :
                cls._logger = _logger

        return cls._logger


class SlowApiLog(object):
    """
    SlowApiLog 仅用于配合 do_slow_api 实现将较慢接口记录到日志中
    接口自动化执行过程中, 较慢接口肯定是有重复的
    执行如下 linux 命令可对记录的慢接口根据接口去重, 并留下最慢的时间:

    awk '{print $2,$3,$6,$8}' slow_api_log.out | sort -k 4 -nr | sort -k 3,3 -u

    slow_api.yaml 中对该命令有详细说明, windows 下无法使用

    """
    _logger = None
    _lock = threading.Lock()

    @classmethod
    def _acquire_lock(cls):
        cls._lock.acquire()

    @classmethod
    def _release_lock(cls):
        cls._lock.release()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not hasattr(cls, '_logger') or not cls._logger:

                # 日志收集器 :
                _logger = logging.getLogger('slow_api_logger')
                _logger.setLevel(do_conf.read_one('log', ('log_level', 'log_collection')).upper())

                # 输出到控制台 :
                if_in_console = do_conf.read_one('log', 'slow_in_console')
                if if_in_console:
                    console_handler = logging.StreamHandler()
                    console_handler.setLevel(do_conf.read_one('log', ('log_level', 'log_slow_console')).upper())
                    fmt = do_conf.read_one('log', ('format', 'slow_api_console'))
                    log_colors = do_conf.read_one('log', 'color')
                    color_format = colorlog.ColoredFormatter(fmt=fmt, log_colors=log_colors)
                    console_handler.setFormatter(color_format)

                # 输出到文件 , 按时间切割 :
                if not os.path.exists(LOG_FOLDER):
                    os.mkdir(LOG_FOLDER)
                filehandler = TimedRotatingFileHandler(SLOW_API_LOG_FILE, when='D', backupCount=5, encoding='utf8')
                filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"
                filehandler.setFormatter(logging.Formatter(do_conf.read_one('log', ('format', 'slow_api_file'))))
                filehandler.setLevel(do_conf.read_one('log', ('log_level', 'log_slow_file')).upper())

                if not _logger.handlers:
                    if if_in_console:
                        _logger.addHandler(console_handler)
                    _logger.addHandler(filehandler)
                filehandler.close()

                cls._logger = _logger

        return cls._logger


yl_log = YLLog()
slow_log = SlowApiLog()

if __name__ == '__main__':
    # 打印日志 :
    """
    def create_yl_log():
        for i in range(2):
            g1, g2 = YLLog(), YLLog()
            g1.debug(f'YLLog() 对象1:{id(g1)} , YLLog()对象2:{id(g2)}')
            g1.debug(f'YLLog 单例' if id(g1) == id(g2) == id(yl_log) else 'YLLog 非单例')
            g2.debug('我是一条 debug 等级的日志')
            g2.info('我是一条 info 等级的日志')
            yl_log.warning('我是一条 warning 等级的日志')
            yl_log.exception(f'捕获到异常 : {Exception("RunTime Error")}')
            yl_log.critical('我是一条 critical 等级的日志')

            slow_log.info('simulate_slow_api')


    t1 = threading.Thread(target=create_yl_log())
    t2 = threading.Thread(target=create_yl_log())
    t1.run()
    t2.run()
    # """

    print(do_conf.read_one('log', 'log_level', ))
    print(do_conf.read_one('log', ['log_level', 'log_slow_console']))
