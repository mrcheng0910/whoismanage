#!/usr/bin/python
# encoding:utf-8
"""
更新DomainWhois.table_overall_history表,汇总28张表中各个标记位的情况
@作者：程亚楠
@时间：2015.12.20
"""
import time
from threading import Thread
from Queue import Queue
from datetime import datetime
from data_base import MySQL
from config import DESTINATION_CONFIG


num_thread = 5      # 线程数量
queue = Queue()     # 任务队列，存储sql


def count_domain(q,queue):
    """执行数据库更新功能
    参数：
        queue : Queue
            任务队列，存储mysql执行语句
        q : int
            线程编号
    """
    while 1:
        tb_name = queue.get()
        update_table(tb_name)
        queue.task_done()
        time.sleep(1)  # 去掉偶尔会出现错误


def update_table(tb_name):
    """
    更新表
    :param tb_name:
    :return:
    """
    sql = 'SELECT flag,sum(whois_sum) FROM domain_whois_%s GROUP BY flag' % tb_name.lower()
    flag_undetected = flag_no_svr = flag_no_connect = 0
    flag_reg_info = flag_reg_date = flag_part_info = 0
    db = MySQL(DESTINATION_CONFIG)
    db.query(sql)
    results = db.fetchAllRows()

    for item in results:
        flag = item[0]
        whois_sum = item[1]
        print whois_sum
        if flag == '-6':
            flag_undetected += whois_sum
        if flag == '-5':
            flag_no_svr += whois_sum
        elif flag == '-1' or flag == '-2' or flag == '-3' or flag == '-4':
            flag_no_connect += whois_sum
        elif flag == '120' or flag == '121' or flag == '122':
            flag_reg_info += whois_sum
        elif flag == '110' or flag == '102' or flag == '112':
            flag_reg_date += whois_sum
        elif flag == '100' or flag == '101' or flag == '111':
            flag_part_info += whois_sum

    sql = 'INSERT INTO table_overall_history (table_name,flag_undetected,\
          flag_no_svr,flag_no_connect,flag_reg_info,flag_reg_date,flag_part_info) \
          VALUES ("%s","%s","%s","%s","%s","%s","%s")' % (tb_name,flag_undetected,flag_no_svr,flag_no_connect,flag_reg_info,flag_reg_date,flag_part_info)
    db.insert(sql)
    db.close()


def create_queue():
    """创建任务队列
    共有28张表，需要创建28个任务
    """
    for i in xrange(65, 91):     # 创建任务队列，A-Z
        queue.put(chr(i))
    queue.put('num')  # domain_whois_num 加入队列
    queue.put('other')  # domain_whois_other 加入队列


def create_thread():
    """创建任务线程"""
    
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=count_domain, args=(q,queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()


def table_overall():
    """主操作"""
    print str(datetime.now()),'开始统计数据库表WHOIS信息'
    create_queue()
    create_thread()
    print str(datetime.now()),'结束统计数据库表WHOIS信息'


# table_overall()