# -*- coding: utf-8 -*-
# @File    : handle_excel.py
# @Time    : 2022/3/30 21:29
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2022/3/30
"""
#用例挑选
    1- 全部运行 all    默认模式
    2- 只选择某一个  tc003
    3- 连续用例 tc003-tc005
    4- 组合型  ['tc003','tc005-tc007','tc009']
"""
import xlrd
import os

get_yaml_data = {'file_name': 'Delivery_System_V1.5.xls', 'col_name': ['标题', '请求参数', '响应预期结果']}
config_path = r'D:\Common\Job\codes\yljk_api_test\yljk_api_test\yljk_api_test/configs'
data_path = r'D:\Common\Job\codes\yljk_api_test\yljk_api_test\yljk_api_test/data\Delivery_System_V1.5.xls'


def get_excel_data(sheet_name, case_name, run_case=['all']):  # *['标题','请求参数','响应预期结果']
    """
    :param file_path: 文件的路径
    :param sheet_name: 具体操作的sheet名
    :return: [(),()]
    """

    # ---------------------------------
    # 读取excel配置文件
    config_data = {'file_name': 'Delivery_System_V1.5.xls', 'col_name': ['标题', '请求参数', '响应预期结果']}
    # excel路径获取函数
    file_path = data_path
    # Excel 表头
    args = config_data['col_name']

    # args 就是那三列

    # ---------------------------------

    res_list = []  # 存放结果的
    # 1-打开excel文件
    # formatting_info = True  保持原样式
    work_book = xlrd.open_workbook(file_path, formatting_info=True)
    # 2-指定对应的表
    # print(work_book.sheet_names())#查看所有的表名

    # 获取 Sheet :    (连锁企业管理)
    work_sheet = work_book.sheet_by_name(sheet_name)

    # print(work_sheet.row_values(0))#打印第一行数据
    # print(work_sheet.col_values(0))  # 打印第一列数据

    # --------------列名--转化--列下标-------------
    # args == ['标题','请求参数','响应预期结果']

    col_indexs = []  # 列表

    # 列名是第0行数据
    for col_name in args:  # args 元组
        col_indexs.append(work_sheet.row_values(0).index(col_name))

        # col_name 就成了表头那三列对应的列号

    # print('需要获取的列名--->',col_indexs)
    # ------------------------------------------

    # ----------------用例筛选--------------------

    # 组合型  ['all','003','005-007','009']
    run_case_data = []  # 需要运行的用例

    if 'all' in run_case:  # 所有的用例全部运行！
        run_case_data = work_sheet.col_values(0)  # ['Login003']
    else:  # 不是全部运行---['003','005-007','009']
        for one in run_case:  # one == '003','005-007','009'
            if '-' in one:  # 连续的用例---'005-007'
                start, end = one.split('-')  # 获取对应的数值 '005'  '007'--字符串类型
                for num in range(int(start), int(end) + 1):
                    run_case_data.append(case_name + f'{num:0>3}')  # 5 6 7---Login005
            else:  # 不连续的用例---'005'
                run_case_data.append(case_name + f'{one:0>3}')

    # -----------------------------------------

    # for item in run_case_data:
    #     print(item)

    # 取出 Excel 中的具体数据
    # 3-获取指定数据
    row_idx = 0
    for one in work_sheet.col_values(0):
        if case_name in one and one in run_case_data:  # listShoping in listShoping005
            # req_body = work_sheet.cell(row_idx,9).value#cell(行编号，列编号)
            # resp_data = work_sheet.cell(row_idx, 11).value  # cell(行编号，列编号)
            col_datas = []  # 每一行所有获取的列数据
            for num in col_indexs:  # [4, 9, 11]
                tmp = is_josn(work_sheet.cell(row_idx, num).value)  # cell(行编号，列编号)
                col_datas.append(tmp)

            res_list.append(tuple(col_datas))  # [(1,2,3),(1,2,3)]   通过 parametrize  注入
        row_idx += 1  # 下一行循环

    for item in res_list:
        pass

    return res_list


# -------自己根据需求写函数-----------------
import json


def is_josn(inStr):  # 返回值 ： 是  ,不是
    try:
        return json.loads(inStr)  # 没有报错---可以转化为字典 --就json格式
    except:
        return inStr  # 返回需要判断的字符串--不是json字符串


# --------------------------------------
if __name__ == '__main__':
    # conf_data = ['请求参数', '响应预期结果']
    from time import time

    b = time()
    res = get_excel_data('机构管理模块', 'Add_Merchant')  # *[]  解包
    print('res : ', res)
    print(time() - b)

    # res = get_excel_data('登录模块', 'Login', run_case=['001'])  # *[]  解包
    # print(res)
    # for one in res:
    #     print(one)

    from common import all_data

    b = time()


    def get_excel_datas(x, xx):
        return all_data.original(x, xx)


    res = get_excel_datas('机构管理模块', 'Add_Merchant')
    print('res : ', res)
    print(time() - b)
