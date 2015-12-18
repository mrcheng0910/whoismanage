#!/usr/bin/python
# encoding:utf-8
"""
网站后台定期更新程序
功能：更新表domain_summary,domain_update两个表。

"""
import sys
from database import conn_db
import time
import threading
from threading import Thread
from Queue import Queue
import MySQLdb


num_thread = 5      # 线程数量
queue = Queue()     # 任务队列，存储sql


def count_domain(q, queue):
    """计算各个列表中，各个顶级后缀的数量，并求和"""
    while 1:
        content = queue.get()
        if not content:
            queue.task_done()
            # break
        try:
            print "线程：" + str(q) + "探测各个域名顶级后缀的域名数量..."
            conn = conn_db()
            cur = conn.cursor()
            cur.execute(content)
            conn.commit()
            queue.task_done()
            time.sleep(1)  # 去掉偶尔会出现错误
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            print "线程: "+str(q)+" 探测结束"
            cur.close()
            conn.close()


def create_queue():
    """
    创建任务队列91
    """
    for i in xrange(65, 91):     # 创建任务队列，A-Z
        
        sql = "INSERT INTO table_overall_histroy (table_name,flag_undetected,\
               flag_no_svr,flag_no_connect,flag_reg_info,flag_reg_date,flag_part_info) \
               SELECT  \
                 'domain_whois_%s' AS `table_name`, \
                 COUNT( CASE WHEN flag ='-6' THEN 1 ELSE NULL END ) AS `flag_undetected`,\
                 COUNT( CASE WHEN flag = '-5' THEN 1 ELSE NULL END ) AS `flag_no_svr`, \
                 COUNT( CASE WHEN flag = '-1' OR flag ='-2' OR flag = '-3'  OR flag = '-4' THEN 1        ELSE NULL END ) AS `flag_no_connect`,\
                 COUNT( CASE WHEN flag = '120' OR flag ='121' OR flag = '122'  THEN 1 ELSE NULL END )    AS `flag_reg_info`, \
                 COUNT( CASE WHEN flag = '110' OR flag ='102' OR flag = '112'  THEN 1 ELSE NULL END )    AS `flag_reg_date`, \
                 COUNT( CASE WHEN flag = '100' OR flag ='101' OR flag = '111'  THEN 1 ELSE NULL END )    AS `flag_part_info` \
               FROM domain_whois_%s" % (chr(i),chr(i))
        queue.put(sql)
    
    sql_num = "INSERT INTO table_overall_histroy (table_name,flag_undetected,\
               flag_no_svr,flag_no_connect,flag_reg_info,flag_reg_date,flag_part_info) \
               SELECT  \
                 'domain_whois_num' AS `table_name`, \
                 COUNT( CASE WHEN flag ='-6' THEN 1 ELSE NULL END ) AS `flag_undetected`,\
                 COUNT( CASE WHEN flag = '-5' THEN 1 ELSE NULL END ) AS `flag_no_svr`, \
                 COUNT( CASE WHEN flag = '-1' OR flag ='-2' OR flag = '-3'  OR flag = '-4' THEN 1        ELSE NULL END ) AS `flag_no_connect`,\
                 COUNT( CASE WHEN flag = '120' OR flag ='121' OR flag = '122'  THEN 1 ELSE NULL END )    AS `flag_reg_info`, \
                 COUNT( CASE WHEN flag = '110' OR flag ='102' OR flag = '112'  THEN 1 ELSE NULL END )    AS `flag_reg_date`, \
                 COUNT( CASE WHEN flag = '100' OR flag ='101' OR flag = '111'  THEN 1 ELSE NULL END )    AS `flag_part_info` \
               FROM domain_whois_num" 
    queue.put(sql_num)  # domain_whois_num 加入队列
    sql_other = "INSERT INTO table_overall_histroy (table_name,flag_undetected,\
               flag_no_svr,flag_no_connect,flag_reg_info,flag_reg_date,flag_part_info) \
               SELECT  \
                 'domain_whois_other' AS `table_name`, \
                 COUNT( CASE WHEN flag ='-6' THEN 1 ELSE NULL END ) AS `flag_undetected`,\
                 COUNT( CASE WHEN flag = '-5' THEN 1 ELSE NULL END ) AS `flag_no_svr`, \
                 COUNT( CASE WHEN flag = '-1' OR flag ='-2' OR flag = '-3'  OR flag = '-4' THEN 1        ELSE NULL END ) AS `flag_no_connect`,\
                 COUNT( CASE WHEN flag = '120' OR flag ='121' OR flag = '122'  THEN 1 ELSE NULL END )    AS `flag_reg_info`, \
                 COUNT( CASE WHEN flag = '110' OR flag ='102' OR flag = '112'  THEN 1 ELSE NULL END )    AS `flag_reg_date`, \
                 COUNT( CASE WHEN flag = '100' OR flag ='101' OR flag = '111'  THEN 1 ELSE NULL END )    AS `flag_part_info` \
               FROM domain_whois_other"
    queue.put(sql_other)  # domain_whois_other 加入队列
    
def create_thread():
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=count_domain, args=(q, queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()

def table_overall():
    """主操作"""
    create_queue()
    create_thread()
    