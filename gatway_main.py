#!/usr/bin/env python  
 

# import io,sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

import binascii
import signal,threading
from scapy.all import *
from juntechGW_setting import *
from thread_pool import *


hostname_vendor = {}
host_info = {}

#判断ip属于哪个vlan接口
def getbr(avail_ip):
	'''
		locals() : 基于字典的访问局部变量的方式。键是变量名，值是变量值。
		globals() : 基于字典的访问全局变量的方式。键是变量名，值是变量值。
	'''
	if 'br' in globals() and 'br_ip' in globals():
		if br_ip in avail_ip:
			return br
	elif 'br2' in globals() and 'br2_ip' in globals():
		if br2_ip in avail_ip:
			return br2
	elif 'br3' in globals() and 'br3_ip' in globals():
		if br3_ip in avail_ip:
			return br3
	elif 'br4' in globals() and 'br4_ip' in globals():
		if br4_ip in avail_ip:
			return br4
	elif 'br5' in globals() and 'br5_ip' in globals():
		if br5_ip in avail_ip:
			return br5
	else:
		print ('Without this vlan,ip:'+avail_ip)
		return False

#提取bytes类型的mac地址
def MacExtract(binmac):
	#二进制串转16进制使用hexlify
	#比如python3中类型一定要是bytes的,如s=b'\x00\x0c)P\xfc\xcc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
   mac=binascii.hexlify(binmac)[0:12].decode()
   #截取mac的2位数,循环这个长度来生成一个列表,最后字符串拼接列表
   blocks = [mac[x:x+2] for x in range(0, len(mac), 2)]
   return ':'.join(blocks)

# def dhcp_test(pkg):
# 	# print (pkg.getlayer(BOOTP).fields)
# 	# print (pkg[DHCP].fields)
# 	client_mac = MacExtract(pkg[BOOTP].chaddr)
#   pkt.summary()    #简要信息,查看有哪些层

def signal_handler(signum,frame):  #退出主程序讯号
	import sys,os
	print ('退出主程序')
	# sys.exit()是退出你整个执行进程的。但如果不是这个进程的事，就不归它管了,且sys.exit()一般退出会有异常需要捕获处理
	try:
		os._exit(0)
	except Exception as e:
		pass

class SnifferDHCP(threading.Thread):
	def __init__(self):
		super(SnifferDHCP,self).__init__()
		self.filter = "port bootps or port bootpc"
		self.kill_received = False
		self.dhcp_count = 0

	#定义run方法,把父类的run方法给覆盖掉,自己定义
	def run(self):
		while True:
			sniff(filter=self.filter,prn=self.detect_dhcp)

	def detect_dhcp(self,pkt):
		# print (pkt[DHCP].fields)
		# print ('======',pkt.show2())

		if DHCP in pkt:
			# print (pkt[DHCP].fields['options'][0][1])
			#如果dhcp消息类型为ack或者nak,那么代表获取ip成功
			if pkt[DHCP].fields['options'][0][1] == 5 or pkt[DHCP].fields['options'][0][1] == 6:

				op = pkt[BOOTP].op  				#op位
				client_ip = pkt[BOOTP].ciaddr		#客户端IP地址
				user_ip = pkt[BOOTP].yiaddr			#如果客户端知道IP地址,就手动,一般在交互式dhcp请求需要该参数或者dhcp客户端租约没有到期不需要申请新的ip资源时
				server_ip = pkt[BOOTP].siaddr		#服务器IP
				gia_ip =  pkt[BOOTP].giaddr			#通过代理启动时代理的 IP 地址
				client_mac = MacExtract(pkt[BOOTP].chaddr)
				print ('DHCP SERVER ACK/NAK from:'+ pkt[Ether].src + ',IP:' + pkt[IP].src)
				# print ('OP:',op)
				# print ('\033[5;33;40mClient IP: ',client_ip + '\033[0m')
				# # "\033[1;31;46m usage \033[0m"
				# print ('Client_Mac:',client_mac)
				# print ('User IP:',user_ip)
				# print ('Server IP',server_ip)
				# print ('Gia IP',gia_ip)

				#DHCP Client启动时，由于没有IP地址，会自动发送以discover的广播报文，源地址为0.0.0.0目的地址为255.255.255.255(广播)
				if client_mac == '0:0:0:0:0:0' or client_mac == '00:00:00:00:00:00':
					return

				#首先定义有效IP为0.0.0.0
				avail_ip = '0.0.0.0'
				#因为为了判断user_IP有交互式输出,所以这里多一个判断
				if user_ip == '0.0.0.0':
					avail_ip = client_ip
				else:
					avail_ip = user_ip

				#判断这个ip属于哪个vlan
				br = getbr(avail_ip)
				# print ('--',br)


				host_info['client_ip'] = client_ip
				host_info['avail_ip'] =  avail_ip
				host_info['client_mac'] =  client_mac
				host_info['server_ip'] =  server_ip
				host_info['gia_ip'] =  gia_ip
				
				try:
					if hostname_vendor[client_mac]['hostname'] is not None:
						host_info['hostname'] = hostname_vendor[client_mac]['hostname']
						del hostname_vendor[client_mac]['hostname']
				except Exception:
					pass
				try:	
					if hostname_vendor[client_mac]['vendor'] is not None:
						host_info['vendor'] = hostname_vendor[client_mac]['vendor']
						del hostname_vendor[client_mac]
				except Exception:
					pass

			elif pkt[DHCP].fields['options'][0][1] == 3:
				# print (pkt[DHCP].fields)
				# global hostname_vendor
				try:
					client_mac = MacExtract(pkt[BOOTP].chaddr)
					'''
					这里注意变量的声明,如果是下面这样，那么就是重新生成一个变量了
					# hostname_vendor = {client_mac:{}}
					'''
					hostname_vendor[client_mac] = {}
				except Exception:
					print ("Mac not obtained.")

				for i in pkt[DHCP].fields['options']:
					# print (i,'===',len(pkt[DHCP].fields['options']))
					if isinstance(i,tuple):
						if i[0] == 'hostname':
							hostname = [i][0][1].decode()
							try:
								hostname_vendor[client_mac]['hostname'] = hostname
							except Exception:
								print ("Vendor not obtained.")
						elif i[0] == 'vendor_class_id':
							vendor = [i][0][1].decode()
							try:
								hostname_vendor[client_mac]['vendor'] = vendor
							except Exception:
								print ('Host name not obtained.')
					else:
						pass

def start_gatway():
	signal.signal(signal.SIGINT,signal_handler)
	sniffThread = SnifferDHCP()
	sniffThread.start()

# if __name__ == "__main__":
# 	start_gatway()

