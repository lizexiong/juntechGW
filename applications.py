#!/usr/bin/env python


import os
import tornado.web
from url import urls

PORT = 8888
SETTINGS = dict(
	# 配置静态文件和html的目录；默认是在根目录下（也就是主.py文件的同级目录）
    template_path = os.path.join(os.path.dirname(__file__),  "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    login_url = "/",
    cookie_secret="235lksjfASKJFlks=jdfGLKS=JDFLKSsfjlk234dsjflksdjffj/=sf"
	)

#路由系统
application = tornado.web.Application(
	handlers=urls,
	#把配置文件传入进去
	**SETTINGS
	)