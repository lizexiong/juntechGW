#!/usr/bin/env python


import subprocess

def get_mac(client_ip):
	'''
	从本地arp中获取客户端的mac地址
	'''
	command = "arp -n | grep '\\b%s\\b' | awk {'print $3'} " %(client_ip)
	result = subprocess.check_output(command,shell=True)
	if result.decode().strip() == "":
		return 'not find'
	else:
		return result.decode().strip()

