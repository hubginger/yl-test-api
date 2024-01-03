# coding=utf-8
"""
    发起请求
"""
import hashlib

import requests

from common import do_conf


class BaseApi:
    """
        发起请求
    """

    def __init__(self, token=None, terminal='WEBPC', host='a', ):
        """
            terminal 默认为 WEBPC, 当 terminal 不为 WEBPC 时, 需创建对象的位置传递 terminal
                可能为 :
                    APP_DOCTOR
                    MINIPROGRAM_AGENT
                    MINIPROGRAM_DOCTOR
                    MINIPROGRAM_DRUG_STORE
                    MINIPROGRAM_YLHEALTH
                    MINIPROGRAM_CLOUDDIAG
                    WOA_YLJT
                    WOA_YLHEALTH
                    ...
            host 默认为 a
                可能为 :
                    a  --->  对应运营端
                    h  --->  对应科室端
                    c  --->  对应CRM端
            token 默认为 None
                实际登录之后, 传 token
        """

        host_dict = do_conf.read_all('request')
        self.host = host_dict.get('host').get(host)
        self.verify_code_url = host_dict.get('verify_url').get(host)

        headers = {'terminal': terminal, 'token': token}
        self.headers = headers

    def send(self, uri, method, data=None, params=None, files=None, json=None, i_d=''):
        _res = requests.request(
            url=f'{self.host}{uri}{i_d}',
            method=method,
            data=data,
            params=params,
            files=files,
            json=json,
        )
        return _res.json()

    # 文件上传
    def file_upload(self, uri, method, file_path: str):
        file_name = file_path.split('/')[-1]
        file_type = file_path.split('.')[-1]
        file = {'files': (file_name, open(file_path, 'rb'), file_type)}
        path = self.send(uri=uri, method=method, files=file)
        return path['result']

    # 需自行封装 get / post / put / delete 等接口


class BaseLogin(BaseApi):

    @classmethod
    def __md5(cls, pwd: str, salt=''):
        md5 = hashlib.md5()
        pwd += salt
        md5.update(pwd.encode('utf-8'))
        return md5.hexdigest()

    def __verify_info(self):
        """ 根据 terminal 标记来获取验证码 """
        verify_code_url = self.verify_code_url
        response = requests.get(url=verify_code_url).json()
        result = {'verifyCode': response['result']['verifyCode'], 'verifyId': response['result']['verifyId']}
        return result

    def login(self, username, password=None):
        password = password if password else 'dc483e80a7a0bd9ef71d8cf973673924'
        _verify_info = self.__verify_info()
        # 构造登录数据

        # 登录

        # 返回 token
        return None


if __name__ == '__main__':
    pass
    # 调试, crm 登录:
    # """
    crl_login_url = ''
    # """
