#!/usr/bin/env python  



import os,sys
sys.path.append('..')
#获取绝对路径 os.getcwd()或者os.path.abspath('.') .代表当前目录

import qrcode

#导入配置文件
from settings import server_ip




current_path = os.getcwd()
img_path = current_path + "/img"


def two_code(mac):
	'''
	生成二维码,并返回二维码路径
	'''
	url = "http://" + server_ip + "/sweepcodeceriticationafter?mac=%s&flag=" % (mac)
	if os.path.isdir(img_path):
		pass
	else:
		os.mkdir(img_path)
	img_file = r'%s/%s.jpg' %(img_path,mac)
	qr = qrcode.QRCode(
	    version=1,
	    error_correction=qrcode.constants.ERROR_CORRECT_L,
	    box_size=10,
	    border=4
	)

	qr.add_data(url)
	qr.make(fit=True)
	img = qr.make_image()
	img.save(img_file)
	return img_file
	# img.show()
print (two_code('11:22:33'))

'''
QRCode参数详细说明：
	version: 一个整数，范围为1到40，表示二维码的大小（最小值是1，是个12×12的矩阵），如果想让程序自动生成，将值设置为 None 并使用 fit=True 参数即可。
	error_correction: 二维码的纠错范围，可以选择4个常量： 
	ERROR_CORRECT_L 7%以下的错误会被纠正 
	ERROR_CORRECT_M (default) 15%以下的错误会被纠正 
	ERROR_CORRECT_Q 25 %以下的错误会被纠正 
	ERROR_CORRECT_H. 30%以下的错误会被纠正
	boxsize: 每个点（方块）中的像素个数
	border: 二维码距图像外围边框距离，默认为4，而且相关规定最小为4
'''