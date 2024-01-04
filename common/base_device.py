# coding=utf-8
"""

"""

# @Time    :  2024-01-04 15:02:43
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  device

from enum import Enum


class Device(Enum):
    """
        pc 表示 pc 端
        app 表示 app 端           --->  医生 / 健管师
        public 表示 "患者app"     --->  患者

        a 运营端
        c CRM
        h 全病程

        根据 pc / app / public, 获取登录时的参数格式
        根据 pc_a / pc_c / pc_h / app_h / public_h, 获取登录时的 url

        为什么患者 app 是用 public 标识的?
            因为患者 app 的参数传递与医生和健管师的参数传递是不一样的
            患者 app 传递参数时, 多了 userType / canVerifyCode 参数
            又因为 userType 值为 PUBLIC_USER, 所以我们取 public 作为患者的 app 标识

        这个枚举就放在这里做提示作用好了, 其实没什么用, 传递参数时, 如果以枚举传递, 则无法调用 split('_') 方法 ...
    """
    PC_A: str = 'pc_a'
    PC_C: str = 'pc_c'
    PC_H: str = 'pc_h'
    APP_H: str = 'app_h'
    PUBLIC_H: str = 'public_h'
