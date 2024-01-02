# coding=utf-8
"""

"""
import requests

from common import do_conf


class BaseApi:
    """

    """

    def __init__(self, host, terminal='WEBPC', token=None):
        headers = {
            'terminal': terminal,
            'token': token
        }
        host_dict = do_conf.read_all('host')

        self.headers = headers
        self.host = host_dict.get(host)

    def request_send(self, uri, method, data=None, params=None, files=None, json=None, i_d=''):
        _res = requests.request(
            url=f'{self.host}{uri}{i_d}',
            method=method,
            headers=self.headers,
            data=data,
            params=params,
            files=files,
            json=json,
        )
        return _res.json()

    def query(self, uri, method, data):
        return self.request_send(data=data)

    def add(self, uri, method, data):
        return self.request_send(json=data)

    def update(self, uri, method, data):
        return self.request_send(json=data)

    def delete(self, uri, method, id):
        return self.request_send(id=id)

    def lock(self, uri, method, id):
        return self.request_send(id=id)

    # 文件上传
    def file_upload(self, file_path: str):
        # 1-获取文件名
        file_name = file_path.split('/')[-1]
        # 2-文件类型
        file_type = file_path.split('.')[-1]
        file = {'files': (file_name, open(file_path, 'rb'), file_type)}
        # 3-发送请求
        path = self.request_send(files=file)
        # 返回oss路径
        return path['result']


if __name__ == '__main__':
    base_req = {
        'url': 'a',
        'method': 'b',
        'terminal': 'c',
        'token': 'd',
        'type': 'e',
        'parameters': 'f'
    }
    b = BaseApi(**base_req)
    b.request()
