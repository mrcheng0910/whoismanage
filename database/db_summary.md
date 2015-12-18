## 数据库表整体介绍
1. [`domain_whois_A---domain_whois_Z`](#domain_whois_*)  
	为根据主域名首字母建立的域名WHOIS信息存储表;
2. [`domain_whois_num`](#domain_whois_*)  
	主域名首字母为数字的域名WHOIS信息存储表;
3. [`domain_whois_other`](#domain_whois_*)  
	顶级后缀或者主域名为特殊字符的域名WHOIS信息存储表;
4. [`domain_summary`](#domain_summary)  
	统计域名WHOIS信息存储表中，各个顶级后缀的域名的最新数量,该表只保存最近一次统计数据;
5. [`domain_update`](#domain_update)  
	定期统计域名WHOIS信息存储表中，各个顶级后缀的域名数量，其包括历史数据，最新一次统计结果则保存到`domain_summary`;
7. [`tld_details`](#tld_details)  
	存储最新域名顶级后缀,包括后缀类型、管理组织、网址等；
8. `whois_addr`  
	存储WHOIS信息获取需要的各类信息，包括主服务器，函数名称，标记位等;
10. `svr_country`  
	记录域名WHOIS服务器的地理位置，**需要添加二级服务器，暂未更新**
10. [`msvr_ssvr`](#msvr_ssvr)  
	存储主和次域名WHOIS服务器的各自数量,每7天更新一次；
11. [`tld_whois_flag`](#tld_whois_flag)  
    记录各个域名顶级后缀的whois信息情况，通过flag标记位分类，flag\_details是详细信息。每小时更新一次最新数据
12. [`tld_whois_sum`](#tld_whois_sum)  
	记录最新一次的各个域名顶级后缀探测的域名whois的总数，每小时更新一次最新数据
13. [`tld_whois_sum_history`](#tld_whois_sum_history)  
	记录数据库中每天每小时各个域名顶级后缀探测的域名whois的总数，每小时插入一次最新数据
14. [`whois_sum`](#whois_sum)  
	记录每天每小时的数据库中域名whois的总数，简单来说就是多少个域名已探测，每小时插入一次最新数据；
15. [`whois_sum_by_day`](#whois_sum_by_day)  
	记录每天数据库中已经探测得到的域名WHOIS总数,在每天晚上11点50分左右插入一次最新数据
16. [`table_overall`](#table-overall)
    记录28张表中，数据的增长情况，包括各个标记为的数量;
17. [`table_overall`]

## 负责人说明
1. **程亚楠**负责整个数据库的信息维护；
2. **王凯**负责表1-3、9的维护；
3. **赵新岭**负责表4、5、6、8维护
4. **马有为**负责表7的维护
5. **程亚楠**负责表10、11、12、13、14、15的维护

## 表功能说明
1. 表1-3、9为域名WHOIS信息存储表，为获取系统的整体表。
2. 表4-8、9为域名WHOIS信息统计web所需要表。


## 表结构详细说明
介绍各个表的结构，字段说明

<h3 id="domain_whois_*">domain_whois_*</h3>

这类表共有28张，分别包括26个首字母表、num、other。这些表分别存储对应的域名以及whois信息。

<h3 id="domain_summary">domain_summary</h3>

**字段说明**

- id: 编号
- tld\_name: 域名顶级后缀
- domain\_num: 域名数量
- query\_time: 插入时间，应该域名插入时间，默认是insert\_timestamp，会自动更新

**例子**

id    | tld_name  | domain_num |  query_date
------|------|------|--------
1| net | 73443434  | 2015-12-07 09:40:45
2| com | 434343434| 2015-12-07 09:40:45

<h3 id="domain_update">domain_update</h3>

**字段说明**

- id: 编号
- tld\_name: 域名顶级后缀
- domain\_num: 域名数量
- query\_time: 插入时间，应该域名插入时间，默认是insert\_timestamp，会自动更新

**例子**

id    | tld_name  | domain_num |  query_date
------|------|------|--------
1| net | 73443434  | 2015-12-07 09:40:45
2| com | 434343434| 2015-12-07 09:40:45
...|...|...|...
55|net|434343434|2015-12-09 09:40:45
56|com|434343434|2015-12-09 09:40:45

<h3 id="tld_details">tld_details</h3>

**字段说明**

- id: 编号
- tld: 顶级后缀
- type：类型
- organisation:组织
- url： 官网地址

**例子**

id    | tld  | type |  organisation|url
------|------|------|--------|-----
1| com | generic  | VeriSign Global Registry Services|[http://www.iana.org/domains/root/db/com.html](http://www.iana.org/domains/root/db/com.html)
2|cn| country-code|China Internet Network Information Center (CNNIC)|[http://www.iana.org/domains/root/db/cn.html](http://www.iana.org/domains/root/db/cn.html)


<h3 id="msvr_ssvr">msvr_ssvr</h3>

**字段说明**

- id: 编号
- msvr: 主服务器数量
- ssvr: 二级服务器数量
- updata\_time: 更新时间,默认是update\_timestamp，会自动更新

**例子**

id    | msvr  | ssvr |  update_date
------|------|------|--------
1| 381 | 734  | 2015-12-07 09:40:45


<h3 id="tld_whois_flag">tld_whois_flag</h3>

**字段说明**

- id：编号
- tld: 域名顶级后缀
- flag：标记位分类
- flag\_detail:详细分类
- whois\_sum:已探测的whois数量
- update\_time:更新时间,默认为当前时间current\_timestamp

**例子：**

id    | tld  | flag | flag_detail|whois_sum  | update_date
------|------|------|---------|--------|--------
1| net| 3 | 100 | 434  | 2015-12-07 09:40:45
2| org| 2 | 122 | 222  | 2015-12-07 10:42:32
3| org| 1 | 101 | 2232 | 2015-12-07 10:42:32

**flag标记位说明**
- 0：表示无法连接；
- 1：表示注册者信息完整;
- 2:表示注册者时间完整;
- 3：表示注册者和注册时间都不完整

**flag_detail标记位说明**

序号 | flag | flag_detail |解释
----|----|----|-----
1 | 0 | -1 | 链接超时
2 | 0 | -2 | 解析失败
3 | 0 |-3 | 无法链接
4 | 0 |-4 | 其他链接错误
5 | 1 |120 | 注册者信息完整，无注册日期信息
6 | 1 |121 | 注册者信息完整，注册日期信息不完善
7 | 1 |122 | 注册者信息完整，注册日期信息完整
8 | 2 |110 | 注册者信息不完善，无注册信息
9 |2 | 102 | 无注册者信息，注册日期完整
10 |2 | 112 | 注册者信息不完善，注册日期完整
11 |3 | 100 | 无注册者信息，无注册日期
12 |3 | 101 | 无注册者信息，注册日期不完善
13 | 3 |111 | 注册者信息不完善，注册日期不完善

<h3 id="tld_whois_sum">tld_whois_sum</h3>

字段说明

- id：编号
- tld: 域名顶级后缀
- whois\_sum：目前为止总共探测的域名whois数量
- update\_date:更新时间，其实应该是插入时间,默认为当前时间current\_timestamp

例子：

id    | tld  | whois_sum  | update_date
------|------|---------|---------
1| net| 434343434|2015-12-07 09:40:45
2| org| 22222222|2015-12-07 10:42:32

<h3 id="tld_whois_sum_history">tld_whois_sum_history</h3>

字段说明

- id：编号
- tld: 域名顶级后缀
- whois\_sum：目前为止总共探测的域名whois数量
- update\_date:更新时间，其实应该是插入时间,默认为当前时间current\_timestamp

例子：

id    | tld  | whois_sum  | update_date
------|------|---------|---------
1| net| 434343434|2015-12-07 09:40:45
2| org| 22222222|2015-12-07 10:42:32

<h3 id="whois_sum">whois_sum</h3>

字段说明

- id：编号
- tld\_sum：目前为止总共探测的域名数量
- insert\_date:插入时间

例子：

id    | tld_sum  | insert_date
------|------|---------
1| 30098330| 2015-12-07 09:40:45
2| 30101000| 2015-12-07 10:42:32


<h3 id="whois_sum_by_day">whois_sum_by_day</h3>

字段说明

- id：编号
- sum：目前为止总共探测的域名数量
- insert\_date:插入时间,默认为当前时间current\_timestamp

例子:

id    | sum  | insert_date
------|------|---------
1| 30098330| 2015-12-04 09:40:45
2| 30101000| 2015-12-05 09:40:45
