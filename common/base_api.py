# coding=utf-8
"""
    发起请求
"""
import hashlib
from time import time

import allure
import requests

from common.base_device import Device
from common.utils.do_conf import do_conf
from common.utils.do_log import yl_log
from common.utils.do_slow_api import AnswerTime


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

    @allure.step('请求')
    @AnswerTime()
    def send(self, uri: str, method: str, data=None, params=None, files=None, json=None, i_d=''):
        url = uri if uri.startswith('http') else f'{self.host}{uri}{i_d}'
        params.update({'_t': int(time())}) if params else None
        _res = requests.request(url=url, method=method, data=data, params=params, files=files, json=json, headers=self.headers)
        yl_log.debug(f'接口地址 : {url}')
        yl_log.debug(f'响应结果 : {_res.content.decode('utf-8')}')
        # try:
        #     _resp = _res.json()
        # except (BaseException,):
        #     _resp = _res.content.decode('utf8')
        _res.encoding = 'utf-8'
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

    def __verify_info(self, device: str = 'pc'):
        """
            根据 device 标记来获取验证码
            device 仅可以为: pc / app / mini
            当为 pc 时, 查询验证码, 返回 code 和 id 组成的字典
            不为 pc 时, 不查验证码, 返回空字典, 空字典是为了无缝 update , 机智吧, 哈哈哈
        """
        result = {}
        if device and device.strip().lower() == 'pc':
            _res = self.send(uri=self.verify_code_url, method='get')
            result = {'verifyCode': _res.get('result').get('verifyCode'), 'verifyId': _res.get('result').get('verifyId')}
        return result

    def login(self, uri, username, method='post', password=None, device='pc'):
        """
            username 为登录时的用户名或手机号, 如果是 app 端, 通过手机号登录, 则 username 传手机号,

            password 可以不传, 因为测试环境都是默认密码, 默认密码进行 md5 加密, 始终都是: dc483e80a7a0bd9ef71d8cf973673924
                如果哪一天默认密码统一调整了, 那就调用 __md5 生成一个, 如果不是 md5 加密了, 就封装新的加密算法

            device 仅可传, pc / app / mini , 标识三端, 当前三端不同用户登录所传的参数格式都是一样的, 如果登录根据用户不同而不同, 此处逻辑需调整
                device 默认为 pc, 根据 device 的值, 去 login.yml 中可以查看登录参数的格式
        """
        # 参数处理 :
        login_info = do_conf.read_one('login', device)
        password = password if password else do_conf.read_one('login', 'password')
        _verify_info = self.__verify_info(device)

        login_info['loginId'] = username
        login_info['password'] = password
        login_info.update(_verify_info)

        # 登录 :
        _res = self.send(uri, method, json=login_info)
        _token = None
        if _res:
            _token = _res.get('result').get('token')

        # 返回 token :
        return _token

    @allure.step('登录')
    def simple_login(self, username, password=None, device='pc_a'):
        """
            简化登录, 最少只需要一个参数, 即可登录 , (username)
            username  就是登录的用户名/手机号
            password  原密码, 如果没有修改原密码, 则不用传
            device    两部分组成, 用下划线区分
                device 当前仅支持:
                    pc_a          pc 端, 运营端
                    pc_c          pc 端, CRM
                    pc_h          pc 端, 全病程
                    app_h         app 端, host 为全病程
                    public_h      app 端, host 为全病程, 专为患者服务, 患者登录时和医生与健管师不一致

            该方法需维护
            当有其他参数类型, 有其他端时, 需要到 login.yml 中维护数据
        """

        # 根据 pc_c 中的 pc, 从 login.yml 配置文件中取登录时的参数格式. 根据 pc_a 从 login.yml 中取登录时的 url.
        _terminal = device.split('_')[0]
        login_info = do_conf.read_one('login', _terminal)
        login_url = do_conf.read_one('login', device)
        password = password if password else do_conf.read_one('login', 'password')
        _verify_info = self.__verify_info(_terminal)

        login_info['loginId'] = username
        login_info['password'] = password
        login_info.update(_verify_info)

        # 登录 :
        _res = self.send(login_url, 'post', json=login_info)
        _token = None
        if _res:
            _token = _res.get('result').get('token')

        # 返回 token :
        return _token


if __name__ == '__main__':
    pass
    # 调试, 全病程登录 :
    # """
    __uri = 'https://h-test.yljk.cn/api/yft/user/agency_user/username_pwd/sign_in'
    __method = 'post'
    __token = BaseLogin(host='h').login(uri=__uri, method=__method, username='test_admin')
    print(__token)
    # """

    # 调试, 患者登录 :
    # """
    __uri = ''
    __method = ''
    __token = BaseLogin().login(uri=__uri, method=__method, username='test_admin')
    print(__token)
    # """
