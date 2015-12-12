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
            
            
    def get_speed(self,period):
        period = period.split('-')
        if period[0]=='one':
            top = 2
        elif period[0]=='three':
            top = 4
        elif period[0]=='seven':
            top = 8
        elif period[0]=='twelve':
            top = 13
            
        if period[1]=='hours':
            table_name = 'whois_sum'
            flag = 'tld_sum'
        else:
            table_name = 'whois_sum_by_day'
            flag = 'sum'
        
        sql = 'SELECT %s FROM %s ORDER BY insert_time DESC LIMIT %s' % (flag,table_name,top)
        results = self.db.query(sql)
        length = len(results)
        total = 0
        for i in xrange(1,length):
            total = total + results[i-1][flag]-results[i][flag]
        
        if period[1]=='hours':
            return total/(length-1)
        else:
            return total/((length-1)*24)