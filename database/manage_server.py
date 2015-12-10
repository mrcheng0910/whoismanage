#!/usr/bin/python
#encoding:utf-8

import sys
import time
from tasks.update_flag import update_whois_flag
from tasks.update_tld_whois import tld_whois_sum
from tasks.simple_update import update_day,update_top_sec_num
from tasks.update_domain import tld_domain
from tasks.update_top_sec_svr import top_sec
try:
    import schedule
except ImportError:
    sys.exit("无schedul模块,请安装 easy_install schedule")


if __name__ == "__main__":
    
    schedule.every().hour.do(update_whois_flag)  # 更新域名顶级后缀的whois数量
    schedule.every().hour.do(tld_whois_sum)   #  更新各个whois_sum相关表
    schedule.every().day.do(update_top_sec_num)  # 更新顶级和二级服务器数量
    schedule.every().day.at("23:40").do(update_day) # 更新每天的whois探测数量
    schedule.every(8).days.do(tld_domain)
    schedule.every().day.do(top_sec)
    while True:
        schedule.run_pending()
        time.sleep(1)