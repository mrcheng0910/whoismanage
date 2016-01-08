# encoding:utf-8
"""
更新top_sec_svr定时更新程序

"""

import time
import threading
from Queue import Queue
from threading import Thread
from datetime import datetime
from data_base import MySQL
from config import DESTINATION_CONFIG,SOURCE_CONFIG


sum_svr = []
num_thread = 5  # 线程数量
queue = Queue()  # 任务队列，存储sql语句
lock = threading.Lock()  # 锁


def sum_all_list(single_svr=[]):
    """
    合并两个表，top_svr,sec_svr相同的合并
    :param sum_svr:
    :param single_svr:
    :return:
    """
    for index_single, value_single in enumerate(single_svr):
        flag = 0
        for index_sum, value_sum in enumerate(sum_svr):
            if value_sum[0] == value_single[0] and value_sum[1] == value_single[1]:
                del sum_svr[index_sum]
                sum_svr.insert(
                    index_sum, (value_sum[0], value_sum[1], value_sum[2] + value_single[2]))
                flag = 1
                break  # 若有相同说明已经结束
        if flag == 0:
            sum_svr.append(single_svr[index_single])


def update_db():
    """
    更新数据库
    """

    db = MySQL(DESTINATION_CONFIG)
    db.truncate('TRUNCATE TABLE top_sec_svr')
    sql = 'INSERT INTO top_sec_svr(top_svr, sec_svr, whois_sum) VALUES("%s", "%s", "%s")'
    for item in sum_svr:
        db.insert_no_commit(sql % (item[0],item[1],item[2]))
    db.commit()
    db.close()


def get_source_data(tb_name):
    """

    :param tb_name:
    :return:
    """
    db = MySQL(SOURCE_CONFIG)
    sql = 'SELECT top_whois_server as top_svr, sec_whois_server AS sec_svr, count(*) \
               FROM domain_whois_%s WHERE sec_whois_server <> "" GROUP BY top_svr, sec_svr' % tb_name

    db.query(sql)
    results = db.fetchAllRows()
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
        results = get_source_data(tb_name)
        lock.acquire()  # 加锁
        sum_all_list(list(results))
        lock.release()  # 解锁
        queue.task_done()
        time.sleep(1)


def create_thread():
    '''创建线程'''
    for q in xrange(num_thread):  # 开始任务
        worker = Thread(target=count)
        worker.setDaemon(True)
        worker.start()
    queue.join()


def top_sec():
    print str(datetime.now()),'开始统计最新的二级服务器地址'
    global sum_svr
    sum_svr = []
    create_queue()
    create_thread()
    update_db()
    print str(datetime.now()),'结束统计最新的二级服务器地址'

# top_sec()