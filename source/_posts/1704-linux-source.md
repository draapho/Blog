---
title: Linux 0.11 源码阅读笔记-总览
date: 2017-01-23
categories: linux
tags: [linux]
description: 如题.
---

# 总览

- [Linux 0.11 源码阅读笔记-总览](https://draapho.github.io/2017/01/23/1704-linux-source/)
- [Linux 0.11 源码阅读笔记-内存的基础概念](https://draapho.github.io/2017/01/26/1704-linux-source1/)
- [Linux 0.11 源码阅读笔记-启动程序](https://draapho.github.io/2017/01/28/1704-linux-source2/)
- [Linux 0.11 源码阅读笔记-内核代码](https://draapho.github.io/2017/01/31/1704-linux-source3/)
- [Linux 0.11 源码阅读笔记-设备驱动程序](https://draapho.github.io/2017/02/01/1704-linux-source4/)
- [Linux 0.11 源码阅读笔记-文件系统](https://draapho.github.io/2017/02/13/1704-linux-source5/)
- [Linux 0.11 源码阅读笔记-内存管理](https://draapho.github.io/2017/02/15/1704-linux-source6/)


## Linux 发展背景

Linux操作系统的诞生(1991年),发展和成长过程依赖于以下五个重要支柱

1. UNIX操作系统 (诞生于1969年, 版权和专利问题不断, 大公司不愿公开操作系统原理和源码)
2. MINIX操作系统 (诞生于1987年, 意为 Mini UNIX. 教学使用是开源免费的! linus从中学习了操作系统的工作原理)
3. GNU计划 (诞生于1984年, 意为 GNU's Not Unix 递归缩写. 宗旨是开发一个类Unix的自由软件操作系统)
   有名的免费软件有: emacs, bash shell, gcc 编译程序, gdb 调试程序
   因此, 目前许多人将Linux操作系统称之为 [GNU/Linux 操作系统](http://www.gnu.org/gnu/gnu-linux-faq.html#why).
4. POSIX标准 (V1诞生于1988年, Portable Operating System Interface for Computing Systems)
   描述了操作系统的调用服务接口标准, 便于应用程序在不同操作系统上的移植.
   这为linux系统对应用程序的兼容提供了一套标准. 也是linux能流行起来的基础条件之一.
5. Internet网络 (确保了linux系统由众人开发维护, 其发展和推广都离不开Internet!)


## Linux, GNU, POSIX 的关系

![Linux_kernel_System_Call_Interface_and_glibc](https://draapho.github.io/images/1704/0-Linux_kernel_System_Call_Interface_and_glibc.png)


## 内核代码框图

![kernal-struct](https://draapho.github.io/images/1704/0-kernal-struct.png)


## 内核函数关系图

![kernal-fucntion](https://draapho.github.io/images/1704/0-linux-kernal-map.png)



# 参考

- [Linux 诞生和发展的五个重要支柱 - 赵炯](http://oldlinux.org/download/linux-devel.pdf)
- [GNU Operating System](http://www.gnu.org/gnu/gnu-linux-faq.html#why).)

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***