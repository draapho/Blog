---
title: Linux 0.11 源码阅读笔记-内存的基础概念
date: 2017-01-26
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


# Linux 内存的基础概念

## 内存条的分配
*Linux0.11 对物理内存条的分配*
![memory](https://draapho.github.io/images/1704/1-memory.jpg)
- `内核模块`, Linux Kernel的代码
- `高速缓冲 Buffer`, 缓存内核对硬盘的读写操作. 仅部分内核函数可用
- `主内存 Memory`, 应用程序可用的内存区. 虚拟内存也是针对这一块区域而言的.

## 内存的几个概念
- Virtual Memory
  linux 0.11内核中, 每个程序都划分了总容量为64Mb的虚拟内存空间
- Logical Address
  程序在虚拟内存空间的偏移量就是逻辑地址, 范围是0x0000000-0x4000000
- Linear Address
  在内存分段机制中, 把相应的段基址加上逻辑地址就是线性地址. 若没有开启分页功能, 直接就是物理地址.
  分段机制虽然保证了程序内存的相互隔离, 但是对内存的使用效率是非常低的!
  80x86 实时模式下, 寻址采用的是段和偏移值. 无分页机制.
  80x86 保护模式下, 会启用分页机制, 需要使用描述表(Descriptor Table)
- Physical Address
  真正的内存物理地址, 从逻辑地址到物理地址, 需要经过分段和分页两次转换.
- 分段机制
  - 相关概念有, GDT(全局描述符表), LDT(局部描述符表)
  - Linux基本忽略了分段机制, 通过"欺骗", 使得逻辑地址与线性地址是一致的! (用GDT, 基地址为0)
- 分页机制
  - 相关概念有 Page Directory(页目录), Page Table(页表)
  - 新版的linux, 为了提高兼容性, 直接采用了4级分页机制:
  - 页全局目录, Page Global Directory, 对应80x86的 Page Directory
  - 页上级目录, Page Upper Directory,  长度设为0即可
  - 页中间目录, Page Middle Directory, 长度设为0即可
  - 页表, Page Table, 对应80x86的 Page Table
- 任务状态段
  - TSS (Task State Segment)
  - TSS包含了所有硬件切换任务时, 需要保存的寄存器信息.
  - TSS存放于GDT内

## 内存地址的转换
*从逻辑地址变换为物理地址的过程*
![address-convert](https://draapho.github.io/images/1704/1-address-convert.jpg)

*从逻辑地址变化为物理地址的框图*
![address-convert-detail](https://draapho.github.io/images/1704/1-address-convert-detail.jpg)

*逻辑地址转换为线性地址的过程*
![logical2linear](https://draapho.github.io/images/1704/1-logical2linear.jpg)

*线性地址(页目录项, 页表项)在内存中位置*
![linear2physical](https://draapho.github.io/images/1704/1-linear2physical.jpg)

*页目录(Page Directory), 页表(Page Table)和物理内存的关系图*
![address-pdpt](https://draapho.github.io/images/1704/1-address-pdpt.jpg)

*进程代码和数据在其逻辑地址空间中的分布 (在物理地址中的分布是随机)*
![code-address](https://draapho.github.io/images/1704/1-code-address.jpg)

*linux 使用描述符表的示意图*
![gdt-ldt-memory](https://draapho.github.io/images/1704/1-gdt-ldt-memory.jpg)

*任务1在三种地址空间中的关系*
![address-relationship](https://draapho.github.io/images/1704/1-address-relationship.jpg)

## 80x86 多任务
- Intel 80x86分为4个保护级别, Linux 0.11只使用了0和3两个保护级别.
- 0为最高优先级, 对应于Linux内核态
- 3为最低优先级, 对应于Linux用户态
- 这样划分主要是为了安全考虑进行的系统级别的隔离.
- 用户态无权直接使用硬件资源, 必须通过调用内核函数.
- 多任务间, 内存是完全隔离的, 因此任务之间不会相互影响.

*linux 的多任务及保护方式*
![mulit-process](https://draapho.github.io/images/1704/1-mulit-process.jpg)

*linux 任务切换操作示意图*
![switch-process](https://draapho.github.io/images/1704/1-switch-process.jpg)



# 参考

- [Linux 内核完全注释 内核版本0.11 - 赵炯](http://oldlinux.org/download/clk011c-3.0-toc.pdf)


----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***