# encoding:utf-8
import tornado
from models.domain_db import DomainDb

PATH = './domain/'

class DomainIndexHandler(tornado.web.RequestHandler):
    """各个顶级后缀域名数量统计"""

    def get(self):
        domains, total = DomainDb().get_domain(10)
        self.render(PATH+'domain_index.html',
                    domains=domains,
                    total=total
                    )

