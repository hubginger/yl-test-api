# coding=utf-8
"""
    MongDB说明 ( 类比 Mysql ) :

    Mysql 有数据库和表的概念
    在 MongoDB 中是数据库和集合的概念

    查询:
    Mysql:
        select * from Table where 1=1
    MongoDB:
        db.collection.find({'key':'value'})

    删除:
    Mysql:
        delete from Table where 1=1
    MongoDB:
        db.collection.deleteOne({'key':'value'})

    MongoDbUtil :
    不需要编写操作语句, 调用方法即可, 主要方法:
        select
        select_count
        delete
    参数统一为:
        database=None, collection=None, **kwargs
            database    是要操作的目标数据库, 当前统一为 : yl_share_platform , 支持指定 , 无需指定 ,
            collection  是目标集合, 需要传递, Excel 中有一列是 collection , 需要指定 ,
            **kwargs    是查询条件, 以关键字传参接收, 比如 查询 'name' 为 '张三' 的数据, 则传递 name='张三' 即可 ,
"""

# @Time    :  2023-12-29 17:51:31
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  do_mongo
from pymongo import MongoClient

from common import yl_log, do_conf
from common import do_conf


class MongoDbUtil:
    """
    操作 MongoDB
    用于数据验证和销毁
    """

    def __init__(self, db_conf='own_mongo', database=None, collection=None):
        """
            读取 db_conf 指定的配置文件, 默认是 mongo , 也就是 mongo.yml .
            如果传递了 database , 就读取该配置文件中指定的 database 下的具体链接信息
            如果没传递 database , 就读取该配置最外层定义的链接信息 , 针对某 database 定义了自己的用户名密码的情况
        """
        self._client = None
        self.db_conf = db_conf
        self.database = database
        self.collection = collection

        # 根据传递的 db_conf ( 配置文件名 ) 加载配置文件, 获取链接信息 :
        mongo_connection_s = do_conf.read_all(self.db_conf)

        # 读取配置文件 :
        __connection_info = {
            "host": mongo_connection_s['host'],
            "port": mongo_connection_s['port'],
            "username": mongo_connection_s['username'],
            "password": mongo_connection_s['password'],
            "database": database if database else mongo_connection_s['database'],
            "collection": collection if collection else mongo_connection_s['collection'],
        }
        # 如果传递了 database , 则加载配置文件中的 database 下的具体配置 : ( 当前不使用 )
        """
        # 这里 database 其实还有分类: 1. 配置文件中单独定义了 database 的链接, 走配置文件, 2. 配置文件中未定义, 走通用... 
        __connection_info.update(username=mongo_connection_s[database]['username'] if database else mongo_connection_s['username'])
        __connection_info.update(password=mongo_connection_s[database]['password'] if database else mongo_connection_s['password'])
        __connection_info.update(database=database if database else mongo_connection_s['database'])
        __connection_info.update(collection=collection if collection else mongo_connection_s['collection'])
        """
        yl_log.debug(f'__connection_info : {__connection_info}')
        self.__connection_info = __connection_info

    def _connect(self, database=None, collection=None):
        """
            链接 MongoDB 并进入对应集合
            关于 database :
                insert 调用时 ( 其他调用同理 ) ,
                    如果 insert 没传递, 则使用创建对象时传递的 database
                    如果 创建对象时也没传递, 则使用配置文件中定义的 database
            collection 同 database .

            当前一般场景 :
                database 直接使用配置文件中即可 , 也就是不需要传递
                collection 在创建对象时传递 , 使用创建对象时传递的 collection.
        """

        # 链接信息 :
        host = self.__connection_info['host']
        port = self.__connection_info['port']
        username = self.__connection_info['username']
        password = self.__connection_info['password']
        # 传递了 database , 则走传递的 database , 未传递则走配置文件中的 database : ( 一般在创建对象时指定 )
        database = database if database else self.__connection_info['database']
        # 传递了 collection , 则走传递的 collection , 未传递则走配置文件中的 collection : ( 一般在创建对象时指定 )
        collection = collection if collection else self.__connection_info['collection']

        # 链接格式 :
        _connection_info = f'mongodb://{username}:{password}@{host}:{port}?authSource=admin'
        if not self._client:
            self._client = MongoClient(_connection_info)

        # 链接 database 和 collection
        _db = self._client[database]
        _collection = _db[collection]
        return _collection

    def insert(self, database=None, collection=None, **kwargs):
        """
            插入数据
        """
        _database = database if database else self.database
        _collection = collection if collection else self.collection
        _coll = self._connect(_database, _collection)
        _res = _coll.insert_one(kwargs)
        yl_log.debug(f'MongoDB 新增 , 参数为: << {kwargs} >>')
        return _res

    def delete(self, database=None, collection=None, **kwargs):
        """
            删除单个结果
            直接使用关键字传参数即可
        """
        _database = database if database else self.database
        _collection = collection if collection else self.collection
        _coll = self._connect(_database, _collection)
        _res = _coll.delete_one(kwargs)
        yl_log.debug(f'MongoDB 删除 , 参数为: << {kwargs} >>')
        yl_log.debug(f'MongoDB 删除 , 删除的行数: << {_res.raw_result.get("n")} >> 行')
        return _res.raw_result.get('n')

    def update(self, query_value: dict = None, new_values: dict = None, database=None, collection=None):
        """
            更新数据,
        """

        _database = database if database else self.database
        _collection = collection if collection else self.collection
        _coll = self._connect(_database, _collection)

        # 先查询再更新, 调试时可放开, 方便调试
        # _query_res = self.select(**query_value)
        # yl_log.debug(f'MongoDB 更新 , 查询参数为: << {query_value} >> , 查询到结果: << {_query_res} >>')

        _res = _coll.update_one(query_value, new_values)
        yl_log.debug(f'MongoDB 更新 , 查询参数为: << {query_value} >> , 更新项: << {new_values} >>')

        _log_msg = '更新成功' if _res.raw_result.get("n") else '更新失败, 未匹配到数据'
        yl_log.debug(f'MongoDB 更新 , {_log_msg} , 更新的行数: << {_res.raw_result.get("n")} >>')
        return _res

    def select(self, database=None, collection=None, **kwargs):
        """
            查询单个结果
            直接使用关键字传参数即可
        """
        _database = database if database else self.database
        _collection = collection if collection else self.collection
        _coll = self._connect(_database, _collection)
        _res = _coll.find_one(kwargs)
        yl_log.debug(f'MongoDB 查询 , 查询参数为: << {kwargs} >> , 查询结果为: << {_res} >>')
        return _res

    def select_count(self, database=None, collection=None, **kwargs):
        """
            查询 数量 .
            直接使用关键字传参数即可
        """
        _database = database if database else self.database
        _collection = collection if collection else self.collection
        _coll = self._connect(_database, _collection)
        _res = _coll.count_documents(kwargs)
        yl_log.debug(f'MongoDB 查询 , 查询数量 ,  查询参数为: << {kwargs} >> , 查询结果为: << {_res} >>')
        return _res

    def select_all(self, database=None, collection=None, **kwargs):
        """
            查询多个结果, find 查出来是 Cursor 对象, 这里将 Cursor 对象转列表并返回.
            直接使用关键字传参数即可 , 要先传 database, collection
        """
        _database = database if database else self.database
        _collection = collection if collection else self.collection
        _coll = self._connect(_database, _collection)
        _res = list(_coll.find(kwargs))
        yl_log.debug(f'MongoDB 查询 , 查询参数为: << {kwargs} >> , 查询结果为: << {_res} >>')
        return _res

    def con(self, database=None, collection=None):
        return self._connect(database=database, collection=collection)


if __name__ == '__main__':
    _mongo = MongoDbUtil()
    res = _mongo.select(code='OK')
    print(res)
