# encoding:utf-8
"""
域名WHOIS服务器信息
"""
import tornado
import json
from models.svr_db import SvrDb

PATH = './svrs/'


class DomainSvrHandler(tornado.web.RequestHandler):
    """
    域名WHOIS服务器所负责的顶级后缀统计
    """

    def get(self):
        svrs, total = SvrDb().get_svrs(10)
        self.render(PATH + 'svr_index.html',
                    title_name="域名WHOIS信息",
                    svrs=json.dumps(svrs),
                    total=total
                    )

    def post(self):
        num = self.get_argument('num', "None")
        # self.write(num)
        svrs, total = SvrDb().get_svrs(int(num))
        self.write(json.dumps(svrs))


class SvrGeoHandler(tornado.web.RequestHandler):
    """WHOIS服务器的地理位置统计展示"""

    def get(self):
        results = SvrDb().get_svr_addr()
        self.render(PATH + 'svr_geo.html',
                    title_name="全球域名WHOIS服务器地理位置分布",
                    data=json.dumps(results)
                    )


class SvrPerformanceHandler(tornado.web.RequestHandler):
    """whois服务器性能统计分析"""

    def get(self):
        results = SvrDb().svr_sum()
        self.render(PATH + 'svr_performance.html',
                    title_name="域名WHOIS服务器性能",
                    results=results
                    )


class SvrTableHandler(tornado.web.RequestHandler):
    """域名是否含有whois服务器列表"""

    def get(self):
        flag = self.get_argument('flag',None)
        if flag=='True':
            results = SvrDb().tld_exist_svr() # 含有whois域名列表
            title = "含有WHOIS域名列表"
        else:
            results = SvrDb().tld_no_exist_svr() # 不含有whois域名列表
            title = "不含有WHOIS域名列表"
        self.render(PATH + 'tld_svr_table.html',
                    results=results,
                    title = title
                    )

class SvrInfoHandler(tornado.web.RequestHandler):
    def get(self):
        results = SvrDb().get_svr_info()
        self.render(PATH+'tld_svr_detail.html',
                    results=results,
                    title='详细信息'
                    )
class SvrDetectHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(PATH+'detect_info.html',
                    title_name="探测信息")