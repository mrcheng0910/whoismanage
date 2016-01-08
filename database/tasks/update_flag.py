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
from data_base import MySQL
from config import DESTINATION_CONFIG


num_thread = 5      # 线程数量
queue = Queue()     # 任务队列，存储sql
sum_flags = []    # 存储域名的和
lock = threading.Lock()  # 锁


def sum_all_flags(single_domains=[]):
    """合并两个列表，相同名称求和
    :param single_domains: 单独一张表中数据
    """

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


def count_flag():
    """计算各个列表中，各个顶级后缀的flag中域名whois数量，并求和"""
    while 1:
        tb_name = queue.get()
        print tb_name
        single_flags = get_source_data(tb_name)
        lock.acquire()  # 锁
        sum_all_flags(list(single_flags))
        lock.release()  # 解锁
        queue.task_done()
        time.sleep(1)  # 去掉偶尔会出现错误


def update_db():
    """更新数据库"""
    db = MySQL(DESTINATION_CONFIG)
    sql = 'INSERT INTO tld_whois_flag(tld, flag,flag_detail, whois_sum) VALUES("%s", "%s", "%s", "%s")'
    db.truncate('TRUNCATE TABLE tld_whois_flag')
    for item in sum_flags:
        try:
            if int(item[1]) < 0:
                flag = '0'
            elif int(item[1]) >= 120:
                flag = '1'
            elif item[1] == '102' or item[1] == '110' or item[1] == '112':
                flag = '2'
            else:
                flag = '3'
            db.insert_no_commit(sql % (item[0],flag,item[1],item[2]))
        except:
            continue
    db.commit()
    db.close()


def get_source_data(tb_name):
    """
    获取原始数据
    :param tb_name: string 表名
    :return: results 结果
    """
    db = MySQL(DESTINATION_CONFIG)
    db.query('SELECT tld,flag, whois_sum AS count FROM domain_whois_%s WHERE flag <> "-6" GROUP BY tld,flag' % tb_name)
    results = db.fetchAllRows()
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