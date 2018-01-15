#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
二叉搜索树（BST）

二叉搜索树中的关键字key的存储方式总是满足二叉搜索树的性质：
设x是二叉搜索树中的一个结点。
如果y是x左子树中的一个结点，那么会有y.key<=x.key；
如果y是x右子树中的一个节点，那么有y.key>=x.key。
"""

# 搜索
# 递归实现
def Tree_Search(node, k):
	if node == None or node.key == k:
		return node
	if k < node.key:
		return Tree_Search(node.left, k)
	else:
		return Tree_Search(node.right, k)
# 非递归迭代实现 
def Tree_Search(node, k):
	while node != None and node.key != k:
		if k < node.key:
			node = node.left
		else:
			node = node.right
	return node