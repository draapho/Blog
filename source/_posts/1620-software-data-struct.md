---
title: 数据结构资料收集
date: 2016-11-23
categories: software
tags: [data struct]
---


# python各数据结构性能列表, [TimeComplexity](https://wiki.python.org/moin/TimeComplexity)
- list

Operation      | Average Case | Amortized Worst Case
-------------- | ------------ | --------------------
Copy           | O(n)         | O(n)                
Append[1]      | O(1)         | O(1)                
Insert         | O(n)         | O(n)                
Get Item       | O(1)         | O(1)                
Set Item       | O(1)         | O(1)                
Delete Item    | O(n)         | O(n)                
Iteration      | O(n)         | O(n)                
Get Slice      | O(k)         | O(k)                
Del Slice      | O(n)         | O(n)                
Set Slice      | O(k+n)       | O(k+n)              
Extend[1]      | O(k)         | O(k)                
Sort           | O(n log n)   | O(n log n)          
Multiply       | O(nk)        | O(nk)               
x in s         | O(n)         | -                   
min(s), max(s) | O(n)         | -                   
Get Length     | O(1)         | O(1)                

- collections.deque

Operation  | Average Case | Amortized Worst Case
---------- | ------------ | --------------------
Copy       | O(n)         | O(n)                
append     | O(1)         | O(1)                
appendleft | O(1)         | O(1)                
pop        | O(1)         | O(1)                
popleft    | O(1)         | O(1)                
extend     | O(k)         | O(k)                
extendleft | O(k)         | O(k)                
rotate     | O(k)         | O(k)                
remove     | O(n)         | O(n)                

- dict

Operation    | Average Case | Amortized Worst Case
------------ | ------------ | --------------------
Copy[2]      | O(n)         | O(n)                
Get Item     | O(1)         | O(n)                
Set Item[1]  | O(1)         | O(n)                
Delete Item  | O(1)         | O(n)                
Iteration[2] | O(n)         | O(n)                


# [教科书风格的数据结构](http://sjjp.tjuci.edu.cn/sjjg/datastructure/ds/web/gailun/gailun1.1.1b.htm)
- 讲述了 `线性链表`, `字符串`, `栈和队列`, `多维数组`, `广义表`, `树`, `图`, `排序`, `查找`, `文件`
- **有较为详细的性能分析**, 偏重理论细节, 还有习题可以做!
  - 平方阶(O(n^2))排序: 一般称为简单排序，例如直接插入、直接选择和冒泡排序
  - 线性对数阶(O(nlgn))排序: 如快速、堆和归并排序
  - O(n^(1+￡))阶排序(0<￡<1): 如希尔排序
  - 线性阶(O(n))排序: 如桶、箱和基数排序
- 排序方法的选择
  - 简单排序中直接插入最好，快速排序最快，当文件为正序时，直接插入和冒泡均最佳。
  - 若n较小(如n≤50)，可采用直接插入或直接选择排序。
  - 若文件初始状态基本有序(指正序)，则应选用直接插人、冒泡或随机的快速排序为宜；
  - 若n较大，则应采用时间复杂度为O(nlgn)的排序方法：快速排序、堆排序或归并排序。
    - 快速排序是目前基于比较的内部排序中被认为是最好的方法，当待排序的关键字是随机分布时，快速排序的平均时间最短；
    - 堆排序所需的辅助空间少于快速排序，并且不会出现快速排序可能出现的最坏情况。这两种排序都是不稳定的。
    - 若要求排序稳定，则可选用归并排序。


# [纸上谈兵: 算法与数据结构](http://www.cnblogs.com/vamei/archive/2013/03/22/2974052.html)
- 理论与实践相结合的讲述数据结构, **配图很有意思, 并提供了C代码**. 但没有对性能和特性做详细介绍.
- [纸上谈兵: 数学归纳法, 递归, 栈](http://www.cnblogs.com/vamei/archive/2013/03/30/2989930.html)
- [纸上谈兵: 排序算法简介及其C实现](http://www.cnblogs.com/vamei/archive/2013/03/12/2948847.html)
- [纸上谈兵: 表 (list)](http://www.cnblogs.com/vamei/archive/2013/03/14/2958940.html)
- [纸上谈兵: 栈 (stack)](http://www.cnblogs.com/vamei/archive/2013/03/14/2960201.html)
- [纸上谈兵: 队列 (queue)](http://www.cnblogs.com/vamei/archive/2013/03/15/2961729.html)
- [纸上谈兵: 树, 二叉树, 二叉搜索树](http://www.cnblogs.com/vamei/archive/2013/03/17/2962290.html)
  - [纸上谈兵: AVL树](http://www.cnblogs.com/vamei/archive/2013/03/21/2964092.html)
  - [纸上谈兵: 伸展树 (splay tree)](http://www.cnblogs.com/vamei/archive/2013/03/24/2976545.html)
- [纸上谈兵: 堆 (heap)](http://www.cnblogs.com/vamei/archive/2013/03/20/2966612.html)
  - [纸上谈兵: 左倾堆 (leftist heap)](http://www.cnblogs.com/vamei/archive/2013/04/19/2978555.html)
- [纸上谈兵: 哈希表 (hash table)](http://www.cnblogs.com/vamei/archive/2013/03/24/2970339.html)
- [纸上谈兵: 图 (graph)](http://www.cnblogs.com/vamei/p/3113912.html)
  - [纸上谈兵: 拓扑排序](http://www.cnblogs.com/vamei/p/3232432.html)
  - [纸上谈兵: 最短路径与贪婪](http://www.cnblogs.com/vamei/p/3604629.html)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***