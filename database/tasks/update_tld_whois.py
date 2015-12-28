#!/usr/bin/python
# encoding:utf-8
"""
功能：更新表tld_whois_sum_history、whois_sum两个表。
作者：程亚楠
时间：2015.12.20
更新时间:2015.12.28
"""

import sys
import time
import threading
from threading import Thread
from Queue import Queue
from datetime import datetime

# import MySQLdb

# import re
# from database import conn_db
from data_base import MySQL


num_thread = 5      # 线程数量
queue = Queue()     # 任务队列，存储sql
sum_domains = []    # 存储域名的和
lock = threading.Lock()


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


def count_domain(q, queue):
    """计算各个列表中，各个顶级后缀的数量，并求和"""
    while 1:
        content = queue.get()
        try:
            db = MySQL()
            db.query(content)
            single_domains = db.fetchAllRows()
            lock.acquire()  # 锁
            sum_all_domains(sum_domains, list(single_domains))
            lock.release()  # 解锁
            queue.task_done()
            time.sleep(1)  # 去掉偶尔会出现错误
        except :
            print "Query Wrong"
            sys.exit(1)
        finally:
            db.close()


def update_db():
    """更新数据库"""
    total = 0
    db = MySQL()
    sql = 'INSERT INTO tld_whois_sum_history(tld,whois_sum) VALUES("%s", "%s")' # 插入数据
    for domain in sum_domains:
        db.insert(sql % (domain[0],domain[1]))
        total += domain[1]
    sql = 'INSERT INTO whois_sum(tld_sum) VALUES("%s")'
    db.insert(sql % total)
    db.close()

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
    

def tld_whois_sum():
    """主操作"""
    print str(datetime.now()),'开始统计各个顶级后缀的whois数量和whois总量'
    global sum_domains  
    sum_domains = [] # 务必添加，初始化，否则会一直累加
    create_queue()
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=count_domain, args=(q, queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()
    update_db()
    print str(datetime.now()),'结束统计各个顶级后缀的whois数量和whois总量'
    