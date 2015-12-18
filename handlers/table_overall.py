#encoding:utf-8
import tornado.web

class TableOverallHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('table_overall.html',
                    )


