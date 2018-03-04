# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

from mysql_pool import MysqlServer

from settings import DATABASES

import datetime







def sql(createtime,expretime):
	sql = "insert into white_list (createtime,expiretime) values('%s','%s')" %(createtime,expretime)
	print (sql)
	obj.run_sql(sql)


def select_sql():
	obj = MysqlServer(DATABASES)
	sql = "select * from white_list"
	result = obj.run_sql(sql)
	time1 = datetime.datetime.strptime(result[1][6].split('.')[0],'%Y-%m-%d %H:%M:%S')
	time2 = datetime.datetime.now() - time1
	print (time2)

now = datetime.datetime.now()
# 现在时间 + 8小时
expretime = now + datetime.timedelta(hours=+8)

last_time = expretime - now

print (last_time.seconds / 1800)
# sql(now,expretime)


# select_sql()




