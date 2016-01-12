#!/usr/bin/python
# encoding:utf-8
"""
功能：更新表tld_whois_sum_history、whois_sum两个表。
作者：程亚楠
创建时间：2015.12.20
更新时间：2016.1.10
使用collections模块优化程序
更新时间:2015.12.28
"""

import time
import threading
from Queue import Queue
from threading import Thread
from datetime import datetime
from collections import defaultdict
from data_base import MySQL
from config import DESTINATION_CONFIG

num_thread = 5      # 线程数量
queue = Queue()     # 任务队列，存储sql
sum_domains = []    # 存储域名的和
lock = threading.Lock()
sum_tld_whois = defaultdict(list)


def merge_tld_whois(tb_tld_whois):
    """
    :param tb_tld_whois:tuple, 合并所有相同表的tld，whois信息
    :return:
    """
    for item,value in tb_tld_whois:
        sum_tld_whois[item].append(value)


def sum_all_whois():
    """合并两个列表，相同名称求和"""

    tld_whois = []

    for item in sum_tld_whois:
        tld_whois.append((item,sum(sum_tld_whois[item])))
    return tld_whois


def count_domain():
    """计算各个列表中，各个顶级后缀的数量，并求和"""

    while 1:
        tb_name = queue.get()
        tb_tld_whois = get_resource_data(tb_name)
        lock.acquire()  # 锁
        merge_tld_whois(tb_tld_whois)
        # sum_all_domains(single_domains)
        lock.release()  # 解锁
        queue.task_done()
        time.sleep(1)  # 去掉偶尔会出现错误


def update_db():
    """更新数据库"""
    tld_whois = sum_all_whois()
    total = 0
    db = MySQL(DESTINATION_CONFIG)
    sql = 'INSERT INTO tld_whois_sum_history(tld,whois_sum) VALUES("%s", "%s")' # 插入数据
    for tld,whois in tld_whois:
        db.insert_no_commit(sql % (tld,whois))
        total += whois
    db.commit()
    sql = 'INSERT INTO whois_sum(tld_sum) VALUES("%s")'
    db.insert(sql % total)
    db.close()


def get_resource_data(tb_name):
    """
    获得基础数据
    :param tb_name:string 表名
    :return: 返回基础数据
    """
    db = MySQL(DESTINATION_CONFIG)
    db.query('SELECT tld, SUM(whois_sum) AS count FROM domain_whois_%s WHERE flag <> "-6" GROUP BY tld' % tb_name)
    results = db.fetch_all_rows()
    return results


def create_queue():
    for i in xrange(97, 123):     # 创建任务队列，a-z
        queue.put(chr(i))
    queue.put('other')   # domain_whois_other 加入队列
    queue.put('num')


def tld_whois_sum():
    """主操作"""
    print str(datetime.now()), '开始统计各个顶级后缀的whois数量和whois总量'
    global  sum_tld_whois
    sum_tld_whois = defaultdict(list)
    create_queue()
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=count_domain)
        worker.setDaemon(True)
        worker.start()
    queue.join()
    update_db()
    print str(datetime.now()), '结束统计各个顶级后缀的whois数量和whois总量'

tld_whois_sum()