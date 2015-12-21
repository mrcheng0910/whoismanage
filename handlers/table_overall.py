#encoding:utf-8

import tornado.web
from models.table_overall_db import TableOverallDb
import json
from datetime import datetime

class TableOverallHandler(tornado.web.RequestHandler):

    def get(self):
        results = TableOverallDb().get_table_info()
        self.render('./table_overall/table_overall.html',
                    results = json.dumps(results)
                    )
                    
class TableDataHistoryHandler(tornado.web.RequestHandler):
    
    def get(self):
        table_name = self.get_argument('table_name','None')
        results = TableOverallDb().get_data_history(table_name)
        self.render('./table_overall/table_data_history.html',
                    results = json.dumps(results,default=json_serial)
        )
        
        
def json_serial(obj):
    """格式化时间"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")