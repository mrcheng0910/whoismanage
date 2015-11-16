#encoding:utf-8
import tornado
class DomainGeoHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.render('coming.html',
                    title_name="域名地理位置分布",
                    page_header="域名的地理位置分布"
                    )