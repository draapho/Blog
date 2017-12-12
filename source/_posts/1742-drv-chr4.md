---
title: 驱动之poll机制
date: 2017-12-11
categories: embedded linux
tags: [linuxembedded linux, drv]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之字符设备-框架](https://draapho.github.io/2017/11/22/1733-drv-chr1/)
- [驱动之基于LinK+设计按键驱动](https://draapho.github.io/2017/11/30/1740-drv-chr2/)
- [驱动之基于中断设计按键驱动](https://draapho.github.io/2017/12/07/1741-drv-chr3/)
- [驱动之poll机制](https://draapho.github.io/2017/12/11/1742-drv-chr4/)
- [驱动之异步通知](https://draapho.github.io/2017/12/12/1743-drv-chr5/)
- [驱动之同步互斥阻塞](https://draapho.github.io/2017/12/13/1744-drv-chr6/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.

# POLL机制分析

## 三种按键驱动的比较
- 查询方式: 依赖于应用程序的编写方式, 写的不好会非常耗费CPU资源
- 中断方式: 解决了CPU资源问题, 但是应用程序会阻塞在读取函数上
- poll方式: 应用程序上, 实现了非阻塞读取. 先poll判断是否发生事件, 有事件处理, 无事件可以做其它事情.

## 核心流程

基本流程如下:
- 应用程序调用poll > sys_poll > `do_sys_poll` > do_poll > do_pollfd > 驱动程序poll
- 从 `do_sys_poll` 函数深入分析:
    - 先调用 `poll_initwait`, 注册一下 `__pollwait` 函数.
    - 再调用 `do_poll` 判断条件. 这里会调用驱动函数的poll
        - 调用 `do_pollfd` 函数, 实际上就是调用驱动的poll函数
        - 返回值为1或等待超时或触发信号, 执行 `__set_current_state` 继续运行当前进程.
        - 返回值为0, 则执行 `schedule_timeout` 当前进程睡眠, 切换到其它进程.
- 驱动函数里的poll会调用 `poll_wait`, 只是把当前的进程加入到 button_waitq 队列里去, 并没有立刻切换进程
    - `poll_wait` 调用 `p->qproc(filp, wait_address, p);`, 实际就是调用了 `__pollwait` 函数
    - 进程并不会阻塞在 `poll_wait` 函数. (这个函数的命名容易让人误解, 因此特此强调!)
    - 整个进程会根据驱动的poll返回值确定是休眠还是继续运行.

``` c
app: poll, 会去调用 sys_poll. 共三个参数
    // 1. *ufds, 文件指针. 需要查询的驱动文件列表
    // 2. nfds, 文件个数.
    // 3. timeout_msecs, 超时时间.
kernel: sys_poll    // 位于 /fs/select.c
            do_sys_poll(..., timeout_jiffies)
                poll_initwait(&table);
                    init_poll_funcptr(&pwq->pt, __pollwait);
                    // table->pt->qproc = __pollwait. 相当于注册一下 __pollwait.
                    // __pollwait 是系统函数, 用于初始化一个 poll_wqueues 的 table
                    // 驱动程序的poll函数会调用__pollwait函数.
                do_poll(nfds, head, &table, timeout)
                    for (;;) {
                        if (do_pollfd(ftd, pt)) {
                            // 进入函数 do_pollfd, 有如下两句:
                            mask = file->f_op->poll(file, pwait);
                                // 实际上, 就是调用驱动代码里的poll, 驱动代码里会调用
                                pollwait(filp, &button_waitq, p) {
                                    // 把当前的进程挂到button_waitq队列里去
                                    // 整个进程并不会阻塞在 pollwait 这里!
                                    p->qproc(filp, wait_address, p);    // 相当于调用 __pollwait
                                    // 这里我有过疑惑, 为何不直接指定 __pollwait 这么一个系统函数, 而是用初始化函数指针再调用的晦涩方法.
                                    // 搜索 init_poll_funcptr 后, 就可以知道, 这也是一个系统架构, 不同的地方会有不同的函数.
                                }
                                // 驱动poll函数给出返回值. 赋值给mask
                                // 因此整个进程会在调用完驱动poll函数后, 根据返回值进行休眠或继续运行.
                            return mask;
                            count++; // 如果驱动的poll返回非0值, 那么count++
                            pt = NULL;
                        }

                        // break的条件: count非0, 超时, 有信号在等待处理
                        if (count || !*timeout || signal_pending(current))
                            break;

                        // 休眠 __timeout
                        __timeout = schedule_timeout(__timeout);
                    }

                    // 设置当前进程为运行态
                    __set_current_state(TASK_RUNNING);
```


# 更多资料
- [linux poll 和 等待队列休眠的关系](http://blog.csdn.net/rockrockwu/article/details/7310518)
- [select(poll)系统调用实现解析(一)](http://blog.csdn.net/lizhiguo0532/article/details/6568964)
- [select(poll)系统调用实现解析(二)](http://blog.csdn.net/lizhiguo0532/article/details/6568968)
- [select(poll)系统调用实现解析(三)](http://blog.csdn.net/lizhiguo0532/article/details/6568969)
- [linux的poll的工作机制](http://www.cnblogs.com/jack204/archive/2011/10/30/2229331.html)
- [字符设备驱动-poll机制](http://blog.csdn.net/czg13548930186/article/details/77825262)



# 驱动源码

驱动源码基于 [驱动之基于中断设计按键驱动](https://draapho.github.io/2017/12/07/1741-drv-chr3/) 增加poll函数即可.
然后应用层的测试文件改动较大.
**注意驱动层和应用层的poll函数写法就可以了, 都是固定的结构**

## drv_key_poll.c

``` c
// 基于 驱动之基于中断设计按键驱动 源码增加而来. 只显示新增和修改的部分. 这样更直观易懂.

#include"drv_key_poll.h"                    // 头文件改一下
#define DRV_KEY_INT_NODE_NAME "key_poll"    // 名称改一下

static unsigned drv_key_poll(struct file *file, poll_table *wait)
{
    unsigned int mask = 0;
    poll_wait(file, &key_waitq, wait);      // 这里不会休眠. 进程不阻塞

    if (ev_press)
        mask |= POLLIN | POLLRDNORM;        // 关键是返回值, 返回值为0, 进程可能休眠.
        // POLLIN, 是标准的事件值, 测试程序就基于此判断.
        // POLLRDNORM, Normal data may be read without blocking. 作用应该是告知应用程序类型和后续动作.

    return mask;
}

static const struct file_operations drv_key_int_fops= {
    .owner              = THIS_MODULE,
    .open               = drv_key_int_open,
    .release            = drv_key_int_release,
    .read               = drv_key_int_read,
    .poll               = drv_key_poll,     // 新增这一行
};
```

## drv_key_poll.h

``` c
#define DRIVER_NAME "drv_key_poll"          // 名称改一下
#define PDEBUG(fmt,args...) printk(KERN_DEBUG"%s:"fmt,DRIVER_NAME, ##args)
#define PERR(fmt,args...) printk(KERN_ERR"%s:"fmt,DRIVER_NAME,##args)
#define PINFO(fmt,args...) printk(KERN_INFO"%s:"fmt,DRIVER_NAME, ##args)
#include<linux/cdev.h>
#include<linux/device.h>
#include<linux/fs.h>
#include<linux/init.h>
#include<linux/kdev_t.h>
#include<linux/module.h>
#include<linux/types.h>
#include<linux/uaccess.h>

#include <linux/interrupt.h>
#include <linux/irq.h>
#include <linux/poll.h>                     // 新增poll头文件
#include <asm/irq.h>
#include <asm/arch-s3c2410/irqs.h>
#include <asm/uaccess.h>
#include <asm/io.h>
#include <asm/arch/regs-gpio.h>
#include <asm/hardware.h>
```

## Makefile

``` makefile
obj-m		:= drv_key_poll.o 
KERN_SRC	:= /home/draapho/share/kernel/linux-2.6.22.6/
PWD			:= $(shell pwd)

modules:
	make -C $(KERN_SRC) M=$(PWD) modules

install:
	make -C $(KERN_SRC) M=$(PWD) modules_install
	depmod -a

clean:
	make -C $(KERN_SRC) M=$(PWD) clean
```

## 测试文件 test_drv_key_int.c

``` c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <poll.h>

int main(int argc, char **argv)
{
    int fd, ret;
    unsigned char keys_val;
    struct pollfd fds[1];                   // poll 关联的文件, 可多个文件

    fd = open("/dev/key_poll0", O_RDWR);
    if (fd < 0) {
        printf("can't open!\n");
        return 0;
    }

    fds[0].fd     = fd;                     // 关联的驱动文件
    fds[0].events = POLLIN;                 // 事件类型

    while (1) {
        ret = poll(fds, 1, 5000);           // 执行poll. 最多阻塞5s (有按键事件会立刻返回)
        if (ret == 0) {
            printf("time out\n");           // 5s后超时
        } else {
            read(fd, &keys_val, 1);         // 有按键, 读取按键值
            printf("keys_val = 0x%x\n", keys_val);
        }
    }

    return 0;
}
```


# 编译并测试

## Ubuntu主机端

``` bash
# 主机端, 编译源码
# pwd = /home/draapho/share/drv/drv_key_poll/KERN_SRC   # 驱动源码路径, share是nfs共享文件夹

# 编译驱动
$ make clean
$ make modules                      # 也可以在LinK+里面直接编译, 更方便

# 编译测试代码
$ arm-linux-gcc test_drv_key_poll.c -o test_drv_key_poll
```

## 开发板端
``` bash
# 开发板端, 测试驱动功能
# pwd = /home/draapho/share/drv/drv_key_poll/KERN_SRC   # 驱动源码路径, share是nfs共享文件夹

$ insmod drv_key_poll.ko            # 加载模块
drv_key_int:INIT

$ ./test_drv_key_poll               # 检测按键中断
drv_key_poll:In char driver open() function
# 无按键时, 每5s打印 time out
# 有按键时, 立刻打印按键值

# 按ctrl+c 终止进程

$ ./test_drv_key_poll &             # 后台运行
$ top                               # 查看系统资源情况
# 可以看到 ./test_drv_key_poll 进程占用很少的资源.
```
