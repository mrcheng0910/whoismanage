# encoding:utf-8

from base_db import BaseDb


class IndexDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def get_domain_num(self):
        """获取数据库中域名总数"""
        domain_sum = 0
        sql = 'SELECT SUM(domain_num) AS domain_sum FROM domain_summary'  # 求和
        domain_sum = self.db.query(sql)[0]['domain_sum']
        return round(domain_sum/1000000,2)

    def get_tld_num(self):
        """获取域名顶级后缀"""
        tld_num = 0
        sql = 'SELECT count(*) AS tld_num FROM tld_details'
        tld_num = self.db.query(sql)[0]['tld_num']
        return tld_num

    def get_svr_sum(self):
        """获取WHOIS服务器（主/次）数量"""
        # msvr_sum = ssvr_sum = 0
        sql = 'SELECT msvr,ssvr FROM msvr_ssvr'
        result = self.db.query(sql)
        msvr_sum = result[0]['msvr']
        ssvr_sum = result[0]['ssvr']
        return msvr_sum, ssvr_sum

    def get_whois_sum(self):
        """获取数据库中已有域名whois信息的数量"""
        whois_sum = 0
        sql = 'SELECT tld_sum FROM `whois_sum` ORDER BY insert_time DESC LIMIT 1'
        result = self.db.query(sql)
        whois_sum = result[0]['tld_sum']
        print whois_sum
        return round(whois_sum/1000000.0,2)
        
    def get_increase(self,top=11):
        """获取域名whois增量"""
        sql = 'SELECT sum,insert_time FROM whois_sum_by_day order by insert_time desc limit %d' % top
        results = self.db.query(sql)
        # print results
        return results