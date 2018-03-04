# -*- coding: utf-8 -*-

from sqlalchemy import create_engine,text,update
#mysql 日期设置默认值必须使用timestamp类型
from sqlalchemy import Column,String,Integer,ForeignKey,BigInteger,Date,TIMESTAMP
#func用来生成数据库函数代码，跟踪进源代码看一***释就明白了
from sqlalchemy.sql import func
#创建对象的基类
from sqlalchemy.ext.declarative import declarative_base
#创建DB的会话类型,就是传一些连接信息里面去
from sqlalchemy.orm import sessionmaker


#python3必加
import pymysql
pymysql.install_as_MySQLdb()


engine = create_engine('mysql://root:huawei@localhost:3306/juntechGW',
                       )

Base = declarative_base()

class WhiteList(Base):
    __tablename__ = 'white_list'
    id = Column(Integer,primary_key=True)                       
    name = Column(String(32))                                
    os_type = Column(String(32))                                
    hostname = Column(String(32))                                   
    mac = Column(String(32),unique=True)                                  
    ip = Column(String(32))                                    
    createtime = Column(String(32))                               
    expiretime = Column(String(32))
    createtime_timestamp = Column(BigInteger)
    expiretime_timestamp = Column(BigInteger)
    #将字段类型设为TIMESTAMP ,那么sql将自动写入生成时间
    sql_createtime = Column(TIMESTAMP, server_default = func.now())
    interface = Column(String(16))
    network = Column(String(32))
    dept = Column(String(32))
    job_number = Column(String(32))
    content = Column(String(256))
    last_visit = Column(String(32))
    status = Column(Integer,default=0)

    def __repr__(self):
        return ("<WhiteList>(name = '%s',os_type = '%s', hostname = '%s', mac = '%s',ip = '%s', \
                createtime = '%s',expiretime = '%s', createtime_timestamp = '%s', expiretime_timestamp = '%s',interface= '%s', \
                network = '%s',dept = '%s',job_number = '%s',content = '%s',last_visit = '%s',status = '%s')")   \
            %(     self.name,
                   self.os_type,
                   self.hostname,
                   self.mac,
                   self.ip,
                   self.createtime,
                   self.expiretime,
                   self.createtime_timestamp,
                   self.expiretime_timestamp,
                   self.interface,
                   self.network,
                   self.docker_version,
                   self.dept,
                   self.job_number,
                   self.content,
                   self.last_visit,
                   self.status,
            )



class UserHistory(Base):
    __tablename__ = 'user_history'
    id = Column(Integer,primary_key=True)                       
    name = Column(String(32))                                
    os_type = Column(String(32))                                
    hostname = Column(String(32))                                   
    mac = Column(String(32),)                                  
    ip = Column(String(32))                                    
    createtime = Column(String(32))                               
    expiretime = Column(String(32))
    createtime_timestamp = Column(BigInteger)
    expiretime_timestamp = Column(BigInteger)
    #将字段类型设为TIMESTAMP ,那么sql将自动写入生成时间
    sql_createtime = Column(TIMESTAMP, server_default = func.now())
    interface = Column(String(16))
    network = Column(String(32))
    dept = Column(String(32))
    job_number = Column(String(32))
    content = Column(String(256))
    last_visit = Column(String(32))
    status = Column(Integer,default=1)


    def __repr__(self):
        return ("<WhiteList>(name = '%s',os_type = '%s', hostname = '%s', mac = '%s',ip = '%s', \
                createtime = '%s',expiretime = '%s', createtime_timestamp = '%s', expiretime_timestamp = '%s',interface= '%s', \
                network = '%s',dept = '%s',job_number = '%s',content = '%s',last_visit = '%s')")   \
            %(     self.name,
                   self.os_type,
                   self.hostname,
                   self.mac,
                   self.ip,
                   self.createtime,
                   self.expiretime,
                   self.createtime_timestamp,
                   self.expiretime_timestamp,
                   self.interface,
                   self.network,
                   self.docker_version,
                   self.dept,
                   self.job_number,
                   self.content,
                   self.last_visit,
                   self.status,
            )

class CasualUser(Base):
    __tablename__ = 'casual_user'
    id = Column(Integer,primary_key=True)                       
    name = Column(String(32))                                
    os_type = Column(String(32))                                
    hostname = Column(String(32))                                   
    mac = Column(String(32),unique=True)                                  
    ip = Column(String(32))                                    
    createtime = Column(String(32))                               
    expiretime = Column(String(32))
    createtime_timestamp = Column(BigInteger)
    expiretime_timestamp = Column(BigInteger)
    #将字段类型设为TIMESTAMP ,那么sql将自动写入生成时间
    sql_createtime = Column(TIMESTAMP, server_default = func.now())
    interface = Column(String(16))
    network = Column(String(32))
    dept = Column(String(32))
    job_number = Column(String(32))
    content = Column(String(256))
    last_visit = Column(String(32))
    status = Column(Integer,default=1)


    def __repr__(self):
        return ("<WhiteList>(name = '%s',os_type = '%s', hostname = '%s', mac = '%s',ip = '%s', \
                createtime = '%s',expiretime = '%s', createtime_timestamp = '%s', expiretime_timestamp = '%s',interface= '%s', \
                network = '%s',dept = '%s',job_number = '%s',content = '%s',last_visit = '%s')")   \
            %(     self.name,
                   self.os_type,
                   self.hostname,
                   self.mac,
                   self.ip,
                   self.createtime,
                   self.expiretime,
                   self.createtime_timestamp,
                   self.expiretime_timestamp,
                   self.interface,
                   self.network,
                   self.docker_version,
                   self.dept,
                   self.job_number,
                   self.content,
                   self.last_visit,
                   self.status,
            )






if __name__ == "__main__":
    Base.metadata.create_all(engine)
