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
            
            
    def get_detecting_tld(self):
        """
        获得最近一小时的域名whois后缀
        """
        results = []
        sql_not_exist= 'SELECT tld,whois_sum FROM (SELECT *  FROM tld_whois_sum_history \
              WHERE update_time BETWEEN DATE_SUB(NOW(),INTERVAL 1 HOUR)  AND NOW()) as t1 \
              WHERE NOT EXISTS (SELECT * FROM (SELECT *  FROM tld_whois_sum_history \
              WHERE update_time BETWEEN DATE_SUB(NOW(),INTERVAL 2 HOUR) \
              AND DATE_SUB(NOW(),INTERVAL 1 HOUR) ) as t2 WHERE t1.tld=t2.tld)'
        results_not_exist = self.db.query(sql_not_exist)
        
        sql_change = 'SELECT t1.tld,t1.whois_sum AS n_num,t3.whois_sum AS p_num FROM \
                      (SELECT *  FROM tld_whois_sum_history WHERE update_time \
                      BETWEEN DATE_SUB(NOW(),INTERVAL 1 HOUR)  AND NOW()) as t1 \
                      JOIN (SELECT * FROM (SELECT *  FROM tld_whois_sum_history \
                      WHERE update_time BETWEEN DATE_SUB(NOW(),INTERVAL 2 HOUR) \
                      AND DATE_SUB(NOW(),INTERVAL 1 HOUR) ) as t2) as t3 ON t1.tld = t3.tld AND t1.whois_sum<>t3.whois_sum'
        results_change = self.db.query(sql_change)
        if  results_not_exist:
            for value in results_not_exist:
                results.append({'tld':value['tld'],'num':value['whois_sum']})
        if  results_change:
            for value in results_change:
                results.append({'tld':value['tld'],'num':(int(value['n_num'])-int(value['p_num']))})
        return results
        