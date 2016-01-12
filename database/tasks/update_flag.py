#!/usr/bin/python
# encoding:utf-8
"""
功能：更新表tld_whois_flag表
作者: 程亚楠
更新日期：2015.12.28
"""

import time
import threading
from threading import Thread
from Queue import Queue
from datetime import datetime
from collections import defaultdict
from data_base import MySQL
from config import DESTINATION_CONFIG

tld_flag_total = defaultdict(list)
num_thread = 5      # 线程数量
queue = Queue()     # 任务队列，存储sql
sum_flags = []    # 存储域名的和
lock = threading.Lock()  # 锁


def merge_same_tld_flag(tb_tld_flag):
    """

    :param tb_tld_flag: 当前表中的tld的flag信息
    :return:
    """
    for tld,flag,whois_sum in tb_tld_flag:
        tld_flag_total[(tld, flag)].append(whois_sum)
        # print tld,flag,whois_sum


def sum_all_flags(single_domains=[]):
    """合并两个列表，相同名称求和
    :param single_domains: 单独一张表中数据
    """
    tld_flag_num = []
    for item in tld_flag_total:
        tld_flag_num.append((item[0],item[1],sum(tld_flag_total[item])))
    return tld_flag_num


def count_flag():
    """计算各个列表中，各个顶级后缀的flag中域名whois数量，并求和"""
    while 1:
        tb_name = queue.get()
        tb_tld_flag = fetch_source_data(tb_name)
        lock.acquire()  # 锁
        merge_same_tld_flag(tb_tld_flag)
        lock.release()  # 解锁
        queue.task_done()
        time.sleep(1)  # 去掉偶尔会出现错误


def update_db():
    """更新数据库"""
    db = MySQL(DESTINATION_CONFIG)
    truncate_sql = 'TRUNCATE TABLE tld_whois_flag'
    db.truncate(truncate_sql)
    sql = 'INSERT INTO tld_whois_flag(tld, flag,flag_detail, whois_sum) VALUES("%s", "%s", "%s", "%s")'
    tld_flag_num = sum_all_flags()
    for tld, flag_detail, num in tld_flag_num:
        try:
            if int(flag_detail) < 0:
                flag = '0'
            elif int(flag_detail) >= 120:
                flag = '1'
            elif flag_detail == '102' or flag_detail == '110' or flag_detail == '112':
                flag = '2'
            else:
                flag = '3'
            db.insert_no_commit(sql % (tld,flag,flag_detail,num))
        except:
            continue
    db.commit()
    db.close()


def fetch_source_data(tb_name):
    """获取源数据
    :param tb_name: string 表名
    :return: results 数据
    """
    db = MySQL(DESTINATION_CONFIG)
    db.query('SELECT tld,flag,whois_sum FROM domain_whois_%s WHERE flag <> "-6" GROUP BY tld,flag' % tb_name)
    results = db.fetch_all_rows()
    db.close()
    return results


def create_queue():
    """
    创建任务队列
    """
    for i in xrange(97, 123):     # 创建任务队列，A-Z
        queue.put(chr(i))
    queue.put('num')   # domain_whois_num 加入队列
    queue.put('other')   # domain_whois_other 加入队列


def create_thread():
    """创建任务线程"""
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=count_flag)
        worker.setDaemon(True)
        worker.start()
    queue.join()


def update_whois_flag():
    """主操作"""
    print str(datetime.now()),'开始统计各个标记位的whois数量'
    global sum_flags
    sum_flags = [] # 务必添加，初始化，否则会一直累加
    create_queue()  # 创建任务队列
    create_thread() # 创建线程
    update_db()
    print str(datetime.now()),'结束统计各个标记位的whois数量'

# update_whois_flag()