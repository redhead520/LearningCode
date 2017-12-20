#!/usr/bin/python
# coding:utf8
'''
Template Method

意图：
定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。TemplateMethod 使得子类可以不改变一个算法的结构即可重定义该算法的某些特定步骤。

适用性：
一次性实现一个算法的不变的部分，并将可变的行为留给子类来实现。
各子类中公共的行为应被提取出来并集中到一个公共父类中以避免代码重复。

首先识别现有代码中的不同之处，并且将不同之处分离为新的操作。
最后，用一个调用这些新的操作的模板方法来替换这些不同的代码。
控制子类扩展。模板方法只在特定点调用“hook ”操作（参见效果一节），这样就只允许在这些点进行扩展。
'''

ingredients = "spam eggs apple"
line = '-' * 10


# Skeletons
def iter_elements(getter, action):
    """Template skeleton that iterates items"""
    for element in getter():
        action(element)
        print(line)


def rev_elements(getter, action):
    """Template skeleton that iterates items in reverse order"""
    for element in getter()[::-1]:
        action(element)
        print(line)

        # Getters


def get_list():
    return ingredients.split()


def get_lists():
    return [list(x) for x in ingredients.split()]


# Actions
def print_item(item):
    print(item)


def reverse_item(item):
    print(item[::-1])


# Makes templates
def make_template(skeleton, getter, action):
    """Instantiate a template method with getter and action"""

    def template():
        skeleton(getter, action)

    return template




if __name__ == '__main__':
    # Create our template functions
    templates = [make_template(s, g, a)
                 for g in (get_list, get_lists)
                 for a in (print_item, reverse_item)
                 for s in (iter_elements, rev_elements)]

    # Execute them
    for template in templates:
        template()