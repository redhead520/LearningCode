#!/usr/bin/env python
# -*- coding: utf-8 -*-

' 3.00 数据结构：栈和队列'

# 栈：stack, 后进先出 last-in,first-out LIFO
# 队列：queue 先进先出 first-in,first-out FIFO

# 栈S
# S.push(), S.pop(), S.top, S.isempty()
# 栈下溢underflow, 栈上溢owerflow
import exceptions
class STACK():
    def __init__(self, num=50, type=list):
        if type == dict:
            self.stacks = dict()
        else:
            self.stacks = [None] * num

        self.top = -1
        self.max = num
    def push(self, item):
        if self.top == self.max - 1:
            raise exceptions.OverflowError('stack was overflow!')
        self.top = self.top + 1
        self.stacks[self.top] = item
        return self.stacks

    def pop(self):
        if self.isempty():
            raise exceptions.Exception('stack was underflow!')
        self.top = self.top - 1
        return self.stacks[self.top + 1]

    def isempty(self):
        if self.top < 0:
            return True
        return False

# S = STACK(5)
# print S.push('111')
# print S.push('222')
# print S.push('333')
# print S.push('444')
# print S.push('555')
# # print S.push('666')
# print S.pop()
# 队列：
class QUEUE():
    def __init__(self, num=50, type=dict):
        if type == dict:
            self.Q = dict()
        else:
            self.Q = [None] * num
        self.head = -1
        self.tail = 0
        self.max = num

    def isempty(self):
        if self.tail == self.head + 1:
            return True
        return False
    def isfull(self):
        if self.tail == self.head:
            return True
        return False

    def enter(self, item):
        if self.isfull():
            raise exceptions.OverflowError('Queue was full!')
        if self.isempty():
            self.head = 0
        self.Q[self.tail] = item
        self.tail = self.tail + 1
        if self.tail == self.max:
            self.tail = 0
        return self.Q

    def out(self):
        if self.isempty():
            raise exceptions.Exception('Queue was empty!')
        self.head = self.head + 1
        if self.head == self.max:
            self.head = 0 if self.tail != 0 else -1
        return self.Q[self.head - 1]

# q = QUEUE(5)
# print q.isempty()
# print q.__dict__
# print q.enter('111')
# print q.enter('222')
# print q.enter('333')
# print q.enter('444')
# print q.enter('555')
# print '-'*10
# print q.__dict__
# print q.out()
# print '-'*10
# print q.__dict__
# print q.out()
# print '-'*10
# print q.__dict__
# print q.out()
# print q.enter('666')
