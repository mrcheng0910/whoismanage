# encoding:utf-8
"""
首页handler
"""
import tornado.web
from models.index_db import IndexDb
import json
from datetime import datetime

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        index_db = IndexDb()
        domain_num = index_db.get_domain_num()  # 获取数据库中域名总数
        tld_num = index_db.get_tld_num()  # 获取数据库中所有域名顶级后缀
        msvr_sum, ssvr_sum = index_db.get_svr_sum()  # 获取whois服务器(主/次)数量
        whois_sum = index_db.get_whois_sum()
        self.render('index.html',
                    domain_num=domain_num,
                    tld_num=tld_num,
                    msvr_sum=msvr_sum,
                    ssvr_sum=ssvr_sum,
                    whois_sum=whois_sum,
                    )


class RateOfIncrease(tornado.web.RequestHandler):
    
    def get(self):
        index_db = IndexDb()
        raw_data = index_db.get_increase(top=15)
        self.write(json.dumps(raw_data,default=json_serial))


def json_serial(obj):
    """格式化时间"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")