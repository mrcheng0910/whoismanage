# encoding:utf-8
"""
域名WHOIS服务器相关操作操作
1、获取whois服务器负责顶级后缀的数量
2、获取whois服务器的地理位置
3、获取域名whois服务器列表
"""

from models.base_db import BaseDb


class SvrDb(BaseDb):
    """域名WHOIS服务器相关操作操作"""

    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def get_svrs(self, top=1):
        """获得WHOIS服务器负责的域名数量"""
        svrs = []
        sql = 'SELECT addr as svr_name,count(*)as domain_sum FROM whois_addr \
                GROUP BY addr ORDER BY domain_sum DESC '
        svrs = self.db.query(sql)
        for index, value in enumerate(svrs):   # 用来将None替换
            if not value['svr_name']:
                print index, value
                del svrs[index]
                svrs.insert(index, {'svr_name': '无WHOIS服务器',
                                    'domain_sum': value['domain_sum']
                                    }
                            )
                break

        total = sum(item['domain_sum'] for item in svrs)
        svrs = svrs[:top]
        top_sum = sum(item['domain_sum'] for item in svrs)
        svrs.append({'svr_name': 'Other', 'domain_sum': total - top_sum})
        return svrs, total

    def get_svr_addr(self):
        """获取whois服务器所在国家code，以及数量"""

        sql = 'SELECT COUNT(*) as value,upper(code) as code,country FROM svr_country \
                GROUP BY code ORDER BY value DESC'
        results = self.db.query(sql)
        return results

    def tld_exist_svr(self):
        """获取含有whois服务器的域名列表"""

        sql = 'SELECT tld,addr FROM whois_addr WHERE addr IS NOT NULL'
        results = self.db.query(sql)
        return results

    def tld_no_exist_svr(self):
        """获取没有域名whois的域名列表"""
        sql = 'SELECT tld,addr FROM whois_addr WHERE addr IS NULL'
        results = self.db.query(sql)
        return results

    def svr_sum(self):
        """获取信息"""
        sql = "SELECT COUNT( CASE WHEN addr IS NULL THEN 1 ELSE NULL END ) AS exist_y,\
                    COUNT( CASE WHEN addr IS NOT NULL THEN 1 ELSE NULL END ) AS exist_n,\
                    COUNT( CASE WHEN flag_reg= '0' THEN 1 ELSE NULL END ) AS reg_n,\
                    COUNT( CASE WHEN flag_reg= '1' THEN 1 ELSE NULL END ) AS reg_p,\
                    COUNT( CASE WHEN flag_reg= '2' THEN 1 ELSE NULL END ) AS reg_y,\
                    COUNT( CASE WHEN flag_org= '0' THEN 1 ELSE NULL END ) AS org_n,\
                    COUNT( CASE WHEN flag_org= '1' THEN 1 ELSE NULL END ) AS org_y,\
                    COUNT( CASE WHEN flag_date= '0' THEN 1 ELSE NULL END ) AS data_n,\
                    COUNT( CASE WHEN flag_date= '1' THEN 1 ELSE NULL END ) AS data_p,\
                    COUNT( CASE WHEN flag_date= '2' THEN 1 ELSE NULL END ) AS data_y\
               FROM whois_addr"
        results = self.db.query(sql)
        return results

    def get_svr_info(self):
        sql = "SELECT DISTINCT(addr),flag_reg,flag_org,flag_date FROM \
              whois_addr WHERE flag_addr='1'"
        results = self.db.query(sql)
        return results

    

    def top_sec(self):
        """
        获取顶级和二级服务器统计信息
        """
        results = []
        sql = "SELECT top_svr,count(*) as num FROM top_sec_svr group by top_svr"
        results = self.db.query(sql)
        return results
        
    def sec_num(self):
        """
        获得二级服务器服务器
        """
        results = []
        sql = "select count(distinct(sec_svr)) as num from top_sec_svr"
        results = self.db.query(sql)
        return results
        
    def top_sec_test(self):
        """
        """
        sql = "SELECT top_svr,SUM(whois_sum) as total FROM top_sec_svr group by top_svr"
        top_results = self.db.query(sql)
        sql = "SELECT top_svr,sec_svr,whois_sum FROM top_sec_svr order by whois_sum desc"
        sec_results = self.db.query(sql)
        return top_results,sec_results
    
    def get_code_svr(self,code):
        sql = 'SELECT * FROM svr_country WHERE code = "%s"' % code
        results = self.db.query(sql)
        return results