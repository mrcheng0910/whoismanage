# encoding:utf-8
"""
更新top_sec_svr定时更新程序
作者：程亚楠
更新时间：2016.1.10
"""

import time
import threading
from Queue import Queue
from threading import Thread
from datetime import datetime
from collections import defaultdict
from data_base import MySQL
from config import DESTINATION_CONFIG, SOURCE_CONFIG


sum_svr = defaultdict(list)
num_thread = 5  # 线程数量
queue = Queue()  # 任务队列，存储sql语句
lock = threading.Lock()  # 锁


def merge_svr_num(tb_svr_num):
    """
    合并所有表的服务器信息
    :param tb_svr_num:
    :return:
    """
    for top, sec, num in tb_svr_num:
        sum_svr[(top,sec)].append(num)


def sum_all_list():
    """
    合并两个表，top_svr,sec_svr相同的合并
    :param sum_svr:
    :param single_svr:
    :return:
    """
    svr_num = []
    for item in sum_svr:
        svr_num.append((item[0], item[1], sum(sum_svr[item])))
    return svr_num


def update_db():
    """
    更新数据库
    """
    svr_num = sum_all_list()
    db = MySQL(DESTINATION_CONFIG)
    db.truncate('TRUNCATE TABLE top_sec_svr')
    sql = 'INSERT INTO top_sec_svr(top_svr, sec_svr, whois_sum) VALUES("%s", "%s", "%s")'
    for top,sec,num in svr_num:
        db.insert_no_commit(sql % (top,sec,num))
    db.commit()
    db.close()


def get_source_data(tb_name):
    """
    得到基础数据
    :param tb_name:string 表名
    :return:
    """
    db = MySQL(SOURCE_CONFIG)
    sql = 'SELECT top_whois_server as top_svr, sec_whois_server AS sec_svr, count(*) \
               FROM domain_whois_%s WHERE sec_whois_server <> "" GROUP BY top_svr, sec_svr' % tb_name

    db.query(sql)
    results = db.fetch_all_rows()
    db.close()
    return results


def create_queue():
    """创建任务队列"""
    for i in xrange(65, 91):     # 创建任务队列，A-Z
        queue.put(chr(i))
    queue.put('num')   # domain_whois_num 加入队列
    queue.put('other')


def count():
    """
    任务操作：获取表中二级服务器数量并添加到num_svr
    :param q:
    :param queue:
    :return:
    """
    while 1:
        tb_name = queue.get()
        tb_svr_num = get_source_data(tb_name)
        lock.acquire()  # 加锁
        merge_svr_num(tb_svr_num)
        lock.release()  # 解锁
        queue.task_done()
        time.sleep(1)


def create_thread():
    """
    创建线程
    :return:
    """
    for q in xrange(num_thread):  # 开始任务
        worker = Thread(target=count)
        worker.setDaemon(True)
        worker.start()
    queue.join()


def top_sec():
    print str(datetime.now()),'开始统计最新的二级服务器地址'
    global sum_svr
    # sum_svr = []
    sum_svr = defaultdict(list)
    create_queue()
    create_thread()
    update_db()
    print str(datetime.now()),'结束统计最新的二级服务器地址'

# top_sec()
