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
        sql = "SELECT tld,flag,sum(whois_sum) as whois_sum FROM tld_whois_flag WHERE tld \
                in (SELECT tld FROM (SELECT tld FROM tld_whois_flag GROUP BY tld \
                 ORDER BY sum(whois_sum) DESC LIMIT %s) as t) GROUP BY tld,flag" % top
        result = self.db.query(sql)
        return result
