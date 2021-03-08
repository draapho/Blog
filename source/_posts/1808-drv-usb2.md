---
title: 驱动之USB设备驱动程序
date: 2018-01-19
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


# 查看USB设备信息

``` bash
$ cat /proc/bus/usb/devices           # 查看USB设备信息, 但是jz2440里没有devices目录
$ cat /proc/bus/input/devices         # 接入的是USB鼠标, 是输入设备, 这里可以看到USB鼠标的信息
I: Bus=0003 Vendor=046d Product=c52b Version=0111
N: Name="Logitech USB Receiver"

# 接入USB鼠标后, 会显示如下信息, 可知被分配到input10.
usb 1-1: new full speed USB device using s3c2410-ohci and address 8
usb 1-1: configuration #1 chosen from 1 choice
input: Logitech USB Receiver as /class/input/input10

# 然后用如下指令, 可以查处VID, PID
$ cat sys/class/input/input10/id/product
c52b
$ cat sys/class/input/input10/id/vendor
046d
$ cat sys/class/input/input10/id/version
0111
```


# 源码, 第一版

第一版, 先实现USB框架.
使用 `LinK+ Device Driver Development` 生成并部分修改而来.

![drv_usb.jpg](https://draapho.github.io/images/1808/drv_usb.jpg)

基本步骤如下:
1. 分配/设置 `struct usb_driver` 结构体
    - `.id_table`
    - `.probe`
    - `.disconnect`
2. 注册 `usb_register`


## mousekey.c

``` c
/*
===============================================================================
Driver Name     :       mousekey
Author          :       DRAAPHO
License         :       GPL
Description     :       LINUX DEVICE DRIVER PROJECT
===============================================================================
*/

#include"mousekey.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

/* TODO Fill the USB device table */
static const struct usb_device_id mousekey_usb_ids[] = {
// 可以选择 USB设备类型, 或者 VID/PID 匹配驱动
    { USB_INTERFACE_INFO(USB_INTERFACE_CLASS_HID, USB_INTERFACE_SUBCLASS_BOOT, USB_INTERFACE_PROTOCOL_MOUSE) },
//    { USB_DEVICE(0x046d,0xc52b) },  // idVendor(VID), idProduct(PID)
    {}
};

//struct usb_private {
//  struct urb *urb;
//  struct usb_device *udev;
//};

struct usb_driver mousekey_usb_driver;

static int mousekey_probe(
    struct usb_interface *iface, const struct usb_device_id *id)
{
//    struct usb_private *priv;

    // struct usb_device_id *id 只记录用于匹配的信息.
    // 因此这里需要通过 iface 获取 usb_device 的信息.
    struct usb_device *dev = interface_to_usbdev(iface);

    PINFO("found USB mousekey! ==========>\n");
    printk("USB address=%d\n"
           "manufacturer=%s, product=%s, serial=%s\n"
           "idVendor=0x%x, idProduct=0x%x\n"
           "Device Class=%d, SubClass=%d, Protocol=%d\n",
           dev->devnum,
           dev->manufacturer, dev->product, dev->serial,
           dev->descriptor.idVendor, dev->descriptor.idProduct,
           dev->descriptor.bDeviceClass,
           dev->descriptor.bDeviceSubClass,
           dev->descriptor.bDeviceProtocol);
    printk("InterfaceNumber=%d, NumberOfEndpoints=%d\n"
           "Interface Class=%d, SubClass=%d, Protocol=%d\n",
           iface->cur_altsetting->desc.bInterfaceNumber,
           iface->cur_altsetting->desc.bNumEndpoints,
           iface->cur_altsetting->desc.bInterfaceClass,
           iface->cur_altsetting->desc.bInterfaceSubClass,
           iface->cur_altsetting->desc.bInterfaceProtocol);

//    priv = kzalloc(sizeof(*priv), GFP_KERNEL);
//    if (!priv) {
//        PERR("Failed to allocate the device's private data\n");
//        return -ENOMEM;
//    }
//
//    usb_set_intfdata(iface, priv);
//    priv->udev = interface_to_usbdev(iface);
    return 0;
}

static void mousekey_disconnect(struct usb_interface *iface)    {
//    struct usb_private *priv = usb_get_intfdata(iface);

    PINFO("disconnect USB mousekey\n");
//    kfree(priv);
}

/* 1. 分配/设置 struct usb_driver */
struct usb_driver mousekey_usb_driver = {
    .name           = DRIVER_NAME,
    .id_table       = mousekey_usb_ids,
    .probe          = mousekey_probe,
    .disconnect     = mousekey_disconnect,
};

static int __init mousekey_init(void)
{
    /* TODO Auto-generated Function Stub */
    int res;

    /* 2. 注册 */
    res = usb_register(&mousekey_usb_driver);
    if( res ) {
        PERR("Error registering the USB Driver\n");
        return res;
    }

    PINFO("INIT\n");
    return 0;
}

static void __exit mousekey_exit(void)
{
    /* TODO Auto-generated Function Stub */
    PINFO("EXIT\n");
    usb_deregister(&mousekey_usb_driver);
}

module_init(mousekey_init);
module_exit(mousekey_exit);
```


## mousekey.h

``` h
#define DRIVER_NAME "mousekey"
#define PDEBUG(fmt,args...) printk(KERN_DEBUG"%s:"fmt,DRIVER_NAME, ##args)
#define PERR(fmt,args...) printk(KERN_ERR"%s:"fmt,DRIVER_NAME,##args)
#define PINFO(fmt,args...) printk(KERN_INFO"%s:"fmt,DRIVER_NAME, ##args)
#include<linux/init.h>
#include<linux/module.h>
#include<linux/slab.h>
#include<linux/usb.h>

#include <linux/hid.h>
```

## Makefile

``` makefile
obj-m       := mousekey.o
KERN_SRC    := /home/draapho/share/jz2440/kernel/linux-2.6.22.6/
PWD         := $(shell pwd)

modules:
    make -C $(KERN_SRC) M=$(PWD) modules

install:
    make -C $(KERN_SRC) M=$(PWD) modules_install
    depmod -a

clean:
    make -C $(KERN_SRC) M=$(PWD) clean
```

## 测试

由于内核自带了USB鼠标驱动程序, 因此需要重新编译内核, 去掉内核的HID的USB功能

``` bash
# Ubuntu 主机端
# pwd = ./linux-2.6.22.6_custom  复制一个新的内核源码目录

$ make clean
$ make menuconfig                               # 去掉自带的HID USB驱动程序
# -> Device Drivers
#   -> HID Devices
#     < > USB Human Interface Device (full HID) support     # 取消HID的USB支持

$ make uImage
# 烧录新的uImage
# 重启开发板进入uboot烧录界面, 按k准备烧录内核. 略过不表
$ sudo dnw ./arch/arm/boot/uImage

# pwd = ~/share/jz2440/drivers/mousekey/        # USB鼠标驱动目录
$ make modules                                  # 生成mousekey.ko


# 开发板端, 开始测试
# pwd = ~/share/jz2440/drivers/mousekey/        # USB鼠标驱动目录, nfs
$ insmod mousekey.ko                            # 加载驱动, 开始测试
usbcore: registered new interface driver mousekey
mousekey:INIT

# 开发板上接入USB鼠标, 会打印如下信息:
usb 1-1: new full speed USB device using s3c2410-ohci and address 7
usb 1-1: configuration #1 chosen from 1 choice
mousekey:found USB mousekey! ==========>
......                                          # 打印具体信息. 可以看出Device不重要, Interface才重要.

# 开发板上拔出USB鼠标, 会打印如下信息:
usb 1-1: USB disconnect, address 7
mousekey:disconnect USB mousekey

# rmmod mousekey
mousekey:EXIT
usbcore: deregistering interface driver mousekey
```

# 源码, 第二版

实现USB设备驱动, 将USB鼠标识别成按键.
左键输入`l`, 右键输入`s`, 中键输入`enter`

- `mousekey.h` 和 `Makefile` 参考 `源码, 第一版`
- 这里因为是用的input子系统, 所以注册设备用了 `input_register_device`, 而不是 `usb_register_dev`
    - 用 `input_register_device` 注册的话, 会在 `/dev/` 下面新增一个 `event*`
    - 用 `usb_register_dev` 注册的话, 会在 `/sys/class/usb/` 下面看到节点名称.
- `input 子系统` 参考 [驱动之input子系统](https://draapho.github.io/2018/01/05/1802-drv-input/)
    1. 分配一个input_dev变量
    2. 设置/初始化此变量
    3. 注册, input_register_device
    4. 硬件相关代码, open, close, event, sync等等.
- `URB`, 即 `usb request block`. 基本用法:
    1. 分配 URB. `usb_alloc_urb`
    2. 初始化 URB 结构体 `struct urb`
    3. 提交URB (开始通讯). `usb_submit_urb`
- 可参考 Linux 内核里的 `/drivers/hid/usbhid/usbmouse.c`

## mousekey.c

``` c
/*
===============================================================================
Driver Name     :       mousekey
Author          :       DRAAPHO
License         :       GPL
Description     :       LINUX DEVICE DRIVER PROJECT
===============================================================================
*/

#include"mousekey.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

/* TODO Fill the USB device table */
static const struct usb_device_id mousekey_usb_ids[] = {
// 可以选择 USB设备类型, 或者 VID/PID 匹配驱动
    { USB_INTERFACE_INFO(USB_INTERFACE_CLASS_HID, USB_INTERFACE_SUBCLASS_BOOT, USB_INTERFACE_PROTOCOL_MOUSE) },
//    { USB_DEVICE(0x046d,0xc52b) },  // idVendor(VID), idProduct(PID)
    {}
};

struct usb_driver mousekey_usb_driver;

struct usb_private {
    struct urb *urb;                // usb请求块
    struct usb_device *udev;        // usb 设备
    struct input_dev *idev;         // input 设备
    char *buf;                      // urb 用的缓冲
    dma_addr_t buf_phys;            // 缓冲物理地址, dma要用
    int len;                        // 缓冲区大小
};

static void mousekey_irq(struct urb *urb)
{
    struct usb_private *priv = urb->context;

#if 0
    // 先打印查看usb鼠标发来的数据, 不同的鼠标数据格式略有不同!
    int i;
    for (i = 0; i < priv->len; i++) {
        printk("%02x ", priv->buf[i]);
    }
    printk("\n");
    usb_submit_urb(priv->urb, GFP_KERNEL);
#else

    switch (urb->status) {
    case 0:             /* success */
        break;
    case -ECONNRESET:   /* unlink */
    case -ENOENT:
    case -ESHUTDOWN:
        return;
    /* -EPIPE:  should clear the halt */
    default:            /* error */
        goto resubmit;
    }

    /* USB鼠标数据含义
     * data[0]: bit0-左键, 1-按下, 0-松开
     *          bit1-右键, 1-按下, 0-松开
     *          bit2-中键, 1-按下, 0-松开
     */
    input_report_key(priv->idev, KEY_L,     priv->buf[0] & 0x01);
    input_report_key(priv->idev, KEY_S,     priv->buf[0] & 0x02);
    input_report_key(priv->idev, KEY_ENTER, priv->buf[0] & 0x04);
    input_sync(priv->idev);

resubmit:
    /* 重新提交urb */
    usb_submit_urb (urb, GFP_ATOMIC);
#endif
}

static int mousekey_probe(struct usb_interface *iface,
                            const struct usb_device_id *id)
{
    int pipe;
    struct usb_private *priv;
    struct usb_endpoint_descriptor *endpoint;
    PINFO("found USB mousekey! ==========>\n");

    priv = kzalloc(sizeof(*priv), GFP_KERNEL);
    if (!priv) {
        PERR("Failed to allocate the device's private data\n");
        return -ENOMEM;
    }
    usb_set_intfdata(iface, priv);
    priv->udev = interface_to_usbdev(iface);

    printk("USB address=%d\n"
           "manufacturer=%s, product=%s, serial=%s\n"
           "idVendor=0x%x, idProduct=0x%x\n"
           "Device Class=%d, SubClass=%d, Protocol=%d\n",
           priv->udev->devnum,
           priv->udev->manufacturer, priv->udev->product, priv->udev->serial,
           priv->udev->descriptor.idVendor, priv->udev->descriptor.idProduct,
           priv->udev->descriptor.bDeviceClass,
           priv->udev->descriptor.bDeviceSubClass,
           priv->udev->descriptor.bDeviceProtocol);
    printk("InterfaceNumber=%d, NumberOfEndpoints=%d\n"
           "Interface Class=%d, SubClass=%d, Protocol=%d\n",
           iface->cur_altsetting->desc.bInterfaceNumber,
           iface->cur_altsetting->desc.bNumEndpoints,
           iface->cur_altsetting->desc.bInterfaceClass,
           iface->cur_altsetting->desc.bInterfaceSubClass,
           iface->cur_altsetting->desc.bInterfaceProtocol);

    if (iface->cur_altsetting->desc.bNumEndpoints != 1)     // endpoint 不为1, 认为不是USB鼠标
        return -ENODEV;
    endpoint = &iface->cur_altsetting->endpoint[0].desc;
    if (!usb_endpoint_is_int_in(endpoint))                  // endpoint 传输属性必须是中断输入
        return -ENODEV;

    /* a. 分配一个input_dev */
    priv->idev = input_allocate_device();

    /* b. 设置 */
    /* b.1 能产生哪类事件 */
    set_bit(EV_KEY, priv->idev->evbit);
    set_bit(EV_REP, priv->idev->evbit);
    /* b.2 能产生哪些事件 */
    set_bit(KEY_L, priv->idev->keybit);                     // 鼠标按键模拟键盘 L S ENTER
    set_bit(KEY_S, priv->idev->keybit);
    set_bit(KEY_ENTER, priv->idev->keybit);

    /* c. 注册 */
    input_register_device(priv->idev);


    /* d. 硬件相关操作, 这里就是使用urb进行USB通讯 */
    /* 1. 分配 URB. */
    priv->urb = usb_alloc_urb(0, GFP_KERNEL);

    /* 2. 初始化 URB 结构体 */
    pipe = usb_rcvintpipe(priv->udev, endpoint->bEndpointAddress);  // 指定USB通讯类型和endpoint
    priv->len = endpoint->wMaxPacketSize;                           // buf大小
    priv->buf = usb_buffer_alloc(priv->udev, priv->len, GFP_ATOMIC, &priv->buf_phys);
    // 分配buf, usb会使用dma进行数据传输, buf_phys用于记录buf的物理地址.

    usb_fill_int_urb(priv->urb, priv->udev, pipe, priv->buf, priv->len, mousekey_irq, priv, endpoint->bInterval);
    // mousekey_irq, usb中断发生时的回调函数. priv, 回调函数用的私有参数, 可以是NULL. bInterval, USB HUB的轮询间隔时间.
    priv->urb->transfer_dma = priv->buf_phys;                       // dma传输需要物理地址
    priv->urb->transfer_flags |= URB_NO_TRANSFER_DMA_MAP;

    /* 3. 提交URB (开始通讯) */
    usb_submit_urb(priv->urb, GFP_KERNEL);
    return 0;
}

static void mousekey_disconnect(struct usb_interface *iface)    {
    struct usb_private *priv = usb_get_intfdata(iface);
    PINFO("disconnect USB mousekey\n");

    usb_kill_urb(priv->urb);
    usb_free_urb(priv->urb);
    usb_buffer_free(priv->udev, priv->len, priv->buf, priv->buf_phys);
    input_unregister_device(priv->idev);
    input_free_device(priv->idev);
    kfree(priv);
}

/* 1. 分配/设置 struct usb_driver */
struct usb_driver mousekey_usb_driver = {
    .name           = DRIVER_NAME,
    .id_table       = mousekey_usb_ids,
    .probe          = mousekey_probe,
    .disconnect     = mousekey_disconnect,
};

static int __init mousekey_init(void)
{
    /* TODO Auto-generated Function Stub */
    int res;

    /* 2. 注册 */
    res = usb_register(&mousekey_usb_driver);
    if( res ) {
        PERR("Error registering the USB Driver\n");
        return res;
    }

    PINFO("INIT\n");
    return 0;
}

static void __exit mousekey_exit(void)
{
    /* TODO Auto-generated Function Stub */
    PINFO("EXIT\n");
    usb_deregister(&mousekey_usb_driver);
}

module_init(mousekey_init);
module_exit(mousekey_exit);
```

## 测试

``` bash
# 先按照此文之前的测试步骤烧录好无HID USB驱动的内核文件.

# pwd = ~/share/jz2440/drivers/mousekey/        # USB鼠标驱动目录, nfs
$ insmod mousekey.ko                            # 加载驱动, 开始测试
usbcore: registered new interface driver mousekey
mousekey:INIT

$ ls /dev/event*                                # 查看已有的event号

# 开发板上接入USB鼠标, 会打印如下信息:
usb 1-1: new full speed USB device using s3c2410-ohci and address 7
usb 1-1: configuration #1 chosen from 1 choice
mousekey:found USB mousekey! ==========>
......                                          # 打印具体信息. 可以看出Device不重要, Interface才重要.

$ ls /dev/event*                                # 查看新增的event号, 就是此驱动的event
/dev/event1                                     # 譬如, 新增了event1

# 方法一 (没有LCD):
$ cat /dev/tty1
# 点击鼠标, 终端会显示输入, 但没有输出反馈.

# 方法二 (没有LCD):
$ hexdump /dev/event1
# 字节数|   秒    |  微秒   | 类  |code|  value      # 小端模式, 低位在前!
0000000 0bb2 0000 0e48 000c 0001 0026 0001 0000    # input_event(keydev, EV_KEY, key_val, 1)
0000010 0bb2 0000 0e54 000c 0000 0000 0000 0000    # input_sync(keydev);
0000020 0bb2 0000 5815 000e 0001 0026 0000 0000    # input_event(keydev, EV_KEY, key_val, 0)
0000030 0bb2 0000 581f 000e 0000 0000 0000 0000    # input_sync(keydev);

# 方法三 (有LCD, 没有QT)
$ vi /etc/inittab
    # ===== 设置为如下内容 =====
    ::sysinit:/etc/init.d/rcS
    s3c2410_serial0::askfirst:-/bin/sh
    # 增加了下面一行, 用于屏幕打开终端
    tty1::askfirst:-/bin/sh
    ::ctrlaltdel:/sbin/reboot
    ::shutdown:/bin/umount -a -r
    # ===== wq保存, 退出 =====
$ reboot                                        # 重启终端
# 这样点击鼠标就直接能在LCD上查看输入和输出了.
```

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***