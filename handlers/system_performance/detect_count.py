#encoding:utf-8

import tornado.web
from models.domain_whois_db import DomainWhoisDb
import json
import decimal

PATH = './system_performance/'

class DomainCountHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render(PATH + 'detect_count.html')


class GetDomainCountHandler(tornado.web.RequestHandler):
    
    def get(self):
        argument = self.get_argument('argument', '')
        options = self.get_argument('options','')
        if options == 'num':
            results = DomainWhoisDb().get_detect(argument)
        else:
            results = DomainWhoisDb().get_tld_detect(argument)
        self.write(json.dumps(results,cls=DecimalEncoder))


class DecimalEncoder(json.JSONEncoder):
    """
    解决json.dumps不能格式化Decimal问题
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)