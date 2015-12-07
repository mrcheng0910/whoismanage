#!/usr/bin/python
# encoding:utf-8
"""
网站后台定期更新程序
功能：更新tld_whois_sum_history表，完成数据库中已经探测的域名数量，包括顶级后缀和域名后缀
其他：tld_whois_sum_history的update_time字段为自动添加，插入数据后，根据系统时间自动生成
"""
import sys
import MySQLdb
import time
try:
    import schedule
except ImportError:
    sys.exit("无schedul模块,请安装 easy_install schedule")
from datetime import datetime
import threading
from threading import Thread
from Queue import Queue


num_thread = 5      # 线程数量
queue = Queue()     # 任务队列，存储sql
sum_domains = []    # 存储域名的和


def sum_all_domains(sum_domains=[], single_domains=[]):
    """合并两个列表，相同名称求和"""

    del_index = []      # 用来存放待删除的index
    for index_sum, value_sum in enumerate(sum_domains):
        for index_single, value_single in enumerate(single_domains):
            if value_sum[0] == value_single[0]:
                sum_domains.append(
                    (value_sum[0], value_single[1] + value_sum[1]))
                del_index.append(index_sum)
                del single_domains[index_single]  # 删除

    sum_domains.extend(single_domains)  # 将次列表中未删除的添加
    del_index.reverse()  # 反向求解,比较巧妙,防止删除前面项后，导致错位
    for i in del_index:  # 删除重复的项
        del sum_domains[i]


def conn_db():
    """连接数据库"""
    try:
        conn = MySQLdb.connect(
                host="172.26.253.3",
                user="root",
                passwd="platform",
                db="DomainWhois"
                )
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return conn


def count_domain(q, queue):
    """计算各个列表中，各个顶级后缀的数量，并求和"""
    while 1:
        content = queue.get()
        if not content:
            queue.task_done()
        try:
            print content
            conn = conn_db()
            cur = conn.cursor()
            cur.execute(content)
            single_domains = cur.fetchall()
            cur.close()
            # conn.close()
            lock.acquire()  # 锁
            sum_all_domains(sum_domains, list(single_domains))
            lock.release()  # 解锁
            queue.task_done()
            time.sleep(1)  # 去掉偶尔会出现错误
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            conn.close()


def update_db():
    """更新数据库"""
    total = 0
    conn = conn_db()
    sql = 'INSERT INTO tld_whois_sum_history(tld,whois_sum) VALUES(%s, %s)' # 插入数据
    cur = conn.cursor()
    for domain in sum_domains:
        cur.execute(sql,(domain[0], domain[1]))
    conn.commit()
    cur.execute('TRUNCATE TABLE tld_whois_sum')
    sql = 'INSERT INTO tld_whois_sum(tld,whois_sum) VALUES(%s, %s)'
    for domain in sum_domains:
        cur.execute(sql,(domain[0], domain[1]))
        total = total + domain[1]
    conn.commit()
    sql = 'INSERT INTO whois_sum(tld_sum) VALUES(%s)'
    cur.execute(sql,total)
    conn.commit()
    conn.close()

def create_queue():
    """
    创建任务队列
    """
    for i in xrange(65, 91):     # 创建任务队列，A-Z
        sql = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, count(*) AS count \
               FROM domain_whois_%s WHERE flag <> -6 GROUP BY tld' % chr(i)
        queue.put(sql)
    sql_num = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, count(*) AS count \
                FROM domain_whois_num WHERE flag <> -6 GROUP BY tld'
    queue.put(sql_num)   # domain_whois_num 加入队列
    sql_other = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, count(*) AS count \
                FROM domain_whois_other WHERE flag <> -6 GROUP BY tld'
    queue.put(sql_other)   # domain_whois_other 加入队列
    

def main():
    """主操作"""
    global sum_domains  # 务必添加，初始化，否则会一直累加
    sum_domains = []
    create_queue()
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=count_domain, args=(q, queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()

    # test
    for value in sum_domains:
        print value
    update_db()
    
def update_day():
    """更新每天的数据"""
    conn = conn_db()
    sql = 'insert into DomainWhois.whois_sum_by_day(sum) select max(tld_sum) from DomainWhois.whois_sum where to_days(insert_time) = to_days(now())' # 插入数据
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    
    lock = threading.Lock()
    schedule.every().hour.do(main)   # 每小时运行一次
    # schedule.every(15).minutes.do(main)
    # schedule.every(30).minutes.do(update_day)
    schedule.every().day.at("23:40").do(update_day)
    while True:
        schedule.run_pending()
        time.sleep(1)
