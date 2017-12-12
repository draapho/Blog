---
title: 驱动之异步通知
date: 2017-12-12
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

# 异步通知范例

## 范例源码
``` c
#include <stdio.h>
#include <signal.h>

void get_signal(int signum) 
{
	static int cnt = 0;
	printf("signal=%d, %d times\n", signum, ++cnt);
}

int main(int argc, char **argv)
{
	printf("main start\n");
	signal(SIGUSR1, get_signal);
	printf("wait signal\n");
	while (1) {
		sleep(1000);
	}
	return 0;
}
```

## 范例测试
``` bash
# ubuntu主机端
$ arm-linux-gcc signal.c -o signal

# jz2440端
$ ./signal &        # 背景运行
main start
wait signal         # 程序顺序执行
$ ps                # 查看进程
790 0          1312 S   ./signal
$ kill -SIGUSR1 790 # 发送SIGUSR1信号
signal=10, 1 times  # 直接调用的 get_signal, 打印信息
$ kill -10 790      # 发送SIGUSR1信号
signal=10, 1 times  # 直接调用的 get_signal, 打印信息

# 这里说明一下kill指令, 其本意是发送signal给进程, 而不是杀死进程.
# 但如果进程没有对应的signal处理, 其默认方式就是结束进程.
# 可以在ubuntu主机端查看详情:
$ man kill          # kill的帮助信息
$ kill -l           # 列出所有signal值, 其中:
10) SIGUSR1
```

## 异步机制核心点
- 异步机制使得应用层代码可以获得有如"中断"处理一般的能力!
    - 注册好signal和函数
    - 主代码始终自己管自己运行
    - signal触发后, 系统会自动调用注册好的函数.
- 异步通知的四个要点:
    - 注册处理函数: 应用程序中注册
    - 谁来发? 驱动来发
    - 发给谁? 驱动发给应用程序
    - 怎么发? 驱动调用 `kill_fasyn()`


# 驱动源码

驱动源码基于 [驱动之基于中断设计按键驱动](https://draapho.github.io/2017/12/07/1741-drv-chr3/) 
增加fasync函数, 发送SIGIO信号.
然后应用层的测试文件改动较大.


## drv_key_async.c

为了使设备支持异步通知机制, 驱动程序涉及以下3项工作:
- 应用程序调用 `fcntl(fd, F_SETOWN, pid)` 时. 能在这个控制命令处理中设置 filp->f_owner为对应进程ID. 此工作已由内核完成
- 应用程序调用 `fcntl(fd, F_SETFL, oflags | FASYNC)` 后, FASYNC标志改变, 会调用驱动的fasync函数. 驱动需要实现fasync. 
- 在设备资源可获得时, 调用 `kill_fasync()` 函数触发信号.


``` c
// 基于 驱动之基于中断设计按键驱动 源码增加而来. 只显示新增和修改的部分. 这样更直观易懂.

#include"drv_key_async.h"                           // 头文件改一下
#define DRV_KEY_INT_NODE_NAME "key_async"           // 名称改一下

static struct fasync_struct *keys_async;            // 新增, kill_fasync使用

static irqreturn_t keys_irq(int irq, void *dev_id)
{
    ......

    ev_press = 1;                              
    wake_up_interruptible(&key_waitq);     
    kill_fasync(&keys_async, SIGIO, POLL_IN);           // 新增, 发送SIGIO信号
    return IRQ_RETVAL(IRQ_HANDLED);
}

static int drv_key_fasync (int fd, struct file *filp, int on)
{
    PINFO("drv_key_fasync\n");
    return fasync_helper (fd, filp, on, &keys_async);   // 初始化keys_async
}

static const struct file_operations drv_key_int_fops= {
	.owner				= THIS_MODULE,
	.open				= drv_key_int_open,
	.release			= drv_key_int_release,
	.read				= drv_key_int_read,
	.fasync             = drv_key_fasync,               // 新增fasync
};
```

## drv_key_async.h

``` c
#define DRIVER_NAME "drv_key_async"     // 名称改一下
```

## Makefile

``` makefile
obj-m		:= drv_key_async.o          # 目标名称改一下
```


## 测试文件 test_drv_key_async.c

为了使设备支持异步通知机制, 应用层程序涉及以下工作:
- 调用 `fcntl(fd, F_SETOWN, getpid())`, 告诉内核, 发给谁 
- 调用 `fcntl(fd, F_SETFL, oflags | FASYNC)`, 改变fasync标记.
- 此时, 内核会调用驱动的fasync函数, 通过 `fasync_helper` 完成初始化.


``` c
#include <sys/types.h>  
#include <sys/stat.h>  
#include <fcntl.h>  
#include <stdio.h>
#include <signal.h>
#include <sys/types.h>
#include <unistd.h>

int fd;

void keys_signal_handler(int signum)        // 信号中断处理函数
{
    unsigned char key_val = 0;
    read(fd,&key_val,1);
    printf("key_val: 0x%x\n",key_val);
}

int main(int argc, char **argv)
{
    int ret;
    int oflags;
    
    fd = open("/dev/key_async0", O_RDWR);
    if (fd < 0) {
        printf("can't open!\n");
        return 0;
    }

    signal(SIGIO, keys_signal_handler);     // 注册信号中断处理函数
    fcntl(fd,F_SETOWN,getpid());            // 告诉内核，发给本进程
    oflags = fcntl(fd,F_GETFL);
    printf("before fcntl\n");
    fcntl(fd, F_SETFL, oflags | FASYNC);    // 改变fasync标记, 内核会调用驱动fasync, 完成初始化
    printf("after fcntl\n");
    
    while(1) {                              // 开始主任务
        sleep(1000);
    }
    return 0;
}
```


# 编译并测试

## Ubuntu主机端

``` bash
# 主机端, 编译源码
# pwd = /home/draapho/share/drv/drv_key_async/KERN_SRC   # 驱动源码路径, share是nfs共享文件夹

# 编译驱动
$ make clean
$ make modules                      # 也可以在LinK+里面直接编译, 更方便

# 编译测试代码
$ arm-linux-gcc test_drv_key_async.c -o test_drv_key_async
```

## 开发板端
``` bash
# 开发板端, 测试驱动功能
# pwd = /home/draapho/share/drv/drv_key_async/KERN_SRC  # 驱动源码路径, share是nfs共享文件夹

$ insmod drv_key_async.ko           # 加载模块
drv_key_async:INIT

$ ./test_drv_key_async              # 运行测试代码
drv_key_async:In char driver open() function
before fcntl
drv_key_async:drv_key_fasync        # 运行fcntl后, 驱动调用async函数
after fcntl

# 按下按键, 应用程序就会调用 keys_signal_handler 函数.
# 打印出按键信息, 譬如 key_val: 0x1

# 按ctrl+c 终止进程
```
