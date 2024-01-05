# coding=utf-8
"""

"""

# @Time    :  2024-01-03 15:37:41
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  demo_time


import time

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))
print(time.time())
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int('1704267177121'[:-3]))))
