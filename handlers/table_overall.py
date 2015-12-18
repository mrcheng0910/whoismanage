#encoding:utf-8

import tornado.web
from models.table_overall_db import TableOverallDb
import json

class TableOverallHandler(tornado.web.RequestHandler):

    def get(self):
        results = TableOverallDb().get_table_info()
        self.render('table_overall.html',
                    results = json.dumps(results)
                    )
                    
    


