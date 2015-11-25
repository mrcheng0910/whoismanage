#encoding:utf-8
import tornado.web
from models.tld_db import TldDb

class TldHandler(tornado.web.RequestHandler):

    def get(self):
        tlds = TldDb().get_tlds()
        self.render('tld.html',
                    tlds_num=len(tlds),
                    tlds=tlds,
                    )


