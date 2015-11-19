#coding=utf-8
"""
系统路由设置
"""
from handlers.index import IndexHandler
from handlers.domain import DomainHandler
from handlers.domain_geo import DomainGeoHandler
from handlers.svr import *
from handlers.tld import TldHandler

urls = [
    (r'/', IndexHandler),
    (r'/tld', TldHandler),
    (r'/domain_geography', DomainGeoHandler),
    (r'/domain', DomainHandler), # 域名首页
    (r'/svr', DomainSvrHandler), # 域名whois服务器首页
    (r'/svr_geo',SvrGeoHandler),  # 域名whois服务器地理位置
    (r'/svr_performance',SvrPerformanceHandler), # whois服务器性能
    (r'/svr_table',SvrTableHandler), # 服务器表格内容测试，测试
    (r'/svr_table_info',SvrInfoHandler) # 信息
]
