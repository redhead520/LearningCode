#!/usr/bin/env python2
# -*- coding: utf-8 -*-
### 算法设计模式
# - 枚举法
# - 贪心法
# - 分治法
# - 回溯法
# - 动态规划法
# - 分支限界法

## 算法的代价
# - 存储开销（空间开销）
# - 时间开销

#### 算法分析就是针对一个具体算法，设法确定一种函数关系，问题实例的某种规模n为参数，反映出这个算法在处理规模n的问题实例时需要付出的时间（或空间）代价.

## 大O记法、渐进算法
# 对于充分大的n, 总有 0 < f(n) ≦ c • g(n) ==> 函数g是函数f的一个渐进函数（忽略）常量因子
# 标记为： f(n) = O(g(n))

## 算法时间复杂度： T(n) = O(g(n)) （最坏情况运行时间）
# O(g(n)):
# - O(1)       # 常量复杂度
# - O(log n)    # 对数复杂度
# - O(n)        # 线性复杂度
# - O(n*log n)
# - O(n**2)      # 平方复杂度
# - O(n**3)
# - O(2**n)      # 指数复杂度
#
# 空间复杂度： S(n) = O(g(n))
#
# 大O:(上界渐进线)
# f(n) ≦ O(g(n))
# o:(上界非渐进紧确线)
# f(n) < o(g(n)) 当n --> ∞时，  o(g(n))/f(n) --> ∞

# Ω: omega（下界渐进线)
# 0 < Ω(g(n) ≦ f(n) ≦ c • g(n)
# ω：(下界非渐进紧确线)


# Θ:theta（上下界）
# f(n) = Θ(g(n)) (g(n)为f(n)到渐进紧确线)
# 存在c1,c2,n0,使得 n > n0时，0 ≦ c1•g(n) ≦ f(n) ≦ c2•g(n) 成立
#
# Θ(g(n)) = O(g(n)) ∩ Ω(g(n))
# Θ记号渐进地给出一个函数到上界和下界，
# 但只有一个渐进上界时，使用O记号“大Og(n)”
# 但要渐进下界时，使用Ω记号“Ωg(n)”