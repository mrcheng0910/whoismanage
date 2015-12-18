#encoding:utf-8

import tornado.web
from models.domain_whois_db import DomainWhoisDb
import json
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
        self.write(json.dumps(results))