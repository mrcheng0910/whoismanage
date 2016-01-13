#encoding:utf-8

import tornado.web
from models.table_overall_db import TableOverallDb
import json
from datetime import datetime
from collections import OrderedDict  # 用来固定输出数据


class TableOverallHandler(tornado.web.RequestHandler):

    def get(self):
        results = TableOverallDb().get_table_info()
        self.render('./table_overall/table_overall.html',
                    results = json.dumps(results)
                    )
                    
class TableDataHistoryHandler(tornado.web.RequestHandler):
    
    def get(self):
        table_name = self.get_argument('table_name','None')
        results = TableOverallDb().get_data_history(table_name)
        self.render('./table_overall/table_data_history.html',
                    results = json.dumps(results,default=self._json_serial)
        )

    def _json_serial(self, obj):
        """格式化时间"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError ("Type not serializable")


class TableIncreaseHandler(tornado.web.RequestHandler):
    """数据库表增长趋势统计"""

    def get(self):

        tb_increase, tb_total = TableOverallDb().fetch_table_increase(top=11)  # 近top个小时内数据
        tb_increase = self._increase(tb_increase,tb_total)

        self.render(
            './table_overall/table_increase.html',
            tb_increase = tb_increase
        )

    def _increase(self, tb_increase,tb_total):
        """增长率
        :param tb_increase:
        :return:
        """
        results = {}
        temp = []
        sort_results = OrderedDict()  # 存储固定字典数据
        for item in tb_increase:
            temp.append(tb_increase[item][0])  # 已经探测的域名数量
            temp.append(tb_total[item][0])  # 域名总数
            # temp.append(self._data2increase(tb_increase[item]))
            increase,flag = self._data2increase(tb_increase[item])
            temp.append(increase)
            temp.append(flag)
            results[item] = temp
            temp = []   # 清空

        keys = results.keys()
        keys.sort()
        print keys
        for key in keys:
            sort_results[key] = results[key]
        return sort_results

    def _data2increase(self, data_list):
        """将列表中的数据变为增长率
        :param data_list: 原始数据列表
        :return: results 增长率的数据
        """
        results = []
        data_list.reverse()
        length = len(data_list)
        for i in range(1,length):
            results.append(data_list[i]-data_list[i-1])

        return self._list2str(results),self.judge_flag(results)

    def _list2str(self, list_data):
        """将int类型的list转为字符串
        :param list_data:待转换的list
        :return: 字符串
        """
        return ','.join(str(item) for item in list_data)

    def judge_flag(self,results):
        tmp_result = results[:]
        tmp_result.reverse()
        if tmp_result[0] == 0 and tmp_result[1]== 0 and tmp_result[2] == 0:
            return 'danger'
        elif tmp_result[0] == 0 and tmp_result[1] == 0:
            return 'warning'
        elif tmp_result[0] == 0:
            return 'info'
        else:
            return ''