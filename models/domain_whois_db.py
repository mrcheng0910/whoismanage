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
        # 1.先获取whois数量排名前10的顶级后缀 CAST(sum(number)/count(number) as UNSIGNED)
        # 2.再获取前十名当中的tld，标记位和数量
        sql = 'SELECT tld,flag,CAST(sum(whois_sum) as UNSIGNED) AS whois_sum FROM tld_whois_flag WHERE tld \
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
        
        sql = 'SELECT tld, CAST(sum(whois_sum) as UNSIGNED) AS total FROM tld_whois_flag WHERE flag=%s GROUP BY tld'
        results_type = self.db.query(sql,whois_type)
        
        sql = 'SELECT tld, CAST(sum(whois_sum) as UNSIGNED) AS total FROM tld_whois_flag WHERE (tld in (SELECT tld            FROM tld_whois_flag WHERE flag = %s GROUP BY tld)) AND flag <> %s GROUP BY tld'
        results_no_type = self.db.query(sql,whois_type,whois_type)
        
        return results_type,results_no_type
    
    
    def get_detect(self,top_num=10):
        """
        获取已探测域名和未探测域名的数量
        :param top_num:
        :return: results 结果
        注意：sum返回的数据类型为Decimal,Decimal不能使用json，所以把它转为int
        """
        results = []
        detect_sql = 'SELECT tld,SUM(whois_sum) as detect_sum FROM tld_whois_flag GROUP BY tld'
        detect_results = self.db.query(detect_sql)
        sum_sql = 'SELECT tld_name, domain_num FROM domain_summary WHERE tld_name IN(SELECT tld FROM tld_whois_flag) ORDER BY domain_num DESC LIMIT %s'
        sum_results = self.db.query(sum_sql,int(top_num))
        for sum_value in sum_results:
            for detect_value in detect_results:
                if detect_value['tld']==sum_value['tld_name']:
                    results.append({
                        'tld': detect_value['tld'],
                        'detected': int(detect_value['detect_sum']),
                        'undetected':int(sum_value['domain_num'])-int(detect_value['detect_sum'])
                    })
        return results
     
    def get_tld_detect(self, tld):
        """
        获取指定域名后缀的探测情况
        """
        result = []
        detected_sql = 'SELECT sum(whois_sum) as detect_sum FROM tld_whois_flag WHERE tld = %s'
        detected_result = self.db.query(detected_sql,tld)
        total_sql = 'SELECT domain_num FROM  domain_summary WHERE tld_name = %s'
        total_result = self.db.query(total_sql,tld)
        result.append({
            'tld': tld,
            'detected': int(detected_result[0]['detect_sum']),
            'undetected': int(total_result[0]['domain_num']-detected_result[0]['detect_sum'])
        })
        return result