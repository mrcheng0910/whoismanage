# encoding:utf-8
"""
功能: 更新数据库中总共的域名whois数量，表为whois_sum_by_day
作者: 程亚楠
更新日期: 2015.12.28
更新日期: 2016.1.8
"""

from datetime import datetime
from data_base import MySQL
from config import DESTINATION_CONFIG


def update_day():
    """更新表whois_sum_by_day，即统计数据库中最新的域名whois总量
    """

    print str(datetime.now()), '开始更新当天数据库中最新的WHOIS总量(whois_sum_by_day)'
    db = MySQL(DESTINATION_CONFIG)
    sql = 'INSERT INTO whois_sum_by_day(sum) SELECT MAX(tld_sum) FROM whois_sum \
            WHERE to_days(insert_time) = to_days(now())'
    db.insert(sql)
    db.close()
    print str(datetime.now()), '结束更新当天数据库中最新的WHOIS总量(whois_sum_by_day)'

# update_day()
