# encoding:utf-8
"""
获取DomainWhois探测数据库中的基础数据到domain_whois_statistics统计数据库中
"""

import sys
import time
from threading import Thread
from Queue import Queue
from datetime import datetime
from data_base import MySQL
from config import DESTINATION_CONFIG, SOURCE_CONFIG

num_thread = 5  # 线程数量
queue = Queue()  # 任务队列，存储sql


def update_whois_num(q, queue):
    """计算各个列表中，各个顶级后缀的数量，并求和"""
    while 1:
        tb_name = queue.get()
        results = get_data_from_source(tb_name)
        update_destination(tb_name.lower(), results)
        queue.task_done()
        time.sleep(1)  # 去掉偶尔会出现错误


def get_data_from_source(tb_name):
    """
    :param name:string 数据库名称
    :return: results 数据库whois数量分布
    """
    source_db = MySQL(SOURCE_CONFIG)
    source_db.query('select tld,flag,count(*) as whois_sum from domain_whois_%s group by tld,flag' % (tb_name))
    results = source_db.fetchAllRows()
    source_db.close()
    return results


def update_destination(tb_name, results):
    """
    更新数据库
    :param results:
    :return:
    """
    destination_db = MySQL(DESTINATION_CONFIG)
    destination_db.truncate('TRUNCATE TABLE domain_whois_%s' % tb_name)
    for item in results:
        destination_db.insert_no_commit('INSERT INTO domain_whois_%s (tld,flag,whois_sum) VALUES ("%s","%s","%s")' % (
            tb_name, item[0], item[1], item[2]))
    destination_db.commit()
    destination_db.close()


def create_queue():
    """
    创建任务队列，即各个数据库的名称
    """
    for i in xrange(65, 91):  # 创建任务队列，A-Z
        queue.put(chr(i))
    queue.put('other')  # num 加入队列
    queue.put('num')  # other 加入队列


def update_foundation_data():
    """主操作"""
    print str(datetime.now()), '开始更新基础数据库数据'
    create_queue()
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=update_whois_num, args=(q, queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()
    print str(datetime.now()), '结束更新基础数据库数据'


# update_foundation_data()
