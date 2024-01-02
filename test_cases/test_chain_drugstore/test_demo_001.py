# coding=utf-8
"""

"""
import pytest
from common import get_excel_data, all_data


# @Time    :  2024-01-02 01:51:50
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  test_demo_001


class TestCaseA:

    @pytest.mark.parametrize('title,req_body,exp_resp', get_excel_data('登录模块', 'Login'))
    def test_a(self, title, req_body, exp_resp):
        """
            调用接口仅需要 : host, url, method, data 等
        """
        print()
        print(title)
        print(req_body)
        print(exp_resp)

    @pytest.mark.parametrize('case_data', all_data.get('登录模块', 'Login'))
    def test_b(self, case_data):
        print()
        print(case_data)


if __name__ == '__main__':
    pytest.main([
        '-vs',
    ])
