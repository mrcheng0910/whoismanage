#encoding:utf-8
import tornado.web
from models.index_db import IndexDb
import json
PATH = './system_performance/'

class DetectForcastHandler(tornado.web.RequestHandler):
    """首页渲染"""
    
    def get(self):
        db = IndexDb()
        domain_total = db.get_domain_num()
        domain_detected = db.get_whois_sum()
        total = [domain_total,domain_detected,domain_total-domain_detected]
        self.render(PATH + 'detect_forcast.html',
                    total = total
                    )
    