#coding=utf-8
"""
系统路由设置
"""

from handlers.index import IndexHandler,RateOfIncrease
from handlers.domain import DomainIndexHandler
from handlers.domain_geo import DomainGeoHandler
from handlers.svr import *
from handlers.tld import TldHandler
from handlers.system_performance.whois_integrity import DomainWhoisHandler,ShowAssignmentTld,ShowAssignmentType
from handlers.system_performance.detect_efficiency import DetectHandler,ManageIncreaseHandler
from handlers.system_performance.detect_forcast import DetectForcastHandler,ForcastPeriodHandler
from handlers.system_performance.detect_count import DomainCountHandler,GetDomainCountHandler

from handlers.table_overall import TableOverallHandler,TableDataHistoryHandler

urls = [
    (r'/', IndexHandler),
    (r'/rate_of_increase',RateOfIncrease),
    (r'/tld', TldHandler),
    (r'/domain_geography', DomainGeoHandler), #域名地理位置查询
    (r'/domain', DomainIndexHandler), # 域名首页
    (r'/svr', DomainSvrHandler), # 域名whois服务器首页
    (r'/svr_geo',SvrGeoHandler),  # 域名whois服务器地理位置
    (r'/svr_geo_table',SvrGeoTableHandler), # 详细信息
    (r'/svr_performance',SvrPerformanceHandler), # whois服务器性能
    (r'/svr_table',SvrTableHandler), # 服务器表格内容测试，测试
    (r'/svr_table_info',SvrInfoHandler),  # 信息
    
    (r'/top_sec',TopSecSvr), # 一级和二级服务器
    # (r'/top_sec/query',TopSecQuery), # 获取信息
    (r'/top_sec/query_num',TopSecNum), #获取对比数据
    
    (r'/whois_integrity',DomainWhoisHandler), # whois信息完整性分析
    (r'/whois_integrity/assignment_tld',ShowAssignmentTld),  # 查询指定后缀的flag分布
    (r'/whois_integrity/assignment_type',ShowAssignmentType), # 查询指定类型的whois分布
    (r'/detect',DetectHandler),  # 探测效率
    (r'/detect/increase',ManageIncreaseHandler),  # 探测性能
    (r'/forcast',DetectForcastHandler), # 预测
    (r'/forcast/period',ForcastPeriodHandler),  # 预测
    (r'/detect_count',DomainCountHandler),  # 探测信息
    (r'/detect_count/data',GetDomainCountHandler),
    
    (r'/table_overall',TableOverallHandler), # 数据库表整体情况
    (r'/table_overall_history',TableDataHistoryHandler),
]
