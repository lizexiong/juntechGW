#!/usr/bin/env python

template_variables = dict(
    title=u'上海询诺无线网关平台',
    name =u'上海询诺无线网关平台',
    username="",
)


DATABASES = dict(
    DB='juntechGW',
    USERNAME='root',
    PASSWORD='huawei',
    HOST='localhost',
    PORT=3306,
)

COOKIE_NAME  = "user_id"


server_ip = '192.168.100.250'