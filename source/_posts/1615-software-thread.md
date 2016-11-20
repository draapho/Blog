---
title: 协程/进程/线程资料收集
date: 2016-11-14
categories: software
tags: [python, process, ipc]
---

协程(Coroutine), 多线程(Thread), 多进程(Multiprocessing)资料繁多, 学无止境, 就集中在这一篇收集贴中. 便于查阅学习



# 自己的理解

- 协程, 任务之间不是竞争关系, 而是协作关系, 需要每个任务都需要有一颗舍己为公的心!
  - 大家排队喝水, 喝到差不多就自己让给下一个人, 自己再去排队! 可按照优先级来插队的.
  - 遇到不讲道理的人, 那这个机制就失效了. 因为没有抢占, 大家都只会默默等待...
  - 优点, 任务切换的代价非常小. 由于没有抢占, 也就没有复杂的临界区问题. 锁的问题也变得简单.
  - 缺点, 这个世界上总有不讲理的人, 所以, 大型任务和系统不敢这么用...
  - 单片机开发是非常适合使用协程的! (资源有限, 需要减小任务切换的开销. 任务可控, 意味着易于协作)
  - python 下可用 gevent. 


- 多线程, 任务之间是竞争关系, 高优先级优先执行, 同时又有时间片限制, 避免高优先级任务霸占CPU
  - 谁强谁喝水, 不过旁边有个管理员, 哪个家伙喝水时间太久了, 就会把他给跩一边去, 大家重新来抢.
  - 线程是共享内存的, 理解为这些水来自于同一个自来水厂(这个水厂有毒的话, 谁了逃不了),
  - 多核就是多个水龙头, 同一时刻可以有多个人在喝水.
  - 优点, 任务的开销比进程小(因为共享内存), 通讯方式多样. 加个水龙头和造个水厂的区别!!!
  - 缺点, 一大帮自私又不讲理的人在一起总是很难管理的... 需要各种锁机制来维持和谐共处...
  - python的多线程, 由于GIL机制的存在, 是无法利用多核的. (意味着不适用于CPU密集型任务)
  - python有一个类进程版本的线程池 `multiprocessing.pool.ThreadPool`, 可以获取返回值 
    由于本质是线程, Windows下terminate方法是没有用的.


- 多进程, 任务之间是竞争关系, 任务之间的数据全部隔离, 没有共享.
  - 进程是资源分配的基本单位. 进程包含线程, 线程共用进程的资源.
  - 进程比线程安全性更高, 因为拥有独立的内存块(独立水厂供水)
  - 进程的建立和调度比线程更费时间和资源
  - 进程间的数据共享和交换很麻烦. (python例子中, 进程内 print 不会打印, 参数传递需要可以pickle)
  - python 下推荐使用 `multiprocessing.pool.Pool`. 可以获取返回值.


- 进程和线程以及多核
  - 操作系统必须有一个进程, 创建进程时, 会分配好供这个进程使用的内存和上下文环境.
  - 线程依赖于进程, 多线程运行于同一个进程下面, 会共享同一个进程的内存.
  - 事实上, 线程是最难写好的一种多任务方式(因为共享内存).
  - 以android为例,
    - android的每一个应用就是一个linux进程, 所以写的再烂的应用也不会导致整个android系统崩溃.
    - 应用内支持多线程, 也事实上都对应到linux的线程, 这些线程运行在分配好的linux进程中.
  - 进程和线程的概念和单核还是多核一点关系都没有! 先理解好单核再说, 真正涉及到CPU密集型任务时, 再考虑多核优化...



# 优缺点比较

- 协程具有进程和线程各自的优点. 但其缺点是需要任务间自己来协作调度(很容易写成阻塞等待), 这一点直接导致了通用性很差.
- [多线程还是多进程的选择及区别](http://blog.csdn.net/lishenglong666/article/details/8557215), 比较全面的一篇文章!
  - 本文也有一个转字, 应该是综合了多种搜素结果写出来的一篇博文. 有结论, 有实验代码和过程
  - 鱼还是熊掌：浅谈多进程多线程的选择
  - 1.进程与线程
  - 一、重复周丽论文实验步骤
  - 二、增加并发数量的实验
  - 三、增加每进程/线程的工作强度的实验
  - 四、多进程和多线程在创建和销毁上的效率比较
  - 五、双核系统重复周丽论文实验步骤
  - 六、并发服务的不可测性


对比维度 |      多进程 |       多线程 |  总结
---------|------------|------------|-------
数据共享、同步| 数据共享复杂，需要用IPC；数据是分开的，**同步简单**|因为共享进程数据，**数据共享简单**，但也是因为这个原因导致同步复杂|各有优势
内存、CPU  |占用内存多，切换复杂，CPU利用率低 |  **占用内存少，切换简单，CPU利用率高**|线程占优
创建销毁、切换|创建销毁、切换复杂，速度慢|**创建销毁、切换简单，速度很快**|线程占优
编程、调试|**编程简单，调试简单**|编程复杂，调试复杂|进程占优
可靠性|**进程间不会互相影响**|一个线程挂掉将导致整个进程挂掉|进程占优
分布式|**适应于多核、多机分布式**；如果一台机器不够，扩展到多台机器比较简单|适应于多核分布式|进程占优



# 资料集

- [Python Multithreaded Programming](https://www.tutorialspoint.com/python/python_multithreading.htm)
  - Python多线程入门教程, 有详细的说明, 源代码及运行结果.
  - 主要有3个示例, 多线程, 多线程同步, 使用Queue来通讯

- [Python 多线程](http://www.jianshu.com/p/0e4ff7c856d3)
  - 介绍了Python多线程的状态, 类型
  - 线程的创建, 合并(join), 同步, 锁(Lock, 死锁, RLock), 其它IPC
  - 将子线程设置**后台线程**(setDaemon), 让子线程随主线程一起结束.
  - 提了一下Python的GIL, 参考资料中的一篇对此做了很好的说明: [python 线程，GIL 和 ctypes](http://zhuoqiang.me/python-thread-gil-and-ctypes.html)

- [Python线程同步机制: Locks, RLocks, Semaphores, Conditions, Events和Queues](http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/)
  - 内容如题, 无需多言. 文章最后重点推荐使用Queue

- [理解 Python 中的多线程](https://my.oschina.net/leejun2005/blog/179265)
  - 示例1, 请求五个不同的url. 比较了单线程和多线程性能上的差别
  - 示例2, 全局变量的线程安全问题（race condition）. BUG版和修改版
  - 示例3, 多线程环境下的原子操作. BUG版和修改版
  - 示例4, Python多线程简易版：线程池 threadpool
  - 附上了很多参考和推荐阅读的资料!

- 线程池 threadpool (需安装)
  - [Python多线程简易版 - 线程池threadpool](http://www.zhidaow.com/post/python-threadpool), 新手上路版
  - [Parallelism in one line](http://chriskiehl.com/article/parallelism-in-one-line/), 比较了传统方案和线程池方案, 并给出了范例
  - 这是`Parallelism in one line`的中文翻译版本, 并有遇到小坑和补充说明. [Python 并行任务技巧](https://my.oschina.net/leejun2005/blog/194270)
  - **注意： threadpool 是非线程安全的**。
    - 关于线程安全, 可参考[Java线程安全和非线程安全](http://blog.csdn.net/xiao__gui/article/details/8934832)
    - 个人理解, 对于python的非线程安全, 编程时需要特别注意 `可变对象` 和 `不可变对象`, 弄清楚Python到底是在`赋值`还是`引用`(相当于指针)
    - 可以参考此文 [python基础（5）：深入理解 python 中的赋值、引用、拷贝、作用域](https://my.oschina.net/leejun2005/blog/145911)
  - 初步结论, 还是比较推崇线程池的: 比起经典的方式来说简单很多，效率高，易懂，而且没什么死锁的陷阱。

- [Python 多线程教程：并发与并行](https://my.oschina.net/leejun2005/blog/398826)
  - 讲了多线程, 多进程, 以及分布式任务.
  - 原作者已下载网络图片来说明问题, 转发者为了便于测试和理解, 简化了代码.
  - 1, 单线程执行. 花了19.4秒去下载91张图片
  - 2, 多线程. 下载时间变成了4.1秒. 并说明了为何有GIL的情况下, 多线程仍然是有效的(因为是IO密集型的任务)
  - 3, 多进程. 优点, 避免了GIL, 适用于CPU密集型任务. 缺点, 耗内存!
  - 4, 分布式任务. 提了一下`RQ`和`Celery`
  - 5, 总结: IO密集型，多线程或多进程. CPU密集型, 多进程. 网络应用, 分布式任务
  - 6, 并发、并行区别与联系. 并发, 一个人按优先级处理多件事情(任一时刻只能做一件事情). 并行, 有多个人各自做事(多核多任务).

- **进程池 multiprocessing.Pool 以及 multiprocessing.pool.ThreadPool**
    - [Python 多进程实践](https://segmentfault.com/a/1190000003044986)
      - Python多进程的实现入门级文章
      - 创建子进程的方法: fork, multiprocessing, Pool 进程池
      - IPC(进程间通讯): Queue, Pipe
    - [Python 多进程 multiprocessing.Pool类详解](http://blog.csdn.net/seetheworld518/article/details/49639651)
    - [Python's undocumented ThreadPool](http://lucasb.eyer.be/snips/python-thread-pool.html), 提了一下 ThreadPool
    - [python 延时及超时](https://draapho.github.io/2016/11/28/1622-python-time/), "学习过程中的例子" 中有尝试使用进程池
    - [Python 中 Ctrl+C 不能终止 Multiprocessing Pool 的解决方](http://www.eenot.com/thread-103459-1-1.html), ThreadPool有同样的问题. 可以搜索关键字: Keyboard Interrupts multiprocessing Pool.
    - [使用 multiprocessing.pool.ThreadPool 可能的潜在风险](http://bugs.python.org/issue17140), 本质是线程, 而且没有文档说明

- [浅谈 python multiprocessing（多进程）下如何共享变量](https://my.oschina.net/leejun2005/blog/203148)
  - 1, 抛出了一个多进程的问题.
  - 2, python 多进程共享变量的几种方式
  - 3, 多进程的问题远不止这么多：数据的同步. (需要Lock)
  - 4, 总结为: 多进程最好还是用IPC(message之类的). 如果一定要用共享变量, 那也是可以的...

- [Python之路：(十五）进程、线程和协程](https://liangxiansen.github.io/2016/08/08/python%E8%BF%9B%E7%A8%8B%E7%BA%BF%E7%A8%8B%E5%92%8C%E5%8D%8F%E7%A8%8B/)
  - Python线程, 线程锁(Lock, Rlock), 其它IPC, 线程池
  - Python进程, 进程数据共享, 进程IPC. (Python Windows下是可以用进程的, 只是不支持fork)
  - Python协程, greenlet(主动切换), gevent(遇到IO操作, 自动切换).

- **[gevent程序员指南](http://xlambda.com/gevent-tutorial/)**
  - 核心部分, 较为详细的介绍了 gevent 的原理和使用方式.
  - 数据结构, 介绍了协程之间的通讯工具
  - 真实世界的应用, 几个实际应用的例子
  


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***