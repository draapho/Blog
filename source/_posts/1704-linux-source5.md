---
title: Linux 0.11 源码阅读笔记-文件系统
date: 2017-02-13
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

- 推荐阅读 [我是一块硬盘-码农翻身-刘欣](https://mp.weixin.qq.com/s?__biz=MzI5ODExMDQzNw==&mid=2650737282&idx=1&sn=07a3fc491dbd06ea61afe4c7108cf7b9&chksm=f4a17608c3d6ff1e7bb2b1168efa53f39db5c77b474296ba6086c1cf6612a452a6d234766b52&scene=0&key=7b81aac53bd2393d2edc7d94c6241745fd19b9a63b96f3683b767fbe2d367bd483fac89816919a23882f7bb13be77dc2&ascene=7&uin=MTUzODYxOTg2MQ%3D%3D&devicetype=android-19&version=26031933&nettype=live.vodafone.com&pass_ticket=MhcadpuflaJvGcaLNh0HQ3y1Ae%2FL2WCKStoj0RjDWXVN6c001WFeoX4HFyF1KE51)
  通俗易懂的介绍了硬盘及文件系统的管理方式, 也简单提了一下inode. 可以作为此部分的入门.


# 文件系统

本人手工制作的 **Linux 0.11 文件系统图解**
![fs](https://draapho.github.io/images/1704/5-fs-map.jpg)

几个核心点:
- Linux下**一切皆文件, 文件即i节点!**
- 文件名和i节点的关联, 在目录项结构中实现.
  索引过程为: **目录inode->目录名/文件名->对应inode->具体内容**
- 任何读写硬盘的过程都是通过内存的buffer(高速缓冲)实现的, 系统不能直接读写硬盘! 由此产生同步问题.
  调用过程为: **系统函数->buffer->硬盘**
- Linux对内存条的分配和使用. `Buffer` `Memory` 的概念和用途. `Buffer Head` `Buffer Hash List`.
  `Buffer` 介于高速的CPU指令和低速的硬盘之间, 用于缓存CPU对硬盘的读写内容, 提高CPU执行效率.
  `Memory` 是系统可用的内存. 系统变量, `malloc` 都是用的这块空间.
  `虚拟内存` 把使用频率低的 `Memory` 暂时搬到硬盘, 以便存放使用频率更高的内存数据. 依赖于硬盘读写操作!

## 硬盘设备分区

硬盘设备上的分区和文件系统
![hard disk](https://draapho.github.io/images/1704/5-fs-hard-disk.jpg)

- 主引导扇区: 存放硬盘引导程序和分区表信息.
- 分区表: 标明了每个分区的类型, 起止位置以及占用的扇区数.
- 相关文件: `kernel/blk_drv/hd.c`

下面, 将以MINIX1.0为例说明文件系统的基本概念.
Linux使用的其它的文件系统核心概念都是一样的! 只是支持的大小, 寻址速度, 文件上限有区别.


## MINIX1.0 文件系统

MINIX1.0 文件系统布局示意图
![minix](https://draapho.github.io/images/1704/5-fs-minix.jpg)

- 引导块: 上电时, BISO自动读入的部分. 有了引导块内引导程序, BIOS才能启动系统
- Super Block(超级块): 存放文件系统的结构信息, 说明各部分的大小. `super_block[8]`, 可加载8个文件系统
- Inode Bitmap(i节点位图): 记录i节点的使用情况, 1bit代表一个i节点. `s_imap[8]`, 占用8个块, 可表示8191个i节点情况
- Zone Bitmap(逻辑块位图): 记录数据区的使用情况, 1bit代表一个盘块(block). `s_zmap[8]`, 占用8个块, 最大支持64M的硬盘
- Inode(i节点): 每个文件或目录名唯一对应一个i节点, 在i节点中, 储存 id信息, 文件长度, 时间信息, 实际数据所在位置等等
- Zone Data(数据区): `8 (bit/byte)  * 1024 (byte/block) * 8(zmap blocks) * 1024 (byte/block)= 64M byte`

MINIX1.0 的超级块数据结构
![super block](https://draapho.github.io/images/1704/5-fs-super-block.jpg)


# 一切皆文件

## inode 详解

MINIX1.0 的i节点数据结构
![inode](https://draapho.github.io/images/1704/5-fs-inode.jpg)
- `i_nlinks`: **硬链接**计数器. 因此硬连接具有相同的inode号, 硬连接不能跨文件系统!

命令 `ls -l` 显示的文件信息, 多数信息读取i节点就可获得
![file info](https://draapho.github.io/images/1704/5-fs-file-info.jpg)
- 符号连接 `s`: 就是常说的**软连接**, 类似于windows下的快捷方式, 占用i节点, 在对应的数据块内存放路径

`i_zone[9]` i节点的逻辑块数组功能.
![izone](https://draapho.github.io/images/1704/5-fs-izone.jpg)
- `i_zone[0-6]` 直接块号: 存放文件开始的7个磁盘块号. 此时文件大小: `7*1024(byte/block)=7K byte`
- `i_zone[7]` 一次间接块号: 地址占用2byte, 因此一个数据块可存放512个地址. 此时可寻块 `7+512 blocks`
- `i_zone[8]` 二次间接块号: 此时可寻块 `7+512+512*512 blocks`, 文件的最大可达 `512M byte`
- `/dev/`下设备文件的 `i_zone[0]`: 设备文件不占用硬盘, 因此i节点仅保存设备的属性和设备号.


## 文件名的存储及查找

Linux 0.11 的目录项结构
``` c
// 定义在 include/linux/fs.h 文件中
#define NAME_LEN 14                 // 名字长度值
#define ROOT_INO 1                  // 根i节点

// 文件目录项结构
struct dir_entry {
    unsigned short inode;           // i节点号
    char name[NAME_LEN];            // 文件名
};
```
- 可见, linux下的文件名称都存在了目录项的数据里面, 并且唯一关联其i节点号.
- 每个目录项占用16字节, 因此, 一个盘块可以存放 `1024/16=64` 个目录项
- 对于空目录, 也至少会有名称未 `.` 和 `..` 两项, 指向 `当前目录inode` 和 `上级目录inode`
- 因此, 空目录的硬连接计数值`i_nlinks`为2, 每多一个文件, `i_nlinks`再加1.


通过文件名最终找到对应文件盘块位置的示意图
![inode find](https://draapho.github.io/images/1704/5-fs-inode-find.jpg)

整个搜索过程是根据`目录项结构`及对应的`inode 号`, 逐步深入路径的过程.
以路径名 `/usr/bin/vi` 搜索对应的i节点, 然后读取文件内容为例:
1. 根目录 `/` 具有固定的 inode号 `1`.
2. 读取`inode 1`的数据块, 搜索名为`usr`的目录项, 从而得到`/usr`的inode号, 假设为 `23`
3. 读取`inode 23`的数据块, 搜索名为`bin`的目录项, 假设`/usr/bin`的inode号为 `61`
4. 读取`inode 61`的数据块, 搜索名为`vi`的文件名, 假设获得`/usr/bin/vi`的inode号 `98`
5. 读取`inode 98`的数据块, 根据i节点信息, 如 `i_size` `i_zone[9]`, 最终读取文件内容


# 高速缓存 `buffer.c`

`buffer_head` 的数据结构
``` c
struct buffer_head {
    char * b_data;                      // 指向该缓冲块中数据区(1024字节)的指针
    unsigned long b_blocknr;            // 块号
    unsigned short b_dev;               // 数据源的设备号(0=free)
    unsigned char b_uptodate;           // 更新标记: 表示数据是否已更新
    unsigned char b_dirt;               // 修改标记: 0-未修改(clean), 1-已修改(dirty)
    unsigned char b_count;              // 使用该块的用户数
    unsigned char b_lock;               // 缓冲区是否被锁定. 0-ok, 1-locked
    struct task_struct * b_wait;        // 指向等待该缓冲区解锁的任务
    struct buffer_head * b_prev;        // hash 队列的前一块. (这四个指针用于缓冲区管理)
    struct buffer_head * b_next;        // hash 队列的下一块
    struct buffer_head * b_prev_free;   // 空闲表上前一块
    struct buffer_head * b_next_free;   // 空闲表上下一块
}
```

buffer的初始化
![inode find](https://draapho.github.io/images/1704/5-fs-buffer-init.jpg)

buffer的双向循环链表
![inode find](https://draapho.github.io/images/1704/5-fs-buffer-list.jpg)
- 该双向链表是最近最少使用LRU链表(Least Recently Used), `free_list` 指向最为空闲的缓冲块指针

buffer的hash表
![inode find](https://draapho.github.io/images/1704/5-fs-buffer-hash.jpg)
- Linux 0.11 使用的hash函数是 `设备号^逻辑块号 Mod 307`, 因此共有307项hash表
- hash的功能类似于字典, 先预先归类, 然后可以按类查找, 加快了查找速度.

缓冲区管理函数关系图
![inode find](https://draapho.github.io/images/1704/5-fs-buffer-function.jpg)

详解 `getblk()` 函数. 用于寻找最为空闲的buffer缓冲块.
![inode find](https://draapho.github.io/images/1704/5-fs-getblk.jpg)
- 首先调用 `get_hash_table()`, 查看搜索的指定缓冲块是否已经存在于buffer中. 存在就立刻返回该buffer指针.
- 不存在时, 从空闲链表头开始扫描, 寻找最合适的空闲块(没有被使用, 没有被上锁, 没有被修改). 实现LRU
- 因为可能别的进程已经加入了所需的缓冲块, 因此再调用一遍 `get_hash_table()`
- 此时, 可以将块应用计数置1, 把该缓冲块移到空闲队列末尾.


# 参考

- [Linux 内核完全注释 内核版本0.11 - 赵炯](http://oldlinux.org/download/clk011c-3.0-toc.pdf)
- [我是一块硬盘-码农翻身-刘欣](https://mp.weixin.qq.com/s?__biz=MzI5ODExMDQzNw==&mid=2650737282&idx=1&sn=07a3fc491dbd06ea61afe4c7108cf7b9&chksm=f4a17608c3d6ff1e7bb2b1168efa53f39db5c77b474296ba6086c1cf6612a452a6d234766b52&scene=0&key=7b81aac53bd2393d2edc7d94c6241745fd19b9a63b96f3683b767fbe2d367bd483fac89816919a23882f7bb13be77dc2&ascene=7&uin=MTUzODYxOTg2MQ%3D%3D&devicetype=android-19&version=26031933&nettype=live.vodafone.com&pass_ticket=MhcadpuflaJvGcaLNh0HQ3y1Ae%2FL2WCKStoj0RjDWXVN6c001WFeoX4HFyF1KE51)

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***