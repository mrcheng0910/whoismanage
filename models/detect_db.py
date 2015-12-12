# encoding:utf-8

from base_db import BaseDb
import time
import datetime

class DetectDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

        
    def manage_increase(self,start_date,end_date):
        """获取域名whois增量"""
        
        if start_date == "None":
            sql = 'SELECT tld_sum as sum,insert_time FROM `whois_sum` WHERE TO_DAYS(insert_time) BETWEEN TO_DAYS(NOW()) AND TO_DAYS(NOW()) ORDER BY insert_time DESC'
            return self.db.query(sql)
        
        elif start_date==end_date:
            sql = "SELECT tld_sum as sum,insert_time FROM whois_sum WHERE DATE_FORMAT(insert_time,'%%Y-%%m-%%d') BETWEEN %s AND %s ORDER BY insert_time DESC"
            results = self.db.query(sql,str(start_date),str(end_date))
            return results
            
        else:
            # test = time.strftime(start_date,'%Y-%m-%d')
            start = datetime.datetime.strptime(start_date,'%Y-%m-%d')
            start_previous= (start-datetime.timedelta(days=1)).strftime('%Y-%m-%d') # 增加一天时间是用来统计增长率
            sql = 'SELECT sum,insert_time FROM whois_sum_by_day WHERE DATE_FORMAT(insert_time,"%%Y-%%m-%%d") BETWEEN %s AND %s ORDER BY insert_time DESC'
            results = self.db.query(sql,str(start_previous),str(end_date))
            return results