#!/usr/bin/env python  
# -*- coding:utf-8 -*-  


"""
一个基于thread和queue的线程池，以任务为队列元素，动态创建线程，重复利用线程，
通过close和terminate方法关闭线程池。
"""
import queue
import threading
import contextlib
import time
 
# 创建空对象,用于停止线程
StopEvent = object()
 
 
def callback(status, result):
    """
    根据需要进行的回调函数，默认不执行。
    :param status: action函数的执行状态
    :param result: action函数的返回值
    :return:
    """
    pass
 
 
def action(arg):
    """
    线程池测试函数
    真实的任务定义在这个函数里
    :param thread_name: 执行该方法的线程名
    :param arg: 该函数需要的参数
    :return:
    """
    # 模拟该函数执行了0.1秒
    # print("第%s个任务调用了线程 %s，并打印了这条信息！" % (arg+1, thread_name))

    while True:
    	print (arg,'---')
    	time.sleep(3)
    	print ('sldkjflk',arg)
    arg += 1
 
class ThreadPool:
 
    def __init__(self, max_num, max_task_num=None):
        """
        初始化线程池
        :param max_num: 线程池最大线程数量
        :param max_task_num: 任务队列长度
        """
        # 如果提供了最大任务数的参数，则将队列的最大元素个数设置为这个值。
        if max_task_num:
            self.q = queue.Queue(max_task_num)
        # 默认队列可接受无限多个的任务
        else:
            self.q = queue.Queue()
        # 设置线程池最多可实例化的线程数
        self.max_num = max_num
        # 任务取消标识
        self.cancel = False
        # 任务中断标识
        self.terminal = False
        # 已实例化的线程列表
        self.generate_list = []
        # 处于空闲状态的线程列表
        self.free_list = []
 
    def put(self, func, args, callback=None):
        """
        往任务队列里放入一个任务
        :param func: 任务函数
        :param args: 任务函数所需参数
        :param callback: 任务执行失败或成功后执行的回调函数，回调函数有两个参数
        1、任务函数执行状态；2、任务函数返回值（默认为None，即：不执行回调函数）
        :return: 如果线程池已经终止，则返回True否则None
        """
        # 先判断标识，看看任务是否取消了
        if self.cancel:
            return
        # 如果没有空闲的线程，并且已创建的线程的数量小于预定义的最大线程数，则创建新线程。
        '''
        	如果没有空闲线程才会去执行创建新线程,然后执行 put,第一次执行创建线程有一个q.get(),
        	队列里面没有值q.get()就会停住,等待q.put()讲值给put进去

        	个人认为,没有必要在设置free_list,因为只要正在执行任务数不大于最大任务数,就无法在创建新线程了,
        	那么就回一直使用已创建的线程
        '''
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num:
            self.generate_thread()
        # 构造任务参数元组，分别是调用的函数，该函数的参数，回调函数。
        w = (func, args, callback,)
        # 将任务放入队列
        self.q.put(w)
 
    def generate_thread(self):
        """
        创建一个线程
        """
        # 每个线程都执行call方法
        t = threading.Thread(target=self.call)
        t.start()
 
    def call(self):
        """
        循环去获取任务函数并执行任务函数。在正常情况下，每个线程都保存生存状态，
        直到获取线程终止的flag。
        """
        # 获取当前线程的名字
        current_thread = threading.currentThread().getName()
        print ('\033[0;33;40mGenerate Total:\033[0m',len(self.generate_list))
        # 将当前线程的名字加入已实例化的线程列表中
        self.generate_list.append(current_thread)
        # 从任务队列中获取一个任务
        event = self.q.get()
        # 让获取的任务不是终止线程的标识对象时
        while event != StopEvent:
            # 解析任务中封装的三个参数
            func, arguments, callback = event
            # print (arguments)
            # 抓取异常，防止线程因为异常退出
            try:
                # 正常执行任务函数
                '''
                有了*arguments,调用赋值的时候必须使用元祖或者列表
                '''
                result = func(arguments)

                success = True
            except Exception as e:
                # 当任务执行过程中弹出异常
                result = None
                success = False
            # 如果有指定的回调函数
            if callback is not None:
                # 执行回调函数，并抓取异常
                try:
                    callback(success, result)
                except Exception as e:
                    pass
            # 当某个线程正常执行完一个任务时，先执行worker_state方法
            with self.worker_state(self.free_list, current_thread):
                # 如果强制关闭线程的flag开启，则传入一个StopEvent元素
                if self.terminal:
                    event = StopEvent
                # 否则获取一个正常的任务，并回调worker_state方法的yield语句
                else:
                    # 从这里开始又是一个正常的任务循环
                    event = self.q.get()
        else:
            # 一旦发现任务是个终止线程的标识元素，将线程从已创建线程列表中删除
            self.generate_list.remove(current_thread)
 
    def close(self):
        """
        执行完所有的任务后，让所有线程都停止的方法
        """
        # 设置flag
        self.cancel = True
        # 计算已创建线程列表中线程的个数，然后往任务队列里推送相同数量的终止线程的标识元素
        full_size = len(self.generate_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1
 
    def terminate(self):
        """
        在任务执行过程中，终止线程，提前退出。
        """
        self.terminal = True
        # 强制性的停止线程
        while self.generate_list:
            self.q.put(StopEvent)
 
    # 该装饰器用于上下文管理
    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        """
        用于记录空闲的线程，或从空闲列表中取出线程处理任务
        """
        # 将当前线程，添加到空闲线程列表中
        '''
        with上下文的时候,到这里这个线程,因为此时线程正在执行中,因为上述代码有一个如果free_list
        为0才会创建线程,如果此时有一个值在里面,那么就不需要创建新线程
        '''
        state_list.append(worker_thread)
        # 捕获异常
        try:
            # 在此等待
            yield
        finally:
            # 将线程从空闲列表中移除
            '''
            因为到这里之后,这个线程就已经执行完成了
            '''
            # ('\033[5;33;40mClient IP: ',client_ip + '\033[0m')
            print ('\033[0;33;40mtask Total:\033[0m',self.q.qsize() ,'\033[0;33;40mfree Total:\033[0m',len(state_list))
            state_list.remove(worker_thread)
 
# # 调用方式
# if __name__ == '__main__':
#     # 创建一个最多包含5个线程的线程池
#     pool = ThreadPool(20)
#     # 创建100个任务，让线程池进行处理
#     for i in range(20):
#         pool.put(action, i, callback)
#     # 等待一定时间，让线程执行任务

#     # 正常关闭线程池
#     pool.close()

#     # 强制关闭线程池
#     # pool.terminate()
#     # print("强制停止任务！")

#     time.sleep(5)
#     print("任务执行完毕，正常退出！")
#     # print("-" * 50)
#     # print("\033[32;0m任务停止之前线程池中有%s个线程，空闲的线程有%s个！\033[0m"
#     #       % (len(pool.generate_list), len(pool.free_list)))