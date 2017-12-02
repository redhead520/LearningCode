#!/usr/bin/env python
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'redhead'

# 1 使用__new__方法
class Singleton0(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton0, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

#2 共享属性
# 创建实例时把所有实例的__dict__指向同一个字典,这样它们具有相同的属性和方法.
class Singleton1(object):
    _dict = {}
    def __new__(cls, *args, **kwargs):
        new_instance = super(Singleton1, cls).__new__(cls, *args, **kwargs)
        new_instance.__dict__ = cls._dict
        return new_instance

# 3 装饰器版本
def singleton(cls):
    instances = {}
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

# 4 import方法
# 作为python的模块是天然的单例模式
# mysingleton.py
class My_Singleton(object):
    def foo(self):
        pass

my_singleton = My_Singleton()

# to use
#from mysingleton import my_singleton
my_singleton.foo()

if __name__ == '__main__':

    # 1 使用__new__方法
    print('1 使用__new__方法:')
    class Myclass0(Singleton0):
        a = 1
    a = Myclass0()
    b = Myclass0()
    print id(a) == id(b)

    #2 共享属性
    print('2 共享属性:')
    class Myclass1(Singleton1):
        a = 1
    c = Myclass1()
    d = Myclass1()
    print id(c) == id(d)
    print id(c.__dict__) == id(d.__dict__)

    # 3 装饰器版本
    print('3 装饰器版本:')
    @singleton
    class Myclass2(object):
        x = 0

    e = Myclass2()
    e.y = 444
    f = Myclass2()
    print f.y
    print id(e) == id(f)