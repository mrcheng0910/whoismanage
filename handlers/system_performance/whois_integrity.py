# encoding:utf-8
"""
统计域名whois信息的完整性
"""
import tornado.web
from models.domain_whois_db import DomainWhoisDb
import json

PATH = './system_performance/'

class DomainWhoisHandler(tornado.web.RequestHandler):
    def get(self):
        tld_whois_sum = manage_flag()  # 获取whois类型信息
        self.render(PATH+'whois_integrity.html',
                    tld_whois_sum=json.dumps(tld_whois_sum)
                    )


def manage_flag():
    """
    获取前top顶级后缀域名的whois信息的数量类型分布
    :return tld_whois_sum:
    """
    tld_whois_sum = []
    top = 15  # 域名whois数量前top，默认为10
    results = DomainWhoisDb().get_tld_whois_flag(top)  # 获取查询结果
    for index, value in enumerate(results):
        flag = find_tld(tld_whois_sum, value['tld'])  # 查询顶级后缀是否已在列表中
        if flag == -1:  # 若无则加入到列表中
            tld_whois_sum.append({'tld_name': value['tld'], flag_change(str(value['flag'])): value['whois_sum']})
        else:
            tld_whois = merge_tld_whois(tld_whois_sum[flag], value)
            del tld_whois_sum[flag]  # 删除原来的数据
            tld_whois_sum.append(tld_whois)  # 添加新数据
    return tld_whois_sum


def merge_tld_whois(tld_whois, value):
    """
    向域名whois字典中添加新的数据
    :param tld_whois: 已有的域名whois信息
    :param value:要插入的数据
    :return:返回新数据
    """
    tld_whois[flag_change(value['flag'])] = value['whois_sum']
    return tld_whois

def find_tld(tld_whois_sum, tld_name):
    """
    查询顶级后缀是否在列表中，若存在则返回位置，不存在返回-1
    :param tld_whois_sum: 域名whois类型列表
    :param tld_name: 顶级后缀名称
    :return: -1表示列表无该后缀，index表示在列表中的位置
    """
    for index, value in enumerate(tld_whois_sum):
        if value['tld_name'] == tld_name:
            return index
    return -1


def flag_change(flag):
    """
    更换标记位名称
    :param flag 标记位
    :rtype: change_flag，变化后的标记位
    """
    if flag == '0':
        return 'no_connect'  # 无法连接
    elif flag == '1':
        return 'reg_info'  # 注册人信息
    elif flag == '2':
        return 'reg_date'  # 注册日期
    elif flag == '3':
        return 'part_info'  # 部分信息
