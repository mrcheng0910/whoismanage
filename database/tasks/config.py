# encoding:utf-8
"""
数据库配置文件
"""

SOURCE_CONFIG = {  # 原始数据库配置
    'host': '172.26.253.3',
    'port': 3306,
    'user': 'root',
    'passwd': 'platform',
    'db': 'DomainWhois',
    'charset': 'utf8'
}

DESTINATION_CONFIG = {  # 目标数据库配置
    'host': '172.26.253.3',
    'port': 3306,
    'user': 'root',
    'passwd': 'platform',
    'db': 'domain_whois_statistics',
    'charset': 'utf8'
}