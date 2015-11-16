# encoding:utf-8
"""
操作数据库基础类
"""
import torndb

class BaseDb(object):

    def __init__(self):
        self.db = torndb.Connection(
            host="172.26.253.3",
            database="DomainWhois",
            user="root",
            password="platform",
            charset="utf8"
        )
