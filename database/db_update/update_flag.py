#!/usr/bin/python
# encoding:utf-8
"""
网站后台定期更新程序
功能：更新表tld_whois_sum_history、tld_whois_sum、whois_sum、whois_sum_by_day四个表。

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
sum_flags = []    # 存储域名的和
lock = threading.Lock()  # 锁


def sum_all_flags(sum_flags=[], single_domains=[]):
    """合并两个列表，相同名称求和"""

    del_index = []      # 用来存放待删除的index
    for index_sum, value_sum in enumerate(sum_flags):
        for index_single, value_single in enumerate(single_domains):
            if value_sum[0] == value_single[0] and value_sum[1]==value_single[1] :
                sum_flags.append(
                    (value_sum[0], value_sum[1], value_sum[2] + value_single[2]))
                del_index.append(index_sum)
                del single_domains[index_single]  # 删除

    sum_flags.extend(single_domains)  # 将次列表中未删除的添加
    del_index.reverse()  # 反向求解,比较巧妙,防止删除前面项后，导致错位
    for i in del_index:  # 删除重复的项
        del sum_flags[i]


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


def count_flag(q, queue):
    """计算各个列表中，各个顶级后缀的flag中域名whois数量，并求和"""
    while 1:
        content = queue.get()
        if not content:
            queue.task_done()
        try:
            print content
            conn = conn_db()
            cur = conn.cursor()
            cur.execute(content)
            single_flags = cur.fetchall()
            cur.close()
            lock.acquire()  # 锁
            sum_all_flags(sum_flags, list(single_flags))
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
    try:
        conn = conn_db()
        sql = 'INSERT INTO tld_whois_flag(tld, flag,flag_detail, whois_sum) VALUES(%s, %s, %s, %s)'
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE tld_whois_flag')
        for item in sum_flags:
            if item[1] < 0:
                flag = 0
            elif item[1] >= 120:
                flag = 1
            elif item[1] == 102 or item[1] == 110 or item[1] == 112:
                flag = 2
            else:
                flag = 3
            cur.execute(sql, (item[0], flag, item[1], item[2]))
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "update_db Error %d: %s " % (e.args[0], e.args[1])
        sys.exit(1)

def create_queue():
    """
    创建任务队列
    """
    for i in xrange(65, 91):     # 创建任务队列，A-Z
        sql = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld,flag, count(*) AS count \
               FROM domain_whois_%s WHERE flag <> -6 GROUP BY tld,flag' % chr(i)
        queue.put(sql)
    sql_num = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, flag,count(*) AS count \
                FROM domain_whois_num WHERE flag <> -6 GROUP BY tld,flag'
    queue.put(sql_num)   # domain_whois_num 加入队列
    sql_other = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, flag,count(*) AS count \
                FROM domain_whois_other WHERE flag <> -6 GROUP BY tld,flag'
    queue.put(sql_other)   # domain_whois_other 加入队列
    
    
def create_thread():
    """创建任务线程"""
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=count_flag, args=(q, queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()


def main():
    """主操作"""
    global sum_flags  
    sum_flags = [] # 务必添加，初始化，否则会一直累加
    create_queue()  # 创建任务队列
    create_thread() # 创建线程
    update_db()
    
    # test
    for value in sum_flags:
        print value
 
if __name__ == "__main__":
    
    # schedule.every().hour.do(main)   # 每小时运行一次
    schedule.every(5).minutes.do(main)
    # schedule.every(30).minutes.do(update_day)
    # schedule.every().day.at("23:40").do(update_day)
    while True:
        schedule.run_pending()
        time.sleep(1)
