# encoding:utf-8
import tornado
from models.domain_db import DomainDb

PATH = './domain/'

class DomainIndexHandler(tornado.web.RequestHandler):
    """各个顶级后缀域名数量统计"""

    def get(self):
        domains, total = DomainDb().get_domain(10)
        self.render(PATH+'domain_index.html',
                    title_name="顶级后缀统计",
                    domains=domains,
                    total=total
                    )


class DomainQueryHandler(tornado.web.RequestHandler):
    """域名相关查询"""
    def get(self):
        self.render(PATH+'domain_query.html',
                    title_name = "域名查询"
                    )