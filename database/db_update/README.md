#domain_whois相关信息表更新程序
##更新程序
- `update_datebase.py`:  tld_whois_sum表（有whois信息的域名数量，以tld分组）初始化程序
- `update_ssvr.py`:msvr_ssvr表中ssvr字段（二级服务器数量）定时更新函数
- `update_summary.py`:domain_summary表（各顶级后缀对应的域名数量）定时更新程序
- `update_tld_whois_flag.py`:tld_whois_flag表的定时更新程序
- `update_top_sec_svr.py`:top_sec_svr表（二级服务器对应的顶级服务器及域名数量）定时更新程序
##触发器
- `update_summary.sql`:触发器--将domain_summary表中最新数据更新到domain_update表中
- `update_trigger.sql`:触发器--统计所有含有whois信息的域名数量，按tld分组，存入tld_whois_sum表中