# coding=utf-8
"""
    demo:
    crm 查询客户列表
"""
import os

import pytest

from common import BaseApi, BaseAssert, ALLURE_RESULT_FOLDER, ALLURE_REPORT_FOLDER, json_one, set2yml


# @Time    :  2024-01-04 15:17:55
# @Author  :  jiangtong
# @Email   :  gingerqgyy@outlook.com
# @Project :  yl_test_api
# @File    :  test_crm_

class TestCRM:

    def test_crm_page(self, token, page):
        url = 'https://crm-test.yljt.cn/api/crm/client/page'
        _res = BaseApi(token).send(uri=url, method='get', params=page)
        _exp = {'result': {'size': page['pageSize']}}
        BaseAssert.assert_common(_exp, _res, 'result', 'size')

        _id = json_one(_res, 'id')
        set2yml('_id', _id)


if __name__ == '__main__':
    pytest.main(
        ['--alluredir', ALLURE_RESULT_FOLDER, '--clean-alluredir']
    )
    os.system(f"allure generate {ALLURE_RESULT_FOLDER} -o {ALLURE_REPORT_FOLDER} --clean")
