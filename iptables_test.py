#!/usr/bin/env python

import subprocess

def command_test(interface,mac):

	result  = query_iptable(interface,mac)
	if result == 0:
		print ('is exist')
	else:
		command = "iptables -I INPUT -o %s -i %s -m mac --mac-source %s -j ACCEPT | grep '11:22:33:55:44:66'" %(interface,interface,mac)
		print (command)
		commands = command.split(' ')
		print (commands)
		subprocess.call(commands)

def query_iptable(interface,mac):
	command = "iptables -nvL INPUT | grep '%s' >> /dev/null" %(mac)
	result = subprocess.call(command,shell=True)
	return result
command_test('br0','11:22:33:55:44:66')
