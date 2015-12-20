#!/usr/bin/python
# encoding:utf-8
"""
更新DomainWhois.table_overall_history表,汇总28张表中各个标记位的情况
@作者：程亚楠
@时间：2015.12.20
"""
import sys
from database import conn_db
import time
from threading import Thread
from Queue import Queue
import MySQLdb
from datetime import datetime
import re

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
    
    pattern = re.compile(r"domain_whois_(\w*)")  # 获取探测数据库表名称
    while 1:
        content = queue.get()
        table_name = pattern.search(content) # 获得表名称
        print " ".join(['开始探测时间:',str(datetime.now()),'任务:更新表table_overll','字段:',table_name.group()])
        
        try:
            conn = conn_db()
            cur = conn.cursor()
            cur.execute(content)
            cur.close()
            conn.commit()
            queue.task_done()
            time.sleep(1)  # 去掉偶尔会出现错误
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            print " ".join(['结束探测时间:',str(datetime.now()),'任务:更新表table_overll','字段:',table_name.group()])
            conn.close()


def create_queue():
    """创建任务队列
    共有28张表，需要创建28个任务
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
    """创建任务线程"""
    
    for q in range(num_thread):  # 开始任务
        worker = Thread(target=count_domain, args=(q,queue))
        worker.setDaemon(True)
        worker.start()
    queue.join()

def table_overall():
    """主操作"""
    create_queue()
    create_thread()
    