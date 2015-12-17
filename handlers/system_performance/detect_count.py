#encoding:utf-8

import tornado.web
from models.domain_whois_db import DomainWhoisDb
import json
PATH = './system_performance/'
class SvrDetectHandler(tornado.web.RequestHandler):
    def get(self):
        results = DomainWhoisDb().get_detect()
        self.render(PATH + 'detect_count.html',
                    results1=json.dumps(results[:7])
                    )