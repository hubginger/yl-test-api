# coding=utf-8
"""
    操作 Mysql, 支持元祖和字典的返回格式

    DoMySql(_id='全局元祖')
        : 创建一个返回结果为 tuple 的链接 , 命名为 "全局元祖"

    DoMySql(cursor_type='dict', _id='全局字典')
        : 创建一个返回结果为 dict 的链接 , 命名为 "全局字典"

"""

# @Time    :  2023-12-29 17:51:21
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  do_mysql

import pymysql
from common import do_conf, yl_log


class DoMySql:
    """
        MySQL 操作
        创建对象时, 建立连接
        销毁对象时, 断开连接

        销毁对象时 gc 的自动操作的, 我们不用显式断开连接
        缺点就是如果频繁进行数据库的断言和提值的话, 就会频繁建立和数据库的链接

        因此,
            可以创建一个全局对象,
            配置文件配置 autocommit: True,
            反复使用这个对象, 只要该对象未被 gc 回收, 就可以避免频繁创建连接
    """

    def __init__(self, db_conf='db', cursor_type: str = None, database=None, _id=None):
        """

            创建对象时, 建立链接并创建 cursor, 赋值给 self

        db_conf      :  配置文件的文件名, 用于区分不同数据库连接, 不用环境连接
        cursor_type  :  dict/其他 , 当为 dict 时候, cursor 会返回 dict
        database     :  库名, 如未指定, 则只连接数据库, 此时 sql 语句需要 database.table 进行查询. 如指定, 则连接该库, sql 语句只需要 table 即可
        _id          :  起名字, 如未指定, 则使用 id(self), 拿到对象的内存地址值作为 _id, 如指定, 则使用指定的内容作为 _id
        """
        if _id:
            self._id = _id
        try:

            _connection_info = do_conf.read_all(db_conf)
            connection_info = {
                'host': _connection_info.get('host'),
                'port': _connection_info.get('port'),
                'user': _connection_info.get('user'),
                'password': str(_connection_info.get('password')),
                'read_timeout': _connection_info.get('read_timeout'),
                'autocommit': _connection_info.get('autocommit'),
            }

            if cursor_type and cursor_type.lower() == 'dict':
                _cursor_type = pymysql.cursors.DictCursor
            else:
                _cursor_type = pymysql.cursors.Cursor

            if database:
                connection_info['database'] = database

            self.connection = pymysql.connect(**connection_info)
            self.cursor = self.connection.cursor(cursor=_cursor_type)

        except AttributeError as e:
            yl_log.exception('数据库连接失败，失败原因 %s', e)
        else:
            if _id:
                yl_log.info(f' < id: {_id} > 连接 MySql 成功')
            else:
                yl_log.info(f' < id: {id(self)} > 连接 MySql 成功')

    def __del__(self):
        """
            对象销毁时, 自动释放连接
            不用显式调用这两个 close() 方法
        """
        try:
            self.cursor.close()
            self.connection.close()
        except AttributeError as e:
            yl_log.exception('数据库连接失败，失败原因 %s', e)
        else:
            if hasattr(self, '_id'):
                yl_log.info(f' < id: {self._id} > 断开 MySql 成功')
            else:
                yl_log.info(f' < id: {id(self)} > 断开 MySql 成功')

    def select_one(self, sql, args=None):
        """
            sql = "insert into user values(1, 'ginger', 18)"
            sql = "insert into user values( %s, %s, %s)", args = (1, 'ginger', 18)
        """
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def select_all(self, sql, args=None):
        """
            sql = "insert into user values(1, 'ginger', 18)"
            sql = "insert into user values( %s, %s, %s)", args = (1, 'ginger', 18)
        """
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def __exec(self, sql, args=None):
        try:
            affected_rows = self.cursor.execute(sql, args)
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            self.connection.commit()
        return affected_rows

    def insert(self, sql, args=None):
        affected_rows = self.__exec(sql, args)
        return affected_rows

    def update(self, sql, args=None):
        affected_rows = self.__exec(sql, args)
        return affected_rows

    def delete(self, sql, args=None):
        affected_rows = self.__exec(sql, args)
        return affected_rows

    def exec_many(self, sql, args=None):
        """
            sql = "insert into user values( %s, %s, %s)",
            args = [(1, 'ginger', 18), (2, 'ginger', 18), (3, 'ginger', 18),]"
        """
        try:
            affected_rows = self.cursor.executemany(sql, args)
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            self.connection.commit()
        return affected_rows


if __name__ == '__main__':
    # 连接和释放:
    sql_database = DoMySql(cursor_type='dict', database='yl_common', _id='yl_common')

    # mysql 结果为 tuple :
    # """
    d = DoMySql()
    res = d.select_one('select * from yl_common.sms_verify_code limit 1')
    print(res)
    print(type(res))
    # """

    # mysql 结果为 dict :
    # """
    d = DoMySql(cursor_type='dict')
    res = d.select_one('select * from yl_common.sms_verify_code limit 1')
    print(res)
    print(type(res))
    # """
