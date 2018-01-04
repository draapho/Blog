---
title: 驱动之基于中断设计按键驱动
date: 2017-12-07
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
- [驱动之定时器按键防抖](https://draapho.github.io/2018/01/04/1801-drv-chr7/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.

# Linux的中断实现

## 核心流程
- `trap_init`, 构造异常向量表
    - 位于 `arch/arm/kernel/traps.c`, 三个memcpy函数
- `s3c24xx_init_irq` 芯片初始化 `struct irq_desc` 结构体.
    - 由 `MACHINE_START(S3C2440, "SMDK2440")` 宏定义加入系统的初始化数据段 `".arch.info.init"`.
    - 位于 `arch/arm/plat-s3c24xx/irq.c`
    - `s3c24xx_init_irq` 会调用函数 `set_irq_chip`, `set_irq_handler` 完成irq的初始化
- cpu发生中断，跳到异常向量入口执行(`b vector_irq + stubs_offset`)
    - 位于 `arch/arm/kernel/entry-armv.S`
- `vector_irq` 用宏实现保存,执行(`asm_do_IRQ`),恢复.
    - `vector_irq` 由宏定义 `vector_stub` 而来
    - 函数调用 `__irq_usr`->`irq_handler`->`asm_do_IRQ`
- `asm_do_IRQ` 根据中断号irq=(EINT4~EINT23)调用irq_desc[irq].handle_irq=(handle_edge_irq)
    - 位于 `arch/arm/kernel/irq.c`, 调用 `desc_handle_irq` 函数
    - handle_irq 的初始化由 `s3c24xx_init_irq` 完成, 位于 `arch/arm/plat-s3c24xx/irq.c`
- `handle_edge_irq` 使用chip成员中的函数=&s3c_irqext_chip来设置硬件
    - 函数 `set_irq_chip`, 指定 `struct irq_chip` 结构,
    - 此结构定义了中断的基本操作, 譬如启动, 关闭, 使能, 禁止, 触发条件, 响应(ack), mask 等等.
- `handle_edge_irq` 逐个调用用户在irq_desc[irq].action连表中注册的处理函数
    - 函数 `set_irq_handler`, 实际调用 `__set_irq_handler`
    - 此函数指定了 `struct irq_desc` 结构, 其中 `action` 维护用户回调函数链表.
- 用户注册中断服务程序 `request_irq`include/linux/irq.h
    - 供内核驱动代码调用
    - 分配一个 `irqaction` 结构
    - 将其加入`irq_desc[irq].action`中
    - 设置中断触发方式和引脚状态 `desc->chip->set_type()`
    - 使能中断
- 卸载中断服务程序 `free_irq`
    - 供内核驱动代码调用
    - 由irq号定位action链表, 然后将其删掉
    - 关闭中断

## 更多资料
- [字符设备驱动-Linux内核异常处理体系结构](http://blog.csdn.net/czg13548930186/article/details/77715829)
- [字符设备驱动-中断方式操控按键](http://blog.csdn.net/czg13548930186/article/details/77751916)
- [Linux kernel的中断子系统之（六）：ARM中断处理过程](http://www.wowotech.net/irq_subsystem/irq_handler.html)


# 驱动源码

## 核心点
此次为中断的驱动源码, 核心点有2个地方
- `request_irq` `free_irq`
    - 这两个函数用于注册和释放中断号, 重点说注册
    - 调用`request_irq`后, 对应的中断会自动初始化并使能.
    - 相应的调用`free_irq`后, 对应的中断会自动被屏蔽掉.
    - `irq`, 中断号. 见`#include <asm/arch-s3c2410/irqs.h>`
    - `handler`, 由驱动编程人员实现的回调函数
    - `irqflags`, 中断触发类型, 见`#include <asm/arch-s3c2410/irqs.h>`
    - `*devname`, 自己给中断取个名字, 和驱动的设备名称无关. 会在 `cat /proc/interrupts` 下面显示出来.
    - `*dev_id`, 可以认为是中断设备的ID号, 但此处习惯于导入驱动自用的数据结构指针.
- `wake_up_interruptible` `wait_event_interruptible`
    - 用了这两个函数, 才会真正提高系统的运行效率.
    - 其概念是, 中断触发时, 调用 `wake_up_interruptible`, 告知中断发生, 需要处理
    - 此时, `wait_event_interruptible` 就会被唤醒, 判断条件后, 决定是继续执行还是进程睡眠.


## drv_key_int.c

``` c
/*
===============================================================================
Driver Name     :       drv_key_int
Author          :       DRAAPHO
License         :       GPL
Description     :       LINUX DEVICE DRIVER PROJECT, 由LinK+生成模板, 部分修改而来.
===============================================================================
*/

#include"drv_key_int.h"

#define DRV_KEY_INT_N_MINORS 1              // 三个按键, 但作为一个字符设备就可以了.
#define DRV_KEY_INT_FIRST_MINOR 0
#define DRV_KEY_INT_NODE_NAME "key_int"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

int drv_key_int_major=0;

dev_t drv_key_int_device_num;

struct class *drv_key_int_class;

typedef struct privatedata {                // 驱动私有结构, 模板生成, 此驱动没用.
    int nMinor;
    struct cdev cdev;
    struct device *drv_key_int_device;
} drv_key_int_private;

drv_key_int_private devices[DRV_KEY_INT_N_MINORS];


// ===== 中断驱动增加的代码 =====
static DECLARE_WAIT_QUEUE_HEAD(key_waitq);  // 作用类似于信号量, 这里是向系统加入一个等待列表.
static volatile int ev_press = 0;           // 中断事件标记, 手动值1或者清0
static unsigned char keys_val;              // 记录按键值

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
    struct pin_desc * pindesc = (struct pin_desc *)dev_id;  // 获取自用的数据指针
    unsigned int pinval;

    PINFO("keys_irq, irq=%d\n", irq);
    pinval = s3c2410_gpio_getpin(pindesc->pin);             // 读取按键电平

    if (pinval) {                                           // 松开
        keys_val &= ~pindesc->key_val;
    } else {                                                // 按下
        keys_val |= pindesc->key_val;
    }

    ev_press = 1;                                           // 表示中断发生
    wake_up_interruptible(&key_waitq);                      // 唤醒休眠的进程
    return IRQ_RETVAL(IRQ_HANDLED);
}

// ===== 部分修改模板代码 =====
static int drv_key_int_open(struct inode *inode,struct file *filp)
{
    int ret;
    /* TODO Auto-generated Function */
    drv_key_int_private *priv = container_of(inode->i_cdev ,
                                    drv_key_int_private ,cdev);
    filp->private_data = priv;
    PINFO("In char driver open() function\n");

    // 注册中断号, 设置中断类型, 设置中断名称(和设备名称无关), 传入自用的数据指针
    ret  = request_irq(IRQ_EINT0, keys_irq, IRQT_BOTHEDGE, "S2", &pins_desc[0]);
    ret |= request_irq(IRQ_EINT2, keys_irq, IRQT_BOTHEDGE, "S3", &pins_desc[1]);
    ret |= request_irq(IRQ_EINT11, keys_irq, IRQT_BOTHEDGE, "S4", &pins_desc[2]);

    if (ret) return -EINVAL;
    else return 0;
}

static int drv_key_int_release(struct inode *inode,struct file *filp)
{
    /* TODO Auto-generated Function */
    drv_key_int_private *priv;
    priv=filp->private_data;
    PINFO("In char driver release() function\n");

    free_irq(IRQ_EINT11, &pins_desc[2]);                    // 注销中断
    free_irq(IRQ_EINT2, &pins_desc[1]);
    free_irq(IRQ_EINT0, &pins_desc[0]);
    return 0;
}

static ssize_t drv_key_int_read(struct file *filp,
    char __user *ubuff,size_t count,loff_t *offp)
{
    /* TODO Auto-generated Function */
    drv_key_int_private *priv;
    priv = filp->private_data;
    PINFO("In char driver read() function\n");

    if (count != 1)
        return -EINVAL;

    // ev_press, 用于判断是否可以让当前进程睡眠(让出CPU, 进程切换)
    wait_event_interruptible(key_waitq, ev_press);
    ev_press = 0;                                           // 运行后, 立刻清零

    if (copy_to_user(ubuff, &keys_val, 1)) {                // 传回按键值
        return -EFAULT;
    }
    return 1;
}

// ===== 模板代码, 没有修改 =====
static const struct file_operations drv_key_int_fops= {
    .owner              = THIS_MODULE,
    .open               = drv_key_int_open,
    .release            = drv_key_int_release,
    .read               = drv_key_int_read,
};

static int __init drv_key_int_init(void)
{
    /* TODO Auto-generated Function Stub */
    int i;
    int res;

    res = alloc_chrdev_region(&drv_key_int_device_num,DRV_KEY_INT_FIRST_MINOR,DRV_KEY_INT_N_MINORS ,DRIVER_NAME);
    if(res) {
        PERR("register device no failed\n");
        return -1;
    }
    drv_key_int_major = MAJOR(drv_key_int_device_num);

    drv_key_int_class = class_create(THIS_MODULE , DRIVER_NAME);
    if(!drv_key_int_class) {
        PERR("class creation failed\n");
        return -1;
    }

    for(i=0;i<DRV_KEY_INT_N_MINORS;i++) {
        drv_key_int_device_num= MKDEV(drv_key_int_major ,DRV_KEY_INT_FIRST_MINOR+i);
        cdev_init(&devices[i].cdev , &drv_key_int_fops);
        cdev_add(&devices[i].cdev,drv_key_int_device_num,1);

        devices[i].drv_key_int_device  =
                device_create(drv_key_int_class , NULL ,drv_key_int_device_num ,
                            DRV_KEY_INT_NODE_NAME"%d",DRV_KEY_INT_FIRST_MINOR+i);
        if(!devices[i].drv_key_int_device) {
            class_destroy(drv_key_int_class);
            PERR("device creation failed\n");
            return -1;
        }

        devices[i].nMinor = DRV_KEY_INT_FIRST_MINOR+i;
    }

    PINFO("INIT\n");

    return 0;
}

static void __exit drv_key_int_exit(void)
{
    /* TODO Auto-generated Function Stub */

    int i;

    PINFO("EXIT\n");

    for(i=0;i<DRV_KEY_INT_N_MINORS;i++) {
        drv_key_int_device_num= MKDEV(drv_key_int_major ,DRV_KEY_INT_FIRST_MINOR+i);

        cdev_del(&devices[i].cdev);

        device_destroy(drv_key_int_class ,drv_key_int_device_num);

    }

    class_destroy(drv_key_int_class);

    unregister_chrdev_region(drv_key_int_device_num ,DRV_KEY_INT_N_MINORS);

}

module_init(drv_key_int_init);
module_exit(drv_key_int_exit);
```

## drv_key_int.h

``` c
#define DRIVER_NAME "drv_key_int"
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
#include <asm/irq.h>
#include <asm/arch-s3c2410/irqs.h>
#include <asm/uaccess.h>
#include <asm/io.h>
#include <asm/arch/regs-gpio.h>
#include <asm/hardware.h>
```

## Makefile

``` makefile
obj-m		:= drv_key_int.o 
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

int main(int argc, char **argv)
{
    int fd;
    unsigned char keys_val;

    fd = open("/dev/key_int0", O_RDWR);
    if (fd < 0) {
        printf("can't open!\n");
        return 0;
    }

    while (1) {
        read(fd, &keys_val, 1);
        printf("keys_val = 0x%x\n", keys_val);
    }

    return 0;
}
```


# 编译并测试

## Ubuntu主机端

``` bash
# 主机端, 编译源码
# pwd = /home/draapho/share/drv/drv_key_int/KERN_SRC    # 驱动源码路径, share是nfs共享文件夹

# 编译驱动
$ make clean
$ make modules                      # 也可以在LinK+里面直接编译, 更方便

# 编译测试代码
$ arm-linux-gcc test_drv_key_int.c -o test_drv_key_int
```

## 开发板端

``` bash
# 开发板端, 测试模块和中断加载情况
# pwd = /home/draapho/share/drv/drv_key_int/KERN_SRC    # 驱动源码路径, share是nfs共享文件夹

$ insmod drv_key_int.ko             # 加载模块
drv_key_int:INIT

$ cat /proc/devices                 # 查看设备, 可以看到 drv_key_int
$ cat /proc/interrupts              # 查看中断设备, 没有 s2,s3,s4

$ exec 5</dev/key_int0              # 打开设备, 相当于open.
drv_key_int:In char driver open() function
# 5是文件描述符, 其它数字也可以. ls -l /proc/self/fd/ 下可以查看文件描述符

$ cat /proc/interrupts              # 再查看中断设备, 可以看到 s2,s3,s4 了!
# 此时按下按键的话, 会触发中断, 打印 drv_key_int:keys_irq, irq=16/18/55

$ exec 5<&-                         # 关闭设备, 相当于close
drv_key_int:In char driver release() function

$ rmmod drv_key_int.ko              # 移除模块
drv_key_int:EXIT
```

下面, 使用测试文件进行测试

``` bash
# 开发板端, 测试驱动功能
# pwd = /home/draapho/share/drv/drv_key_int/KERN_SRC    # 驱动源码路径, share是nfs共享文件夹

$ insmod drv_key_int.ko             # 加载模块
drv_key_int:INIT

$ ./test_drv_key_int                # 检测按键中断
# 可以发现, 打印有时候有点乱, 那是因为中断的关系

# 按ctrl+c 终止进程

$ ./test_drv_key_int &              # 后台运行
$ top                               # 查看系统资源情况
# 可以看到 ./test_drv_key_int 进程占用很少的资源.
```

分析测试代码, 在死循环里面, 会调用到 `wait_event_interruptible`, 当没有中断发生时, 就会切换用户进程.
当中断发生后, 驱动通过 `wake_up_interruptible` 唤醒用户进程, 继续执行.
然后由于, 用户的printf和内核的printk相互独立, 所以最终打印可能会有点乱.

