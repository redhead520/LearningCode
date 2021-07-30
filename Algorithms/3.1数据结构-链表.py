#!/usr/bin/env python
# -*- coding: utf-8 -*-

' 3.1 数据结构：链表'

# 双向链表：key, next, prev
# 单向链表：key, next
# 已排序的sorted，未排序的unsorted
# 循环链表 circular list

# 链表默认为 未排序的双链接
class ITEM():
    def __init__(self, key=None, next=None, prev=None):
        self.key = key
        self.next = next
        self.prev = prev
    def __str__(self):
        return str(self.__dict__)

class LIST_Linked():
    def __init__(self):
        self.head = None

    def search(self, k):
        x = self.head
        while x != None and x.key != k:
            x = x.next
        return x
    def insert(self, k):
        new = ITEM(key=k,next=self.head)
        if self.head != None:
            self.head.prev = new
        self.head = new
    def delete(self, k):
        item = self.search(k)
        if item.prev != None:
            item.prev.next = item.next
        else:
            self.head = item.next
        if item.next != None:
            item.next.prev =- item.prev

# l = LIST_Linked()
# l.insert(3)
# l.insert(6)
# print l.head
# print l.search(3)

# 带哨兵(sentinel)的链表
class LIST_Linked():
    def __init__(self):
        self.nil = ITEM()  # 哨兵
        self.nil.next = self.nil
        self.nil.prev = self.nil
    def search(self, k):
        item = self.nil.next
        while item != self.nil and item.key != k:
            item = item.next
        return item
    def insert(self, k):
        new = ITEM(key=k,next=self.nil.next,prev=self.nil)
        self.nil.next.prev = new
        self.nil.next = new

    def delete(self, k):
        item = self.search(k)
        item.prev.next = item.next
        item.next.prev =- item.prev
    def __str__(self):
        return str(self.__dict__)

# l = LIST_Linked()
# l.insert(5)
# l.insert(7)
# print l.search(5)
# print l.nil.next