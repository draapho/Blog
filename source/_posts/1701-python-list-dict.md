---
title: Python 列表和字典的常见操作
date: 2017-01-03
categories: python
tags: [python, list, dict, tuple, set, collections]
---


# list `[]`

list是一种有序的集合，可以随时添加和删除其中的元素。 形式和特性都像C语言的数组

## 赋值修改及取值

``` python
# list 赋值
l = range(1,9,2)   # l = [1,3,5,7]      9是不包含在里面的
l = [1,3]*3        # l = [1,3,1,3,1,3]  *表示重复次数
l = [1, 2, 3, 4, 5]

# 使用切片 (同字符串用法)
l[0]        # 1                 显示第一个元素
l[-1]       # 5                 显示最后一个元素
l[0:2]      # [1, 2]            显示0,1两个元素
l[-2:]      # [4, 5]            显示最后二个元素
l[::-1]     # [5, 4, 3, 2, 1]   步进-1, 就是倒序了

# 使用切片修改元素
l[0] = 3        # [3, 2, 3, 4, 5]       修改l[0]的值
# l[1] = [7,8]  # [3, [7, 8], 3, 4, 5]  修改为list表, 存储其指针. 注意和 l[1:2] = [7,8] 的本质区别!
l[1:2] = [7,8]  # [3, 7, 8, 3, 4, 5]    将l[1]修改为元素[7,8]
l[1:3] = []     # [3, 2, 3, 4, 5]       删除1-2的元素
l[1:1] = [7,8,2]# [3, 7, 8, 2, 3, 4, 5] 在l[1]处插入元素[7,8,2]

# 取长度
len(l)      # 7

# 排序
l.sort()    # l=[2, 3, 3, 4, 5, 7, 8]

# 获取元素出现的个数
l.count(3)  # 2

# for循环取索引和值, 使用enumerate
for i, x in enumerate(l):
    print '{}: {}'.format(i, x)         # i为index, x为list的值
```


## 增减元素

``` python
l = ['John', 'Bob', 'Tracy']

# 增减元素
l.append('Adam')    # 追加元素到末尾,    l=['John', 'Bob', 'Tracy', 'Adam']
l.insert(1, 'Jack') # 在索引1处插入元素, l=['John', 'Jack', 'Bob', 'Tracy', 'Adam']
l[1:1]=["Jack"]     # 在索引1处插入元素, l=['John', 'Jack', 'Jack', 'Bob', 'Tracy', 'Adam']

# 删减元素
l.remove("Jack")    # 删除第一次出现的该元素, l=['John', 'Jack', 'Bob', 'Tracy', 'Adam']
l.pop()             # 返回并删除末尾的元素,   l=['John', 'Jack', 'Bob', 'Tracy']
l.pop(1)            # 返回并删除索引1的元素,  l=['John', 'Bob', 'Tracy']
del l[0]            # 删除索引0的元素,       l=['Bob', 'Tracy']
del l[0:2]          # 删除多个元素,          l=[]

# 列表扩展/叠加
l1=[3,2,1]; l2=[3,4,5]
l=list(set(l1+l2))  # l=[1,2,3,4,5], 避免了重复元素, 但会丢失原有的排序!
l=l1+l2             # l=[3,2,1,3,4,5], 简单的叠加, 非常直观!
```


## 拷贝(浅拷贝, 深拷贝)

``` python
l = [['a'], ['b', 'c'], ['d', 'e', 'f']]

# 别名及浅拷贝
l1 = l              # l1为l的别名/指针, 指向相同的地址. (l is l1 = True)
l1 = l[:]           # 浅拷贝(只拷贝一维的数据). (l is l1 = False. l[0] is l1[0] = True)
# 在此例中, 由于是浅拷贝, 因此修改元素如 l[0][0]='z' 后, l1显示内容会和l一样.

# 深拷贝
import copy
l1 = copy.deepcopy(l)   # 深拷贝(遇到指针类型继续深挖). (l is l1 = False. l[0] is l1[0] = False)
# 在此例中, l1 和 l 再无任何关联
```


# tuple `()`

理解为list的常量形式即可, 赋值后就不可增减和修改

``` python
# 赋值
t = (1,2)   # 赋值2个元素
t = (1,)    # 赋值1个元素时, 必须加上逗号, 避免误解
t = (1,3)*3        # t = (1,3,1,3,1,3)

# 取值, 使用切片即可
t[-1]       # 取最后一个值, 3
t[0::2]     # 跳着取值, (1,1,1)

# 取长度
len(t)      # 6

# 获取元素出现的个数
t.count(1)  # 3

# list 与 tuple 互相转换
l = list(t) # 把tuple变为list
t = tuple(l)# 把list变为tuple

# 拷贝的问题同list
```



# dict `{}`

dict全称dictionary，在其他语言中也称为map，使用键-值（key-value）存储，具有极快的查找速度。


## 赋值及取值

``` python
# dict 赋值
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}

# 获取值
d['Thomas']             # 不存在会报错
d.get('Thomas', -1)     # 不存在返回设定的默认值

# 判断键值
'Michael' in d          # in方法即可, 返回True

# 键值个数
len(d)                  # 3

# 获取key和value
d.keys()                # 关键字列表, ['Bob', 'Michael', 'Tracy']
d.values()              # 字典值列表, [75, 95, 85]
d.items()               # 转换为列表, [('Bob', 75), ('Michael', 95), ('Tracy', 85)]

# for循环取索引和值, 使用iteritems
for k, v in d.iteritems():
    print '{}: {}'.format(k, v)         # k为key, v为value值
```

## 增减及修改字典

``` python
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}

# 修改值 (如果key不存在, 变成增加元素)
d['Michael'] = 88       # d={'Bob': 75, 'Michael': 88, 'Tracy': 85}

# 增加值
d[0] = 0                # d={0: 0, 'Bob': 75, 'Michael': 88, 'Tracy': 85}

# 删除一个键值
d.pop(0)                # 返回value并删除键值    d={'Bob': 75, 'Michael': 95, 'Tracy': 85}
d.popitem()             # 返回value并删除首键值  d={'Michael': 95, 'Tracy': 85}
del d[0]                # 删除键值              d={'Michael': 95, 'Tracy': 85}
if 0 in d: del d[0]     # 避免报错的写法         d={'Michael': 95, 'Tracy': 85}

# 删除整个字典
d.clear()               # 清空字典, d变成空字典   d={}
del d                   # 删除了d这个字典

# 合并字典
x = {'a': 1, 'b': 2}; y = {'b': 3, 'c': 4}
z = x.copy()            # 字典拷贝              z = {'a': 1, 'b': 2}
z.update(y)             # 字典合并(新值覆盖旧值)  z = {'a': 1, 'c': 4, 'b': 3}
# z = {**x, **y}        # python 3.5以上, 可以直接使用
```


## 拷贝(浅拷贝, 深拷贝)

``` python
d = {0: [1,2,3], 1:{'k1': 'v1', 'k2': 'v2'}}

# 注意, d.update(), d.copy() 都是浅拷贝!

# 别名及浅拷贝
d1 = d                  # l1为l的别名/指针, 指向相同的地址. (d is d1 = True)
d1 = d.copy()           # 浅拷贝(只拷贝一维的数据). (d is d1 = False. d[0] is d1[0] = True)
# 设置 d[0][0] = 3; d[1]["k2"]=2 后, 会发现d1的值也跟着变了. 因为浅拷贝值拷贝一维的数据(指针).

# 深拷贝
import copy
d1 = copy.deepcopy(d)   # 深拷贝(遇到指针类型继续深挖). (d is d1 = False. d[0] is d1[0] = False)
# d 和 d1 再无任何瓜葛
```


# set `{}` `set([])`

set即集合, 是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。
集合不可放入可变对象, 如list(报`unhashable type`的错)

``` python
# 赋值
s = {1, 2, 3}               # s = set([1, 2, 3])
s = {1, 1, 2, 2, 3, 3}      # s = set([1, 2, 3]), 重复元素会被过滤掉

# 检查元素是否存在
3 in s                      # True

# 增加元素
s.add(4)                    # s = set([1, 2, 3, 4])
s.add(4)                    # 重复增加不会报错

# 删除元素
s.remove(4)                 # s = set([1, 2, 3])
if 4 in s: s.remove(4)      # 避免报错

# 集合的运算符号
s1 = {1, 2, 3}; s2 = {2, 3, 4}
s1 & s2                     # 交集    set([2, 3])
s1 | s2                     # 并集    set([1, 2, 3, 4])
s1 ^ s2                     # 补集    set([1, 4])
s1 - s2                     # 减法    set([1])
s2 - s1                     # 减法    set([4])
```



# collections模块的使用

## numedtuple 给tuple命名

``` python
>>> import collections
>>> Point = collections.namedtuple('Point', ['x', 'y'])
>>> p = Point(1.0, 2.0)
>>> p.x; p.y; p             # 也可以使用p[0], p[1]
1.0
2.0
Point(x=1.0, y=2.0)

# 修改值
>>> p = p._replace(x = 1.5, y= 1.1)
>>> p[0]; p[1]              # 等同于 p.x; p.y
1.5
1.1
```

## deque 双向队列

英文全称 `Double-ended queue`, 特性近似于双向链表, 适用于队列和栈

``` python
>>> import collections
>>> q = collections.deque(['a', 'c'])
>>> q.append(1)             # q=deque(['a', 'c', 1])
>>> q.appendleft(2)         # q=deque([2, 'a', 'c', 1])
>>> q.extend([3, 4])        # q=deque([2, 'a', 'c', 1, 3, 4])
>>> q.extendleft([5, 6])    # q=deque([6, 5, 2, 'a', 'c', 1, 3, 4])
>>> q.pop()                 # q=deque([6, 5, 2, 'a', 'c', 1, 3])
4
>>> q.popleft()             # q=deque([5, 2, 'a', 'c', 1, 3])
6
>>> q.rotate(1)             # q=deque([3, 5, 2, 'a', 'c', 1])
>>> q.rotate(-2)            # q=deque([2, 'a', 'c', 1, 3, 5])

# 限长的双向队列
>>> last_three = collections.deque([1,2,3,4,5], maxlen=3)
>>> last_three
que([3, 4, 5], maxlen=3)    # 队列长度最多为3.
```

## defaultdict 带默认键值的dict

使用`dict`时，如果引用的Key不存在，就会抛出`KeyError`。如果希望key不存在时，返回一个默认值，就可以用`defaultdict`

``` python
# 普通字典
>>> m = dict()
>>> m['a']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'a'

# 默认字典
>>> import collections
>>> m = collections.defaultdict(int)
>>> m['a']
0

>>> m = collections.defaultdict(str)
>>> m['a']
''

>>> m = collections.defaultdict(lambda: 'N/A')
>>> m['a']
'N/A'
```

## OrderedDict 可排序的dict

``` python
# 普通字典, key是无需的
>>> d = dict([('a', 1), ('b', 2), ('c', 3)])
>>> d
{'a': 1, 'c': 3, 'b': 2}

# 可排序字典, 按照key插入的顺序排序
>>> import collections
>>> od = collections.OrderedDict([('a', 1), ('b', 2), ('c', 3)])
>>> od
OrderedDict([('a', 1), ('b', 2), ('c', 3)])
```


实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key

``` python
from collections import OrderedDict

class FifoDict(OrderedDict):

    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print 'remove:', last
        if containsKey:
            del self[key]
            print 'set:', (key, value)
        else:
            print 'add:', (key, value)
        OrderedDict.__setitem__(self, key, value)
```

## Counter 计数类

`Counter`实际上是`dict`的一个子类, 是一个简单的计数器.

### 应用一: 多重集合(显示元素个数)

``` python
>>> import collections
>>> A = collections.Counter([1, 2, 2])
>>> B = collections.Counter([2, 2, 3])
>>> A; B
Counter({2: 2, 1: 1})
>>> A | B
Counter({2: 2, 1: 1, 3: 1})
>>> A & B
Counter({2: 2})
>>> A + B
Counter({2: 4, 1: 1, 3: 1})
>>> A - B
Counter({1: 1})
>>> B - A
Counter({3: 1})
```

### 应用二: 统计最常出现的元素

``` python
>>> A = collections.Counter(list("hello"))
>>> A
Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
>>> A.most_common(1)
[('l', 2)]
```


# 高阶应用

## list 加入索引值

``` python
>>> seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]

>>> list(enumerate(seasons, start=1))
[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
```

## list的压缩和解压, 以及转换为dict

``` python
>>> a = [1, 2, 3]; b = ['a', 'b', 'c']
>>> z = zip(a, b)
>>> z
[(1, 'a'), (2, 'b'), (3, 'c')]
>>> dict(z)     # 转换为dict
{1: 'a', 2: 'b', 3: 'c'}
>>> zip(*z)
[(1, 2, 3), ('a', 'b', 'c')]
```

## list相邻元素压缩器, 升维

``` python
>>> a = [1, 2, 3, 4, 5, 6]

>>> # Using iterators / 使用迭代器
>>> group_adjacent = lambda a, k: zip(*([iter(a)] * k))
>>> group_adjacent(a, 3)
[(1, 2, 3), (4, 5, 6)]
>>> group_adjacent(a, 2)
[(1, 2), (3, 4), (5, 6)]
>>> group_adjacent(a, 1)
[(1,), (2,), (3,), (4,), (5,), (6,)]

>>> # Using slices / 使用切片
>>> from itertools import islice
>>> group_adjacent = lambda a, k: zip(*(islice(a, i, None, k) for i in range(k)))
# 该lambda函数展开形式如下:
# def n_grams(a, n):
#     z = (islice(a, i, None) for i in range(n))
#     return zip(*z)
>>> group_adjacent(a, 3)
[(1, 2, 3), (4, 5, 6)]
>>> group_adjacent(a, 2)
[(1, 2), (3, 4), (5, 6)]
>>> group_adjacent(a, 1)
[(1,), (2,), (3,), (4,), (5,), (6,)]
```

## list展开, 降维

``` python
# 推荐使用 itertools.chain.from_iterable
>>> import itertools
>>> a = [[1, 2], [3, 4], [5, 6]]
>>> list(itertools.chain.from_iterable(a))
[1, 2, 3, 4, 5, 6]

# 不推荐使用 sum
>>> sum(a, [])
[1, 2, 3, 4, 5, 6]

# for 循环
>>> [x for l in a for x in l]
[1, 2, 3, 4, 5, 6]
>>> a = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
>>> [x for l1 in a for l2 in l1 for x in l2]
[1, 2, 3, 4, 5, 6, 7, 8]

>>> a = [1, 2, [3, 4], [[5, 6], [7, 8]]]
>>> flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
>>> flatten(a)
[1, 2, 3, 4, 5, 6, 7, 8]
```

## 快速查找list的若干最值

``` python
>>> import heapq, random
>>> a = [random.randint(0, 100) for __ in xrange(100)]
>>> heapq.nsmallest(5, a)
[0, 2, 4, 6, 6]             # a中最小的5个数
>>> heapq.nlargest(5, a)
[100, 100, 99, 98, 95]      # a中最大的5个数
```

## dict和list互换

``` python
# dict->list
>>> m = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
>>> m.keys()
['a', 'c', 'b', 'd']
>>> m.values()
[1, 3, 2, 4]
>>> m.items()
[('a', 1), ('c', 3), ('b', 2), ('d', 4)]

# list->dict
>>> l=[('a', 1), ('c', 3), ('b', 2), ('d', 4)]
>>> dict(l)
{'a': 1, 'c': 3, 'b': 2, 'd': 4}

>>> names = ['Michael', 'Bob', 'Tracy']; scores = [95, 75, 85]
>>> zip(names, scores)
[('Michael', 95), ('Bob', 75), ('Tracy', 85)]
>>> dict(zip(names, scores))
{'Bob': 75, 'Michael': 95, 'Tracy': 85}
```

## dict内key和value互换

``` python
# using zip
>>> m = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
>>> zip(m.values(), m.keys())
[(1, 'a'), (3, 'c'), (2, 'b'), (4, 'd')]
>>> dict(zip(m.values(), m.keys()))
{1: 'a', 2: 'b', 3: 'c', 4: 'd'}

# using a dictionary comprehension
>>> m = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
>>> m.items()
[('a', 1), ('c', 3), ('b', 2), ('d', 4)]
>>> {v: k for k, v in m.items()}
{1: 'a', 2: 'b', 3: 'c', 4: 'd'}
```

##  快速生成规律性字典

``` python
>>> {x: x ** 2 for x in range(5)}
{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

>>> {x: 'A' + str(x) for x in range(10)}
{0: 'A0', 1: 'A1', 2: 'A2', 3: 'A3', 4: 'A4', 5: 'A5', 6: 'A6', 7: 'A7', 8: 'A8', 9: 'A9'}
```

## 字符串与列表字典的互换

``` python
# 字符串->列表 (去掉引号)
>>> eval("[1,2,3]")
[1, 2, 3]
# 如果输入数据不安全, 使用ast.literal_eval(), eval的替代品, 更安全

# 字符串->字典 (去掉引号)
>>> eval("{'one':1, 'two':2}")
{'two': 2, 'one': 1}
# 如果输入数据不安全, 使用ast.literal_eval(), eval的替代品, 更安全

# 字符串->列表
>>> lst = list("hello")
>>> lst
['h', 'e', 'l', 'l', 'o']

# 列表->字符串
>>> ''.join(lst)
'hello'

# 字符串->列表 (指定分隔符, 如空格, 逗号)
>>> season = 'spring, summer, autumn, winter'
>>> season.split (',')
['spring', ' summer', ' autumn', ' winter']

# 列表->字符串
>>> lst = ["spring", "summer", "autumn", "winter"]
>>> ', '.join(lst)
'spring, summer, autumn, winter'

# 整数列表->字符串
>>> lst = [1, 2, 3]
>>> ''.join(str(e) for e in lst)
'123'
```



# 参考和资料

- [廖雪峰的官方网站之python教程](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001411031239400f7181f65f33a4623bc42276a605debf6000)
- [30 Python Language Features and Tricks You May Not Know About](http://sahandsaba.com/thirty-python-language-features-and-tricks-you-may-not-know.html)
- [怎样合并字典最符合Python语言习惯？](http://codingpy.com/article/the-idiomatic-way-to-merge-dicts-in-python/)

----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***