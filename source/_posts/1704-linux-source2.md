---
title: Linux 0.11 源码阅读笔记-启动程序
date: 2017-01-28
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



# 启动程序 boot

*启动引导时内核在内存中的位置和移动情况*
![bios-boot](https://draapho.github.io/images/1704/2-bios-boot.jpg)

1. 80x86结构的CPU开机后, 从0xFFFF0开始自动执行代码, 通常是 ROM-BIOS中的地址.
   BIOS在内存地址0处初始化中断向量, 然后将可启动设备的第一个扇区(磁盘引导扇区, 512字节)读入内存地址0x7C00处.
2. bootsect.s 被BIOS读入到内存地址 0x7C00(31Kb) 处开始运行后, 立刻把自己移到 0x90000(576Kb) 处.
3. 接着, bootsect.s 把 setup.s 读入到 0x90200 处, system模块(即内核)读入到 0x10000 处.
   - 此版本内核模块不会超过 0x80000, 即512K大小, 因此不会覆盖掉0x90000处的内容
   - setup.s 需要一些 ROM BIOS 保留下来的一些系统参数(如显卡模式, 硬盘参数等), 这些参数被BIOS放在内存起始处, 大小为1Kb.
   - 因而 bootsect.s 只能先把内核放到 0x10000 处而不是直接放到 0x0000 处!
4. bootsect.s 把执行权交给 setup.s.
5. 然后, setup.s 把BIOS预留在内存起始处的参数存储到0x90000处(覆盖了bootsect.s), 再把system模块移到内存起始处 (0x0000)
6. setup.s 把执行权交给 head.s, linux系统代码加载过程完成, linux开始启动!

备注:
- 启动过程涉及到很多80x86的硬件知识, 没必要深究, 重点是理解启动过程和思路!
- 因为目录linux早已支持arm体系结构, 嵌入式也以arm为主. 涉及到硬件的部分需要时再深入了解即可.

## bootsect.s
- bootsect.s 是磁盘引导块程序, 放在磁盘的一个扇区中(引导扇区).
- PC上电, BIOS自检后, BIOS会把引导扇区bootsect加载到内存地址0x7C00处并执行.
- bootsect 立刻把自己挪到 0x90000 处并继续执行
- 利用BISO中断0x13获取启动引导盘参数, 准备读取1.44MB启动磁盘内的后续部分(setup.s + system模块)
- 加载 setup.s 到 0x90200 处
- 在屏幕上显示 "Loading system..."
- 把system模块加载到0x10000处
- 长跳到 setup.s, 执行 setup.s

## setup.s
- setup.s 是一个操作系统加载程序. 主要作用读取BIOS保留的系统参数, 移动system模块到内存0x0000处, 并执行head.s代码
- setup.s 首先是把BIOS预留在内存0x0000处的参数保存到内存 0x90000 处, 会覆盖掉已经没有用的 bootsect.s 代码
- 主要参数有: 光标位置, 扩展内存数, 显示页面, 显示模式, 字符列数, 显示内存, 显示状态, 显卡特性, 硬盘参数, 根设备号
- 接着 setup.s 将system模块从 0x10000-0x8ffff 整体向下移动到 0x0000 处.
- 然后 setup.s 加载 idtr 和 gdtr (中断/全局描述符表寄存器), 重设中断号, 设置CPU进入32位保护模式运行
- 跳转到 system模块的 head.s 继续运行(运行在32位保护模式下)

*setup.s 结束后内中的程序示意图*
![setup-memory](https://draapho.github.io/images/1704/2-setup-memory.jpg)

## head.s
- head.s 位于整个linux操作系统最前面, 主要功能就是为linux的执行检测和初始化系统环境
- 设置系统堆栈
- 设置idt(中断描述符表) 和 gdt(全局表述符表)
- 检测A20地址线是否已真的开启 (就是能读取1M以上的内存地址)
- 将页目录表放在内存地址0处 (会覆盖自己idt部分的内容)
- 最后, heads利用返回指令, 弹出main.c的入口地址, 运行main()程序

*head.s 结束后, system模块在内存中的示意图*
![head-memory](https://draapho.github.io/images/1704/2-head-memory.jpg)

## main.c

*main初始化完成后, 内存功能示意图*
![maim-memory](https://draapho.github.io/images/1704/2-main-memory.jpg)

*内核初始化程序流程示意图*
![maim-flow](https://draapho.github.io/images/1704/2-main-flow.jpg)

*调用fork创建新进程*
![fork-function](https://draapho.github.io/images/1704/2-fork-function.jpg)

*进程(process), 进程组(process group) 和 会话期(session) 的关系图*
![session-process](https://draapho.github.io/images/1704/2-session-process.jpg)

- 一般一个用户登录后, 其所有程序属于同一个session. 用途很多, 譬如便于发出终止信号结束所有进程.



# 参考

- [Linux 内核完全注释 内核版本0.11 - 赵炯](http://oldlinux.org/download/clk011c-3.0-toc.pdf)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***