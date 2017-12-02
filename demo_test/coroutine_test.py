#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
def consumer():
    r = ''
    while True:
        n = yield r
        print '内部打印：n = ', n
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        time.sleep(3)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] send %s...' % n)
        r = c.send(n)
        print('[PRODUCER] get: %s' % r)
    c.close()

c = consumer()
produce(c)
# print '===>', c.next()
# print '==', c.send(3)
# print '===>', c.next()
# print '===>', c.next()
