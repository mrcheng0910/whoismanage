#!/usr/bin/python
# encoding:utf-8
"""
功能：统计数据库中最新的域名数据domain_summary,domain_update两个表。
作者：程亚楠
更新：2015.12.28
"""

import time
import threading
from threading import Thread
from Queue import Queue
from datetime import datetime
from data_base import MySQL
from config import DESTINATION_CONFIG


num_thread = 5      # 线程数量
queue = Queue()     # 任务队列，存储sql
sum_domains = []    # 存储域名的和
lock = threading.Lock()


def sum_all_domains(single_domains=[]):
    """合并探测的表到全局表中
    :param single_domains:当前探测的表
    :return:
    """

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


def count_domain():
    """

    :param q:线程编号
    :param queue: 任务队列
    :return:
    """
    while 1:
        tb_name = queue.get()
        single_domains = get_resource_data(tb_name)
        lock.acquire()  # 锁
        sum_all_domains(list(single_domains))
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
    db.query ('SELECT tld, sum(whois_sum) AS count FROM domain_whois_%s  GROUP BY tld' % tb_name)
    results = db.fetchAllRows()
    db.close()
    return results


def update_db():
    """更新数据库"""
    db = MySQL(DESTINATION_CONFIG)
    db.truncate('TRUNCATE TABLE domain_summary')
    update_sql = 'INSERT INTO domain_update(tld_name, domain_num) VALUES("%s", "%s")'
    summary_sql = 'INSERT INTO domain_summary(tld_name, domain_num) VALUES("%s", "%s")'
    for domain in sum_domains:
        db.insert_no_commit(update_sql % (domain[0],domain[1]))
        db.insert_no_commit(summary_sql % (domain[0],domain[1]))
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
    sum_domains = []  # 务必添加，初始化，否则会一直累加
    create_queue()
    create_thread()
    update_db()
    print str(datetime.now()), '结束统计数据库中域名数量'

# count_tld_domains()