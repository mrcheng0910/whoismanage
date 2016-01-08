# encoding:utf-8
"""
功能: 更新顶级和二级服务器域名的数量,表为msvr_ssvr
作者: 程亚楠
更新日期: 2015.12.28
更新日期: 2016.1.8
"""

from datetime import datetime
from data_base import MySQL
from config import DESTINATION_CONFIG


def update_top_sec_num():
    """
    更新表msvr_ssvr,统计顶级服务器和二级服务器数量
    """
    
    print str(datetime.now()), '开始更新数据库中顶级和二级服务器数量(msvr_ssvr)'
    db = MySQL(DESTINATION_CONFIG)
    sql = 'UPDATE msvr_ssvr SET msvr_ssvr.ssvr=(SELECT COUNT(DISTINCT sec_svr) FROM top_sec_svr)'
    db.update(sql)
    sql = 'UPDATE msvr_ssvr SET msvr=(SELECT COUNT(DISTINCT addr) FROM whois_addr)'
    db.update(sql)
    db.close()
    print str(datetime.now()), '结束更新数据库中顶级和二级服务器数量(msvr_ssvr)'


# update_top_sec_num()
