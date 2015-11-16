#encoding:utf-8
import tornado.web
from models.tld_db import TldDb

class TldHandler(tornado.web.RequestHandler):

    def get(self):
        tlds = TldDb().get_tlds()
        self.render('tld.html',
                    title_name="顶级后缀统计",
                    tlds_num=len(tlds),
                    tlds=tlds,
                    )


