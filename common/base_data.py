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

from typing import Dict, List

from common.utils.do_conf import do_conf
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
        self.data: Dict[str, Dict[str, ExcelData]] = _data

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

            这里存在可以优化的空间, 就是当 scope 非 all 时, 直接生成 key , dict.get(key) 能更快拿到数据
            比如, scope='1' , case_id = 'Login', 则直接 all_data.get('Login001'), 就能很快取到数据, __match 方法肯定比直接字典直接取值慢
            不要小看这一点点的小提升, 如果每条用例都能明确 scope 范围, 不用 all, 那就是一个大提升, 前提每条用例都不用 all, 增加维护成本用以换取效率
        """
        res_data, _data = [], {}
        _data = self.data.get(sheet_name)
        for key, value in _data.items():
            if self.__match(case_id, key, scope):
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

            fetch 其实和 get 是一样的, 只不过 fetch 返回格式为 ('params': [row_obj_01, ...], 'ids':['case', ...])
            fetch 返回的格式, 直接拆包就是 fixture 要的关键字传参格式了
        """
        _data, res_params, res_ids, res_dict = {}, [], [], {'params': None, 'ids': None}
        _data = self.data.get(sheet_name)
        for key, value in _data.items():
            if self.__match(case_id, key, scope):
                res_params.append(value)
                res_ids.append('case')
        res_dict['params'] = res_params
        res_dict['ids'] = res_ids
        return res_dict

    def original(self, sheet_name, case_id, scope='all'):
        """
            原 yljk_api_test 项目中, 参数化时是直接将 'title,req_body,exp_resp' 以列表进行参数化的
            该 original 方法, 就是将 'title,req_body,exp_resp' 构造出来并以列表返回, 兼容老逻辑代码

            使用时, 最好先定义一个和原参数化同名的函数, 注意一定是函数, 不是类方法,
            然后该方法放在原 handle_excel 中, 注释掉函数即可,
            如此就可以无缝实现函数的逻辑替换了, 不用每个用例都去修改导包或者调用了,
        """
        _data: List[ExcelData] = self.get(sheet_name, case_id, scope=scope)
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

            增加逻辑 :
                根据 scope 来匹配
                scope 为 all 时, 全匹配, 也就是 Login001, Login002, Login003, LoginAdmin001, 根据 Login 匹配时, 取到 Login001, Login002, Login003
                scope 为 1-2 时, 取 1-2, 也就是 Login001, Login002,
                scope 传递具体数值时, 要保证 '-' 前的数值小于 '-' 后的数值
        """
        _res = True if target == current or (target.startswith(current) and target.strip(current).isdigit()) else False
        if _res and scope != 'all':
            start, over = str(scope).split('-') if '-' in str(scope) else (scope, scope)
            scope_s = [f'{current}{i:0>3}' for i in range(int(start), int(over) + 1)]
            _res = True if target in scope_s else False
        return _res


all_data = CaseData(do_conf.read_one('excel', 'file_name'))

if __name__ == '__main__':
    # get
    # """
    from time import time

    b = time()

    cd = CaseData('Delivery_System_V1.5.xlsx', '登录模块', )
    print(cd.data)
    match_data = cd.get('登录模块', 'Login', scope='1')
    for data in match_data:
        print('Login : ', data)

    cd = CaseData('Delivery_System_V1.5.xlsx')
    print(cd.data)
    match_data = cd.get('机构管理模块', 'Query_Ent', scope='1-4')
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
