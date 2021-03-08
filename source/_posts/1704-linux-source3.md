---
title: Linux 0.11 源码阅读笔记-内核代码
date: 2017-01-31
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



# 内核代码

![kernel-function](https://draapho.github.io/images/1704/3-kernel-function.jpg)

## 硬件中断程序

处理系统硬件中断. 多为故障处理, 直接打印出堆栈信息帮助排错.

## 系统调用程序
本质是调用中断 int 0x80. 由于是用户发起的, 也称之为软中断.

- system_call.s 会根据 `sys_call_table[]` (在sys.h内) 去调用相应的C函数. sys_xxx函数则很分散.
- signal.c 用于处理内核的信号. (`signal()`可能丢失信号, `sigaction()`更可靠)

*信号处理程序的调用方式*
![signal](https://draapho.github.io/images/1704/3-signal.jpg)

## 调度程序
linux 0.11的调度思路结合`时间片`和`优先权`调度.

*调用fork创建新进程*
![fork-function](https://draapho.github.io/images/1704/2-fork-function.jpg)

- 调度过程: count大, 就优先调度! 计算公式为: `count = counter/2 + priotiry`.
  对于以及运行完成的任务, count 直接为 priotiry
  对于被阻塞的任务, 由于公式内包含有 count/2 的权重, 即使优先级再低, 也会被照顾到.
- `switch_to()` 一段汇编宏定义, 用于切换到指定任务(加载TSS).
- `schedule()` 调度函数, 每10ms判断各任务的信号位图以及比较`counter`值. 需要切换任务时, 调用 `switch_to(next)`
- `do_timer()` 在 system_call.s 中 `_timer_interrupt` 被调用, 每10ms调用一次 `schedule()`
- `sleep_on()` 当进程所请求的资源暂时不可用时, 等待一段时间. 等切换回来后再继续运行. 调用 `schedule()`
- `wake_up()` 把正在等待可用资源的指定任务值为就绪状态, 就如字面意义, 是一个唤醒函数. 但实现比较搞脑子!



# 参考

- [Linux 内核完全注释 内核版本0.11 - 赵炯](http://oldlinux.org/download/clk011c-3.0-toc.pdf)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***