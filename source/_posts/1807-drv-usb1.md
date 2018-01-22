---
title: 驱动之USB基础概念和框架
date: 2018-01-18
categories: embedded linux
tags: [embedded linux, driver]
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


# USB基础知识
- USB是主从结构的
    - 所有的USB传输，都是从USB主机这方发起! USB设备没有"主动"通知USB主机的能力。
    - 例子：USB鼠标滑动一下立刻产生数据，但是它没有能力通知PC机来读数据，只能被动地等得PC机来读。
- USB的传输类型:
    - 控制传输(Control Transfers)：可靠，时间有保证，比如：USB设备的识别过程
    - 批量传输(Bulk Transfers):可靠, 时间没有保证, 比如：U盘
    - 中断传输(Interrupt Transfers)：可靠，实时，比如：USB鼠标
    - 实时传输(Isochronous Transfers)：不可靠，实时，比如：USB摄像头
- USB的识别过程
    - 硬件上(USB2.0)
        - USB主机端D-和D+接有15K下拉电阻, 未接USB设备时为低电平.
        - USB设备端D-或D+接有1.5K上拉电阻.
        - 当USB设备插入USB主机端口时, 就会把D-或D+拉高, 让主机知道有设备接入了
        - 把D-拉高是低速设备, 把D+拉高是高速设备
    - 软件上
        - USB核心驱动程序负责: 识别USB设备, 给USB设备找到对应的驱动程序
        - 当USB设备接入USB主机端后, 其默认的address是0. PC使用此adress与之通讯.
        - 建立通讯后, USB核心驱动会给它分配一个新的address, 并查找有没有对应的驱动.
- USB通讯速率
    - 低速设备(USB1.1, Low speed): 1.5Mb/s
    - 全速设备(USB1.1, Full speed): 12Mb/s
    - 高速设备(USB2.0, High speed): 480Mb/s
    - 超高速设备(USB3.0, Super speed): 5Gb/s, 全双工

# USB主机端驱动框架

![usb_layer.png](https://draapho.github.io/images/1807/usb_layer.png)

各层作用如下:
- USB设备驱动 (USB Device Driver):
    1. 让USB主机知道特定设备的数据含义
    2. linux USB驱动开发就是在这一层. 更底层都是由linux内核完成的.
- USB核心层 (USB Core):
    1. 识别USB设备: 分配并设置USB设备的address, 然后发出命令获取描述符.
    2. 查找并安装匹配的设备驱动
    3. 提供USB读写函数 (只是一个接口, 不知道数据含义)
- USB主机控制器 (USB HCD):
    1. 需要支持的USB接口规范, 譬如USB2.0的设备要向下兼容必须包含USB1.1
    2. OHCI: USB1.1 microsoft等创立的标准. 硬件功能强于软件功能
    3. UHCI: USB1.1 intel创立的标准. 软件功能强于硬件功能, 因此芯片价格更低
    4. EHCI: USB2.0
    5. xHCI: USB3.0


# USB设备端概念

![usb_dev.png](https://draapho.github.io/images/1807/usb_dev.png)

在USB从设备的结构中，从上到下分为:
- 设备(device)
    - 设备即硬件概念上的USB从设备.
    - `address` 的概念就是对设备而言的. 一条USB总线最多外接127个USB设备.
    - 软件数据结构 `usb_device` `usb_device_descriptor`
- 配置(config)
    - 设备可以有一个或多个配置. 但任一时刻只有一个有效配置.
    - 这里其实不难理解. 一个USB硬件设备可以允许多种功能.
    - 个典型的例子是手机, 目前手机自动连接后, 都会弹出问你要用哪种模式连接电脑. 对应了不同的配置
    - 因此选中一个配置后, 就从软件上决定了该USB设备的具体功能.
    - 软件数据结构  `usb_device` `usb_host_config` `usb_config_descriptor`
- 接口(interface)
    - 接口表示逻辑设备, 包含零个或多个endpoint打包.
    - Linux的USB设备驱动是绑定到接口上的, 每个接口在主机看来都是一个独立的功能设备.
    - 譬如录音接口, 播放接口, 数据接口等等.
    - 软件数据结构  `usb_host_interface` `usb_interface_descriptor`.
- 端点(endpoint)
    - 传输数据时, USB使用的就是endpoint概念. endpoint是数据通道.
    - `endpoint0` 用于控制传输, 可双向传输.
    - 除了 `endpoint0` 以外, 每个端点只支持一个方向的数据传输.
    - 每个 endpoint 都有传输类型和传输方向.
    - 传输类型: 控制传输, 批量传输, 中断传输, 实时传输.
    - 传输方向: 输入(IN), 输出(OUT). 注意, 都是基于USB主机来说的! 读U盘, 数据方向就是输入.
    - 譬如"读写U盘", 软件上的概念是: 把数据写到U盘的 endpoint1 上去, 从U盘的 endpoint2 里读数据.
    - 软件数据结构  `usb_device` `usb_host_endpoint` `usb_endpoint_descriptor`


# Linux的USB驱动框架

以下我们用“usb_skel”的USB接口驱动实例（Linux/drivers/usb/usb-skeleton.c）来看看Linux的USB驱动框架：

![usb_skel.png](https://draapho.github.io/images/1807/usb_skel.png)


# USB核心层源码分析

把USB设备接到开发板上，看输出信息:
> usb 1-1: new full speed USB device using s3c2410-ohci and address 2
> usb 1-1: configuration #1 chosen from 1 choice

拔掉后, 显示断开
> usb 1-1: USB disconnect, address 2

尝试寻找源码: `grep "USB device using" -nR`, 找到 `drivers/usb/core/hub.c:2186` 文件.
由此开始分析.

``` c
hub_irq                                 // 硬件检测到USB总线状态变化
    kick_khubd                          // 踢一脚唤醒, 很形象
        wake_up(&khubd_wait);           // 唤醒 hub_thread

hub_thread
    hub_events
        hub_port_connect_change         // USB总线状态改变事件处理函数
            struct usb_device *hdev = hub->hdev             // 处理usb hub的, 忽略
            struct usb_device *udev;                        // usb设备, 后面具体分析 usb_device 数据结构
            udev = usb_alloc_dev(hdev, hdev->bus, port1);   // 申请usb设备, 然后初始化一些参数
            choose_address(udev);                           // 挑出一个空闲的address, 但没有告知这个USB设备
            hub_port_init                                   // 开始对新接入的usb设备进行初始化设置
                dev_info                                    // 打印了如下信息:
                // usb 1-1: new full speed USB device using s3c2410-ohci and address 2
                struct usb_device_descriptor *buf;          // buf 用于取出 bMaxPacketSize0 的大小
                hub_set_address                             // 这里, 才真正把address告诉USB设备
                usb_get_device_descriptor(udev, 8);         // 获取设备描述符, 兼容性考虑
                usb_get_device_descriptor(udev, USB_DT_DEVICE_SIZE); // 获取设备描述符

            usb_new_device(udev)                            // 查找USB设备驱动
                usb_get_configuration(udev);                // 把所有的描述符都读出来，并解析
                    usb_get_descriptor                      // 读描述符
                    usb_parse_configuration                 // 解析配置
                device_add                                  // platform概念的device部分函数.
                // 很熟悉的一个函数了, 见 "驱动之platform概念"
                // 1. 把device放入usb_bus_type的dev链表,
                // 2. 从usb_bus_type的driver链表里取出usb_driver, 把usb_interface和usb_driver的id_table比较
                // 3. 如果能匹配，调用usb_driver的probe
```

下面, 简单分析一下USB的几个描述符结构体
结构体内各个变量的具体含义可参考: [USB Descriptors](http://www.beyondlogic.org/usbnutshell/usb5.shtml)
``` c
// usb_device 和 usb_host_XXX 可以在 include\linux\usb.h 看到
// usb_XXX_descriptor 可以在 include\linux\usb\Ch9.h 看到
// Ch9.h 就是 Chapter9 的缩写, 表示USB协议规范第9章

struct usb_device {                         // usb设备数据结构
    int     devnum;                         /* Address on USB bus */
    enum usb_device_state   state;          /* configured, not attached, etc */
    enum usb_device_speed   speed;          /* high/full/low (or error) */

    // usb_host_*** 里面就包含了 usb 描述符
    struct usb_host_endpoint ep0;           // 特殊的 endpoint0 可双向传输
    struct usb_device_descriptor descriptor;/* Descriptor */
    struct usb_host_config *config;         /* All of the configs */
    struct usb_host_config *actconfig;      /* the active configuration */
    struct usb_host_endpoint *ep_in[16];    // 用做输入的 endpoint
    struct usb_host_endpoint *ep_out[16];   // 用做输出的 endpoint

    /* static strings from the device */
    char *product;                          /* iProduct string, if present */
    char *manufacturer;                     /* iManufacturer string, if present */
    char *serial;                           /* iSerialNumber string, if present */
};

// 整个USB描述符的数据结构框架如下:
struct usb_device                   // usb设备
    struct usb_device_descriptor        // device 描述符
        __le16 bcdUSB;                      // 设备支持的最高USB版本
        __u8  bDeviceClass;                 // 设备类别
        __u8  bDeviceSubClass;              // 设备子类
        __u8  bDeviceProtocol;              // 通信协议
        __u8  bMaxPacketSize0;              // endpoint0 通讯支持的最大数据量
        __le16 idVendor;                    // 经销商ID, 由USB机构分配给厂家
        __le16 idProduct;                   // 产品ID, 由USB厂家自己分配
        __u8  iSerialNumber;                // 产品序列号
    struct usb_host_config              // 主机记录的config信息
        struct usb_config_descriptor        // config 描述符
            __le16 wTotalLength;                // config 总数据长度
            __u8  bNumInterfaces;               // config包含的interface数量
        struct usb_interface                // USB interface
            struct usb_host_interface           // 主机记录的interface信息
                struct usb_interface_descriptor     // interface描述符
                    __u8  bInterfaceNumber;             // interface编号
                    __u8  bNumEndpoints;                // 包含的endpoint数量
                struct usb_host_endpoint            // 该interface包含的endpoint
            int minor;                          // 该USB interface的子设备号
            // 这里可以看出, Linux下, USB设备驱动是被绑到 USB interface 这一层的.
    struct usb_host_endpoint            // 主机记录的该USB设备所有的endpoint
        struct usb_endpoint_descriptor      // endpoint 描述符
            __u8  bEndpointAddress;             // endpoint 地址
            __le16 wMaxPacketSize;              // 支持的数据包大小
        struct list_head urb_list;          // URB列表, USB Request Block.
        // URB 是linux内核给USB底层通讯抽象出来一种方法. 类似于TCP/IP协议里的socket方法.
```


# 参考资料

- [Linux的USB驱动分析](http://blog.csdn.net/ahskx/article/details/50618983)
- [Linux USB驱动工作流程](http://www.embeddedlinux.org.cn/emb-linux/kernel-driver/201710/25-7669.html)
- [浅谈USB驱动架构](http://blog.csdn.net/u014276460/article/details/47292427)
- [Linux usb子系统(一) _写一个usb鼠标驱动](http://www.cnblogs.com/xiaojiang1025/p/6500574.html)
- [USB in a NutShell](http://www.beyondlogic.org/usbnutshell/usb4.shtml)
- [USB Descriptors](http://www.beyondlogic.org/usbnutshell/usb5.shtml)
- [USB控制器类型：OHCI，UHCI，EHCI，xHCI](https://www.crifan.com/files/doc/docbook/usb_basic/release/webhelp/four_hci_relations.html)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***