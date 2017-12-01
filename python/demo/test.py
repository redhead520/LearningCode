#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#    9/2/16

import sys
print sys.version
import time

# x = 40
#
# fib1 = lambda n: n if n <=2 else fib1(n-1) + fib1(n-2)
# t1 = time.time()
# result = fib1(x)
# t2 = time.time()
# print t2-t1, result
#
# def memo(func):
#     cache = {}
#     def wrap(*args):
#         if args not in cache:
#             cache[args] = func(*args)
#         return cache[args]
#     return wrap
#
#
# @memo
# def fib2(i):
#     if i < 2:
#         return 1
#     return fib2(i-1) + fib2(i-2)
#
# t3 = time.time()
# result = fib2(x)
# t4 = time.time()
# print t4-t3, result
#
#
# def fib3(n):
#     a, b = 0, 1
#     for _ in xrange(n):
#         a, b = b, a + b
#     return b
#
# t5 = time.time()
# result = fib3(x)
# t6 = time.time()
# print t6-t5, result

class ListNode:
    nodes = []
    def __init__(self, x):
        self.index = 0
        self.val = x
        self.next = None
        ListNode.nodes.append(self)

    def setNext(self, next):
        self.next = next
        self.next.index = self.index + 1

    @classmethod
    def getHead(cls):
        for item in cls.nodes:
            if item.index == 0:
                return item
    @classmethod
    def show(cls):
        head = cls.getHead()
        txt = str(head.val)
        while head.next != None:
            txt = txt + ' --> ' + str(head.next.val)
            head = head.next
        print txt


class Solution:
    # @param a ListNode
    # @return a ListNode
    @classmethod
    def swapPairs(cls, head):
        if head != None and head.next != None:
            next = head.next
            next.index, head.index = head.index, next.index
            head.next = cls.swapPairs(next.next)
            next.next = head

            return next
        return head

a = ListNode(1)
b = ListNode(2)
c = ListNode(3)
d = ListNode(4)
a.setNext(b)
b.setNext(c)
c.setNext(d)

head = ListNode.getHead()

ListNode.show()

Solution.swapPairs(head)

ListNode.show()
                            #
# l.sort(key=lambda x: x.index)
# print '->'.join(map(lambda i:str(i.val), l))




