---
title: Linux 0.11 源码阅读笔记-设备驱动程序
date: 2017-02-01
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



# 0.11源码设备驱动程序

## 字符设备驱动程序

![char-driver](https://draapho.github.io/images/1704/4-char-driver.jpg)

- `read_q` tty读队列
- `write_q` tty写队列, 调用 `copy_to_cooked()` 后放入 `secondary`
- `secondary` tty辅助队列(存放规范模式字符序列)

## 块设备驱动程序

![block-driver](https://draapho.github.io/images/1704/4-block-driver.jpg)

- `ll_rw_block()`添加完请求项后(使用了链表, 并使用电梯算法改善硬盘访问时间), 真正的操作通过调用`request_fn()`完成
- 操作硬盘 `do_hd_request()`, 操作软盘 `do_fd_request()`, 操作虚拟盘 `do_re_request()`


# linux 设备和模块的分类

## 字符设备

一个字符( char ) 设备是一种可以当作一个字节流来存取的设备( 如同一个文件 ); 一个字符驱动负责实现这种行为.
这样的驱动常常至少实现 `open`, `close`, `read`, 和 `write` 系统调用.

文本控制台 `/dev/console` 和串口 `/dev/ttyS0` 是字符设备的例子, 因为它们很好地展现了流的抽象.
字符设备通过文件系统结点来存取, 例如 `/dev/tty1` 和 `/dev/lp0`.

在一个字符设备和一个普通文件之间唯一有关的不同就是, 你经常可以在普通文件中移来移去, 但是大部分字符设备仅仅是数据通道, 你只能顺序存取.
然而, 存在看起来象数据区的字符设备, 你可以在里面移来移去. 例如, frame grabber 经常这样, 应用程序可以使用 mmap 或者 lseek 存取整个要求的图像.


## 块设备

如同字符设备, 块设备通过位于 `/dev` 目录的文件系统结点来存取. 一个块设备(例如一个磁盘)应该是可以驻有一个文件系统的.

Linux, 允许应用程序像一个字符设备一样读写一个块设备, 允许一次传送任意数目的字节.
如同一个字符设备, 每个块设备都通过一个文件系统结点被存取的, 它们之间的区别对用户是透明的.
因此块和字符设备的区别仅仅在内核在内部管理数据的方式上, 并且因此在内核/驱动的软件接口上不同.

注意, 在大部分的 Unix 系统, 一个块设备只能处理这样的 I/O 操作, 传送一个或多个长度经常是 512 字节的整块(或更大如1024字节)


## 网络接口

任何网络事务都通过一个接口来进行, 就是说, 一个能够与其他主机交换数据的设备.
通常, 一个接口是一个硬件设备, 但是它也可能是一个纯粹的软件设备, 比如环回接口.

一个网络接口负责发送和接收数据报文, 在内核网络子系统的驱动下, 不必知道单个事务是如何映射到实际的被发送的报文上的.
虽然很多网络连接(特别那些使用 TCP 的)是面向流的, 但网络设备却常常设计成处理报文的发送和接收.

网络设备驱动的实现与字符和块设备驱动完全不同. ~~不用 `read` 和 `write`~~, 需要使用和报文传递相关的函数.


## 硬件和驱动的关系

以 USB 设备为例, USB可以虚拟成串口(字符设备), 也可以是USB硬盘(块设备), 或者USB wifi(网络接口)
因此, 使用何种Linux的驱动和硬件无关, 而和与硬件的通讯方式有关.

一般地, 字节流使用字符设备驱动, 大量并发数据的传输使用块设备驱动. 网络接口驱动仅针对网络通讯.


# 参考

- [Linux 内核完全注释 内核版本0.11 - 赵炯](http://oldlinux.org/download/clk011c-3.0-toc.pdf)
- [设备和模块的分类](http://www.deansys.com/doc/ldd3/ch01s03.html)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***