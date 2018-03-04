#!/usr/bin/env python

import sys
import tornado.web

sys.path.append("..")

from settings import COOKIE_NAME

class BaseHandler(tornado.web.RequestHandler):

	pass

