---
title: 驱动之platform概念
date: 2018-01-08
categories: embedded linux
tags: [linuxembedded linux, drv]
---



# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之input子系统](https://draapho.github.io/2018/01/05/1802-drv-input/)
- [驱动之platform概念](https://draapho.github.io/2018/01/08/1803-drv-platform/)
- [驱动之LCD驱动框架和实现](https://draapho.github.io/2018/01/09/1804-drv-lcd/)
- [驱动之触摸屏驱动框架和实现](https://draapho.github.io/2018/01/11/1806-drv-ts/)
- [驱动之USB基础概念和框架](https://draapho.github.io/2018/01/18/1807-drv-usb1/)
- [驱动之USB设备驱动程序](https://draapho.github.io/2018/01/19/1808-drv-usb2/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.


# platform概念

![bus.png](https://draapho.github.io/images/1803/bus.png)

platform 的主要作用是给开发人员搭好了框架.
便于将底层驱动的通用部分放在 `driver` 端实现, 而硬件高度相关部分放在 `device` 端实现.
由于只是架构, 因此这里 `driver` 和 `device` 两个部分都是自己写代码实现的, platform自动完成匹配.

这种架构特别适用于总线设备! 将总线设备的共性提炼成 driver 文件.
而正对支持总线的不同硬件, 分别单独写 device 即可.
因此一般情况下, platform的driver对应多个device.
linux基于platform的概念, 已经帮我们实现了常用总线的driver如: I2C, SPI, USB等


要更细致的了解linux platform 分离分层的概念, 建议参考如下博文:
- [linux内核中的GPIO系统之（1）：软件框架](http://www.wowotech.net/gpio_subsystem/io-port-control.html)
- [Linux设备模型(8)_platform设备](http://www.wowotech.net/linux_kenrel/platform_device.html)


# 源码
LinK+软件也支持配置platform设备, 但是生成的源码放在了同一个文件, 不便于理解.
为了便于理解, 采用点led来说明platform概念. 为保持代码简介, 忽略错误判断, 不支持多个device.
实际开发中, 自己用到platform的机会不多, 因为linux已经将常用的总线写好了.


## led_driver.c (硬件通用代码)

``` c
#include"led_platform.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

int led_major=0;
struct class *led_class=NULL;

volatile unsigned long *gpio_con;
volatile unsigned long *gpio_dat;
int pin;

// ===== led driver 通用文件操作 =====
static int led_driver_open(struct inode *inode, struct file *file)
{
    PINFO("led_driver_open\n");
    *gpio_con &= ~(0x3<<(pin*2));       // 配置为输出
    *gpio_con |= (0x1<<(pin*2));
    return 0;
}
static ssize_t led_driver_write(struct file *file, const char __user *buf, size_t count, loff_t * ppos)
{
    int val;
    PINFO("led_driver_write\n");
    copy_from_user(&val, buf, count);
    if (val == 1)
        *gpio_dat &= ~(1<<pin);         // 点灯
    else
        *gpio_dat |= (1<<pin);          // 灭灯
    return 0;
}

static int led_driver_release (struct inode *inode, struct file *file)
{
    PINFO("led_driver_release\n");
    return 0;
}

static const struct file_operations led_fops= {
    .owner              = THIS_MODULE,
    .open               = led_driver_open,
    .write              = led_driver_write,
    .release            = led_driver_release,
};


// ===== platform 框架使用的函数 =====
static int led_driver_probe(struct platform_device *pdev)
{
    struct resource *resource;
    PINFO("led_driver_probe\n");

    // 根据platform_device的资源进行ioremap
    resource = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    gpio_con = ioremap(resource->start, resource->end - resource->start + 1);
    gpio_dat = gpio_con + 1;

    resource = platform_get_resource(pdev, IORESOURCE_IRQ, 0);
    pin = resource->start;              // 这里只是借用IRQ获取PIN值

    return 0;
}

static int led_driver_remove(struct platform_device *pdev)
{
    iounmap(gpio_con);
    PINFO("led_platform_remove\n");
    return 0;
}

struct platform_driver led_driver = {
        .driver = {
            .name   = DRIVER_NAME,
            .owner  = THIS_MODULE,
        },
        .probe      = led_driver_probe,
        .remove     = led_driver_remove,
};

static int __init led_driver_init(void)
{
    PINFO("led_driver_init\n");

    // 注册字符设备驱动程序.
    // 由于driver和device可以是一对多的关系. 因此注册工作不能放在probe里, 否则会被注册多次.
    led_major = register_chrdev(0, DRIVER_NAME, &led_fops);
    led_class = class_create(THIS_MODULE, DRIVER_NAME);
    class_device_create(led_class, NULL, MKDEV(led_major, 0), NULL, "led"); // /dev/led

    // 注册platform的driver
    platform_driver_register(&led_driver);
    return 0;
}

static void __exit led_driver_exit(void)
{
    // 注销platform的driver
    platform_driver_unregister(&led_driver);

    // 卸载字符设备驱动程序
    class_device_destroy(led_class, MKDEV(led_major, 0));
    class_destroy(led_class);
    unregister_chrdev(led_major, DRIVER_NAME);
    PINFO("led_platform_exit\n");
}

module_init(led_driver_init);
module_exit(led_driver_exit);
```

## led_device.c (硬件专用代码)
``` c
#include"led_platform.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

struct resource led_devs_res1[] = {         // 硬件专用资源信息
    {
        .start  = 0x56000050,
        .end    = 0x56000050 + 8 - 1,
        .flags  = IORESOURCE_MEM,
    },
    {
        .start  = 5,                        // 借用IRQ表示PIN引脚
        .flags  = IORESOURCE_IRQ,
    },
};

static void led_dev_release(struct device * dev)
{
    PINFO("led_dev_release\n");
}

struct platform_device led_devs1 = {
    .name           = DRIVER_NAME,
    .resource       = led_devs_res1,
    .num_resources  = ARRAY_SIZE(led_devs_res1),
    .id             = 0,
    .dev = {
        .release = led_dev_release,         // 必须实现, 否则报错
    },
};

static int led_dev_init(void)
{
    PINFO("led_dev_init\n");
    // 注册device
    platform_device_register(&led_devs1);
    return 0;
}

static void led_dev_exit(void)
{
    // 注销device
    platform_device_unregister(&led_devs1);
    PINFO("led_dev_exit\n");
}

module_init(led_dev_init);
module_exit(led_dev_exit);
```

## led_platform.h

``` c
#define DRIVER_NAME "led_platform"
#define PDEBUG(fmt,args...) printk(KERN_DEBUG"%s:"fmt,DRIVER_NAME, ##args)
#define PERR(fmt,args...) printk(KERN_ERR"%s:"fmt,DRIVER_NAME,##args)
#define PINFO(fmt,args...) printk(KERN_INFO"%s:"fmt,DRIVER_NAME, ##args)
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/interrupt.h>
#include <linux/platform_device.h>
#include <linux/slab.h>
#include<linux/cdev.h>
#include<linux/device.h>
#include<linux/fs.h>
#include<linux/init.h>
#include<linux/interrupt.h>
#include<linux/kdev_t.h>
#include<linux/module.h>
#include<linux/types.h>
#include<linux/uaccess.h>

#include <asm/uaccess.h>
#include <asm/io.h>
```

## led_test.c

``` c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>

/* led_test on
 * led_test off
 */
int main(int argc, char **argv)
{
    int fd;
    int val = 1;
    fd = open("/dev/led", O_RDWR);
    if (fd < 0) {
        printf("can't open!\n");
    }
    if (argc != 2) {
        printf("Usage :\n");
        printf("%s <on|off>\n", argv[0]);
        return 0;
    }

    if (strcmp(argv[1], "on") == 0) {
        val  = 1;
    } else {
        val = 0;
    }

    write(fd, &val, 4);
    return 0;
}
```

## Makefile

``` makefile
TEST_FILE   := led_test
obj-m       += led_driver.o
obj-m       += led_device.o
KERN_SRC    := /home/draapho/share/jz2440/kernel/linux-2.6.22.6/
PWD         := $(shell pwd)

modules:
    make -C $(KERN_SRC) M=$(PWD) modules

install:
    make -C $(KERN_SRC) M=$(PWD) modules_install
    depmod -a

clean:
    make -C $(KERN_SRC) M=$(PWD) clean
    rm -f $(TEST_FILE)

test:
    arm-linux-gcc $(TEST_FILE).c -o $(TEST_FILE)
```

## 测试

``` bash
# Ubuntu主机端, 编译所有源码
$ make clean
$ make modules
$ make test

# 开发板端
$ insmod led_driver.ko              # driver和device的调用顺序不重要
led_platform:led_driver_init
$ insmod led_device.ko
led_platform:led_dev_init
led_platform:led_driver_probe       # platform 在匹配driver和device后, 调用probe
$ ./led_test on
led_platform:led_driver_open        # open
led_platform:led_driver_write       # write
led_platform:led_driver_release     # close
$ ./led_test off
led_platform:led_driver_open
led_platform:led_driver_write
led_platform:led_driver_release
$ rmmod led_device.ko
led_platform:led_platform_remove    # 解绑后, 自动调用remove
led_platform:led_dev_release
led_platform:led_dev_exit
$ rmmod led_driver.ko
led_platform:led_platform_exit
```

# 参考资料
- [linux驱动之分离分层的概念](http://blog.csdn.net/tianzhihen_wq/article/details/42176467)
- [linux内核中的GPIO系统之（1）：软件框架](http://www.wowotech.net/gpio_subsystem/io-port-control.html)
- [Linux设备模型(8)_platform设备](http://www.wowotech.net/linux_kenrel/platform_device.html)
