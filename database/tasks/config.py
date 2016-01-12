# encoding:utf-8
"""
数据库配置文件
"""

# 源数据库配置
SOURCE_CONFIG = {
    'host': '172.26.253.3',
    'port': 3306,
    'user': 'root',
    'passwd': 'platform',
    'db': 'DomainWhois',
    'charset': 'utf8'
}

# 目标数据库配置
DESTINATION_CONFIG = {
    'host': '172.26.253.3',
    'port': 3306,
    'user': 'root',
    'passwd': 'platform',
    'db': 'domain_whois_statistics',
    'charset': 'utf8'
}