#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#    9/2/16

" a module "

__author__ = 'redhead'


# metaclass是创建类，所以必须从`type`类型派生：
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)


class MyList (list):
    __metaclass__ = ListMetaclass  # 指示使用ListMetaclass来定制类

h = MyList()
h.add(2)
print(h)