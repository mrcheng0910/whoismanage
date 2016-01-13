# encoding:utf-8
"""
数据库表内容

"""

from base_db import BaseDb
from collections import defaultdict


class TableOverallDb (BaseDb):
    def __init__(self):
        BaseDb.__init__ (self)  # 执行父类

    def get_table_info(self):
        sql = 'SELECT table_name,flag_no_connect,flag_undetected,flag_reg_info,flag_reg_date,flag_no_svr,flag_part_info FROM table_overall_history  ORDER BY update_time DESC,table_name DESC LIMIT 28'
        results = self.db.query (sql)
        return results

    def get_data_history(self, table_name):
        sql = 'SELECT flag_no_connect,flag_undetected,flag_reg_info,flag_reg_date,flag_no_svr,flag_part_info,update_time FROM `table_overall_history` WHERE table_name = %s ORDER BY update_time DESC LIMIT 12'

        results = self.db.query (sql, table_name)
        return results

    def fetch_table_increase(self, top=6):
        rows = top * 28  # 总共需要获取的行数
        sql = 'SELECT * FROM table_overall_history  order by update_time desc limit %s' % (rows)
        results = self.db.query (sql)
        tb_increase,tb_total = self._mange_data (results)
        return tb_increase, tb_total

    def _mange_data(self, results):
        """
        将各个表中数据添加为字典
        :param results:原始数据
        :return: 整理后的数据
        """
        tb_increase = defaultdict (list)  # 表whois信息探测增长率
        tb_total =defaultdict(list)  # 表中域名总数
        for item in results:
            tb_domains = item['flag_undetected'] + item['flag_no_connect'] + item['flag_no_svr'] + \
                         item['flag_reg_info'] + item['flag_reg_date'] + item['flag_part_info']

            tb_increase[item['table_name']].append (tb_domains - item['flag_undetected'])
            tb_total[item['table_name']].append(tb_domains)
        return tb_increase,tb_total

