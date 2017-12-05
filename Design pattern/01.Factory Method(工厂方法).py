#!/usr/bin/env python
# -*- coding: utf-8 -*-

' Factory Method'

__author__ = 'redhead'

# 定义一个用于创建对象的接口，让子类决定实例化哪一个类。Factory Method 使一个类的实例化延迟到其子类。

# 适用性：
#
# 当一个类不知道它所必须创建的对象的类的时候。
# 当一个类希望由它的子类来指定它所创建的对象的时候。
# 当类将创建对象的职责委托给多个帮助子类中的某一个，并且你希望将哪一个帮助子类是代理者这一信息局部化的时候。

# 简单工厂模式

class LeiFeng():
    def buy_rice(self):
        pass

    def sweep(self):
        pass


class Student(LeiFeng):
    def buy_rice(self):
        print '大学生帮你买米'

    def sweep(self):
        print '大学生帮你扫地'


class Volunteer(LeiFeng):
    def buy_rice(self):
        print '社区志愿者帮你买米'

    def sweep(self):
        print '社区志愿者帮你扫地'


class LeiFengFactory():
    def create_lei_feng(self, type):
        map_ = {
            '大学生': Student(),
            '社区志愿者': Volunteer()
        }
        return map_[type]


if __name__ == '__main__':
    leifeng1 = LeiFengFactory().create_lei_feng('大学生')
    leifeng2 = LeiFengFactory().create_lei_feng('大学生')
    leifeng3 = LeiFengFactory().create_lei_feng('大学生')
    leifeng1.buy_rice()
    leifeng1.sweep()



# 工厂方法模式

class LeiFeng():
    def buy_rice(self):
        pass

    def sweep(self):
        pass


class Student(LeiFeng):
    def buy_rice(self):
        print '大学生帮你买米'

    def sweep(self):
        print '大学生帮你扫地'


class Volunteer(LeiFeng):
    def buy_rice(self):
        print '社区志愿者帮你买米'

    def sweep(self):
        print '社区志愿者帮你扫地'


class LeiFengFactory():
    def create_lei_feng(self):
        pass


class StudentFactory(LeiFengFactory):
    def create_lei_feng(self):
        return Student()


class VolunteerFactory(LeiFengFactory):
    def create_lei_feng(self):
        return Volunteer()


if __name__ == '__main__':
    myFactory = StudentFactory()

    leifeng1 = myFactory.create_lei_feng()
    leifeng2 = myFactory.create_lei_feng()
    leifeng3 = myFactory.create_lei_feng()

    leifeng1.buy_rice()
    leifeng1.sweep()

# 工厂方法相对于简单工厂的优点：
#
# 1.
# 在简单工厂中，如果需要新增类，例如加一个中学生类（MiddleStudent），就需要新写一个类，同时要修改工厂类的map_，加入
# '中学生':MiddleStudent()。这样就违背了封闭开放原则中的一个类写好后，尽量不要修改里面的内容，这个原则。而在工厂方法中，需要增加一个中学生类和一个中学生工厂类（MiddleStudentFactory），虽然比较繁琐，但是符合封闭开放原则。在工厂方法中，将判断输入的类型，返回相应的类这个过程从工厂类中移到了客户端中实现，所以当需要新增类是，也是要修改代码的，不过是改客户端的代码而不是工厂类的代码。
#
# 2.
# 对代码的修改会更加方便。例如在客户端中，需要将Student的实现改为Volunteer，如果在简单工厂中，就需要把
#
# leifeng1 = LeiFengFactory().create_lei_feng('大学生')
# 中的大学生改成社区志愿者，这里就需要改三处地方，但是在工厂方法中，只需要吧
#
# myFactory = StudentFactory()
# 改成
#
# myFactory = VolunteerFactory()
# 就可以了