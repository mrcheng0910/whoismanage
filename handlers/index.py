# encoding:utf-8
"""
首页handler
"""

import tornado.web
import json
from models.index_db import IndexDb


class IndexHandler(tornado.web.RequestHandler):
    """首页控制"""

    def get(self):
        index_db = IndexDb()
        domain_overall = index_db.fetch_tld_overall(top=20)
        domain_num, tld_num, msvr_sum, ssvr_sum, whois_sum,domains = domain_overall

        self.render(
                'index.html',
                domain_num=domain_num,
                tld_num=tld_num,
                msvr_sum=msvr_sum,
                ssvr_sum=ssvr_sum,
                whois_sum=whois_sum,
                domains = json.dumps(domains,default=self._date_handler)
        )

    def _date_handler(self, obj):
        """json支持date格式"""
        return obj.isoformat () if hasattr (obj, 'isoformat') else obj
