---
title: python基础： 深入理解 python 中的赋值、引用、拷贝、作用域
date: 2016-11-21
categories: python
tags: [python]
---

***转载自 [python基础（5）：深入理解 python 中的赋值、引用、拷贝、作用域](https://my.oschina.net/leejun2005/blog/145911)***

---------------------------

# python的赋值
在 python 中赋值语句总是建立对象的引用值，而不是复制对象。因此，python 变量更像是指针，而不是数据存储区域，
![python_point](https://draapho.github.io/images/1618/python_point_1.jpg)
这点和大多数 OO 语言类似吧，比如 C++、java 等 ~


# 先来看个问题吧：
## 一个赋值问题

在Python中，令`values=[0,1,2];values[1]=values`,为何结果是`[0,[...],2]`? [链接](http://www.zhihu.com/question/21000872)

``` python
>>> values = [0, 1, 2]
>>> values[1] = values
>>> values
[0, [...], 2]       # 实际结果, 为何要赋值无限次?
[0, [0, 1, 2], 2]   # 预想结果
```

可以说 Python 没有赋值，只有引用。你这样相当于创建了一个引用自身的结构，所以导致了无限循环。为了理解这个问题，有个基本概念需要搞清楚。

Python 没有「变量」，我们平时所说的变量其实只是「标签」，是引用。

执行 `values = [0, 1, 2]` 的时候，Python 做的事情是首先创建一个列表对象 [0, 1, 2]，然后给它贴上名为 values 的标签。

如果随后又执行 `values = [3, 4, 5]` 的话，Python 做的事情是创建另一个列表对象 [3, 4, 5]，然后把刚才那张名为 values 的标签从前面的 [0, 1, 2] 对象上撕下来，重新贴到 [3, 4, 5] 这个对象上。

至始至终，并没有一个叫做 values 的列表对象容器存在，Python 也没有把任何对象的值复制进 values 去。过程如图所示：

![python_point](https://draapho.github.io/images/1618/python_point_2.jpg)


执行 `values[1] = values` 的时候，Python 做的事情则是把 values 这个标签所引用的列表对象的第二个元素指向 values 所引用的列表对象本身。执行完毕后，values 标签还是指向原来那个对象，只不过那个对象的结构发生了变化，从之前的列表 [0, 1, 2] 变成了 [0, ?, 2]，而这个 ? 则是指向那个对象本身的一个引用。如图所示：

![python_point](https://draapho.github.io/images/1618/python_point_3.jpg)



## 浅复制及其风险

要达到你所需要的效果，即得到 [0, [0, 1, 2], 2] 这个对象，你不能直接将 values[1] 指向 values 引用的对象本身，而是需要吧 [0, 1, 2] 这个对象「复制」一遍，得到一个新对象，再将 values[1] 指向这个复制后的对象。Python 里面复制对象的操作因对象类型而异，复制列表 values 的操作是

``` python
values[:] #生成对象的拷贝或者是复制序列，不再是引用和共享变量，但此法只能顶层复制
```

所以你需要执行 `values[1] = values[:]` 

Python 做的事情是，先 dereference 得到 values 所指向的对象 [0, 1, 2]，然后执行 [0, 1, 2][:] 复制操作得到一个新的对象，内容也是 [0, 1, 2]，然后将 values 所指向的列表对象的第二个元素指向这个复制二来的列表对象，最终 values 指向的对象是 [0, [0, 1, 2], 2]。过程如图所示：

![python_point](https://draapho.github.io/images/1618/python_point_4.jpg)

往更深处说，values[:] 复制操作是所谓的「浅复制」(shallow copy)，当列表对象有嵌套的时候也会产生出乎意料的错误，比如为何要赋值无限次

``` python
a = [0, [1, 2], 3]
b = a[:]
a[0] = 8
a[1][1] = 9
```
问：此时 a 和 b 分别是多少？

正确答案是 a 为 [8, [1, 9], 3]，b 为 [0, [1, 9], 3]。发现没？b 的第二个元素也被改变了。想想是为什么？不明白的话看下图

![python_point](https://draapho.github.io/images/1618/python_point_5.jpg)

## 深复制

正确的复制嵌套元素的方法是进行「深复制」(deep copy)，方法是

``` python
import copy

a = [0, [1, 2], 3]
b = copy.deepcopy(a)
a[0] = 8
a[1][1] = 9
```

![python_point](https://draapho.github.io/images/1618/python_point_6.jpg)


# 引用 VS 拷贝：

- 没有限制条件的分片表达式（L[:]）能够复制序列，但此法只能浅层复制。
- 字典 copy 方法，D.copy() 能够复制字典，但此法只能浅层复制
- 有些内置函数，例如 list，能够生成拷贝 list(L)
- copy 标准库模块能够生成完整拷贝：deepcopy 本质上是递归 copy
- 对于不可变对象和可变对象来说，浅复制都是复制的引用，只是因为复制不变对象和复制不变对象的引用是等效的（因为对象不可变，当改变时会新建对象重新赋值）。所以看起来浅复制只复制不可变对象（整数，实数，字符串等），对于可变对象，浅复制其实是创建了一个对于该对象的引用，也就是说只是给同一个对象贴上了另一个标签而已。

``` python
L = [1, 2, 3]
D = {'a':1, 'b':2}
A = L[:]
B = D.copy()
print "L, D"
print  L, D
print "A, B"
print A, B
print "--------------------"
A[1] = 'NI'
B['c'] = 'spam'
print "L, D"
print  L, D
print "A, B"
print A, B


L, D
[1, 2, 3] {'a': 1, 'b': 2}
A, B
[1, 2, 3] {'a': 1, 'b': 2}
--------------------
L, D
[1, 2, 3] {'a': 1, 'b': 2}
A, B
[1, 'NI', 3] {'a': 1, 'c': 'spam', 'b': 2}
```

# 增强赋值以及共享引用：

x = x + y，x 出现两次，必须执行两次，性能不好，合并必须新建对象 x，然后复制两个列表合并

属于复制/拷贝

x += y，x 只出现一次，也只会计算一次，性能好，不生成新对象，只在内存块末尾增加元素。

当 x、y 为list时， += 会自动调用 extend 方法进行合并运算，in-place change。

属于共享引用

``` python
L = [1, 2]
M = L
L = L + [3, 4]
print L, M
print "-------------------"
L = [1, 2]
M = L
L += [3, 4]
print L, M


[1, 2, 3, 4] [1, 2]
-------------------
[1, 2, 3, 4] [1, 2, 3, 4]
```

# python 从 2k 到 3k，语句变函数引发的变量作用域问题

先看段代码：

``` python
def test():
    a = False
    exec ("a = True")
    print ("a = ", a)
test()

b = False
exec ("b = True")
print ("b = ", b)
```

在 python 2k 和 3k 下 你会发现他们的结果不一样：

``` python
2K：
a =  True
b =  True

3K：
a =  False
b =  True
```

这是为什么呢？

因为 3k 中 exec 由语句变成函数了，而在函数中变量默认都是局部的，也就是说
你所见到的两个 a，是两个不同的变量，分别处于不同的命名空间中，而不会冲突。

具体参考 《learning python》P331-P332

知道原因了，我们可以这么改改：

``` python
def test():
    a = False
    ldict = locals()
    exec("a=True",globals(),ldict)
    a = ldict['a']
    print(a)

test()

b = False
exec("b = True", globals())
print("b = ", b)
```

这是一个典型的 python 2k 移植到 3k 不兼容的案例，类似的还有很多，也算是移植的坑吧~

具体的 2k 与 3k 有哪些差异可以看这里： [**使用 2to3 将代码移植到 Python 3**](http://woodpecker.org.cn/diveintopython3/porting-code-to-python-3-with-2to3.html)


# 深入理解 python 变量作用域及其陷阱

## 可变对象 & 不可变对象

- 在Python中，对象分为两种：可变对象和不可变对象，
- 不可变对象包括int，float，long，str，tuple等，可变对象包括list，set，dict等。
- 需要注意的是：这里说的不可变指的是值的不可变。对于不可变类型的变量，如果要更改变量，则会创建一个新值，把变量绑定到新值上，而旧值如果没有被引用就等待垃圾回收。另外，不可变的类型可以计算hash值，作为字典的key。
- 可变类型数据对对象操作的时候，不需要再在其他地方申请内存，只需要在此对象后面连续申请(+/-)即可，也就是它的内存地址会保持不变，但区域会变长或者变短。

``` python
>>> a = 'xianglong.me'
>>> id(a)
140443303134352
>>> a = '1saying.com'
>>> id(a)
140443303131776
# 重新赋值之后，变量a的内存地址已经变了
# 'xianglong.me'是str类型，不可变，所以赋值操作知识重新创建了str '1saying.com'对象，然后将变量a指向了它
 
>>> a_list = [1, 2, 3]
>>> id(a_list)
140443302951680
>>> a_list.append(4)
>>> id(a_list)
140443302951680
# list重新赋值之后，变量a_list的内存地址并未改变
# [1, 2, 3]是可变的，append操作只是改变了其value，变量a_list指向没有变
```

## 函数值传递

``` python
def func_int(a):
    a += 4
 
def func_list(a_list):
    a_list[0] = 4
 
t = 0
func_int(t)
print t
# output: 0
 
t_list = [1, 2, 3]
func_list(t_list)
print t_list
# output: [4, 2, 3]
```

对于上面的输出，不少Python初学者都比较疑惑：第一个例子看起来像是传值，而第二个例子确实传引用。其实，解释这个问题也非常容易，主要是因为可变对象和不可变对象的原因：对于可变对象，对象的操作不会重建对象，而对于不可变对象，每一次操作就重建新的对象。

在函数参数传递的时候，Python其实就是把参数里传入的变量对应的对象的引用依次赋值给对应的函数内部变量。参照上面的例子来说明更容易理解，func_int中的局部变量"a"其实是全部变量"t"所指向对象的另一个引用，由于整数对象是不可变的，所以当func_int对变量"a"进行修改的时候，实际上是将局部变量"a"指向到了整数对象"1"。所以很明显，func_list修改的是一个可变的对象，局部变量"a"和全局变量"t_list"指向的还是同一个对象。

## 为什么修改全局的dict变量不用global关键字

为什么修改字典d的值不用global关键字先声明呢？

``` python
s = 'foo'
d = {'a':1}
def f():
    s = 'bar'
    d['b'] = 2
f()
print s  # foo
print d  # {'a': 1, 'b': 2}
```

这是因为，在s = 'bar'这句中，它是“有歧义的“，因为它既可以是表示引用全局变量s，也可以是创建一个新的局部变量，所以在python中，默认它的行为是创建局部变量，除非显式声明global，global定义的本地变量会变成其对应全局变量的一个别名，即是同一个变量。

在d['b']=2这句中，它是“明确的”，因为如果把d当作是局部变量的话，它会报KeyError，所以它只能是引用全局的d,故不需要多此一举显式声明global。

上面这两句赋值语句其实是不同的行为，一个是**rebinding（不可变对象）**, 一个是**mutation（可变对象）**.

但是如果是下面这样：

``` python
d = {'a':1}
def f():
    d = {}
    d['b'] = 2
f()
print d  # {'a': 1}
```

在d = {}这句，它是”有歧义的“了，所以它是创建了局部变量d，而不是引用全局变量d，所以d['b']=2也是操作的局部变量。

推而远之，这一切现象的本质就是”它是否是明确的“。

仔细想想，就会发现不止dict不需要global，所有”明确的“东西都不需要global。因为int类型str类型之类的不可变对象，每一次操作就重建新的对象，他们只有一种修改方法，即x = y， 恰好这种修改方法同时也是创建变量的方法，所以产生了歧义，不知道是要修改还是创建。而dict/list/对象等可变对象，操作不会重建对象，可以通过dict['x']=y或list.append()之类的来修改，跟创建变量不冲突，不产生歧义，所以都不用显式global。

## 可变对象 list 的 = 和 append/extend 差别在哪？

接上面 5.3 的理论，下面咱们再看一例常见的错误：

``` python
# coding=utf-8
# 测试utf-8编码
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

list_a = []
def a():
    list_a = [1]      ## 语句1
a()
print list_a    # []

print "======================"

list_b = []
def b():
    list_b.append(1)    ## 语句2
b()
print list_b    # [1]
```

大家可以看到为什么 语句1 不能改变 list_a 的值，而 语句2 却可以？他们的差别在哪呢？

**因为 = 创建了局部变量，而 .append() 或者 .extend() 重用了全局变量。**

##  陷阱：使用可变的默认参数

我多次见到过如下的代码：

``` python
def foo(a, b, c=[]):
# append to c
# do some more stuff
```

永远不要使用可变的默认参数，可以使用如下的代码代替：

``` python
def foo(a, b, c=None):
    if c is None:
        c = []
    # append to c
    # do some more stuff
```

‍‍与其解释这个问题是什么，不如展示下使用可变默认参数的影响：‍‍

``` python
In[2]: def foo(a, b, c=[]):
...        c.append(a)
...        c.append(b)
...        print(c)
...
In[3]: foo(1, 1)
[1, 1]
In[4]: foo(1, 1)
[1, 1, 1, 1]
In[5]: foo(1, 1)
[1, 1, 1, 1, 1, 1]
```

同一个变量c在函数调用的每一次都被反复引用。这可能有一些意想不到的后果。


# REF：
- [《learning python》：P130、P134、P202、P204 、P245](http://www.zhihu.com/question/21000872/answer/16856382)
- [理解 Python 的 LEGB](http://blog.segmentfault.com/sunisdown/1190000000640834)
- [Python函数参数默认值的陷阱和原理深究](http://cenalulu.github.io/python/default-mutable-arguments/)
- [潜在的Python陷阱](http://python.jobbole.com/81564/)
- [陷阱！python参数默认值](http://segmentfault.com/a/1190000000743526)
- [Python中的变量、引用、拷贝和作用域](http://xianglong.me/article/python-variable-quote-copy-and-scope/)
- [Python入门基础知识(1) :locals() 和globals()](http://www.cnblogs.com/wanxsb/archive/2013/05/07/3064783.html)
- [Python程序员写代码时应该避免的16个“坑”](http://bit.ly/29vnLvz)

------------------------------

***转载自 [python基础（5）：深入理解 python 中的赋值、引用、拷贝、作用域](https://my.oschina.net/leejun2005/blog/145911)***
