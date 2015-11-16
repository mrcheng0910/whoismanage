# encoding:utf-8
"""
域名WHOIS服务器相关操作操作
1、获取whois服务器负责顶级后缀的数量
2、获取whois服务器的地理位置
"""
import torndb
from base_db import BaseDb


class SvrDb(BaseDb):

    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def get_svrs(self, top=1):
        """获得WHOIS服务器负责的域名数量"""
        svrs = []
        sql = 'SELECT addr as svr_name,count(*)as domain_sum FROM whois_addr GROUP BY addr ORDER BY domain_sum DESC '
        svrs = self.db.query(sql)
        for index, value in enumerate(svrs):   # 用来将None替换
            if not value['svr_name']:
                print index, value
                del svrs[index]
                svrs.insert(index, {'svr_name': '无WHOIS服务器',
                                    'domain_sum': value['domain_sum']})
                break

        total = sum(item['domain_sum'] for item in svrs)
        svrs = svrs[:top]
        top_sum = sum(item['domain_sum'] for item in svrs)
        svrs.append({'svr_name': 'Other', 'domain_sum': total - top_sum})
        return svrs, total

    def get_svr_addr(self):
        """获取whois服务器所在国家code，以及数量"""

        sql = 'SELECT COUNT(*) as value,upper(code) as code FROM svr_country GROUP BY code'
        results = self.db.query(sql)
        return results

    def tld_exsit_svr(self):
        """获取所有域名以及对应whois服务器"""

        sql = 'SELECT tld,addr FROM whois_addr LIMIT 5'
        results = self.db.query(sql)
        return results