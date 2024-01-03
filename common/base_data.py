"""
    file_name = Delivery_System_V1.5.xlsx

    注意如果新增一个 Excel 文件, 理应重新编辑一个单例类

    do_excel 中, 封装了读取所有 Excel 数据的方法
    但是参数化时, 是参数化一部分数据
    因此需要将 Excel 数据读取到内存, 然后从内存中再找到参数化的数据
    读取出来的格式 :
    read 读取出来是一个键值对, read_all 读取出来是一个 sheet 页一个键值对
        {
            'sheet_1':
                {
                    'case_id_1': row_1,
                    'case_id_2': row_2,
                    'case_id_3': row_3,
                },
            'sheet_2':
                {
                    'case_id_1': row_1,
                    'case_id_2': row_2,
                    'case_id_3': row_3,
                }, ... ,
        }
"""
import threading
from typing import Dict

from common import do_conf
from common.utils.do_excel import DoExcel, ExcelData


# @Time    :  2024-01-01 22:28:14
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  base_data


class CaseData:

    def __init__(self, file_name, sheet_name=None):
        """
            传递了 sheet_name, 则仅读取:  该 sheet
            未传递 sheet_name, 则会读取:  全 sheet
            read 和 read_all 的返回数据格式都是一致地

            通过 self.data 存储 Excel 中所有的数据
        """
        _excel = DoExcel(file_name, sheet_name)
        _data = _excel.read() if sheet_name else _excel.read_all()
        self.data: dict[str, Dict[str, ExcelData]] = _data

    def get(self, sheet_name, case_id, scope='all'):
        """
            获取 Excel 以 case_id 开头的数据

            列表嵌套对象的格式返回
            对象为每一条数据, Excel 中的行

            匹配规则:
                对数据 :
                    add_user / add_user001 / add_user002 / add_user_doctor / add_user_agent001 / add_user_agent002 / user
                使用如下参数进行匹配 :
                    add_user
                可以满足的匹配为:
                    add_user / add_user001 / add_user002
        """
        res_data, _data = [], {}
        _data = self.data.get(sheet_name)
        for key, value in _data.items():
            if self.__match(case_id, key):
                res_data.append(value)
        return res_data

    def fetch(self, sheet_name, case_id, scope='all'):
        """
            获取 Excel 以 case_id 开头的数据

            字典返回, 字典就两个 key, 分别为: params, ids
            params :  匹配到的数据
              ids :   和 params 长度一致, 值均为 'case'

            匹配规则:
                对数据 :
                    add_user / add_user001 / add_user002 / add_user_doctor / add_user_agent001 / add_user_agent002 / user
                使用如下参数进行匹配 :
                    add_user
                可以满足的匹配为:
                    add_user / add_user001 / add_user002
        """
        _data, res_params, res_ids, res_dict = {}, [], [], {'params': None, 'ids': None}
        _data = self.data.get(sheet_name)
        for key, value in _data.items():
            if self.__match(case_id, key):
                res_params.append(value)
                res_ids.append('case')
        res_dict['params'] = res_params
        res_dict['ids'] = res_ids
        return res_dict

    def original(self, sheet_name, case_id, scope='all'):
        """
            原 yljk_api_test 项目中, 参数化时是直接将 'title,req_body,exp_resp' 以列表进行参数化的
            该 compatibility 方法, 就是将 'title,req_body,exp_resp' 构造出来并以列表返回
        """
        _data: list[ExcelData] = self.get(sheet_name, case_id)
        _data_s = []
        for item in _data:
            _data_s.append([item.title, item.data, item.expected_response])
        return _data_s

    @staticmethod
    def __match(current: str, target: str, scope='all'):
        """
            对 target 判断是否是 current 或者 current + 数值
            如果是则返回 True
            如果不是则返回 False
            1.
                target  : login
                current : login
                return  : True
            2.
                target  : login001
                current : login
                return  : True
            3.
                target  : login_crm
                current : login
                return  : False
            4.
                target  : doctor
                current : login
                return  : False
        """
        _res = False
        if target == current:
            _res = True
        elif target.startswith(current) and target.strip(current).isdigit():
            _res = True
        return _res


all_data = CaseData(do_conf.read_one('excel', 'file_name'))

if __name__ == '__main__':
    # get
    # """
    from time import time

    b = time()

    cd = CaseData('Delivery_System_V1.5.xlsx', '登录模块')
    print(cd.data)
    match_data = cd.get('登录模块', 'Login', )
    for data in match_data:
        print('Login : ', data)

    cd = CaseData('Delivery_System_V1.5.xlsx')
    print(cd.data)
    match_data = cd.get('机构管理模块', 'Query_Ent', )
    for data in match_data:
        print('Query_Ent : ', data)

    e = time()
    print('持续时间: ', e - b)

    print('**' * 20)
    # """

    # original
    # """
    cd = CaseData('Delivery_System_V1.5.xlsx', '登录模块')
    _all = cd.original('登录模块', 'Login', )
    print(_all)
    # """
