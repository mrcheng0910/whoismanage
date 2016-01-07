#encoding:utf-8
"""
功能:
1. 更新数据库中总共的域名whois数量，表为whois_sum_by_day
2. 更新顶级和二级服务器域名的数量
作者: 程亚楠
更新日期: 2015.12.28
"""

from datetime import datetime
from data_base import MySQL


def update_day():
    """更新表whois_sum_by_day，即统计数据库中最新的域名whois总量"""
    
    db = MySQL()
    print str(datetime.now()),"开始统计数据库中最新的域名whois数量"
    sql = 'INSERT INTO whois_sum_by_day(sum) SELECT max(tld_sum) FROM whois_sum \
            WHERE to_days(insert_time) = to_days(now())' # 插入数据
    db.insert(sql)
    db.close()
    print str(datetime.now()),"开始统计数据库中最新的域名whois数量"


def update_top_sec_num():
    """统计顶级服务器和二级服务器数量"""
    
    print str(datetime.now()),"开始统计数据库中最新的顶级和二级服务器数量"
    db = MySQL()
    sql = 'UPDATE msvr_ssvr SET msvr_ssvr.ssvr=(SELECT COUNT(DISTINCT sec_svr) FROM top_sec_svr)'
    db.update(sql)
    sql = 'UPDATE msvr_ssvr SET msvr=(SELECT COUNT(DISTINCT addr) FROM whois_addr)'
    db.update(sql)
    db.close()
    print str(datetime.now()),'结束统计数据库中最新的顶级和二级服务器数量'

# update_day()
# update_top_sec_num()