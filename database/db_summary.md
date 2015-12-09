### 数据库表整体介绍
1. `domain_whois_A---domain_whois_Z`,为根据主域名首字母建立的域名WHOIS信息存储表;
2. `domain_whois_num`，主域名首字母为数字的域名WHOIS信息存储表;
3. `domain_whois_other`,顶级后缀或者主域名为特殊字符的域名WHOIS信息存储表;
4. `domain_summary`,统计域名WHOIS信息存储表中，各个顶级后缀的域名的**最新数量**;
5. `domain_update`, 定期统计域名WHOIS信息存储表中，各个顶级后缀的域名数量，最新数据则保存到`domain_summary`内;
6. `msvr_ssvr`,存储主和次域名WHOIS服务器的各自数量；
7. `tld_details`，存储**最新**域名顶级后缀,包括后缀类型、管理组织、网址等；
8. `tld_whois_sum`,存储各个域名顶级后缀已经获取的域名WHOIS信息数量；
9. `whois_addr`，存储WHOIS信息获取需要的各类信息，包括主服务器，函数名称，标记位等;
10. `svr_country`,记录域名WHOIS服务器的地理位置;
11. [`tld_whois_flag`](#t),记录已有whois信息的flag标志位的分布情况
12. [`tld_whois_sum_history`](#tld_whois_sum_history),记录数据库中每天每小时各个域名顶级后缀探测的域名whois的总数，**该表每小时更新一次**
12. [`whois_sum`](#whois_sum),记录每天每小时的数据库中域名whois的总数，简单来说就是多少个域名已探测，**该表每小时更新一次**；
13. [`whois_sum_by_day`](#whois_sum_by_day)，记录每天数据库中已经探测得到的域名WHOIS总数,**该表在每天晚上12点之前更新一次**

### 负责人说明
1. **程亚楠**负责整个数据库的信息维护；
2. **王凯**负责表1-3、9的维护；
3. **赵新岭**负责表4、5、6、8维护
4. **马有为**负责表7的维护
5. **程亚楠**负责表10、11、12、13的维护

### 表功能说明
1. 表1-3、9为域名WHOIS信息存储表，为获取系统的整体表。
2. 表4-8、9为域名WHOIS信息统计web所需要表。

###
- 数据库名称：DomainWhois

## 表结构详细说明
介绍各个表的结构，字段说明

<h3 id="tld_whois_sum_history">tld_whois_sum_history</h3>

字段说明

- id：编号
- tld: 域名顶级后缀
- whois\_sum：目前为止总共探测的域名whois数量
- update\_date:更新时间

例子：

id    | tld  | whois_sum  | update_date
------|------|---------|---------
1| net| 434343434|2015-12-07 09:40:45
2| org| 22222222|2015-12-07 10:42:32

<h3 id="whois_sum">whois_sum</h3>

字段说明

- id：编号
- tld_sum：目前为止总共探测的域名数量
- insert_date:更新时间

例子：

id    | tld_sum  | insert_date
------|------|---------
1| 30098330| 2015-12-07 09:40:45
2| 30101000| 2015-12-07 10:42:32


<h3 id="whois_sum_by_day">whois_sum_by_day</h3>

字段说明

- id：编号
- sum：目前为止总共探测的域名数量
- insert_date:更新时间

例子:

id    | sum  | insert_date
------|------|---------
1| 30098330| 2015-12-04 09:40:45
2| 30101000| 2015-12-05 09:40:45
