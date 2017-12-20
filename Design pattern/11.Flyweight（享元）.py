#!/usr/bin/python
# coding:utf8
'''
Flyweight

意图：
运用共享技术有效地支持大量细粒度的对象。

适用性：
一个应用程序使用了大量的对象。
完全由于使用大量的对象，造成很大的存储开销。
对象的大多数状态都可变为外部状态。
如果删除对象的外部状态，那么可以用相对较少的共享对象取代很多组对象。
应用程序不依赖于对象标识。由于Flyweight 对象可以被共享，对于概念上明显有别的对象，标识测试将返回真值。
'''

import weakref


class Card(object):
    """The object pool. Has builtin reference counting"""
    _CardPool = weakref.WeakValueDictionary()

    """Flyweight implementation. If the object exists in the
    pool just return it (instead of creating a new one)"""

    def __new__(cls, value, suit):
        obj = Card._CardPool.get(value + suit, None)
        if not obj:
            obj = object.__new__(cls)
            Card._CardPool[value + suit] = obj
            obj.value, obj.suit = value, suit
        return obj

    # def __init__(self, value, suit):
    #     self.value, self.suit = value, suit

    def __repr__(self):
        return "<Card: %s%s>" % (self.value, self.suit)


if __name__ == '__main__':
    # comment __new__ and uncomment __init__ to see the difference
    c1 = Card('9', 'h')
    c2 = Card('9', 'h')
    print(c1, c2)
    # c2 = None
    print(c1, c2)
    print(c1 == c2)
    print(id(c1), id(c2))