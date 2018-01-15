#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
二叉树遍历

从树的根节点出发，按照某种次序依次访问二叉树中所有的结点，使得每个结点被访问仅且一次。
这里有两个关键词：访问和次序。
"""
import Queue
class Tree(object):
    data = None
    left = None
    right = None

# 1、前序遍历
# 基本思想：先访问根结点，再先序遍历左子树，最后再先序遍历右子树即根—左—右。
def PreOrderTraverse(tree):
    '''
    前序递归遍历
    '''
    if tree != None:
        print(tree.data)
        PreOrderTraverse(tree.left)
        PreOrderTraverse(tree.right)

def NoPreOrderTraverse(tree):
    '''
    前序非递归遍历
    对于任一结点p：
        a. 访问结点p，并将结点p入栈；
        b. 判断结点p的左孩子是否为空，若为空，则取栈顶结点并进行出栈操作，并将栈顶结点的右孩子置为当前的结点p，循环置a；若不为空，则将p的左孩子置为当前结点p；
        c. 直到p为空，并且栈为空，则遍历结束。
    '''
    Stack = list()
    tmp = tree
    if tmp == None:
        print('the tree is None!')
        return None
    # 现将左子树压入栈，当到叶子结点后，出栈，获取右子树，然后在压入右子树的左子树。
    while tmp != None or len(Stack) != 0:
        while tmp != None:
            Stack.append(tmp)
            print('Node:{}'.format(tmp.data))
            tmp = tmp.left
        if len(Stack) != 0:
            tmp = Stack.pop()
            tmp = tmp.right
    return 1

# 2、中序遍历
# 基本思想：先中序遍历左子树，然后再访问根结点，最后再中序遍历右子树即左—根—右。
def InOrderTraverse(tree):
    '''
    中序递归遍历
    '''
    if tree != None:
        InOrderTraverse(tree.left)
        print(tree.data)
        InOrderTraverse(tree.right)





if __name__ == '__main__':
    pass