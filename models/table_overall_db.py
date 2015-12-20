# encoding:utf-8
import torndb
from base_db import BaseDb

class TableOverallDb(BaseDb):

    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def get_table_info(self):
        sql = 'SELECT table_name,flag_no_connect,flag_undetected,flag_reg_info,flag_reg_date,flag_no_svr,flag_part_info FROM table_overall_histroy GROUP BY table_name ORDER BY update_time DESC,table_name DESC LIMIT 28'
        results = self.db.query(sql)
        return results
        
    def get_data_history(self,table_name):
        sql = 'SELECT flag_no_connect,flag_undetected,flag_reg_info,flag_reg_date,flag_no_svr,flag_part_info,update_time FROM `table_overall_histroy` WHERE table_name = %s ORDER BY update_time DESC LIMIT 12'
        
        results = self.db.query(sql,table_name)
        return results