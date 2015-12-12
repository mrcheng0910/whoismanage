#encoding:utf-8
import tornado.web
from models.detect_db import DetectDb
import json
from datetime import datetime
PATH = './system_performance/'

class DetectHandler(tornado.web.RequestHandler):
    """首页渲染"""
    def get(self):
        self.render(PATH+'detect_efficiency.html')


class ManageIncreaseHandler(tornado.web.RequestHandler):
    
    def get(self):
        start = self.get_argument('start', "None")
        end = self.get_argument('end', "None")
        detect = DetectDb()
        raw_data = detect.manage_increase(start,end)
        self.write(json.dumps(raw_data,default=json_serial))


def json_serial(obj):
    """格式化时间"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")