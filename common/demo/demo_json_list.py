# coding=utf-8
"""

"""
from jsonpath import jsonpath

# @Time    :  2024-01-04 17:58:04
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  demo_json_list


s1 = jsonpath({'a': 'a'}, '$.a')
s2 = jsonpath({'a': 'a'}, '$.b')
print(s1)
print(s2)

print(s1[0])

if s2:
    print(s2[0])
