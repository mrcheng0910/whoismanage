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
        return int(domain_sum / 1000000)

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
        sql = ' SELECT sum(whois_sum) as whois_sum FROM tld_whois_sum '
        result = self.db.query(sql)
        whois_sum = result[0]['whois_sum']
        return int(whois_sum / 1000)

    def get_tld_whois_flag(self, top=10):
        """获取各个标志位的whois域名数量
        :type top: int
        :rtype result: list
        """
        # 1.先获取whois数量排名前10的顶级后缀
        # 2.再获取前十名当中的tld，标记位和数量
        sql = "SELECT tld,flag,sum(whois_sum) as whois_sum FROM tld_whois_flag WHERE tld \
                in (SELECT tld FROM (SELECT tld FROM tld_whois_flag GROUP BY tld \
                 ORDER BY sum(whois_sum) DESC LIMIT %s) as t) GROUP BY tld,flag" % top
        result = self.db.query(sql)
        return result
