# conding:utf-8
# encoding:utf8
'''
二级服务器数量定期更新程序
赵新岭
'''

import sys
import time
import MySQLdb
import logging
import threading
import apscheduler
from Queue import Queue
from datetime import datetime
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler

hours = 3
start_date = '2015-11-18 19:00:00'
num_ssvr = 0  # 二级服务器数量
sum_ssvr = []  #二级服务器列表
num_thread = 5  # 线程数量
queue = Queue()  # 任务队列，存储sql语句
lock = threading.Lock()  # 锁



def update_db():
    """更新数据库"""
    try:
        global num_ssvr
        global sum_ssvr
        sum_ssvr = set(sum_ssvr)
        conn = conn_db()
        current_time = datetime.now()
        sql = 'UPDATE  msvr_ssvr SET ssvr = %s, SET update_time=%s WHERE id = 1'
        cur = conn.cursor()
        num_ssvr = len(sum_ssvr)
        cur.execute(sql, (num_ssvr, current_time))
        # single_domains = cur.fetchall()
        conn.commit()
        conn.close()
        print 'update_db succesed'
    except MySQLdb.Error, e:
        print "update_db Error %d: %s " % (e.args[0], e.args[1])


def count_ssvr(q, queue):
    '''任务操作：获取表中二级服务器数量并添加到num_ssvr'''
    while True:
        global num_ssvr

        if queue.empty():
            print '-------------queue empty --------------'
            break
        conn = conn_db()
        try:
            content = queue.get()
            print content.split()[5] + ' started by threading_' + str(q)
            cur = conn.cursor()
            cur.execute(content)
            single_ssvr = cur.fetchall()
            cur.close()

            lock.acquire()  # 加锁
            sum_ssvr.extend(list(single_ssvr))
            lock.release()  # 解锁

            print content.split()[5] + ' finished'
            queue.task_done()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            if conn:
                conn.close()


def create_thread():
    '''创建线程'''
    for q in xrange(num_thread):  # 开始任务
        worker = Thread(target=count_ssvr, args=(q, queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()


def main():
    global sum_ssvr
    global num_ssvr
    global queue
    sum_ssvr = []
    num_ssvr = 0
    t = time.localtime()
    print ('Started time:{0}-{1}-{2} {3}:{4}:{5}'.format(t[0], t[1], t[2], t[3], t[4], t[5]))
    queue = put_queue(queue)
    create_thread()
    update_db()
    print sum_ssvr
    print num_ssvr
    t = time.localtime()
    print ('Finished time:{0}-{1}-{2} {3}:{4}:{5}'.format(t[0], t[1], t[2], t[3], t[4], t[5]))


def ssvr_time():
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', hours=hours, start_date=start_date)
    scheduler.print_jobs()
    scheduler.start()


if __name__ == '__main__':
    ssvr_time()

