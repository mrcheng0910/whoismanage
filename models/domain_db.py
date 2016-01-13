# encoding:utf-8
"""
获取域名相关的数据
作者：程亚楠
更新：2016.1.12
优化代码

"""
from base_db import BaseDb


class DomainDb(BaseDb):

    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def fetch_domain(self, top=10):
        """获取各个顶级域名数量
        :param top: 排名前top
        :returns
            domains:顶级域名和数量列表
            total:域名总数
        """
        sql = "SELECT tld_name,domain_num FROM domain_summary ORDER BY domain_num DESC"
        domains = self.db.query(sql)
        total = sum([item['domain_num'] for item in domains])  # 得到域名总数
        domains = domains[:top]
        total_top = sum([item['domain_num'] for item in domains])  # 得到前top域名总数
        domains.append({'tld_name': 'Other', 'domain_num': total - total_top})  # 添加top之外顶级域名情况
        return domains, total

    def get_tld_num(self,tld):
        """
        获得制定域名后缀的域名数量
        :param tld:string 域名顶级后缀
        :return: total:int 域名总数
        :return: tld_num: int 顶级后缀域名数量
        :return: whois_num: int 顶级后缀已探测数量
        """

        sql = 'SELECT  \
              (SELECT SUM(domain_num) FROM   domain_summary ) AS total,\
              (SELECT domain_num FROM   domain_summary WHERE tld_name="%s") AS tld,\
              (SELECT whois_sum FROM `tld_whois_sum_history` WHERE tld="%s" ORDER BY update_time DESC LIMIT 1) AS whois_tld,\
              (SELECT tld_sum FROM `whois_sum` ORDER BY insert_time DESC LIMIT 1) AS whois_total'%(tld,tld)

        results = self.db.query(sql)
        print results
        # total = results[0]['total']
        # tld_num = results[0]['tld']
        # whois_tld = results[0]['whois_tld']
        # whois_total = results[0]['whois_total']
        # return total,tld_num,whois_tld,whois_total
        return results