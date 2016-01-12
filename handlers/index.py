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
        domain_overall = index_db.fetch_tld_overall()
        domain_num, tld_num, msvr_sum, ssvr_sum, whois_sum = domain_overall
        self.render(
                'index.html',
                domain_num=domain_num,
                tld_num=tld_num,
                msvr_sum=msvr_sum,
                ssvr_sum=ssvr_sum,
                whois_sum=whois_sum
        )


class RateOfIncrease (tornado.web.RequestHandler):
    """
    首页增长率展示
    """

    def get(self):
        index_db = IndexDb()
        raw_data = index_db.get_increase(top=22)
        self.write (json.dumps(raw_data, default=self.date_handler))

    def date_handler(self, obj):
        """json支持date格式"""
        return obj.isoformat () if hasattr (obj, 'isoformat') else obj
