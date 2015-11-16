# encoding:utf-8
import torndb
import json
from base_db import BaseDb

class DomainDb(BaseDb):

    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def get_domain(self, num=10):
        """获取各个顶级后缀域名数量"""
        total = 0
        domains = []
        sql = "SELECT tld_name,domain_num FROM domain_summary ORDER BY domain_num DESC"
        domains = self.db.query(sql)
        total = sum([item['domain_num'] for item in domains])  # 得到域名总数
        domains = domains[:num]
        total_num = sum([item['domain_num'] for item in domains])  # 得到前num域名总数
        domains.append({'tld_name': 'Other', 'domain_num': total - total_num})
        data_string = json.dumps(domains)
        return data_string, total
