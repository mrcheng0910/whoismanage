#encoding:utf-8
import tornado
from models.domain_db import DomainDb

class DomainHandler(tornado.web.RequestHandler):
    """各个顶级后缀域名数量统计"""

    def get(self):
        domains,total = DomainDb().get_domain(10)
        self.render('domain.html',
                    title_name="顶级后缀统计",
                    domains=domains,
                    total=total
                    )


