# encoding:utf-8

"""
功能：统计数据库中最新的域名数据domain_summary,domain_update两个表。
作者：程亚楠
更新：2016.1.10（程亚楠）
使用了collections模块，提高程序效率以及可读性
更新：2015.12.28
"""

import time
import threading
from threading import Thread
from Queue import Queue
from collections import defaultdict
from datetime import datetime
from data_base import MySQL
from config import DESTINATION_CONFIG


num_thread = 5      # 线程数量
queue = Queue()     # 任务队列，存储sql
lock = threading.Lock()  # 变量锁
sum_domains = defaultdict(list)  # 存储所有表的合字典


def merge_same_tld(tb_tld_num):
    """
    合并所有表中相同tld到字典列表中
    :param tb_tld_num:Tuple 当前表中各个tld的内容
    """
    for item, value in tb_tld_num:
        sum_domains[item].append(value)


def sum_all_domains():
    """计算各个tld的域名数量"""
    tld_num = []
    for item in sum_domains:
        tld_num.append((item,sum(sum_domains[item])))
    return tld_num


def count_domain():
    """
    计算域名的数量
    :param q:线程编号
    :param queue: 任务队列
    :return:
    """
    while 1:
        tb_name = queue.get()
        tb_tld_num = get_resource_data(tb_name)
        lock.acquire()  # 锁
        merge_same_tld(tb_tld_num)
        lock.release()  # 解锁
        queue.task_done()
        time.sleep(1)  # 去掉偶尔会出现错误


def get_resource_data(tb_name):
    """
    得到原始数据
    :param tb_name: string 表名
    :return: results: 查询结果
    """
    db = MySQL(DESTINATION_CONFIG)
    db.query('SELECT tld, sum(whois_sum) AS count FROM domain_whois_%s  GROUP BY tld' % tb_name)
    results = db.fetchAllRows()
    db.close()
    return results


def update_db():
    """更新数据库"""
    tld_num = sum_all_domains()
    db = MySQL(DESTINATION_CONFIG)
    db.truncate('TRUNCATE TABLE domain_summary')
    update_sql = 'INSERT INTO domain_update(tld_name, domain_num) VALUES("%s", "%s")'
    summary_sql = 'INSERT INTO domain_summary(tld_name, domain_num) VALUES("%s", "%s")'
    for tld,num in tld_num:
        db.insert_no_commit(update_sql % (tld,num))
        db.insert_no_commit(summary_sql % (tld,num))
    db.commit()
    db.close()


def create_queue():
    """创建任务队列，即表名称"""
    for i in xrange(97, 123):     # 创建任务队列，a-z
        queue.put(chr(i))
    queue.put('num')  # num 加入队列
    queue.put('other')  # other 加入队列


def create_thread():
    """创建任务线程"""
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=count_domain)
        worker.setDaemon(True)
        worker.start()
    queue.join()


def count_tld_domains():
    """主操作"""
    print str(datetime.now()), '开始统计数据库中域名数量'
    global sum_domains
    sum_domains = defaultdict(list)  # 务必添加，初始化，否则会一直累加
    create_queue()
    create_thread()
    update_db()
    print str(datetime.now()), '结束统计数据库中域名数量'

count_tld_domains()