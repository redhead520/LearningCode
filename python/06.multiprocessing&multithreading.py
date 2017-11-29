#!/usr/bin/env python
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'redhead'

import os
from multiprocessing import Process, Pool
import time
import random

# fork Unix/Linux操作系统提供了一个fork()系统调用, window不行
def test_fork():
    print '主进程开始({})'.format(os.getpid())
    pid = os.fork() # 主进程执行这一句，子进程不执行
    if pid == 0:
        print '子进程启动{},pid={}'.format(os.getpid(), pid)
    else:
        print '主进程进行中{},pid={}'.format(os.getpid(), pid)

# Process 一个子进程
def test_process():
    def run_proc(name):
        print('子进程：{}, pid:{}'.format(name, os.getpid()))
    print '主进程开始({})'.format(os.getpid())
    p = Process(target=run_proc, args=('test',)) # 一个子进程
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')

# Pool 进程池 多个子进程
def long_time_task(name):
    print('Run 子任务 %s (%s)...' % (name, os.getpid()))
def test_pool():
    # long_time_task在此处定义是不行的。
    print('主进程开始 %s.' % os.getpid())
    p = Pool()
    for i in range(10):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('所有子进程结束.')

# subprocess  在系统终端执行任务subprocess.call
import subprocess
def test_subprocess():
    print('$ nslookup www.baidu.com')
    print('-'*30)
    r = subprocess.call(['nslookup', 'www.baidu.com'])
    # subprocess.call(['date'])
    print('-' * 30)
    p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b'www.baidu.com\nexit\n')
    print(output.decode('utf-8'))
    print('-' * 30)

# 进程间通信是通过Queue、Pipes等实现的。

# 多线程:
# Python的标准库提供了两个模块：_thread和threading，_thread是低级模块，threading是高级模块，对_thread进行了封装。绝大多数情况下，我们只需要使用threading这个高级模块。
import threading
def test_thread():
    # 新线程执行的代码:
    def loop():
        print('thread %s is running...' % threading.current_thread().name)
        n = 0
        while n < 5:
            n = n + 1
            print('thread %s >>> %s' % (threading.current_thread().name, n))
            time.sleep(1)
        print('thread %s ended.' % threading.current_thread().name)

    print('thread %s is running...' % threading.current_thread().name)
    t = threading.Thread(target=loop, name='LoopThread') # 子线程名字：LoopThread，不传name的话，默认是Thread-1，Thread-2……
    t.start()
    t.join()
    print('thread %s ended.' % threading.current_thread().name)

# 线程池 ThreadPool
from multiprocessing.dummy import Pool as ThreadPool
def run_task(n):
    print '子线程--{}'.format(n)
def test_threadpool():
    pool = ThreadPool(100)  # create the poll: 25
    print '开始运行子线程：'
    pool.map(run_task, range(5))
    pool.close()
    pool.join()
    print '子线程运行完毕！'


# 线程Lock
balance = 0
def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def test_lock():
    lock = threading.Lock()
    def run_thread(n):
        for i in range(100000):
            # 先要获取锁:
            lock.acquire()
            try:
                # 放心地改吧:
                change_it(n)
            finally:
                # 改完了一定要释放锁:
                lock.release()
                pass

    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)

# GIL全局锁 Global Interpreter Lock
# Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。

# 多线程, 类， 实例：每个实例一个线程
import Queue
class ThreadQueue(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()

    def run(self):
        while True:
            message = self.queue.get()
            print message

# ThreadLocal变量: 虽然是全局变量，但每个线程都只能读写自己线程的独立副本，互不干扰。ThreadLocal解决了参数在一个线程中各个函数之间互相传递的问题
# 创建全局ThreadLocal对象:
def test_threadlocal():
    local_school = threading.local()

    def process_student():
        # 获取当前线程关联的student:
        std = local_school.student
        print('Hello, %s (in %s)' % (std, threading.current_thread().name))

    def process_thread(name):
        # 绑定ThreadLocal的student:
        local_school.student = name
        process_student()

    t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')
    t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    # test_process()
    # test_pool()
    # test_subprocess()
    # test_thread()
    # test_threadpool()
    # test_lock()
    test_threadlocal()