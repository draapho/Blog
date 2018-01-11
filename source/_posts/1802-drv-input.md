---
title: 驱动之input子系统
date: 2018-01-05
categories: embedded linux
tags: [linuxembedded linux, drv]
---



# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之input子系统](https://draapho.github.io/2018/01/05/1802-drv-input/)
- [驱动之platform概念](https://draapho.github.io/2018/01/08/1803-drv-platform/)
- [驱动之LCD驱动框架和实现](https://draapho.github.io/2018/01/09/1804-drv-lcd/)
- [驱动之触摸屏驱动框架和实现](https://draapho.github.io/2018/01/11/1806-drv-ts/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.


# 输入子系统

输入子系统是Linux对硬件设备进一步的抽象.
将输入系统的逻辑概念统一写好, 我们称之为软件抽象层.
而硬件部分的底层工作需要由开发人员具体实现, 我们称之为硬件设备层.
中间还有个连接层, 用于实现软件抽象层和硬件设备层的多对多关联.

按键, 鼠标, 键盘, 触摸屏等设备都可以归属为输入子系统.
这些设备的硬件驱动和输入子系统对接, 输入子系统再统一将输入事件传递给应用层.
这样, 应用层的设备就无需考虑底层硬件的区别.
而我们之前写的按键驱动, LED驱动, 一般只是给公司内部调用的, 不具有通用性!


整个输入子系统完成的工作其实和自己写的驱动是一样的.
只是部分可以软件抽象的功能被输入子系统打包掉了.
其核心代码在 `/drivers/input/input.c`
整体框架如下:

``` c
// ===== 输入子系统, 核心层 =====
文件 /drivers/input/input.c 内, 关键函数
    input_init              // 初始化
    class_register          // 注册类
    register_chrdev         // 注册设备(主设备号13)

    input_register_device   // 注册硬件设备 input_dev
    input_register_handler  // 注册软件抽象 input_handler
    input_register_handle   // 注册连接     input_handle


// ===== 软件抽象层, 系统已实现 =====
1. static 初始化一个 input_handler 全局变量
2. 注册此变量, input_register_handler
3. 实现 event connect 等函数

struct input_handler {
    event,connect, disconnect, start        // 函数具体实现的指针
    int minor;                              // 次设备号
    const char *name;                       // 显示在proc/bus/input/handlers

    const struct input_device_id *id_table; // 驱动支持的id表(用于匹配input_dev)
    const struct input_device_id *blacklist;// id表黑名单

    struct list_head    h_list;             // 存放input_handle(没有r)的链表
    struct list_head    node;               // 存放input_handler自身的链表
};


// ===== 连接层, 系统已实现 =====
多个文件 /drivers/input/*dev.c 内*/
1. *dev_connect里分配 input_handle(没有r)变量
2. 设置/初始化此变量
3. 注册, input_register_handle(没有r)

struct input_handle(没有r) {
    void *private;                          // 私有数据, 指向了父指针
    struct input_dev *dev;                  // 指向input_dev
    struct input_handler *handler;          // 指向 input_handler

    struct list_head    d_node;             // 存放input_dev->h_list的链表
    struct list_head    h_node;             // 存放input_handler->h_list的链表
};

// ===== 硬件设备层, 自己写 =====
1. 分配一个input_dev变量
2. 设置/初始化此变量
3. 注册, input_register_device
4. 硬件相关代码, open, close, event, sync等等.

struct input_dev {
    const char *name;                       // 设备描述
    const char *phys;                       // 设备路径?
    struct input_id id;                     // 总线类型. 供应商/产品/版本信息. 用于匹配 input_handler

    unsigned long evbit[NBITS(EV_MAX)];     // 记录支持的事件类型位图
    unsigned long keybit[NBITS(KEY_MAX)];   // 记录支持的按键值位图
    unsigned long relbit[NBITS(REL_MAX)];   // 记录支持的相对坐标位图, 如滚轮
    unsigned long absbit[NBITS(ABS_MAX)];   // 记录支持的绝对坐标位图, 如触摸屏

    struct list_head    h_list;             // 存放input_handle(没有r)的链表
    struct list_head    node;               // 存放input_dev自身的链表
};
```

如图, 较为直观的说明了三者的指针关系, 以及 `input_handler` 和 `input_dev` 通过 `input_handle(没有r)` 的建立的多对多关系

![input_struct_relation](https://draapho.github.io/images/1802/input_struct_relation.png)


## input核心层

整个input初始化流程大致如下:

``` c
// drivers/input/input.c
static int __init input_init(void)
    class_register(&input_class);       // 注册input类. 对应于自己写的驱动的 class_create, 也会class_register
    input_proc_init();                  // 初始化一些交互文件
    register_chrdev(INPUT_MAJOR, "input", &input_fops); // 对应于自己写的驱动的 register_chrdev, 注册设备
        // input的主设备号固定为13, 子设备号后面会自动分配. 核心是 input_fops 这么一个结构.
        // 查看 input_fops 变量, 只有一个 .open 函数, 指向 input_open_file
        static int input_open_file(struct inode *inode, struct file *file)
            struct input_handler *handler = input_table[iminor(inode) >> 5];    // 取出子设备号高3位, 低5位用于自动分配
            new_fops = fops_get(handler->fops)  // 打开handler指向的fop, 譬如 &evdev_fops (后面会讲到)
            file->f_op = new_fops;
            new_fops->open(inode, file);        // 打开真正可操作的文件, 里面会有 read, write
            // 这样 app:read > ... > file->f_op->read
    // 另外一个 class_device_create 是在 input_handler.connect 的函数里实现的.
```

上述代码, 关键点在于从 input_table 取出 input_handler的指针.
那么 input_table 由谁构造呢? 搜索可知是: `input_register_handler`. 继续往下看.


## 软件抽象层

注册 input_handler 的过程:

``` c
// input_open_file 函数里, 有个关键数组为 input_table, 存储了input_handler的指针!
// 函数 input_register_handler 会设置 input_table. 它被如下代码调用:
// drivers/char/keyboard.c  // 按键抽象
// drivers/input/evbug.c    // 调试用, 所用的事件存到 syslog文件中
// drivers/input/evdev.c    // input_table[2], 子设备号0x40-0x5F, 设备事件抽象
// drivers/input/joydev.c   // input_table[0], 子设备号0x00-0x0F, 游戏杆抽象
// drivers/input/mousedev.c // input_table[1], 子设备号0x20-0x3F, 鼠标抽象
// drivers/input/tsdev.c    // input_table[4], 子设备号0x80-0x9F, 触摸屏抽象
// 上述几个文件真正定义了 input_handler 的变量如 evdev_handler, 并对其初始化, 包括 id_table

int input_register_handler(struct input_handler *handler)
    input_table[handler->minor >> 5] = handler;         // 将input_handler指针放入数组
    list_add_tail(&handler->node, &input_handler_list); // 放入链表
    list_for_each_entry(dev, &input_dev_list, node)
        input_attach_handler(dev, handler);             // 对于每个input_dev, 调用input_attach_handler

static int input_attach_handler(struct input_dev *dev, struct input_handler *handler)
    id = input_match_device(handler->id_table, dev);    // 根据input_handler的id_table判断能否支持这个input_dev
    error = handler->connect(handler, dev, id);         // 匹配的话, 就自动建立连接, 连接函数由软件抽象层实现
```


## 硬件设备层

注册 input_dev 的过程:

``` c
// 函数 input_register_device 用于注册硬件设备, 由开发人员写的驱动代码调用.

int input_register_device(struct input_dev *dev)
    list_add_tail(&dev->node, &input_dev_list);         // 放入链表
    list_for_each_entry(handler, &input_handler_list, node)
        input_attach_handler(dev, handler);             // 对于每一个input_handler，调用 input_attach_handler

static int input_attach_handler(struct input_dev *dev, struct input_handler *handler)
    id = input_match_device(handler->id_table, dev);    // 根据input_handler的id_table判断能否支持这个input_dev
    error = handler->connect(handler, dev, id);         // 匹配的话, 就自动建立连接, 连接函数由软件抽象层实现
```

## 连接层

有上述分析可知, 软件抽象层和硬件设备层建立连接的关键是 `handler->connect` 指向的函数.
建立连接的基本步骤如下:
1. 分配一个 `input_handle(没有r)` 结构体
2. 设置/初始化 `input_handle(没有r)`
    - `input_handle.dev = input_dev;` 保存硬件设备, input_dev
    - `input_handle.handler = input_handler;` 保存软件抽象, input_handler
3. 软件层和硬件层分别注册 `input_handle(没有r)`, 将其指针保存到各自结构体的`h_list`项中
    - `input_handler->h_list = &input_handle;`
    - `inpu_dev->h_list = &input_handle;`


硬件设备层的代码最终是要自己写的, 因此我们会比较熟悉.
下面以软件抽象层的 `drivers/input/evdev.c` 为例, 分析一下整个匹配过程.

``` c
// 之前已经分析到, 调用 input_register_handler 和 input_register_device 时, 都会进行匹配
static int input_attach_handler(struct input_dev *dev, struct input_handler *handler)
    id = input_match_device(handler->id_table, dev);    // 根据input_handler的id_table判断能否支持这个input_dev
    error = handler->connect(handler, dev, id);         // 匹配的话, 就自动建立连接, 连接函数由软件抽象层实现

// 这里说明一下, handler->id_table 和 handler->connect 的初始值都是由软件抽象层几个文件完成的. 具体就是下面几个:
// drivers/char/keyboard.c  // 按键抽象
// drivers/input/evbug.c    // 调试用, 所用的事件存到 syslog文件中
// drivers/input/evdev.c    // input_table[2], 子设备号0x40-0x5F, 设备事件抽象
// drivers/input/joydev.c   // input_table[0], 子设备号0x00-0x0F, 游戏杆抽象
// drivers/input/mousedev.c // input_table[1], 子设备号0x20-0x3F, 鼠标抽象
// drivers/input/tsdev.c    // input_table[4], 子设备号0x80-0x9F, 触摸屏抽象


// 我们以 evdev.c 为例深入分析一下. 其定义的 input_handler 变量名为 evdev_handler. connect会调用evdev_connect
static int evdev_connect(struct input_handler *handler, struct input_dev *dev, const struct input_device_id *id)
    // 1. 分配一个evdev, 里面包含了input_handle(没有r)
    evdev = kzalloc(sizeof(struct evdev), GFP_KERNEL);

    // 2. 设置/初始化
    evdev->handle.dev = dev;            // 保存硬件设备的input_dev指针
    evdev->handle.name = evdev->name;
    evdev->handle.handler = handler;    // 保存软件抽象的input_handler指针
    evdev->handle.private = evdev;      // 保存 evdev 这个指针. 让handle知道归属.

    // 这里对应于自己写的驱动的 class_device_create, 注册input类下面的设备.
    // 另外两个, 注册驱动和注册类都是在 input_init() 里完成的
    class_device_create(&input_class, &dev->cdev, devt,dev->cdev.dev, evdev->name);

    // 3. 注册
    error = input_register_handle(&evdev->handle);              // 注意没有r, 不是 input_register_handler
        list_add_tail(&handle->d_node, &handle->dev->h_list);   // 将 handle 加入 dev->h_list 链表中
        list_add_tail(&handle->h_node, &handler->h_list);       // 将 handle 加入 handler->h_list 链表中
        // 这里可以分析出, 软件抽象层和硬件设备层的对应关系是可以多对多的, 两者都维护着一个handle列表(h_list).
```

## APP层相关函数

最后, 从APP层读取输入子系统进行分析. 以按键为例, 用到 `drivers/input/evdev.c` 和 `drivers/char/keyboard.c`
在书写按键的硬件模块时, input子系统会自动匹配关联到上述两个软件抽象层.
(猜测, keyboard的抽象层次比evdev更高. 因此keyboard没有input_table初始值)

``` c
// app: read 试着读取按键值后:
// ....... 中间过程省略掉, 最后会调用:
    evdev_read
        // 无数据(用的环形缓冲区)并且是非阻塞方式打开，则立刻返回
        if (client->head == client->tail && evdev->exist && (file->f_flags & O_NONBLOCK))
            return -EAGAIN;
        // 否则休眠
        retval = wait_event_interruptible(evdev->wait, client->head != client->tail || !evdev->exist);

    evdev_event     // 休眠后, 由evdev_event来唤醒, 此时间和硬件相关, 由硬件设备层实现
        wake_up_interruptible(&evdev->wait);
```



# 硬件设备端源码

由于input子系统的实际上是帮我们完成了相当一部分的注册工作, 并实现了通用的逻辑功能.
因此实际写硬件设备驱动时, 反而变得更简单了. 核心步骤如下:
1. 分配一个input_dev结构体. `input_allocate_device`
2. 设置事件, 设置事件支持的操作类型
3. 注册 `input_register_device`
4. 硬件初始化和逻辑判断
    - 上报事件: `input_event` `input_sync`


依旧通过 LinK+ 软件来写驱动. LinK+设置步骤可参考 [驱动之基于LinK+设计按键驱动](https://draapho.github.io/2017/11/30/1740-drv-chr2/)

与input有关的设置页面如下:
![link+input](https://draapho.github.io/images/1802/link+input.JPG)


## input_keys.c

``` c
/*
===============================================================================
Driver Name     :       input_keys
Author          :       DRAAPHO
License         :       GPL
Description     :       LINUX DEVICE DRIVER PROJECT
                :       参考drivers\input\keyboard\gpio_keys.c
===============================================================================
*/

#include"input_keys.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

struct keys_desc{                                       // 硬件相关参数
    int irq;
    char *name;
    unsigned int pin;
    unsigned int key_val;
};

struct keys_desc keys_desc_public[4] = {                // 硬件参数初始化
    {IRQ_EINT0,  "S2", S3C2410_GPF0,  KEY_L},
    {IRQ_EINT2,  "S3", S3C2410_GPF2,  KEY_S},
    {IRQ_EINT11, "S4", S3C2410_GPG3,  KEY_ENTER},
    {IRQ_EINT19, "S5", S3C2410_GPG11, KEY_LEFTSHIFT},
};

struct input_keys_private {                             // 私有变量结构体
    struct input_dev *dev;
    struct keys_desc *keysdesc;
    struct timer_list keys_timer;
};

struct input_keys_private *input_keys_priv;             // 私有变量


static irqreturn_t keys_irq(int irq, void *dev_id)      // 按键中断函数
{
    if (!input_keys_priv)
        return IRQ_NONE;

    // 10ms后启动定时器, 用于按键防抖动
    input_keys_priv->keysdesc = (struct keys_desc *)dev_id;
    mod_timer(&input_keys_priv->keys_timer, jiffies+HZ/100);
    return IRQ_RETVAL(IRQ_HANDLED);
}

static void keys_timer_function(unsigned long data)     // 定时器超时中断函数
{
    struct input_dev *keydev;
    struct keys_desc *keydesc;
    unsigned int pinval;

    if (!input_keys_priv)
        return;

    keydesc= input_keys_priv->keysdesc;
    keydev = input_keys_priv->dev;
    pinval = s3c2410_gpio_getpin(keydesc->pin);

    if (pinval) {
        /* 松开 : 最后一个参数: 0-松开, 1-按下 */
        input_event(keydev, EV_KEY, keydesc->key_val, 0);   // 触发按键事件
        input_sync(keydev);                                 // 事件结束, 同步到用户空间
    } else {
        /* 按下 */
        input_event(keydev, EV_KEY, keydesc->key_val, 1);   // 触发按键事件
        input_sync(keydev);                                 // 事件结束, 同步到用户空间
    }
}

static int input_keys_open(struct input_dev *dev)           // 观察用, 初始化代码建议全部放在init函数
{
    PINFO("input_keys_open \n");
    return 0;
}

static void input_keys_close(struct input_dev *dev)         // 观察用, 退出代码建议全部放在exit函数
{
    PINFO("input_keys_close \n");
}

static int __init input_keys_init(void)
{
    int i, res;

    PINFO("input_keys_init\n");
    input_keys_priv = kzalloc(sizeof(struct input_keys_private),GFP_KERNEL);
    /*===== 1. 分配一个input_dev结构体, 并初始化 =====*/
    input_keys_priv->dev = input_allocate_device();
    // 1.1 初始化后dev的一些内容
    input_keys_priv->dev->name = DRIVER_NAME;
    input_keys_priv->dev->open = input_keys_open;           // 可以注释掉
    input_keys_priv->dev->close = input_keys_close;         // 可以注释掉

    /*===== 2. 设置事件. =====*/
    // 2.1 设置event事件
    set_bit(EV_KEY,input_keys_priv->dev->evbit);            // 支持按键事件
    set_bit(EV_REP,input_keys_priv->dev->evbit);            // 支持按键连发功能
    // 2.2 设置key事件支持的按键值
    set_bit(KEY_L, input_keys_priv->dev->keybit);           // 支持按键 l
    set_bit(KEY_S, input_keys_priv->dev->keybit);           // 支持按键 s
    set_bit(KEY_ENTER, input_keys_priv->dev->keybit);       // 支持按键 enter
    set_bit(KEY_LEFTSHIFT, input_keys_priv->dev->keybit);   // shift

    // 1.2 其它初始化, 然后赋值这个私有结构体给 dev->private
    input_keys_priv->keysdesc = keys_desc_public;
    input_keys_priv->keys_timer.function = keys_timer_function;
    input_set_drvdata(input_keys_priv->dev , input_keys_priv);

    /*===== 3. 注册 input_device, 此处会去调用 open 函数 =====*/
    PINFO("input_keys_init_befor_register\n");
    res = input_register_device(input_keys_priv->dev);
    if(res<0) {
        PERR("input registration failed. error_id=%d\n", res);
        goto fail1;
    }
    PINFO("input_keys_init_after_register\n");

    /*===== 4. 硬件相关的操作, 这部分也可以放在open函数中 =====*/
    // 4.1 注册中断号, 设置中断类型, 设置中断名称(和设备名称无关), 传入自用的数据指针
    for (i = 0; i < 4; i++) {
        res = request_irq(keys_desc_public[i].irq, keys_irq, IRQT_BOTHEDGE, keys_desc_public[i].name, &keys_desc_public[i]);
        if (res<0) {
            PERR("request_irq(%d), error_id=%d\n", i, res);
            goto fail2;
        }
    }

    // 4.2 初始化timer, 用于按键延时防抖.
    init_timer(&input_keys_priv->keys_timer);
    add_timer(&input_keys_priv->keys_timer);
    return 0;

    // 错误处理部分.
fail2:
    for (i = 0; i < 4; i++) {
        free_irq(keys_desc_public[i].irq, &keys_desc_public[i]);
    }
fail1:
    input_unregister_device(input_keys_priv->dev);
    input_free_device(input_keys_priv->dev);
    kfree(input_keys_priv);
    return -EBUSY;
}

static void __exit input_keys_exit(void)
{
    int i;

    // exit 是 init 的反操作, 严格按照init的倒序执行!
    del_timer(&input_keys_priv->keys_timer);
    for (i = 0; i < 4; i++) {
        free_irq(keys_desc_public[i].irq, &keys_desc_public[i]);
    }

    PINFO("input_keys_exit_before_unregister\n");
    // 此处会调用 close 函数, 因此之前的内容也可以放到close函数中.
    input_unregister_device(input_keys_priv->dev);
    PINFO("input_keys_exit_after_unregister\n");
    input_free_device(input_keys_priv->dev);
    kfree(input_keys_priv);
    PINFO("input_keys_exit\n");
}

module_init(input_keys_init);
module_exit(input_keys_exit);
```

## input_keys.h
``` c
#define DRIVER_NAME "input_keys"
#define PDEBUG(fmt,args...) printk(KERN_DEBUG"%s:"fmt,DRIVER_NAME, ##args)
#define PERR(fmt,args...) printk(KERN_ERR"%s:"fmt,DRIVER_NAME,##args)
#define PINFO(fmt,args...) printk(KERN_INFO"%s:"fmt,DRIVER_NAME, ##args)
#include<linux/init.h>
#include<linux/input.h>
#include<linux/interrupt.h>
#include<linux/module.h>
#include<linux/slab.h>

#include <linux/irq.h>
#include <asm/gpio.h>
#include <asm/io.h>
#include <asm/arch/regs-gpio.h>
```

## Makefile

``` makefile
obj-m       := input_keys.o
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

``` bash
$ insmod input_keys.ko
input_keys:input_keys_init
input_keys:input_keys_init_befor_register
input: input_keys as /class/input/input1
input_keys:input_keys_open
input_keys:input_keys_init_after_register

# 方法一 (没有启动QT):
$ cat /dev/tty1             # keyboard.c 里面和tty有关联, 不去深究了.
# 依次按下 s2,s3 相当于输入了ls. 此处没有回显! 输入s4, 终端仅显示ls.

# 方法二 (没有启动QT):
$ exec 0</dev/tty1          # 将标准输入改为 /dey/tty1. (没有改标准输出, 因此还是会回显$)
$ ls                        # 依次按下 s2,s3,s4, 相当于输入了ls enter
# 显示文件夹内容

# 说明, 由于改了标准输入, 只能重启后键盘才会有效
# ls -l /proc/pid/fd 查看进程的文件描述符. pid值可以由top指令获得.

# 方法三 (有QT)
# 打开开发板上的记事本, 依次按下 s2,s3,s4, 会看到输入了ls enter.

$ rmmod input_keys.ko
input_keys:input_keys_exit_before_unregister
input_keys:input_keys_close
input_keys:input_keys_exit_after_unregister
input_keys:input_keys_exit
```

额外说一下 `hexdump` 的测试方法

``` bash
$ insmod input_keys.ko                             # 加载模块后, 会自动生成 /dev/event1
$ hexdump /dev/event1                              # 16进制显示event1设备在用户空间获得的数据
#字节数|   秒    |  微秒   | 类 |code|  value        # 小端模式, 低位在前!
0000000 0bb2 0000 0e48 000c 0001 0026 0001 0000    # input_event(keydev, EV_KEY, key_val, 1)
0000010 0bb2 0000 0e54 000c 0000 0000 0000 0000    # input_sync(keydev);
0000020 0bb2 0000 5815 000e 0001 0026 0000 0000    # input_event(keydev, EV_KEY, key_val, 0)
0000030 0bb2 0000 581f 000e 0000 0000 0000 0000    # input_sync(keydev);

# 分析这些数值含义的方法:
# 就是从硬件驱动调用了 input_event 开始逐步深入看, 发现会调用 input_handler->event.
# 于是找到 evdev.c 下的 evdev_event. 看到 client的赋值 和 kill_fasync给用户空间发送异步信号, 可知hexdump显示就是这些数据
# 然后, 查看 struct input_event, 将数据类型一一对应起来就可以了.
```


# 参考资料
- [arm 驱动进阶：输入子系统概念及架构](http://www.cnblogs.com/ITmelody/archive/2012/05/22/2513028.html) 图和流程说明很好
- [Linux Input子系统之第一篇（input_dev/input_handle/input_handler](http://blog.chinaunix.net/uid-29151914-id-3887032.html)
- [输入子系统（1）：数据结构总结](http://blog.csdn.net/Golf_research/article/details/53293601)
- [linux内核input子系统分析](http://www.bijishequ.com/detail/482153)
- [input_dev结构体分析](http://www.360doc.com/content/12/0606/21/7775902_216485127.shtml) 对结构体的注释比较完整
