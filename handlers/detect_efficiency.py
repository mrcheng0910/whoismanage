#encoding:utf-8
import tornado.web

PATH = './domain_whois/'

class DetectHandler(tornado.web.RequestHandler):

    def get(self):
        self.render(PATH+'detect_efficiency.html')
