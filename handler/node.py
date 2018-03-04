#!/usr/bin/env python

import tornado.web


from .base import BaseHandler



class Main(BaseHandler):

	def get(self,*args,**kwargs):
		# remote_ip = self.request
		# print (remote_ip) 
		self.render("node/main.html")