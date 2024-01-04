# coding=utf-8
"""

    将 common 中的内容集成到此处
    导包时都从 common 中导

    只将 test_case 和 lib 中会用到的导入到这里

"""
import hashlib
import threading
from common.utils.do_log import yl_log
from common.utils.do_conf import do_conf
from common.utils.do_mysql import DoMySql
from common.utils.do_excel import ExcelData
from common.utils.do_parametrize import DoExcel, CaseData, all_data
from common.utils.do_path import ALLURE_REPORT_FOLDER, ALLURE_RESULT_FOLDER
from common.base_api import BaseApi, requests
from common.base_data import all_data
from common.base_assert import BaseAssert


# @Time    :  2023-12-29 15:33:44
# @Author  :  ginger
# @Email   :  gingerqgyy@outlook.com
# @Project :  yljk_test_api
# @File    :  __init__.py


class SingleData:
    all_data_s = None
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
                cls.all_data_s = CaseData(do_conf.read_one('excel', 'file_name')).data
                cls.__instance = True
                return cls

    @classmethod
    def get_excel_data(cls, sheet_name, case_id):
        _res = all_data.original(sheet_name, case_id)
        return _res


def get_excel_data(sheet_name, case_id):
    """
        兼容原 yljk_api_test 的参数化逻辑
        方法名 get_excel_data 和原项目参数化时的方法名一致
        只需要将原有 handle_excel.py 下的 get_excel_data 注释掉
        然后导入该方法到 handle_excel.py 中, 即可兼容原 test_case 参数化, 且所有 test_case 中的代码都不需要变更
    """
    single_data = SingleData()
    _res = single_data.get_excel_data(sheet_name, case_id)
    return _res


def get_verify_info(device='a', ):
    _url = do_conf.read_one('request', ['verify_url', device])
    _res = requests.get(url=_url, headers={'terminal': 'WEBPC'}).json()
    result = {'verifyCode': _res.get('result').get('verifyCode'), 'verifyId': _res.get('result').get('verifyId')}
    return result


def md5(pwd: str, salt=''):
    md5 = hashlib.md5()
    pwd += salt
    md5.update(pwd.encode('utf-8'))
    return md5.hexdigest()


if __name__ == '__main__':
    print(get_verify_info())
