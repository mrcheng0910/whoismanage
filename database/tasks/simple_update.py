#encoding:utf-8
"""
该文件主要是实现数据库直接操作功能
"""
from database import conn_db

def update_day():
    """更新每天的数据"""
    conn = conn_db()
    sql = 'insert into DomainWhois.whois_sum_by_day(sum) select max(tld_sum) from DomainWhois.whois_sum where to_days(insert_time) = to_days(now())' # 插入数据
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    
def update_top_sec_num():
    """更新顶级服务器和二级服务器数量"""
    
    conn = conn_db()
    cur = conn.cursor()
    sql = 'UPDATE msvr_ssvr SET msvr_ssvr.ssvr=(SELECT COUNT(DISTINCT sec_svr) FROM top_sec_svr)'
    cur.execute(sql)
    sql = 'UPDATE msvr_ssvr SET msvr=(SELECT COUNT(DISTINCT addr) FROM whois_addr)'
    cur.execute(sql)
    conn.commit()
    conn.close()