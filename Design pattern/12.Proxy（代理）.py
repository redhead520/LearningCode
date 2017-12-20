#!/usr/bin/python
# coding:utf8
'''
Proxy

为其他对象提供一种代理以控制对这个对象的访问。

适用性：
 在需要用比较通用和复杂的对象指针代替简单的指针的时候，使用Proxy模式。下面是一 些可以使用Proxy 模式常见情况：
1) 远程代理（Remote Proxy ）为一个对象在不同的地址空间提供局部代表。 NEXTSTEP[Add94] 使用NXProxy 类实现了这一目的。
Coplien[Cop92] 称这种代理为“大使” （Ambassador ）。
2 )虚代理（Virtual Proxy ）根据需要创建开销很大的对象。在动机一节描述的ImageProxy 就是这样一种代理的例子。
3) 保护代理（Protection Proxy ）控制对原始对象的访问。保护代理用于对象应该有不同 的访问权限的时候。
例如，在Choices 操作系统[ CIRM93]中KemelProxies为操作系统对象提供 了访问保护。
4 )智能指引（Smart Reference ）取代了简单的指针，它在访问对象时执行一些附加操作。
它的典型用途包括：对指向实际对象的引用计数，这样当该对象没有引用时，可以自动释放它(也称为SmartPointers[Ede92 ] )。

 当第一次引用一个持久对象时，将它装入内存。
 在访问一个实际对象前，检查是否已经锁定了它，以确保其他对象不能改变它。
'''

import time


class SalesManager:
    def work(self):
        print("Sales Manager working...")

    def talk(self):
        print("Sales Manager ready to talk")


class Proxy:
    def __init__(self):
        self.busy = 'No'
        self.sales = None

    def work(self):
        print("Proxy checking for Sales Manager availability")
        if self.busy == 'No':
            self.sales = SalesManager()
            time.sleep(2)
            self.sales.talk()
        else:
            time.sleep(2)
            print("Sales Manager is busy")


if __name__ == '__main__':
    p = Proxy()
    p.work()
    p.busy = 'Yes'
    p.work()