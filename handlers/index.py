#encoding:utf-8
"""
首页handler
"""
import tornado.web
from models.index_db import IndexDb
import json


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        index_db = IndexDb()
        domain_num = index_db.get_domain_num()     # 获取数据库中域名总数
        tld_num = index_db.get_tld_num()                # 获取数据库中所有域名顶级后缀
        msvr_sum,ssvr_sum = index_db.get_svr_sum()      # 获取whois服务器(主/次)数量
        whois_sum = index_db.get_whois_sum()
        test = manage_flag()
        self.render('index.html',
                    title_name="测试首页",
                    domain_num=domain_num,
                    tld_num=tld_num,
                    msvr_sum=msvr_sum,
                    ssvr_sum=ssvr_sum,
                    whois_sum=whois_sum,
                    test = json.dumps(test)
                    )



def find_name(test=[],name=""):
    for index,value in enumerate(test):
        # print value
        if value['tld_name']==name:
            return index

    return -1


def flag_change(name):
    print name
    if name=='0':
        return 'no_connect'
    elif name=='1':
        return 'reg_info'
    elif name=='2':
        return 'reg_date'
    elif name=='3':
        return 'no_reg'




def manage_flag():
    test = []
    result = IndexDb().get_tld_whois_flag(5)
    for index,value in enumerate(result):
        flag=find_name(test,value['tld'])
        # print value
        if flag == -1:
            test.append({'tld_name':value['tld'],flag_change(str(value['flag'])):value['whois_sum']})
        else:
            # test[index][value['flag']] = value['whois_sum']

            d = jia(test[flag],value)
            del test[flag]
            test.append(d)
    print test
    return test
    # print test


def jia(test={},v={}):
    # print test
    # print v
    test[flag_change(v['flag'])] = v['whois_sum']
    # print test
    return test





manage_flag()