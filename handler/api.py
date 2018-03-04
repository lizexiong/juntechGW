#!/usr/bin/env python

from .base import BaseHandler

#导入系统命令模块
import sys
sys.path.append("..")
from script.get_mac import get_mac



import script.config
from script.gatway_main import get_name

class SweepCodeCeriticationBefore(BaseHandler):

	def get(self,*args,**kwargs):
		client_ip = self.request.remote_ip
		client_mac = get_mac(client_ip)
		if client_mac == "not find":
			self.wirte('未获取到您的mac地址信息,请联系系统管理员')
		else:
			print (client_mac,)



class SweepCodeCeriticationAfter(BaseHandler):

	def get(self,*args,**kwargs):
		mac = self.get_argument('mac',None)
		flag = self.get_argument('flag',None)
		name = get_name()
		print('----',name)
		if mac and flag:
			self.write('is')