#!/usr/bin python
#encoding:utf8
# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
#import mysql.connector
# 创建对象的基类:
Base = declarative_base()

# 定义User对象: //与原数据表要对应！！！！！！
class Domain(Base):
    # 表的名字:
    __tablename__ = 'tld_whois_sum'

    # 表的结构:
    id = Column(String(11), primary_key=True)
    tld = Column(String(255))
    whois_sum = Column(String(255))
    # update_time = Column(Datetime)
    
    

# 初始化数据库连接:
#用法：'数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名' ！！！
engine = create_engine('mysql+mysqlconnector://root:platform@172.26.253.3:3306/DomainWhois')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

#以上代码完成SQLAlchemy的初始化和具体每个表的定义。如果有其他表则继续定义其他class

#由于有了ORM，我们向数据库表中添加一行记录，可以视为添加一个User对象：！！！！！
# 创建session对象:
session = DBSession()
# 创建新User对象:！！！！！！！！！！！
new_user = Domain(tld='5',whois_sum='Bob')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()