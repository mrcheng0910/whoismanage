# encoding:utf-8
import torndb
from base_db import BaseDb

class TldDb(BaseDb):

    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def get_tlds(self):
        tlds = []
        sql = "SELECT * FROM tld_details"
        tlds = self.db.query(sql)
        return tlds