---
title: 驱动之定时器按键防抖
date: 2018-01-04
categories: embedded linux
tags: [linuxembedded linux, drv]
description: 如题.
---



# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之字符设备-框架](https://draapho.github.io/2017/11/22/1733-drv-chr1/)
- [驱动之基于LinK+设计按键驱动](https://draapho.github.io/2017/11/30/1740-drv-chr2/)
- [驱动之基于中断设计按键驱动](https://draapho.github.io/2017/12/07/1741-drv-chr3/)
- [驱动之poll机制](https://draapho.github.io/2017/12/11/1742-drv-chr4/)
- [驱动之异步通知](https://draapho.github.io/2017/12/12/1743-drv-chr5/)
- [驱动之同步互斥阻塞](https://draapho.github.io/2017/12/13/1744-drv-chr6/)
- [驱动之同步互斥阻塞](https://draapho.github.io/2017/12/13/1744-drv-chr6/)
- [驱动之定时器按键防抖](https://draapho.github.io/2018/01/04/1801-drv-chr7/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.
硬件具备唯一性, 因此某一时刻应该只有一个应用程序能对驱动进行操作.


# 定时器

## 基本用法
定时器的用法一般分为如下步骤:
1. 声明一个 timer
    - `struct timer_list newTimer`
2. 声明并初始化 timer
    - 方法一: `DEFINE_TIMER(newTimer, timer_function, expires, data);`
    - 方法二: `setup_timer(&newTimer, timer_function, data)`
    - 方法三: `init_timer(&newTimer)`
    - timer_function 就是定时器的中断服务函数
3. 完善定时中断服务函数
    - 要周期性调用定时器, 使用 `mod_timer(&newTimer, jiffies+interval)` 重新注册
    - 此部分代码特别注意锁的问题!
4. 注册 timer 到定时器链表
    - 相当于启动定时器, 可用 `add_timer(&newTimer)`
    - 实际上 `add_timer` 并非必须调用, 直接使用`mod_timer`也没问题.
    - `mod_timer` 等效于 `del_timer(); set expires; add_timer();`
5. 重新注册 timer
    - 定时器配在置好后只运行一次，执行完中断服务函数后定时器就会自动销毁!
    - 想要实现周期性定时中断就必须在中断服务程序的结尾重新给定时器写入超时值
    - 使用 `mod_timer(&newTimer, jiffies+interval)` 重新注册
6. 提前停止定时器 timer （非必需步骤）
    - 定时器计时结束后, 系统会自动销毁相关定时器.
    - `del_timer(&newTimer)`
    - `del_timer_sync(&newTimer)`, 用于多核CPU. 单核的话等同于 `del_timer`
7. 其它相关概念
    - `jiffies` 是linux系统启动后芯片时钟的节拍总数
    - `HZ` 每秒经过的jiffies数. 其值就是系统时钟的频率
    - `jiffies/HZ` 就是当前系统运行了多少秒
    - 64位系统中, jiffies 只访问到低32位值, 需要使用 `get_jiffies_64()` 才能获取完整的64位数值.


## 参考资料
- [内核sem、wait_queue_head_t、timer和kernel_thread使用驱动范例](http://blog.csdn.net/armeasy/article/details/6027709) 内核线程和定时器的用法
- [Linux内核 定时器 用法](http://blog.csdn.net/qidi_huang/article/details/51318157)
- [Linux设备驱动——内核定时器](http://www.cnblogs.com/chen-farsight/p/6226562.html)
- [Linux内核中的计时器和列表](https://www.ibm.com/developerworks/cn/linux/l-timers-list/index.html)


# 驱动源码

此驱动源码是韦东山教程里按键的最终版本. 驱动有如下特性:
- 按键使用了中断
- 多线程/进程安全, 硬件使用了互斥量.
- 支持应用层阻塞或者非阻塞访问
- 支持poll机制. 应用层可以使用poll
- 支持异步机制. 应用层可以用信号中断来处理按键事件

但对我个人而言, 这一版本的按键依旧不够好, 有机会自己写一版按键驱动
- 按键状态反馈过于简单, 没有提供诸如短按, 长按, 连发, 释放的按键信息.
- 经典的按键范例是状态机模型, 用定时器定时扫描按键状态, 可以不用硬件中断.
- 没有实现对单个按键的open/closse操作.


## drv_keys.c

``` c
===============================================================================
Driver Name     :       drv_keys
Author          :       DRAAPHO
License         :       GPL
Description     :       LINUX DEVICE DRIVER PROJECT
===============================================================================
*/

#include"drv_keys.h"

#define DRV_KEYS_N_MINORS 1                 // 子设备号, 可用于区别按键.
#define DRV_KEYS_FIRST_MINOR 0
#define DRV_KEYS_NODE_NAME "key"
#define DRV_KEYS_BUFF_SIZE 1024

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

int drv_keys_major=0;
dev_t drv_keys_device_num;
struct class *drv_keys_class;
struct fasync_struct *keys_async;            // 新增, kill_fasync使用
static DECLARE_MUTEX(keys_lock);             // 定义互斥锁

typedef struct privatedata {
    int nMinor;
    struct cdev cdev;
    struct device *drv_keys_device;
} drv_keys_private;

drv_keys_private devices[DRV_KEYS_N_MINORS];

// ===== 中断和定时器增加的代码 =====
static DECLARE_WAIT_QUEUE_HEAD(key_waitq);  // 作用类似于信号量, 这里是向系统加入一个等待列表.
static volatile int ev_press = 0;           // 中断事件标记, 手动值1或者清0
static unsigned char keys_val;              // 记录按键值
struct pin_desc * pindesc;                  // 用于保存中断内的数据指针, 给超时函数使用
struct timer_list keys_timer;               // 定时器

struct pin_desc {
    unsigned int pin;
    unsigned int key_val;
};

struct pin_desc pins_desc[3] = {            // 设置好按键的引脚和对应的值
    {S3C2410_GPF0, 0x01},
    {S3C2410_GPF2, 0x02},
    {S3C2410_GPG3, 0x04},
};

static irqreturn_t keys_irq(int irq, void *dev_id)
{
    PINFO("keys_irq, irq=%d\n", irq);
    pindesc = (struct pin_desc *)dev_id;    // 获取自用的数据指针
    mod_timer(&keys_timer, jiffies+HZ/100); // 每次产生中断, 都等待10ms, 避开按键抖动
    return IRQ_RETVAL(IRQ_HANDLED);
}

static void keys_wait_10ms(unsigned long data) {            // 中断发生10ms后, 在读取电平值
    unsigned int pinval;

    if (!pindesc)
        return;

    pinval = s3c2410_gpio_getpin(pindesc->pin);             // 读取按键电平
    if (pinval) {                                           // 松开
        keys_val &= ~pindesc->key_val;
    } else {                                                // 按下
        keys_val |= pindesc->key_val;
    }

    ev_press = 1;                                           // 表示中断发生
    wake_up_interruptible(&key_waitq);                      // 唤醒休眠的进程
    kill_fasync(&keys_async, SIGIO, POLL_IN);               // 发送SIGIO信号
}

// ===== 部分修改模板代码 =====
static int drv_keys_open(struct inode *inode,struct file *filp)
{
    if (filp->f_flags & O_NONBLOCK) {               // 非阻塞
        if (down_trylock(&keys_lock))               // 尝试获取信号量
            return -EBUSY;
    } else {
        down(&keys_lock);                           // 获取信号量, 阻塞
    }

    int ret;
    drv_keys_private *priv = container_of(inode->i_cdev ,
            drv_keys_private ,cdev);
    filp->private_data = priv;
    PINFO("drv_keys_open\n");

    // 注册中断号, 设置中断类型, 设置中断名称(和设备名称无关), 传入自用的数据指针
    ret  = request_irq(IRQ_EINT0, keys_irq, IRQT_BOTHEDGE, "S2", &pins_desc[0]);
    ret |= request_irq(IRQ_EINT2, keys_irq, IRQT_BOTHEDGE, "S3", &pins_desc[1]);
    ret |= request_irq(IRQ_EINT11, keys_irq, IRQT_BOTHEDGE, "S4", &pins_desc[2]);

    // 定时器初始化.
    setup_timer(&keys_timer, keys_wait_10ms, 0);
    add_timer(&keys_timer);

    if (ret) return -EINVAL;
    else return 0;
}

static int drv_keys_release(struct inode *inode,struct file *filp)
{
    drv_keys_private *priv;
    priv=filp->private_data;
    PINFO("drv_keys_release\n");

    del_timer_sync(&keys_timer);                    // 删除定时器
    free_irq(IRQ_EINT11, &pins_desc[2]);            // 注销中断
    free_irq(IRQ_EINT2, &pins_desc[1]);
    free_irq(IRQ_EINT0, &pins_desc[0]);

    up(&keys_lock);                                 // 释放信号量
    return 0;
}

static ssize_t drv_keys_read(struct file *filp,
    char __user *ubuff,size_t count,loff_t *offp)
{
    drv_keys_private *priv;
    priv = filp->private_data;
    PINFO("drv_keys_read()\n");

    if (count != 1)
        return -EINVAL;

    if (filp->f_flags & O_NONBLOCK) {               // 非阻塞
        if (!ev_press)                              // 无按键, 立刻返回
            return -EAGAIN;
    } else {
        // ev_press, 用于判断是否可以让当前进程睡眠(让出CPU, 进程切换)
        wait_event_interruptible(key_waitq, ev_press);      // 阻塞
    }

    ev_press = 0;                                           // 运行后, 立刻清零
    if (copy_to_user(ubuff, &keys_val, 1)) {                // 传回按键值
        return -EFAULT;
    }
    return 1;
}

static unsigned drv_keys_poll(struct file *file, poll_table *wait)
{
    unsigned int mask = 0;
    poll_wait(file, &key_waitq, wait);      // 这里不会休眠. 进程不阻塞

    if (ev_press)
        mask |= POLLIN | POLLRDNORM;        // 关键是返回值, 返回值为0, 进程可能休眠.
        // POLLIN, 是标准的事件值, 测试程序就基于此判断.
        // POLLRDNORM, Normal data may be read without blocking. 作用应该是告知应用程序类型和后续动作.

    return mask;
}

static int drv_keys_fasync (int fd, struct file *filp, int on)
{
    PINFO("drv_key_fasync\n");
    return fasync_helper (fd, filp, on, &keys_async);       // 初始化keys_async
}

// ===== 模板代码, 没有修改 =====
static const struct file_operations drv_keys_fops= {
    .owner              = THIS_MODULE,
    .open               = drv_keys_open,
    .release            = drv_keys_release,
    .read               = drv_keys_read,
    .poll               = drv_keys_poll,
    .fasync             = drv_keys_fasync,
};

static int __init drv_keys_init(void)
{
    /* TODO Auto-generated Function Stub */

    int i;
    int res;

    res = alloc_chrdev_region(&drv_keys_device_num,DRV_KEYS_FIRST_MINOR,DRV_KEYS_N_MINORS ,DRIVER_NAME);
    if(res) {
        PERR("register device no failed\n");
        return -1;
    }
    drv_keys_major = MAJOR(drv_keys_device_num);

    drv_keys_class = class_create(THIS_MODULE , DRIVER_NAME);
    if(!drv_keys_class) {
        PERR("class creation failed\n");
        return -1;
    }

    for(i=0;i<DRV_KEYS_N_MINORS;i++) {
        drv_keys_device_num= MKDEV(drv_keys_major ,DRV_KEYS_FIRST_MINOR+i);
        cdev_init(&devices[i].cdev , &drv_keys_fops);
        cdev_add(&devices[i].cdev,drv_keys_device_num,1);

        devices[i].drv_keys_device  =
                device_create(drv_keys_class , NULL ,drv_keys_device_num ,
                            // NULL ,DRV_KEYS_NODE_NAME"%d",DRV_KEYS_FIRST_MINOR+i);    // for higher kernel version
                            DRV_KEYS_NODE_NAME"%d",DRV_KEYS_FIRST_MINOR+i);             // for 2.6 kernel version
        if(!devices[i].drv_keys_device) {
            class_destroy(drv_keys_class);
            PERR("device creation failed\n");
            return -1;
        }

        devices[i].nMinor = DRV_KEYS_FIRST_MINOR+i;
    }

    PINFO("INIT\n");

    return 0;
}

static void __exit drv_keys_exit(void)
{
    /* TODO Auto-generated Function Stub */

    int i;

    PINFO("EXIT\n");

    for(i=0;i<DRV_KEYS_N_MINORS;i++) {
        drv_keys_device_num= MKDEV(drv_keys_major ,DRV_KEYS_FIRST_MINOR+i);

        cdev_del(&devices[i].cdev);

        device_destroy(drv_keys_class ,drv_keys_device_num);

    }

    class_destroy(drv_keys_class);

    unregister_chrdev_region(drv_keys_device_num ,DRV_KEYS_N_MINORS);

}

module_init(drv_keys_init);
module_exit(drv_keys_exit);
```


## drv_keys.h

``` c
#define DRIVER_NAME "drv_keys"
#define PDEBUG(fmt,args...) printk(KERN_DEBUG"%s:"fmt,DRIVER_NAME, ##args)
#define PERR(fmt,args...) printk(KERN_ERR"%s:"fmt,DRIVER_NAME,##args)
#define PINFO(fmt,args...) printk(KERN_INFO"%s:"fmt,DRIVER_NAME, ##args)
#include<linux/cdev.h>
#include<linux/device.h>
#include<linux/fs.h>
#include<linux/init.h>
#include<linux/kdev_t.h>
#include<linux/module.h>
#include<linux/poll.h>
#include<linux/types.h>
#include<linux/uaccess.h>

#include <linux/interrupt.h>
#include <linux/irq.h>
#include <asm/irq.h>
#include <asm/arch-s3c2410/irqs.h>
#include <asm/uaccess.h>
#include <asm/io.h>
#include <asm/arch/regs-gpio.h>
#include <asm/hardware.h>
```

## Makefile

这里我修改了一下, 把测试文件的编译也放进了这个文件.
用 `make test` 就能编译测试文件.

``` makefile
TEST_FILE   := drv_keys_test

obj-m       := drv_keys.o
KERN_SRC    := /home/draapho/share/jz2440/kernel/linux-2.6.22.6/
PWD         := $(shell pwd)

modules:
    make -C $(KERN_SRC) M=$(PWD) modules

clean:
    make -C $(KERN_SRC) M=$(PWD) clean
    rm -f $(TEST_FILE)

test:
    arm-linux-gcc $(TEST_FILE).c -o $(TEST_FILE)
```


## drv_keys_test.c

``` c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <signal.h>
#include <sys/types.h>
#include <unistd.h>

int fd;

// void keys_signal_handler(int signum)         // 信号中断处理函数
// {
    // unsigned char key_val = 0;
    // read(fd,&key_val,1);
    // printf("key_val: 0x%x\n",key_val);
// }

int main(int argc, char **argv)
{
    int ret;
    int oflags;                                 // 用于异步通知的设置
    struct pollfd fds[1];                       // poll 关联的文件, 可多个文件
    unsigned char key_val = 0;

    fd = open("/dev/key0", O_RDWR);
    // fd = open("/dev/key0", O_RDWR | O_NONBLOCK); // 非阻塞
    if (fd < 0) {
        printf("can't open!\n");
        return -1;
    }

    // ===== 使用异步通知 =====
    // signal(SIGIO, keys_signal_handler);      // 注册信号中断处理函数
    // fcntl(fd,F_SETOWN,getpid());             // 告诉内核，发给本进程
    // oflags = fcntl(fd,F_GETFL);
    // fcntl(fd, F_SETFL, oflags | FASYNC);     // 改变fasync标记, 内核会调用驱动fasync, 完成初始化

    // ===== POLL轮询 =====
    // fds[0].fd     = fd;                      // 关联的驱动文件
    // fds[0].events = POLLIN;                  // 事件类型
    // while (1) {
        // ret = poll(fds, 1, 5000);            // 执行poll. 最多阻塞5s (有按键事件会立刻返回)
        // if (ret == 0) {
        //     printf("time out\n");            // 5s后超时
        // } else {
        //     read(fd, &keys_val, 1);          // 有按键, 读取按键值
        //     printf("keys_val = 0x%x\n", keys_val);
        // }
    // }

    // ===== 阻塞查询 =====
    while(1) {                                  // 开始主任务
        ret = read(fd,&key_val,1);
        printf("key_val: 0x%x, ret = %d\n", key_val, ret);
    }
    return 0;
}
```

# 编译和测试

## Ubuntu主机端

``` bash
# 主机端, 编译源码
# pwd = /home/draapho/share/drv/drv_key_poll/KERN_SRC   # 驱动源码路径, share是nfs共享文件夹

# 编译驱动
$ make clean
$ make modules                  # 编译驱动
$ make test                     # 编译测试代码
```

## 开发板端

``` bash
# 开发板端, 测试驱动功能
# pwd = /home/draapho/share/drv/drv_key_poll/KERN_SRC   # 驱动源码路径, share是nfs共享文件夹

$ insmod drv_keys.ko            # 加载模块
$ ./drv_keys_test               # 检测按键中断
# 按键测试...
# 按ctrl+c 终止进程

$ ./drv_keys_test &             # 后台运行, 会运行
$ ./drv_keys_test &             # 后台运行, 进程被挂起, 因为资源被锁.
$ top                           # 查看进程情况
$ kill 789                      # 杀死第一个进程
# 第二个进程就能获得资源, 开始运行
$ kill 790                      # 杀死第二个进程
$ rmmod drv_keys.ko             # 卸载模块
```