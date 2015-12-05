#!/usr/bin/python
# encoding:utf-8
"""
网站后台定期更新程序，完成数据库中域名和WHOIS数量的统计分类
程亚楠
"""
import sys
import MySQLdb
import time
from datetime import datetime
import threading
import apscheduler
from threading import Thread
from Queue import Queue
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

hours = 5  
start_date = '2015-11-17 12:00:00'
lock = threading.Lock()
num_thread = 15      # 线程数量
queue = Queue()     # 任务队列，存储sql
sum_domains = []    # 存储域名的和


def sum_all_domains(sum_domains=[], single_domains=[]):
    """合并两个列表，相同名称求和"""

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


def count_domain(q, queue):
    """计算各个列表中，各个顶级后缀的数量，并求和"""
    while 1:
        if queue.empty():
            break
        content = queue.get()
        print content.split()[8]+' started by threading_' + str(q) 
        # if not content:    #无用
        #     queue.task_done()
        try:
            conn = conn_db()
            cur = conn.cursor()
            cur.execute(content)
            single_domains = cur.fetchall()
            cur.close()
            # conn.close()
            lock.acquire()  # 锁
            sum_all_domains(sum_domains, list(single_domains))
            lock.release()  # 解锁
            print content.split()[8]+' finished'
            queue.task_done()
            time.sleep(1)  # 去掉偶尔会出现错误
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            if conn:
                conn.close()


def update_db():
    """更新数据库"""
    conn = conn_db()
    current_time = datetime.now()
    sql = 'INSERT INTO domain_update(tld_name, domain_num,update_time) VALUES(%s, %s,%s)'
    cur = conn.cursor()
    for domain in sum_domains:
        cur.execute(sql, (domain[0], domain[1], current_time))
    # single_domains = cur.fetchall()
    conn.commit()
    conn.close()

    print 'update_db succesed'


def main():
    """操作"""
    global sum_domains
    for i in xrange(65, 91):     # 创建任务队列，A-Z
        sql = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, count(*) AS count \
               FROM domain_whois_%s  GROUP BY tld' % chr(i)
        queue.put(sql)
    sql_num = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, count(*) AS count \
                FROM domain_whois_num GROUP BY tld'
    queue.put(sql_num)  # domain_whois_num 加入队列
    sql_other = 'SELECT SUBSTRING_INDEX(domain,".",-1) as tld, count(*) AS count \
                FROM domain_whois_other GROUP BY tld'
    queue.put(sql_other)  # domain_whois_other 加入队列

    for q in xrange(num_thread):  # 开始任务
        worker = Thread(target=count_domain, args=(q, queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()

    print '----------------------------------'
    t = time.localtime()
    print ('start time:{0}-{1}-{2} {3}:{4}:{5}'.format(t[0], t[1], t[2], t[3], t[4], t[5]))
    print '----------------------------------'
    for value in sum_domains:
        print value
    update_db()
    sum_domains = []
    t = time.localtime()
    print ('finished time:{0}-{1}-{2} {3}:{4}:{5}'.format(t[0], t[1], t[2], t[3], t[4], t[5]))


def err_listener(ev):
    err_logger = logging.getLogger('schedErrJob')
    if ev.exception:
        err_logger.exception('%s error.', str(ev.job))
    else:
        err_logger.info('%s miss', str(ev.job))


def summry_time():
    start = time.clock()
    lock = threading.Lock()

    scheduler = BlockingScheduler()
    scheduler.add_listener(err_listener, apscheduler.events.EVENT_JOB_ERROR | apscheduler.events.EVENT_JOB_MISSED)
    scheduler.add_job(main, 'interval', hours=hours, start_date=start_date )
    scheduler.print_jobs()
    scheduler.start()

    # # main()
    # elapsed = (time.clock() - start)
    # print("Time used:", elapsed)


if __name__ == '__main__':
    summry_time()
