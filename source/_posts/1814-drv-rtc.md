---
title: 驱动之RTC分析
date: 2018-02-08
categories: embedded linux
tags: [embedded linux, driver]
description: 如题.
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之input子系统](https://draapho.github.io/2018/01/05/1802-drv-input/)
- [驱动之platform概念](https://draapho.github.io/2018/01/08/1803-drv-platform/)
- [驱动之RTC分析](https://draapho.github.io/2018/02/08/1814-drv-rtc/)
- [驱动之LCD驱动框架和实现](https://draapho.github.io/2018/01/09/1804-drv-lcd/)
- [驱动之触摸屏驱动框架和实现](https://draapho.github.io/2018/01/11/1806-drv-ts/)
- [驱动之USB基础概念和框架](https://draapho.github.io/2018/01/18/1807-drv-usb1/)
- [驱动之USB设备驱动程序](https://draapho.github.io/2018/01/19/1808-drv-usb2/)


本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.

# 字符设备驱动另一种写法

在 [驱动之字符设备-框架](https://draapho.github.io/2017/11/22/1733-drv-chr1/) 里, 使用的是函数 `register_chrdev` 进行注册的.
其缺点是, 默认调用了 `__register_chrdev_region(major, 0, 256, name);`, 也就是会把256个次设备号全部注册掉.
为了合理使用次设备号, 就需要另外一种写法.

``` c
static int major;                               // 确定主设备号

static struct file_operations hello_fops = {    // fop数据结构
    .owner = THIS_MODULE,
    .open = hello_open,
}

static int __init hello_init(void) {

    // 主设备号已知, 用 register_chrdev_region 即可
    // devid = MKDEV(major, 0);
    // register_chrdev_region(devid, HELLO_CNT, "hello");

    // 主设备号需要系统分配, 用 alloc_chrdev_region 函数
    alloc_chrdev_region(&devid, 0, HELLO_CNT, "hello");
    major = MAJOR(devid);                       // 提取主设备号

    cls = class_create(THIS_MODULE, "hello");   // 创建类
    cdev_init(&hello_cdev, &hello_fops);        // 初始化
    cdev_add(&hello_cdev, devid, HELLO_CNT);    // 添加指定个数的字符设备
    device_create(cls , NULL , MKDEV(major, 0), "hello0");  // 和 class_device_create 没有本质区别.
}
```

本质上, 就是自己实现一遍 `register_chrdev` 函数里的内容, 来控制子设备号个数.
博客里 [驱动之基于LinK+设计按键驱动](https://draapho.github.io/2017/11/30/1740-drv-chr2/) 这些内容都是由 `LinK+` 自动实现的.


# RTC源码分析

这里以RTC源码为例进行分析, 用于熟悉字符设备的写法和分离分层即platform的概念

`/drivers/rtc/rtc-dev.c` 提供了所有的RTC驱动层读写函数.
里面进一步调用了 `/drivers/rtc/class.c` 的一些函数.
这两个文件是linux内核RTC驱动设备的软件抽象核心.

显然的, 后面的很多文件是芯片厂商提供的硬件相关的RTC部分. 譬如 `rtc-s3c.c`.
也可以通过分析 `rtc-dev.c` 里的 `rtc_dev_add_device` 倒过来找到这些文件.

下面, 我们从底层硬件(`rtc-s3c.c`)往上层进行分析, 看看rtc字符设备的整个注册过程.


``` c
// subsys_initcall(rtc_init), 系统初始化时调用
rtc_init();                                         // 此函数位于 "class.c"
    class_create(THIS_MODULE, "rtc");               // =====> class_create
    rtc_dev_init();
        alloc_chrdev_region();                      // =====> alloc_chrdev_region, 分配 RTC_DEV_MAX 个子设备号


// module_init(s3c_rtc_init), 驱动入口函数. insmod 时被调用
s3c_rtc_init();                                     // 此函数位于 "rtc-s3c.c"
    platform_driver_register(&s3c2410_rtcdrv);
    // 明显用了platform框架, 根据 .name = "s3c2410-rtc" 去找 platform_device_register
    // 在 "/arch/arm/plat-s3c24xx/devs.c" 下找到了 s3c_device_rtc. 但没有被内核调用. 后面再说.
s3c_rtc_probe();                                    // platform 的 driver 和 device 匹配后, 自动调用 probe
    // 一系列的RTC硬件相关操作, 忽略
    rtc_device_register();                          // 此函数位于 "class.c"
        rtc_dev_prepare();                          // 此函数位于 "rtc-dev.c"
            rtc->dev.devt = MKDEV(MAJOR(rtc_devt), rtc->id);
            cdev_init();                            // =====> cdev_init

        // device_create 里最终调用的就是 device_register.
        // rtc->dev.devt 的值已经在 rtc_dev_prepare 设置好了.
        device_register();                          // =====> 等效于 device_create.
        rtc_dev_add_device();
            cdev_add();                             // =====> cdev_add

        // 这两个函数似乎也和设备注册相关. 详请不明
        rtc_sysfs_add_device();
        rtc_proc_add_device();
```

# RTC 测试

前面的分析源码说过, `s3c_device_rtc` 没有被调用, 因此当前的系统也无法使用rtc.
这里就加入rtc功能, 并测试.

``` bash
# Ubuntu 主机端
# pwd = ./linux-2.6.22.6
# 打开 ./arch/arm/plat-s3c24xx/common-smdk.c
    # 找到数组 static struct platform_device __initdata *smdk_devs[]
    # 加入一行   &s3c_device_rtc,
    # 此数组会被 "smdk_machine_init" 调用, 里面有 "platform_add_devices",
    # 此函数会对数组里的内容依次进行 "platform_device_register"

$ make clean                                    # 没把握的话, clean一下
$ make uImage
# 烧录新的uImage
# 重启开发板进入uboot烧录界面, 按k准备烧录内核. 略过不表
$ sudo dnw ./arch/arm/boot/uImage

# 开发板端, 开始测试
$ ls /dev/rtc* -l                               # 查看设备, 有 rtc0
$ date                                          # 显示系统时间
Mon Apr  3 06:53:50 UTC 2006

$ date 020811002018.30                          # 设置系统时间 date [MMDDhhmm[[CC]YY][.ss]]
Thu Feb  8 11:00:30 UTC 2018
$ hwclock -w                                    # 把系统时间写入RTC. HardWare CLOCK

# 断电, 重启.
$ date
Thu Feb  8 11:02:01 UTC 2018                    # 设置的时间还在.
```





----------

***原创于 [DRA&PHO](https://draapho.github.io/)***