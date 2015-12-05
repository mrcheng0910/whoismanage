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
                    data=json.dumps(results)
                    )


class SvrPerformanceHandler(tornado.web.RequestHandler):
    """whois服务器性能统计分析"""

    def get(self):
        results = SvrDb().svr_sum()
        self.render(PATH + 'svr_performance.html',
                    results=results
                    )


class SvrTableHandler(tornado.web.RequestHandler):
    """域名是否含有whois服务器列表"""

    def get(self):
        flag = self.get_argument('flag', None)
        if flag == 'True':
            results = SvrDb().tld_exist_svr()  # 含有whois域名列表
            title = "含有WHOIS域名列表"
        else:
            results = SvrDb().tld_no_exist_svr()  # 不含有whois域名列表
            title = "不含有WHOIS域名列表"
        self.render(PATH + 'tld_svr_table.html',
                    results=results,
                    title=title
                    )


class SvrInfoHandler(tornado.web.RequestHandler):
    def get(self):
        results = SvrDb().get_svr_info()
        self.render(PATH + 'tld_svr_detail.html',
                    results=results,
                    title='详细信息'
                    )


class SvrDetectHandler(tornado.web.RequestHandler):
    def get(self):
        results = SvrDb().get_detect()
        self.render(PATH + 'detect_info.html',
                    results1=json.dumps(results[:7]),
                    results2=json.dumps(results[7:15])
                    )


class TopSecSvr(tornado.web.RequestHandler):
    """
    操作域名whois顶级服务器和二级服务器
    """
    def get(self):
        results = SvrDb().sec_num()
        self.render(PATH+'top_sec.html',sec_num=results[0].num)
        
class TopSecQuery(tornado.web.RequestHandler):
    """
    get
    """
    def get(self):
        results = SvrDb().top_sec()
        self.write(json.dumps(results))

class TopSecNum(tornado.web.RequestHandler):
    """
    num
    """
    def get(self):
        top_results,sec_results = SvrDb().top_sec_test()
        results= self.manage(top_results,sec_results)
        self.write(json.dumps(results))
        
    def manage(self,top_results,sec_results):
        top_series = []
        drill_series = []
        for value in top_results:
            top_series.append({
                'name': value['top_svr'],
                'y': int(value['total']),
                'drilldown': value['top_svr']
            })
        drill_series.append({
            'name': sec_results[0]['top_svr'],
            'id': sec_results[0]['top_svr'],
            'data': [[sec_results[0]['sec_svr'],sec_results[0]['whois_sum']],]
        })
        for sec_value in sec_results[1:]:
            for drill_value in drill_series:
                if drill_value['name']==sec_value['top_svr']:
                    if len(drill_value['data']) == 15:
                        pass
                    elif len(drill_value['data'])==14:
                        total = 0
                        total = self.find_svr(top_series,drill_value['name'])-self.find_total(drill_value['data'])
                        drill_value['data'].append(['Ohter',total])
                    else:
                        drill_value['data'].append([sec_value['sec_svr'],sec_value['whois_sum']])
                    break
            else:
                drill_series.append({
                    'name': sec_value['top_svr'],
                    'id': sec_value['top_svr'],
                    'data':[[sec_value['sec_svr'],sec_value['whois_sum']],]
                })
        
        return [top_series,drill_series]
        
    def find_svr(self,top_series,name):
        """
        查找总数
        """
        for value in top_series:
            if value['name']==name:
                return value['y']
        
    def find_total(self,drill_data):
        """
        已有数量
        """
        total = 0
        for value in drill_data:
            total += value[1]
        
        return total
        
