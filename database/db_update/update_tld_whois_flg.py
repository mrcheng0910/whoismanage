#conding:utf-8
#encoding:utf8
'''
tld_whois_flag定时更新程序
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
start_date = '2015-11-19 15:00:00'
sum_tld_whois_flag = []
num_thread = 5  # 线程数量
queue = Queue()  # 任务队列，存储sql语句
lock = threading.Lock()  # 锁


def sum_all_list(sum_tld_whois_flag=[], single_tld_whois_flag=[]):
    '''合并两个表，tld、flag相同的合并'''
    del_index = []  #存放待删除的index
    for index_sum, value_sum in enumerate(sum_tld_whois_flag):
        for index_single, value_single in enumerate(single_tld_whois_flag):
            if value_sum[0] == value_single[0] and value_sum[1] == value_single[1]:
                sum_tld_whois_flag.append(
                    (value_sum[0], value_sum[1], value_sum[2] + value_single[2]))
                del_index.append(index_sum)
                del single_tld_whois_flag[index_single]

    sum_tld_whois_flag.extend(single_tld_whois_flag)
    del_index.reverse()
    for i in del_index:
        del sum_tld_whois_flag[i]


def conn_db():
    """连接数据库"""
    try:
        conn = MySQLdb.connect(
                host="172.26.253.3",
                user="root",
                passwd="platform",
                db="DomainWhois"
                )
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return conn


def update_db():
    """更新数据库"""
    try:
        conn = conn_db()
        current_time = datetime.now()
        sql = 'INSERT INTO tld_whois_flag(tld, flag, \
            flag_detail, whois_sum, update_date) VALUES(%s, %s, %s, %s, %s)'
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE tld_whois_flag')
        for item in sum_tld_whois_flag:
            if item[1] < 0:
                flag = 0
            elif item[1] >= 120:
                flag = 1
            elif item[1] == 102 or item[1] == 110 or item[1] == 112:
                flag = 2
            else:
                flag = 3
            cur.execute(sql, (item[0], flag, item[1], item[2], current_time))
        # single_domains = cur.fetchall()
        conn.commit()
        conn.close()
        print 'update_db succesed'
    except MySQLdb.Error, e:
        print "update_db Error %d: %s " % (e.args[0], e.args[1])


def put_queue():
    """创建任务队列"""
    global queue
    for i in xrange(65, 91):     # 创建任务队列，A-Z
        sql = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, flag, count(*) AS count \
               FROM domain_whois_%s WHERE flag <> -6 GROUP BY tld, flag' % chr(i)
        queue.put(sql)
    sql_num = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, flag, count(*) AS count \
                FROM domain_whois_num WHERE flag <> -6 GROUP BY tld,flag'
    queue.put(sql_num)   # domain_whois_num 加入队列
    sql_other = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, count(*) AS count \
                FROM domain_whois_other WHERE flag <> -6 GROUP BY tld,flag'
    queue.put(sql_num)  

def count(q, queue):
    '''任务操作：获取表中二级服务器数量并添加到num_ssvr'''
    while True:
        global sum_tld_whois_flag

        if queue.empty():
            print '-------------queue empty --------------'
            break
        conn = conn_db()
        try:
            content = queue.get()
            print content.split()[9] + ' started by threading_' + str(q)
            cur = conn.cursor()
            cur.execute(content)
            single_tld_whois_flag = list(cur.fetchall())
            cur.close()

            lock.acquire()  # 加锁
            sum_all_list(sum_tld_whois_flag, single_tld_whois_flag)
            lock.release()  # 解锁

            print content.split()[9] + ' finished'
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
        worker = Thread(target=count, args=(q, queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()


def main():
    global sum_tld_whois_flag
    global queue
    t = time.localtime()
    print ('Started time:{0}-{1}-{2} {3}:{4}:{5}'.format(t[0], t[1], t[2], t[3], t[4], t[5]))
    sum_tld_whois_flag = []
    put_queue()
    create_thread()
    print '--------------'
    print sum_tld_whois_flag
    print '---------------'
    update_db()
    t = time.localtime()
    print ('Finished time:{0}-{1}-{2} {3}:{4}:{5}'.format(t[0], t[1], t[2], t[3], t[4], t[5]))


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', hours=hours, start_date=start_date)
    scheduler.print_jobs()
    scheduler.start()