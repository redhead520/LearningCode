#!/usr/bin/python
# coding:utf8
'''
Visitor

意图：
 定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。
 TemplateMethod 使得子类可以不改变一个算法的结构即可重定义该算法的某些特定步骤。

适用性：
 一次性实现一个算法的不变的部分，并将可变的行为留给子类来实现。
 各子类中公共的行为应被提取出来并集中到一个公共父类中以避免代码重复。
 这是Opdyke和Johnson所描述过的“重分解以一般化”的一个很好的例子[OJ93]。
 首先识别现有代码中的不同之处，并且将不同之处分离为新的操作。
 最后，用一个调用这些新的操作的模板方法来替换这些不同的代码。
 控制子类扩展。模板方法只在特定点调用“hook ”操作（参见效果一节），这样就只允许在这些点进行扩展。
'''


class Node(object):
    pass


class A(Node):
    pass


class B(Node):
    pass


class C(A, B):
    pass


class Visitor(object):
    def visit(self, node, *args, **kwargs):
        meth = None
        for cls in node.__class__.__mro__:
            meth_name = 'visit_' + cls.__name__
            meth = getattr(self, meth_name, None)
            if meth:
                break

        if not meth:
            meth = self.generic_visit
        return meth(node, *args, **kwargs)

    def generic_visit(self, node, *args, **kwargs):
        print('generic_visit ' + node.__class__.__name__)

    def visit_B(self, node, *args, **kwargs):
        print('visit_B ' + node.__class__.__name__)


a = A()
b = B()
c = C()
visitor = Visitor()
visitor.visit(a)
visitor.visit(b)
visitor.visit(c)
