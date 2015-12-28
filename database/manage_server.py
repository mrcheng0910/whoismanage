#!/usr/bin/python
#encoding:utf-8

import sys
import time
from tasks.update_flag import update_whois_flag
from tasks.update_tld_whois import tld_whois_sum  # 更新tld_whois_sum_history,whois_sum
from tasks.simple_update import update_day,update_top_sec_num 
from tasks.update_domain import tld_domain
from tasks.update_top_sec_svr import top_sec

from tasks.update_table_overall import table_overall # 更新table_overall_history表

try:
    import schedule
except ImportError:
    sys.exit("无schedul模块,请安装 easy_install schedule")


if __name__ == "__main__":
    
    schedule.every().hour.do(tld_whois_sum)   #  更新whois探测相关表
    schedule.every().hour.do(update_whois_flag)  # 更新域名顶级后缀的whois数量
    schedule.every().day.do(tld_domain)
    schedule.every().hour.do(top_sec)
    schedule.every().hour.do(table_overall)  # 每2小时更新table_overall_history表
    schedule.every().day.at("23:40").do(update_day) # 更新每天的whois探测数量
    schedule.every().hour.do(update_top_sec_num)  # 更新顶级和二级服务器数量
    
    while True:
        schedule.run_pending()
        time.sleep(1)