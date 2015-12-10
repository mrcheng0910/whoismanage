# encoding:utf-8
'''
top_sec_svr定时更新程序
'''

import sys
import time
import MySQLdb
from database import conn_db
import threading
from Queue import Queue
from threading import Thread


sum_svr = []
num_thread = 5  # 线程数量
queue = Queue()  # 任务队列，存储sql语句
lock = threading.Lock()  # 锁


def sum_all_list(sum_svr=[], single_svr=[]):
    '''合并两个表，top_svr,sec_svr相同的合并'''
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
    """更新数据库"""
    try:
        conn = conn_db()
        sql = 'INSERT INTO top_sec_svr(top_svr, sec_svr, whois_sum) VALUES(%s, %s, %s)'
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE top_sec_svr')
        for item in sum_svr:
            cur.execute(sql, (item[0], item[1], item[2]))
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "update_db Error %d: %s " % (e.args[0], e.args[1])


def create_queue():
    """创建任务队列"""
    for i in xrange(65, 91):     # 创建任务队列，A-Z
        sql = 'SELECT top_whois_server as top_svr, sec_whois_server AS sec_svr, count(*) \
               FROM domain_whois_%s WHERE sec_whois_server <> "" GROUP BY top_svr, sec_svr' % chr(i)
        queue.put(sql)
    sql_num = 'SELECT top_whois_server as top_svr, sec_whois_server AS sec_svr, count(*) \
                FROM domain_whois_num WHERE sec_whois_server <> "" GROUP BY top_svr, sec_svr'
    queue.put(sql_num)   # domain_whois_num 加入队列
    sql_other = 'SELECT top_whois_server as top_svr, sec_whois_server AS sec_svr, count(*) \
                FROM domain_whois_other WHERE sec_whois_server <> "" GROUP BY top_svr, sec_svr'
    queue.put(sql_other)


def count(q, queue):
    '''任务操作：获取表中二级服务器数量并添加到num_ssvr'''
    while True:
        if queue.empty():
            break
        try:
            conn = conn_db()
            content = queue.get()
            cur = conn.cursor()
            cur.execute(content)
            single_tld_whois_flag = list(cur.fetchall())
            cur.close()
            lock.acquire()  # 加锁
            sum_all_list(sum_svr, single_tld_whois_flag)
            lock.release()  # 解锁
            queue.task_done()
            time.sleep(1)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            conn.close()


def create_thread():
    '''创建线程'''
    for q in xrange(num_thread):  # 开始任务
        worker = Thread(target=count, args=(q, queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()


def top_sec():

    global sum_svr
    sum_svr = []
    create_queue()
    create_thread()
    update_db()
