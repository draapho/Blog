---
title: 驱动之触摸屏驱动框架和实现
date: 2018-01-11
categories: embedded linux
tags: [embedded linux, driver]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之input子系统](https://draapho.github.io/2018/01/05/1802-drv-input/)
- [驱动之platform概念](https://draapho.github.io/2018/01/08/1803-drv-platform/)
- [驱动之LCD驱动框架和实现](https://draapho.github.io/2018/01/09/1804-drv-lcd/)
- [驱动之触摸屏驱动框架和实现](https://draapho.github.io/2018/01/11/1806-drv-ts/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.


# 触摸屏驱动框架分析

## 回顾input子系统
在 [驱动之input子系统](https://draapho.github.io/2018/01/05/1802-drv-input/) 一文里, 已经介绍了input子系统的框架.
触摸驱动作为输入设备, 很自然的需要用到input子系统.
input子系统, 核心点如下:
- 软件抽象层, `/drivers/input/input.c` `/drviers/input/*dev.c`
    - 初始化 `input_handler` 结构体变量, 负责软件抽象.
    - 提供 `input_register_handler` 函数
    - 提供 `input_register_handle(没有r)` 函数
    - 提供 `input_register_device` 函数
- 连接层, `/drviers/input/*dev.c`
    - 初始化 `input_handle(没有r)` 结构体变量, 负责input系统的软硬层对接
    - 注册此变量 `input_register_handle(没有r)`
    - 当注册handler或者device时, 会自动调用 `handler->connect`, 匹配并关联软件抽象层和硬件设备层.
- 硬件设备层, 需要自己来实现
    - 负责具体的硬件功能实现.
    - 初始化 `input_dev` 结构体变量
    - 注册此变量 `input_register_device`
    - 实现硬件相关代码. 上报事件 `input_event`

## s3c2410的触摸屏框架

s3c2410的触摸屏框架使用了input层. 硬件设备层又使用了platform框架来进一步隔离硬件上的通用代码和专用参数设置.
platform总线系统的详情可查看 [驱动之platform概念](https://draapho.github.io/2018/01/08/1803-drv-platform/)
整个框架层次如下图:

![ts](https://draapho.github.io/images/1806/ts.png)

platform 总线框架具体分析如下:
- platform_driver `/drivers/input/touchscreen/s3c2410_ts.c`
    - 调用 `platform_driver_register(&s3c2410ts_driver);`
    - 匹配时, 执行 `s3c2410ts_probe`
        - 和想的不一样, 用的 `evbit` 而不是 `absbit`
        - `ts.dev->evbit[0] = BIT(EV_SYN) | BIT(EV_KEY) | BIT(EV_ABS);`
        - `ts.dev->keybit[LONG(BTN_TOUCH)] = BIT(BTN_TOUCH);`
        - 然后向input系统注册device `input_register_device(ts.dev);`
    - timer超时函数 `touch_timer_fire`, 检测和发送触摸事件
        - `input_report_abs`
        - `input_report_key`
- platform_device `/arch/arm/plat-s3c24xx/common-smdk.c`
    - 调用 `platform_add_devices(smdk_devs, ARRAY_SIZE(smdk_devs));`
    - `smdk_devs` 里面包含了 `s3c_device_ts`
    - 通过 `set_s3c2410ts_info` 函数来设置 `s3c_device_ts`



# 测试触摸屏驱动

这里用的开发板自带的触摸屏驱动, 先测试一下.

## 方法一 hexdump

``` bash
# 开发板端
$ ls /dev/event*
# 系统自带的一般是 event0, 对应触摸屏事件
$ hexdump /dev/event0
# 字节数|   秒    |   微秒   |type|code|  value       # 小端模式, 低位在前!
0000000 04aa 0000 8555 000b 0003 0000 0138 0000     # input_report_abs(ts.dev, ABS_X, ts.xp);
0000010 04aa 0000 8569 000b 0003 0001 020e 0000     # input_report_abs(ts.dev, ABS_Y, ts.yp);
0000020 04aa 0000 856e 000b 0001 014a 0001 0000     # input_report_key(ts.dev, BTN_TOUCH, 1);
0000030 04aa 0000 8570 000b 0003 0018 0001 0000     # input_report_abs(ts.dev, ABS_PRESSURE, 1);
0000040 04aa 0000 8573 000b 0000 0000 0000 0000     # input_sync(ts.dev);
```

## 方法二 tslib

``` bash
# Ubuntu 主机端, 需要先编译 tslib
# pwd = ./drivers/ts
$ tar xzf tslib-1.4.tar.gz
$ cd tslib
$ ./autogen.sh

# 报错: ./autogen.sh: 4: autoreconf: not found
# 报错: configure.ac:25: error: possibly undefined macro: AC_DISABLE_STATIC
# sudo apt-get install autoconf automake libtool # 安装相关软件即可

$ mkdir tmp
$ echo "ac_cv_func_malloc_0_nonnull=yes" >arm-linux.cache
$ ./configure --host=arm-linux --cache-file=arm-linux.cache --prefix=$(pwd)/tmp
$ make
$ make install
$ ll tmp/bin                                # 查看一下编译结果.
$ vi tmp/etc/ts.conf
# ===== 修改第二行 =====
    # module_raw input
    # 取消注释, 改为:
    module_raw input
# ===== wq 保存退出 =====


# 开发板端
# pwd = ./drivers/ts/tslib/tmp              # 挂载的nfs文件系统
$ cp * -rf /                                # 拷贝到根目录

# 设置环境变量
$ export TSLIB_TSDEVICE=/dev/event0         # 必须对应ts的event
$ export TSLIB_CALIBFILE=/etc/pointercal
$ export TSLIB_CONFFILE=/etc/ts.conf
$ export TSLIB_PLUGINDIR=/lib/ts
$ export TSLIB_CONSOLEDEVICE=none
$ export TSLIB_FBDEVICE=/dev/fb0            # 对应屏幕的framebuffer

# 开始测试
$ ts_calibrate                              # 五点校验
xres = 480, yres = 272
Top left :
Top right :
Bot right :
Bot left :
Center :
$ ts_test                                   # 开始测试
时间: X坐标 Y坐标 是否按下
$ ts_print_raw                              # 打印原始数据
时间: X电压值 Y电压值 是否按下
```

# 源码, 第一版
第一版源码, 让触摸屏工作起来即可

## ts.c

``` c
#include <linux/errno.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/input.h>
#include <linux/init.h>
#include <linux/serio.h>
#include <linux/delay.h>
#include <linux/platform_device.h>
#include <linux/clk.h>
#include <asm/io.h>
#include <asm/irq.h>

#include <asm/plat-s3c24xx/ts.h>
#include <asm/arch/regs-adc.h>
#include <asm/arch/regs-gpio.h>

MODULE_LICENSE("GPL");

struct s3c_ts_regs {                                // 触摸屏寄存器
    unsigned long adccon;
    unsigned long adctsc;
    unsigned long adcdly;
    unsigned long adcdat0;
    unsigned long adcdat1;
    unsigned long adcupdn;
};

static struct input_dev *s3c_ts_dev;
static volatile struct s3c_ts_regs *s3c_ts_regs;

// 几个模式的设置
static void enter_wait_pen_down_mode(void)
{
    s3c_ts_regs->adctsc = 0xd3;
}

static void enter_wait_pen_up_mode(void)
{
    s3c_ts_regs->adctsc = 0x1d3;
}

static void enter_measure_xy_mode(void)
{
    s3c_ts_regs->adctsc = (1<<3)|(1<<2);
}

static void start_adc(void)
{
    s3c_ts_regs->adccon |= (1<<0);
}

// 触摸事件中断, 按下或松开触摸屏
static irqreturn_t pen_down_up_irq(int irq, void *dev_id)
{
    if (s3c_ts_regs->adcdat0 & (1<<15))
    {
        printk("pen up\n");
        enter_wait_pen_down_mode();
    }
    else
    {
        //printk("pen down\n");
        //enter_wait_pen_up_mode();
        enter_measure_xy_mode();                    // 按下了, 准备开始测量
        start_adc();                                // 测量adc
    }
    return IRQ_HANDLED;
}

// ADC完成中断
static irqreturn_t adc_irq(int irq, void *dev_id)
{
    static int cnt = 0;
    printk("adc_irq cnt = %d, x = %d, y = %d\n", ++cnt,
        s3c_ts_regs->adcdat0 & 0x3ff, s3c_ts_regs->adcdat1 & 0x3ff);
                                                    // 打印测量结果
    enter_wait_pen_up_mode();
    return IRQ_HANDLED;
}

static int s3c_ts_init(void)
{
    struct clk* clk;

    /* 1. 分配一个input_dev结构体 */
    s3c_ts_dev = input_allocate_device();

    /* 2. 设置 */
    /* 2.1 能产生哪类事件 */
    set_bit(EV_KEY, s3c_ts_dev->evbit);             // 按键事件
    set_bit(EV_ABS, s3c_ts_dev->evbit);             // 绝对坐标事件

    /* 2.2 能产生按键事件里的哪些值 */
    set_bit(BTN_TOUCH, s3c_ts_dev->keybit);         // 键盘的虚拟按键

    input_set_abs_params(s3c_ts_dev, ABS_X, 0, 0x3FF, 0, 0);    // 绝对坐标范围设置
    input_set_abs_params(s3c_ts_dev, ABS_Y, 0, 0x3FF, 0, 0);
    input_set_abs_params(s3c_ts_dev, ABS_PRESSURE, 0, 1, 0, 0); // 是否按压, 理解为Z轴即可.


    /* 3. 注册 */
    input_register_device(s3c_ts_dev);

    /* 4. 硬件相关的操作 */
    /* 4.1 使能时钟(CLKCON[15]) */
    clk = clk_get(NULL, "adc");
    clk_enable(clk);

    /* 4.2 设置S3C2440的ADC/TS寄存器 */
    s3c_ts_regs = ioremap(0x58000000, sizeof(struct s3c_ts_regs));

    /* bit[14]  : 1-A/D converter prescaler enable
     * bit[13:6]: A/D converter prescaler value,
     *            49, ADCCLK=PCLK/(49+1)=50MHz/(49+1)=1MHz
     * bit[0]: A/D conversion starts by enable. 先设为0
     */
    s3c_ts_regs->adccon = (1<<14)|(49<<6);

    // 使能两个中断
    request_irq(IRQ_TC, pen_down_up_irq, IRQF_SAMPLE_RANDOM, "ts_pen", NULL);
    request_irq(IRQ_ADC, adc_irq, IRQF_SAMPLE_RANDOM, "adc", NULL);

    enter_wait_pen_down_mode();
    return 0;
}

static void s3c_ts_exit(void)
{
    free_irq(IRQ_TC, NULL);
    iounmap(s3c_ts_regs);
    input_unregister_device(s3c_ts_dev);
    input_free_device(s3c_ts_dev);
}

module_init(s3c_ts_init);
module_exit(s3c_ts_exit);
```

## Makefile
``` c
obj-m       := ts.o
KERN_SRC    := /home/draapho/share/jz2440/kernel/linux-2.6.22.6/
PWD         := $(shell pwd)

modules:
    make -C $(KERN_SRC) M=$(PWD) modules

clean:
    make -C $(KERN_SRC) M=$(PWD) clean
```

## 测试

由于内核自带了驱动程序, 因此需要重新编译内核, 去掉触摸驱动

```
# Ubuntu 主机端
# pwd = ./linux-2.6.22.6_no_lcd  借用之前的 no_lcd 内核, 或者自己拷贝一份内核源码

$ make clean
$ make menuconfig                               # 去掉自带的触摸屏驱动程序
# -> Device Drivers
#   -> Input device support
#     -> Touchscreens
#       < > S3C2410/S3C2440 touchscreens        # 取消触摸屏驱动
# -> Device Drivers
#   -> Graphics support
#     <*> S3C2410 LCD framebuffer support       # 加上自带的LCD驱动

$ make uImage
# 烧录新的uImage
# 重启开发板进入uboot烧录界面, 按k准备烧录内核. 略过不表
$ sudo dnw ./arch/arm/boot/uImage

# pwd = ~/share/jz2440/drivers/ts/              # 触摸屏驱动目录
$ make modules                                  # 生成ts.ko


# 开发板端
# pwd = ~/share/jz2440/drivers/ts/              # 触摸屏驱动目录, nfs
$ insmod ts.ko                                  # 加载驱动, 开始测试
input: Unspecified device as /class/input/input0
adc_irq cnt = 1, x = 17, y = 991
pen up
# 点击触摸屏, 就会打印出坐标, 释放时, 就会显示 pen up
# 至此, 说明触摸屏的硬件设置没有问题!
```

# 源码, 第二版

第一版的源码用于检测触摸屏的硬件设置是否正确, 触摸屏是否能正常工作.
但在实际情况下, 对触摸屏的ADC值还需要进行软件滤波等工作, 以提高可用性.
另外我们去掉了printk的打印信息, 改为 `input_report_abs` `input_report_key`

## ts.c

为方便理解, 减少代码量, 和源码第一版相同的部分删掉了.
譬如头文件, 小函数等.

``` c
static struct timer_list ts_timer;

// 软件过滤用, 如果4次ADC值的差值过大, 直接丢弃
static int s3c_filter_ts(int x[], int y[])
{
    #define ERR_LIMIT 10                                    // 这是个经验值

    int avr_x, avr_y;
    int det_x, det_y;

    avr_x = (x[0] + x[1])/2;                                // 获得数据0,1的平均值
    avr_y = (y[0] + y[1])/2;
    det_x = (x[2] > avr_x) ? (x[2] - avr_x) : (avr_x - x[2]);// 求数据2的差值
    det_y = (y[2] > avr_y) ? (y[2] - avr_y) : (avr_y - y[2]);
    if ((det_x > ERR_LIMIT) || (det_y > ERR_LIMIT))         // 差值太大, 丢弃整组数据
        return 0;

    avr_x = (x[1] + x[2])/2;                                // 获得数据1,2的平均值
    avr_y = (y[1] + y[2])/2;
    det_x = (x[3] > avr_x) ? (x[3] - avr_x) : (avr_x - x[3]);// 求数据3的差值
    det_y = (y[3] > avr_y) ? (y[3] - avr_y) : (avr_y - y[3]);
    if ((det_x > ERR_LIMIT) || (det_y > ERR_LIMIT))         // 差值太大, 丢弃整组数据
        return 0;

    return 1;
}

// 定时器, 用去测量触摸屏长按和移动. 在adc中断函数里触发
static void s3c_ts_timer_function(unsigned long data)
{
    if (s3c_ts_regs->adcdat0 & (1<<15))
    {
        /* 已经松开 */                                       // 向input层报告事件
        input_report_abs(s3c_ts_dev, ABS_PRESSURE, 0);
        input_report_key(s3c_ts_dev, BTN_TOUCH, 0);
        input_sync(s3c_ts_dev);
        enter_wait_pen_down_mode();
    }
    else
    {
        /* 测量X/Y坐标 */
        enter_measure_xy_mode();                            // 没有松开, 周期性测量
        start_adc();                                        // 触发adc, adc完成后又会触发定时器, 形成周期测量.
    }
}

// 触摸事件中断, 按下或松开触摸屏
static irqreturn_t pen_down_up_irq(int irq, void *dev_id)
{
    if (s3c_ts_regs->adcdat0 & (1<<15))
    {
        //printk("pen up\n");                               // 松开, 向input层报告事件
        input_report_abs(s3c_ts_dev, ABS_PRESSURE, 0);
        input_report_key(s3c_ts_dev, BTN_TOUCH, 0);
        input_sync(s3c_ts_dev);
        enter_wait_pen_down_mode();
    }
    else
    {
        //printk("pen down\n");
        //enter_wait_pen_up_mode();
        enter_measure_xy_mode();                            // 刚按下, 开始测量
        start_adc();
    }
    return IRQ_HANDLED;
}

// ADC完成中断
static irqreturn_t adc_irq(int irq, void *dev_id)
{
    static int cnt = 0;
    static int x[4], y[4];
    int adcdat0, adcdat1;

    /* 优化措施2: 如果ADC完成时, 发现触摸笔已经松开, 则丢弃此次结果 */
    adcdat0 = s3c_ts_regs->adcdat0;
    adcdat1 = s3c_ts_regs->adcdat1;

    if (s3c_ts_regs->adcdat0 & (1<<15))
    {
        /* 已经松开 */
        cnt = 0;
        input_report_abs(s3c_ts_dev, ABS_PRESSURE, 0);
        input_report_key(s3c_ts_dev, BTN_TOUCH, 0);
        input_sync(s3c_ts_dev);
        enter_wait_pen_down_mode();
    }
    else
    {
        // printk("adc_irq cnt = %d, x = %d, y = %d\n", ++cnt, adcdat0 & 0x3ff, adcdat1 & 0x3ff);
        /* 优化措施3: 多次测量求平均值 */
        x[cnt] = adcdat0 & 0x3ff;
        y[cnt] = adcdat1 & 0x3ff;
        ++cnt;
        if (cnt == 4)
        {
            /* 优化措施4: 软件过滤 */
            if (s3c_filter_ts(x, y))
            {
                //printk("x = %d, y = %d\n", (x[0]+x[1]+x[2]+x[3])/4, (y[0]+y[1]+y[2]+y[3])/4);
                input_report_abs(s3c_ts_dev, ABS_X, (x[0]+x[1]+x[2]+x[3])/4);
                input_report_abs(s3c_ts_dev, ABS_Y, (y[0]+y[1]+y[2]+y[3])/4);
                input_report_abs(s3c_ts_dev, ABS_PRESSURE, 1);
                input_report_key(s3c_ts_dev, BTN_TOUCH, 1);
                input_sync(s3c_ts_dev);
            }
            cnt = 0;
            enter_wait_pen_up_mode();

            /* 启动定时器处理长按/滑动的情况 */
            mod_timer(&ts_timer, jiffies + HZ/100);
        }
        else
        {
            enter_measure_xy_mode();
            start_adc();
        }
    }

    return IRQ_HANDLED;
}

static int s3c_ts_init(void)
{
    ......                          // 硬件配置都一样, 略过

    // 使能两个中断
    request_irq(IRQ_TC, pen_down_up_irq, IRQF_SAMPLE_RANDOM, "ts_pen", NULL);
    request_irq(IRQ_ADC, adc_irq, IRQF_SAMPLE_RANDOM, "adc", NULL);

    /* 优化措施1:
     * 设置ADCDLY为最大值, 这使得电压稳定后再发出IRQ_TC中断
     */
    s3c_ts_regs->adcdly = 0xffff;

    /* 优化措施5: 使用定时器处理长按,滑动的情况 */
    init_timer(&ts_timer);
    ts_timer.function = s3c_ts_timer_function;
    add_timer(&ts_timer);

    enter_wait_pen_down_mode();
    return 0;
}

static void s3c_ts_exit(void)
{
    free_irq(IRQ_TC, NULL);
    free_irq(IRQ_ADC, NULL);
    iounmap(s3c_ts_regs);
    input_unregister_device(s3c_ts_dev);
    input_free_device(s3c_ts_dev);
    del_timer(&ts_timer);
}
```

## 测试

``` bash
# 先按照此文之前的测试步骤设置好tslib, 烧录无触摸屏驱动的内核文件.

# 开发板端
# pwd = ./drivers/ts/                               # 挂载的nfs文件系统
$ rmmod ts                                          # 卸载源码第一版加载的触摸屏驱动
$ ls /dev/event*
$ insmod ts.ko                                      # 加载驱动
$ ls /dev/event*
# 多出的一个event, 就是触摸屏的event, 譬如event0


# 方法一, 用hexdump测试

$ hexdump /dev/event0
# 字节数|   秒    |   微秒   |type|code|  value       # 小端模式, 低位在前!
0000000 04aa 0000 8555 000b 0003 0000 0138 0000     # input_report_abs(ts.dev, ABS_X, ts.xp);
0000010 04aa 0000 8569 000b 0003 0001 020e 0000     # input_report_abs(ts.dev, ABS_Y, ts.yp);
0000030 04aa 0000 8570 000b 0003 0018 0001 0000     # input_report_abs(ts.dev, ABS_PRESSURE, 1);
0000020 04aa 0000 856e 000b 0001 014a 0001 0000     # input_report_key(ts.dev, BTN_TOUCH, 1);
0000040 04aa 0000 8573 000b 0000 0000 0000 0000     # input_sync(ts.dev);


# 方法二, 用tslib测试

# 设置环境变量
$ export TSLIB_TSDEVICE=/dev/event0         # 必须对应ts的event
$ export TSLIB_CALIBFILE=/etc/pointercal
$ export TSLIB_CONFFILE=/etc/ts.conf
$ export TSLIB_PLUGINDIR=/lib/ts
$ export TSLIB_CONSOLEDEVICE=none
$ export TSLIB_FBDEVICE=/dev/fb0            # 对应屏幕的framebuffer

# 开始测试
$ ts_calibrate                              # 五点校验
xres = 480, yres = 272
Top left :
Top right :
Bot right :
Bot left :
Center :
$ ts_test                                   # 开始测试
时间: X坐标 Y坐标 是否按下
$ ts_print_raw                              # 打印原始数据
时间: X电压值 Y电压值 是否按下
```

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***