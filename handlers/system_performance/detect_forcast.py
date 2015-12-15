#encoding:utf-8
"""
预测探测时间
"""
import tornado.web
from models.index_db import IndexDb
from models.detect_db import DetectDb
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
    

class ForcastPeriodHandler(tornado.web.RequestHandler):
    """提供期间速率查询"""
    def get(self):
        db = DetectDb()
        period = self.get_argument('period', "None")
        speeds = db.get_speed(period)
        self.write(json.dumps(speeds))