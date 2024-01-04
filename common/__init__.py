# coding=utf-8
"""

    将 common 中的内容集成到此处
    导包时都从 common 中导

    只将 conftest 和 test_case 中可能用到的导入到这里

"""
import hashlib
import threading

from common.utils.do_log import yl_log
from common.utils.do_conf import do_conf
from common.utils.do_mysql import DoMySql
from common.utils.do_excel import ExcelData
from common.utils.do_path import ALLURE_REPORT_FOLDER, ALLURE_RESULT_FOLDER
from common.base_api import BaseApi, BaseLogin, requests
from common.base_data import all_data, CaseData
from common.base_assert import BaseAssert
from common.base_extract import extract, extract_set


# @Time    :  2023-12-29 15:33:44
# @Author  :  ginger
# @Email   :  gingerqgyy@outlook.com
# @Project :  yljk_test_api
# @File    :  __init__.py


class SingleData:
    data = None
    __instance = False
    _lock = threading.Lock()

    @classmethod
    def _acquire_lock(cls):
        cls._lock.acquire()

    @classmethod
    def _release_lock(cls):
        cls._lock.release()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls.__instance:
                return cls
            else:
                cls.data = CaseData(do_conf.read_one('excel', 'file_name')).data
                cls.__instance = True
                return cls

    @classmethod
    def get_excel_data(cls, sheet_name, case_id, scope='all'):
        """
            调用 CaseData 类的 original 方法, 进行数据匹配
        """
        _res = all_data.original(sheet_name, case_id, scope=scope)
        return _res


def get_excel_data(sheet_name, case_id, scope='all'):
    """
        兼容原 yljk_api_test 的参数化逻辑
        方法名 get_excel_data 和原项目参数化时的方法名一致
        只需要将原有 handle_excel.py 下的 get_excel_data 注释掉
        然后导入该方法到 handle_excel.py 中, 即可兼容原 test_case 参数化, 且所有 test_case 中的代码都不需要变更
    """
    single_data = SingleData()
    _res = single_data.get_excel_data(sheet_name, case_id, scope=scope)
    return _res


def get_verify_info(device='a', ):
    """
        放在这里, 方便登录时, 获取验证码, 并替换到登录的参数中
        比如登录时的参数为 data : {'authType': 'usernamePassword', ... }
        则直接 data.update(get_verify_info(device)) 即可将验证码和验证码的 id 更新进去
    """
    _url = do_conf.read_one('request', ['verify_url', device])
    _res = requests.get(url=_url, headers={'terminal': 'WEBPC'}).json()
    result = {'verifyCode': _res.get('result').get('verifyCode'), 'verifyId': _res.get('result').get('verifyId')}
    return result


def md5(pwd: str, salt=''):
    """
        默认密码已经在配置文件中维护了, 但是测试密码错误的用例时, 直接替换配置文件中的密码可能导致本身密码错误的用例, 却直接登录成功了
        因此密码错误的用例, 需调用 md5 方法, 来生成对应的密码并替换, data.password = md5(data.password)
    """
    _md5 = hashlib.md5()
    pwd += salt
    _md5.update(pwd.encode('utf-8'))
    return _md5.hexdigest()


if __name__ == '__main__':
    print(get_verify_info())
