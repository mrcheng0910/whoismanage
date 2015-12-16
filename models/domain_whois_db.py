# encoding:utf-8

from base_db import BaseDb


class DomainWhoisDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def get_tld_whois_flag(self, top=10):
        """获取各个标志位的whois域名数量
        :type top: int
        :rtype result: list
        """
        # 1.先获取whois数量排名前10的顶级后缀
        # 2.再获取前十名当中的tld，标记位和数量
        sql = 'SELECT tld,flag,sum(whois_sum) as whois_sum FROM tld_whois_flag WHERE tld \
                in (SELECT tld FROM (SELECT tld FROM tld_whois_flag GROUP BY tld \
                 ORDER BY sum(whois_sum) DESC LIMIT %s) as t) GROUP BY tld,flag' % top
        result = self.db.query(sql)
        return result
    
    def get_assignment_tld_flag(self,tld='net'):
        """获取指定域名后缀的标记位情况"""
        sql = 'SELECT flag,flag_detail,whois_sum FROM tld_whois_flag WHERE tld=%s'
        result =self.db.query(sql,tld)
        return result
    
    def get_assignment_type(self,whois_type='1'):
        """
        获取指定类型的whois分布情况
        """
        
        sql = 'SELECT tld, sum(whois_sum) AS total FROM tld_whois_flag WHERE flag=%s GROUP BY tld'
        results_type = self.db.query(sql,whois_type)
        
        sql = 'SELECT  tld,SUM(whois_sum) AS total FROM tld_whois_flag WHERE (tld in (SELECT tld            FROM tld_whois_flag WHERE flag = %s GROUP BY tld)) AND flag <> %s GROUP BY tld'
        results_no_type = self.db.query(sql,whois_type,whois_type)
        
        return results_type,results_no_type
    
    
    def get_detect(self):
        """
        获取已探测域名和未探测域名的数量
        :return:
        """
        results = []
        detect_sql = "SELECT tld,sum(whois_sum) as detect_sum FROM tld_whois_flag GROUP BY tld"
        detect_results = self.db.query(detect_sql)
        sum_sql = "SELECT tld_name,domain_num FROM domain_summary WHERE tld_name in(SELECT tld FROM tld_whois_flag) ORDER BY domain_num DESC "
        sum_results = self.db.query(sum_sql)

        for sum_value in sum_results:
            for detect_value in detect_results:
                if detect_value['tld']==sum_value['tld_name']:
                    results.append({'tld':detect_value['tld'],
                                    'detected':detect_value['detect_sum'],
                                    'undetected':sum_value['domain_num']-detect_value['detect_sum']})
        return results