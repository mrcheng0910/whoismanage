# conding:utf-8
# encoding:utf8
'''
top_sec_svr定时更新程序
赵新岭
'''
import sys
import time
import MySQLdb
import threading
from Queue import Queue
from datetime import datetime
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler


hours = 3
start_date = '2015-11-18 19:00:00'
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
                break
        if flag == 0:
            sum_svr.append(single_svr[index_single])


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
        sql = 'INSERT INTO top_sec_svr(top_svr, sec_svr, \
            whois_sum, update_time) VALUES(%s, %s, %s, %s)'
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE top_sec_svr')
        for item in sum_svr:
            cur.execute(sql, (item[0], item[1], item[2], current_time))
        conn.commit()
        conn.close()
        print 'update_db succesed'
    except MySQLdb.Error, e:
        print "update_db Error %d: %s " % (e.args[0], e.args[1])


def put_queue():
    """创建任务队列"""
    global queue
    for i in xrange(65, 91):     # 创建任务队列，A-Z
        sql = 'SELECT top_whois_server as top_svr, sec_whois_server AS sec_svr, count(*) \
               FROM domain_whois_%s WHERE top_whois_server <> "" and \
               sec_whois_server <> "" GROUP BY top_svr, sec_svr' % chr(i)
        queue.put(sql)
    sql_num = 'SELECT top_whois_server as top_svr, sec_whois_server AS sec_svr, count(*) \
                FROM domain_whois_num WHERE top_whois_server <> "" and \
                sec_whois_server <> "" GROUP BY top_svr, sec_svr'
    queue.put(sql_num)   # domain_whois_num 加入队列
    sql_other = 'SELECT top_whois_server as top_svr, sec_whois_server AS sec_svr, count(*) \
                FROM domain_whois_other WHERE top_whois_server <> "" and \
                sec_whois_server <> "" GROUP BY top_svr, sec_svr'
    queue.put(sql_num)


def count(q, queue):
    '''任务操作：获取表中二级服务器数量并添加到num_ssvr'''
    while True:
        global sum_svr

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
            sum_all_list(sum_svr, single_tld_whois_flag)
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
    global sum_svr
    global queue
    t = time.localtime()
    print ('Started time:{0}-{1}-{2} {3}:{4}:{5}'.format(t[0], t[1], t[2], t[3], t[4], t[5]))
    sum_svr = []
    put_queue()
    create_thread()
    print '--------------'
    print sum_svr
    print '---------------'
    update_db()
    t = time.localtime()
    print ('Finished time:{0}-{1}-{2} {3}:{4}:{5}'.format(t[0], t[1], t[2], t[3], t[4], t[5]))


def top_sec_svr():
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', hours=hours, start_date=start_date)
    scheduler.print_jobs()
    scheduler.start()


if __name__ == '__main__':
    top_sec_svr()