#encoding:utf-8
"""
首页handler
"""
import tornado.web
from models.index_db import IndexDb

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        index_db = IndexDb()
        domain_num = tld_num = msvr_sum = ssvr_sum =0
        domain_num = index_db.get_domain_num()     # 获取数据库中域名总数
        tld_num = index_db.get_tld_num()                 # 获取数据库中所有域名顶级后缀
        msvr_sum,ssvr_sum = index_db.get_svr_sum()           # 获取whois服务器(主/次)数量
        self.render('index.html',
                    title_name="测试首页",
                    domain_num=domain_num,
                    tld_num=tld_num,
                    msvr_sum=msvr_sum,
                    ssvr_sum=ssvr_sum
                    )
