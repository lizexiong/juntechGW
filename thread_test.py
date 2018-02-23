#!/usr/bin/env python  
# -*- coding:utf-8 -*-  


import threading


li = []

def test(arg):
	if arg == '2':
		li.append('lizexiong')
	elif arg == '3':
		li.append('liuxiaoxiao')


def test2():
	li.append('luoyy')

for i in range(5):
	t = threading.Thread(target=test,args=(str(i),))
	t.start()

t = threading.Thread(target=test2)
t.start()

print (li)