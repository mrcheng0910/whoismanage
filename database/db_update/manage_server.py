#!/usr/bin/python
#encoding:utf-8

import sys
import time
from tasks.update_flag import update_whois_flag
from tasks.update_tld_whois import tld_whois_sum,update_day

try:
    import schedule
except ImportError:
    sys.exit("无schedul模块,请安装 easy_install schedule")


if __name__ == "__main__":
    
    schedule.every().hour.do(update_whois_flag)
    schedule.every().hour.do(tld_whois_sum)   # 每小时运行一次
    schedule.every().day.at("23:40").do(update_day)
    while True:
        schedule.run_pending()
        time.sleep(1)