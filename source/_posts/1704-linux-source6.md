---
title: Linux 0.11 源码阅读笔记-内存管理
date: 2017-02-15
categories: linux
tags: [linux]
---

# 总览

- [Linux 0.11 源码阅读笔记-总览](https://draapho.github.io/2017/01/23/1704-linux-source/)
- [Linux 0.11 源码阅读笔记-内存的基础概念](https://draapho.github.io/2017/01/26/1704-linux-source1/)
- [Linux 0.11 源码阅读笔记-启动程序](https://draapho.github.io/2017/01/28/1704-linux-source2/)
- [Linux 0.11 源码阅读笔记-内核代码](https://draapho.github.io/2017/01/31/1704-linux-source3/)
- [Linux 0.11 源码阅读笔记-设备驱动程序](https://draapho.github.io/2017/02/01/1704-linux-source4/)
- [Linux 0.11 源码阅读笔记-文件系统](https://draapho.github.io/2017/02/13/1704-linux-source5/)
- [Linux 0.11 源码阅读笔记-内存管理](https://draapho.github.io/2017/02/15/1704-linux-source6/)



# 内存管理

本人手工制作的 **Linux 0.11 内存管理图解**
![mm](https://draapho.github.io/images/1704/6-mm-map.jpg)

- 虚拟内存的实现, 使用的是页面出错异常处理. 然后调用 `do_no_page()` 来读取硬盘数据(必要时先回写), 腾出内存空间.
- 写时复制 (copy on write) 机制, 新建进程时, linux不会立刻复制进程数据.
  只有某个进程需要进行数据写操作时, 才真正开始执行复制操作.
  好处是, 节约内存, 加快创建进程的速度.
- Linux 0.11版本的内存管理的主要文件 `/mm/memory.c`
- 内存的一些基础概念请参考 [Linux 0.11 源码阅读笔记-内存的基础概念](https://draapho.github.io/2017/01/26/1704-linux-source1/)


# 进程的内存空间

进程代码和数据在其逻辑地址空间中的分布
![mm](https://draapho.github.io/images/1704/6-mm-process.jpg)
- Linux 0.11 每个进程只能有64M byte的逻辑内存.
- 环境参数块最多128K
- 堆栈指针是在逻辑地址的高位, 向下增长
- bss是进程未初始化的数据段, 第一页会被初始化为0
- 使用需求加载机制 (Load on demand), 因此在加载运行文件时, 只是分配64M的线性地址空间, 没有分配任何真正的物理内存.
- 此时, 内核在执行代码或加载数据时, 会触发缺页异常中断, 此时才调用 `do_no_page` 加载内容到物理内存.



# 内存的分配 `malloc`

使用存储桶原理进行内存的分配管理
![mm](https://draapho.github.io/images/1704/6-mm-malloc.jpg)
- 实现很巧妙. 指针应用的出神入化
- 仅内核代码可以调用.
- 基本思想: 对申请的不同的内存块大小, 使用存储桶分别进行处理.
- 提高内存利用率, 可有效避免内存碎片化.
- 源码文件 `/lib/malloc.c`


# 参考

- [Linux 内核完全注释 内核版本0.11 - 赵炯](http://oldlinux.org/download/clk011c-3.0-toc.pdf)


----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***