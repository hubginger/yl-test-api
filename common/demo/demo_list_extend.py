# coding=utf-8
"""

"""

# @Time    :  2023-12-31 14:58:27
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  demo_list_extend


li = [1, 2, 3, ]
s = None
li.extend(s) if s else None
print(li.extend([4]))
