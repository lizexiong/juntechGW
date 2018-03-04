#!/usr/bin/env python  
# -*- coding:utf-8 -*-  


from thread_pool import *
from scapy.all import *



def run(arg=None):
	flag = True
	# while flag == True:
	# 	print (flag)

	print (arg)
	while True:
		sniff(filter="port bootps or port bootpc",stop_callback=stopfilter )

	print ('end')

def detect_dhcp1(pkt=None):

	print ('dhcp')


def stopfilter():
	return True


# def stopfilter(x):
#      if x[IP].dst == '23.212.52.66':
#          return True
#      else
#          return False

# sniff(iface="wlan0", filter='tcp', stop_filter=stopfilter)



run()
# pool = ThreadPool(5)
# pool.put(run,1)