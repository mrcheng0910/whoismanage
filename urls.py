#coding=utf-8
"""
系统路由设置
"""
from handlers.index import IndexHandler
from handlers.domain import DomainIndexHandler
from handlers.domain_geo import DomainGeoHandler
from handlers.domain import DomainQueryHandler
from handlers.svr import *
from handlers.tld import TldHandler

urls = [
    (r'/', IndexHandler),
    (r'/tld', TldHandler),
    (r'/domain_geography', DomainGeoHandler), #域名地理位置查询
    (r'/domain', DomainIndexHandler), # 域名首页
    (r'/domain_query',DomainQueryHandler),   # 域名查询
    (r'/svr', DomainSvrHandler), # 域名whois服务器首页
    (r'/svr_geo',SvrGeoHandler),  # 域名whois服务器地理位置
    (r'/svr_performance',SvrPerformanceHandler), # whois服务器性能
    (r'/svr_table',SvrTableHandler), # 服务器表格内容测试，测试
    (r'/svr_table_info',SvrInfoHandler),  # 信息
    (r'/svr_detect',SvrDetectHandler),  # 探测信息
    (r'/top_sec',TopSecSvr), # 一级和二级服务器
    (r'/top_sec/query',TopSecQuery), # 获取信息
    (r'/top_sec/query_num',TopSecNum), #获取对比数据
]
