---
title: 驱动之LCD驱动框架和实现
date: 2018-01-09
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


# LCD驱动框架分析

## 字符驱动基本步骤

根据之前写的驱动, 已经对linux驱动基本步骤比较熟悉了.
- 所有的驱动都会调用 `module_init` 和 `module_exit`, 从 `module_init` 开始看比较好.
- 定义并设置 `file_operations` 结构体, 然后实现里面的函数, 如open等.
- 获取`主设备号`, 可以手动分配, 也可以由系统自动分配
- 用 `register_chrdev` 注册字符设备. 核心过程如下:
    - `__register_chrdev_region` 注册/申请主设备号, 并申请子设备号范围.
    - `cdev_init` 用 `file_operations` 结构体初始化一个字符设备
    - `cdev_add` 用设备号向系统添加字符设备.
- 如果要用mdev自动加载驱动, 还需要在init里实现如下函数
    - `class_create`, 创建一个设备类. 可以在 `/sys/class/` 看到设备类名称
    - `device_create`, 创建和注册设备. 可以在 `/dev/` 看到设备名称
    - `class_device_create` 是低版本Linux的函数. 本质就是 `device_create`

## LCD驱动框架分析

Linux的LCD驱动用了分层分离的思想, 用到了platform框架.
- `/drivers/video/fbmem.c` frame buffer memory, 显存操作相关
    - `subsys_initcall(fbmem_init);` fbmem的初始化.
        - `register_chrdev(FB_MAJOR,"fb",&fb_fops)` 注册字符设备,
        - `fb_class = class_create(THIS_MODULE, "graphics");` 注册 graphics 设备类
        - 可以去`/sys/class/graphics` 看看, 下面有 fb0 和 fbcon 两个文件.
        - **这里没有注册设备, 因为视频控制器和具体硬件相关**
    - `registered_fb` 是具体设备给fbmem.c提供信息的关键!
        - `fb_read` `fb_write` 里都可以看到 `struct fb_info *info = registered_fb[fbidx];`
        - 然后, 函数根据 info 信息, 决定是进一步调用具体设备的 read write等函数, 还是使用默认代码.
    - `register_framebuffer(struct fb_info *fb_info)` 供LCD设备调用, 提交`registered_fb`信息并注册设备.
        - `device_create(fb_class, fb_info->device, MKDEV(FB_MAJOR, i), "fb%d", i)`
        - 真正注册一个LCD设备, 名字是fb0, fb1这样递加上去. 可以在 `/dev/` 里找到.
- `/drviers/video/s3c2410fb.c` 具体硬件的LCD驱动.
    - 这里用到了platform框架. `s3c2410fb.c` 是硬件相关的通用操作, 属于 `platform_driver`
    - `module_init` 里, 直接就是 `platform_driver_register`.
    - 我们知道platform框架里, `probe`函数是很关键的, 在drive和device匹配时, 就会调用它.
    - `probe`函数里, 初始化后, 可看到 `register_framebuffer(fbinfo);` 将LCD设备信息提交给fbmem.c, 并注册设备.
- `/arch/arm/mach-s3c2440/mach-smdk2440.c` 配置硬件参数的地方.
    - 这里是platform框架的 `platform_device`.
    - `smdk2440_machine_init` 初始化里
        - `s3c24xx_fb_set_platdata(&smdk2440_lcd_cfg);` 将LCD配置信息拷贝到 `s3c_device_lcd`
        - `platform_add_devices(smdk2440_devices, ARRAY_SIZE(smdk2440_devices));` 注册 platform_device 设备.
        - `smdk2440_devices` 里就包含了 `s3c_device_lcd`
    - 如果硬件平台不变, 只是换屏的话, 只需要修改 `mach-smdk2440.c` 即可. 这就是分层分离概念的意义所在.



补充说明 `fbmem.c` 的上层:

- `/drivers/video/console/fbcon.c` 在lcd上显示终端, 此文件和tty1关联.
    - `class_device_create(fb_class, NULL, MKDEV(0, 0), NULL, "fbcon");` 注册 `fbcon` 设备
    - `fbcon_start`  和 fb设备对接, 开始显示.
- app层调用 `open("/dev/fb0", ...)`, 主设备号为29, 次设备号为0
    - 会对应到kernel层 `fbmem.c` 的 `fb_open`函数:
    - `int fbidx = iminor(inode);`
    - `struct fb_info *info = = registered_fb[0];`
- app层调用 `read()`
    - 会对应到kernel层 `fbmem.c` 的 `fb_read`函数:
    - `registered_fb` 由 `register_framebuffer` 设置.

``` c
fb_read(struct file *file, char __user *buf, size_t count, loff_t *ppos) {
    int fbidx = iminor(inode);                              // 子设备号
    struct fb_info *info = registered_fb[fbidx];            // LCD硬件信息.
    if (info->fbops->fb_read)                               // 如果硬件由自己的read函数
        return info->fbops->fb_read(info, buf, count, ppos);// 调用后, 直接返回

    src = (u32 __iomem *) (info->screen_base + p);          // 获取显存地址
    dst = buffer;
    *dst++ = fb_readl(src++);
    copy_to_user(buf, buffer, c)                            // 将值返回给应用层. 获取显存内容
}
```


# LCD驱动源码

现在尝试忽略 `/drviers/video/s3c2410fb.c` 使用的platform框架.
直接自己写一个 LCD 驱动, 和 `/drivers/video/fbmem.c` 进行对接.
**此处只是为了练习, 实际项目不建议这样使用**

驱动的核心步骤如下:
1. 分配一个fb_info: `s3c_lcd = framebuffer_alloc(0, NULL);`
2. 设置fb_info
    2.1 设置固定的参数, `struct fb_fix_screeninfo`
    2.2 设置可变的参数, `struct fb_var_screeninfo`
    2.3 设置操作函数, `fbops`
    2.4 其他的设置
3. 硬件相关的操作
    3.1 配置GPIO用于LCD
    3.2 根据LCD手册设置LCD控制器, 比如VCLK的频率等
    3.3 分配显存(framebuffer), 并把地址告诉LCD控制器
4. 注册 `register_framebuffer(s3c_lcd);`


## 测试, 原系统

在使用自己写的LCD驱动源码之前, 先用系统提供的LCD框架驱动测试一下显示屏

``` bash
# 开发板端
$ vi /etc/inittab
    # ===== 设置为如下内容 =====
    ::sysinit:/etc/init.d/rcS
    s3c2410_serial0::askfirst:-/bin/sh
    # 增加了下面一行, 用于屏幕打开终端
    tty1::askfirst:-/bin/sh
    ::ctrlaltdel:/sbin/reboot
    ::shutdown:/bin/umount -a -r
    # ===== wq保存, 退出 =====
$ reboot
# 重启终端

# 重启后, 屏幕就会显示终端信息了. 提示输入Enter键来触发终端.
# 加载 "驱动之input子系统" 里的驱动
$ insmod input_keys.ko
# 按下S4按键, 相当于输入了 Enter
# 依次按下 S2, S3, S4, 就是输入了ls指令, 屏幕上会列出文件列表.
```

## lcd.c

``` c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/errno.h>
#include <linux/string.h>
#include <linux/mm.h>
#include <linux/slab.h>
#include <linux/delay.h>
#include <linux/fb.h>
#include <linux/init.h>
#include <linux/dma-mapping.h>
#include <linux/interrupt.h>
#include <linux/workqueue.h>
#include <linux/wait.h>
#include <linux/platform_device.h>
#include <linux/clk.h>

#include <asm/io.h>
#include <asm/uaccess.h>
#include <asm/div64.h>

#include <asm/mach/map.h>
#include <asm/arch/regs-lcd.h>
#include <asm/arch/regs-gpio.h>
#include <asm/arch/fb.h>

MODULE_LICENSE("GPL");

static int s3c_lcdfb_setcolreg(unsigned int regno, unsigned int red,
                 unsigned int green, unsigned int blue,
                 unsigned int transp, struct fb_info *info);

struct lcd_regs {                                   // LCD相关寄存器, 方便操作
    unsigned long   lcdcon1;
    unsigned long   lcdcon2;
    unsigned long   lcdcon3;
    unsigned long   lcdcon4;
    unsigned long   lcdcon5;
    unsigned long   lcdsaddr1;
    unsigned long   lcdsaddr2;
    unsigned long   lcdsaddr3;
    unsigned long   redlut;
    unsigned long   greenlut;
    unsigned long   bluelut;
    unsigned long   reserved[9];
    unsigned long   dithmode;
    unsigned long   tpal;
    unsigned long   lcdintpnd;
    unsigned long   lcdsrcpnd;
    unsigned long   lcdintmsk;
    unsigned long   lpcsel;
};

static struct fb_ops s3c_lcdfb_ops = {
    .owner          = THIS_MODULE,
    .fb_setcolreg   = s3c_lcdfb_setcolreg,          // 设置调色板, 用于色域转换(RGB->RGB565)
    /* 下面三个函数, 需要用 make modules 获得ko文件. 路径 "/drivers/video/cfb*.ko" */
    .fb_fillrect    = cfb_fillrect,                 // 理解为画矩形
    .fb_copyarea    = cfb_copyarea,                 // 理解为拷贝区域
    .fb_imageblit   = cfb_imageblit,                // 理解为画图
};


static struct fb_info *s3c_lcd;
static volatile unsigned long *gpbcon;              // GPIO口的操作
static volatile unsigned long *gpbdat;
static volatile unsigned long *gpccon;
static volatile unsigned long *gpdcon;
static volatile unsigned long *gpgcon;
static volatile struct lcd_regs* lcd_regs;
static u32 pseudo_palette[16];                      // 假调色板


/* from pxafb.c */
static inline unsigned int chan_to_field(unsigned int chan, struct fb_bitfield *bf)
{
    chan &= 0xffff;
    chan >>= 16 - bf->length;
    return chan << bf->offset;
}


// 设置调色板, 用于色域转换(RGB->RGB565)
static int s3c_lcdfb_setcolreg(unsigned int regno, unsigned int red,
                 unsigned int green, unsigned int blue,
                 unsigned int transp, struct fb_info *info)
{
    unsigned int val;

    if (regno > 16)                                 // 一个调色板里, 最多有16个小碟子
        return 1;

    /* 用red,green,blue三原色构造出val */             // 这里是压缩作用, 将红绿蓝压缩成16位真彩色.
    val  = chan_to_field(red,   &info->var.red);
    val |= chan_to_field(green, &info->var.green);
    val |= chan_to_field(blue,  &info->var.blue);

    pseudo_palette[regno] = val;
    return 0;
}

static int lcd_init(void)
{
    /* 1. 分配一个fb_info */
    s3c_lcd = framebuffer_alloc(0, NULL);

    /* 2. 设置 */
    /* 2.1 设置固定的参数, struct fb_fix_screeninfo */
    strcpy(s3c_lcd->fix.id, "mylcd");
    s3c_lcd->fix.smem_len = 480*272*16/8;           // 显存大小(字节), 长*宽*位宽/8 (这里用的RGB565, 2字节)
    s3c_lcd->fix.type     = FB_TYPE_PACKED_PIXELS;  // 压缩格式. 另外有 逐行/隔行/VGA等等
    s3c_lcd->fix.visual   = FB_VISUAL_TRUECOLOR;    // 真彩, 即65536色.
    s3c_lcd->fix.line_length = 480*2;               // 一行占用的字节

    /* 2.2 设置可变的参数, struct fb_var_screeninfo */
    s3c_lcd->var.xres           = 480;              // 实际的屏幕分辨率(像素点)
    s3c_lcd->var.yres           = 272;
    s3c_lcd->var.xres_virtual   = 480;              // 虚拟分辨率
    s3c_lcd->var.yres_virtual   = 272;
    s3c_lcd->var.bits_per_pixel = 16;               // 每个像素点的位宽
    s3c_lcd->var.red.offset     = 11;               // RGB565的位和位偏移
    s3c_lcd->var.red.length     = 5;
    s3c_lcd->var.green.offset   = 5;
    s3c_lcd->var.green.length   = 6;
    s3c_lcd->var.blue.offset    = 0;
    s3c_lcd->var.blue.length    = 5;
    s3c_lcd->var.activate       = FB_ACTIVATE_NOW;  // 实时显示

    /* 2.3 设置操作函数, fbops */
    s3c_lcd->fbops              = &s3c_lcdfb_ops;

    /* 2.4 其他的设置 */
    /* 调色板, 可以理解为色域转换用, 譬如输入是8位, 输出是16位的颜色, 就需要用到调色板 */
    s3c_lcd->pseudo_palette = pseudo_palette;       // 真彩屏需要使用假调色板, 用于色域转换
    //s3c_lcd->screen_base  = ;                     // 3.3处会设置, 显存的虚拟地址
    s3c_lcd->screen_size   = 480*272*16/8;          // Amount of ioremapped VRAM or 0

    /* 3. 硬件相关的操作 */
    /* 3.1 配置GPIO用于LCD */                        // 看原理图和数据手册. 此处不详述了.
    gpbcon = ioremap(0x56000010, 8);
    gpbdat = gpbcon+1;
    gpccon = ioremap(0x56000020, 4);
    gpdcon = ioremap(0x56000030, 4);
    gpgcon = ioremap(0x56000060, 4);

    *gpccon  = 0xaaaaaaaa;                          /* GPIO管脚用于VD[7:0],LCDVF[2:0],VM,VFRAME,VLINE,VCLK,LEND */
    *gpdcon  = 0xaaaaaaaa;                          /* GPIO管脚用于VD[23:8] */
    *gpbcon &= ~(3);                                /* GPB0设置为输出引脚 */
    *gpbcon |= 1;
    *gpbdat &= ~1;                                  /* 输出低电平 */
    *gpgcon |= (3<<8);                              /* GPG4用作LCD_PWREN */

    /* 3.2 根据LCD手册设置LCD控制器, 比如VCLK的频率等 */
    lcd_regs = ioremap(0x4D000000, sizeof(struct lcd_regs));

    /* bit[17:8]: VCLK = HCLK / [(CLKVAL+1) x 2], LCD手册P14
     *            10MHz(100ns) = 100MHz / [(CLKVAL+1) x 2]
     *            CLKVAL = 4
     * bit[6:5]: 0b11, TFT LCD
     * bit[4:1]: 0b1100, 16 bpp for TFT
     * bit[0]  : 0 = Disable the video output and the LCD control signal.
     */
    lcd_regs->lcdcon1  = (4<<8) | (3<<5) | (0x0c<<1);

#if 1
    /* 垂直方向的时间参数
     * bit[31:24]: VBPD, VSYNC之后再过多长时间才能发出第1行数据
     *             LCD手册 T0-T2-T1=4
     *             VBPD=3
     * bit[23:14]: 多少行, 320, 所以LINEVAL=320-1=319
     * bit[13:6] : VFPD, 发出最后一行数据之后，再过多长时间才发出VSYNC
     *             LCD手册T2-T5=322-320=2, 所以VFPD=2-1=1
     * bit[5:0]  : VSPW, VSYNC信号的脉冲宽度, LCD手册T1=1, 所以VSPW=1-1=0
     */
    lcd_regs->lcdcon2  = (1<<24) | (271<<14) | (1<<6) | (9);

    /* 水平方向的时间参数
     * bit[25:19]: HBPD, VSYNC之后再过多长时间才能发出第1行数据
     *             LCD手册 T6-T7-T8=17
     *             HBPD=16
     * bit[18:8]: 多少列, 240, 所以HOZVAL=240-1=239
     * bit[7:0] : HFPD, 发出最后一行里最后一个象素数据之后，再过多长时间才发出HSYNC
     *             LCD手册T8-T11=251-240=11, 所以HFPD=11-1=10
     */
    lcd_regs->lcdcon3 = (1<<19) | (479<<8) | (1);

    /* 水平方向的同步信号
     * bit[7:0] : HSPW, HSYNC信号的脉冲宽度, LCD手册T7=5, 所以HSPW=5-1=4
     */
    lcd_regs->lcdcon4 = 40;

#else
    lcd_regs->lcdcon2 = S3C2410_LCDCON2_VBPD(5) | \
        S3C2410_LCDCON2_LINEVAL(319) | \
        S3C2410_LCDCON2_VFPD(3) | \
        S3C2410_LCDCON2_VSPW(1);

    lcd_regs->lcdcon3 = S3C2410_LCDCON3_HBPD(10) | \
        S3C2410_LCDCON3_HOZVAL(239) | \
        S3C2410_LCDCON3_HFPD(1);

    lcd_regs->lcdcon4 = S3C2410_LCDCON4_MVAL(13) | \
        S3C2410_LCDCON4_HSPW(0);
#endif

    /* 信号的极性
     * bit[11]: 1=565 format
     * bit[10]: 0 = The video data is fetched at VCLK falling edge
     * bit[9] : 1 = HSYNC信号要反转,即低电平有效
     * bit[8] : 1 = VSYNC信号要反转,即低电平有效
     * bit[6] : 0 = VDEN不用反转
     * bit[3] : 0 = PWREN输出0
     * bit[1] : 0 = BSWP
     * bit[0] : 1 = HWSWP 2440手册P413
     */
    lcd_regs->lcdcon5 = (1<<11) | (0<<10) | (1<<9) | (1<<8) | (1<<0);

    /* 3.3 分配显存(framebuffer), 并把地址告诉LCD控制器 */
    /* dma_alloc_writecombine 会分配一段连续的内存地址给内核, 返回的是虚拟地址, 因此此处直接赋值给 s3c_lcd->screen_base
     * s3c_lcd->fix.smem_start, 表示显存的物理起始地址, 同样由函数 dma_alloc_writecombine 设置.
     * 关于分配函数的比较, 可以参考 http://blog.sina.com.cn/s/blog_4770ef020101oy2e.html 看最后一张图
    */
    s3c_lcd->screen_base = dma_alloc_writecombine(NULL, s3c_lcd->fix.smem_len, &s3c_lcd->fix.smem_start, GFP_KERNEL);
    lcd_regs->lcdsaddr1  = (s3c_lcd->fix.smem_start >> 1) & ~(3<<30);
    lcd_regs->lcdsaddr2  = ((s3c_lcd->fix.smem_start + s3c_lcd->fix.smem_len) >> 1) & 0x1fffff;
    lcd_regs->lcdsaddr3  = (480*16/16);                 /* 一行的长度(单位: 2字节) */

    /* 启动LCD */
    lcd_regs->lcdcon1 |= (1<<0);                        /* 使能LCD控制器 */
    lcd_regs->lcdcon5 |= (1<<3);                        /* 使能LCD本身 */
    *gpbdat |= 1;                                       /* 输出高电平, 使能背光 */

    /* 4. 注册 */
    register_framebuffer(s3c_lcd);

    return 0;
}

static void lcd_exit(void)
{
    unregister_framebuffer(s3c_lcd);
    lcd_regs->lcdcon1 &= ~(1<<0);                       /* 关闭LCD本身 */
    *gpbdat &= ~1;                                      /* 关闭背光 */
    dma_free_writecombine(NULL, s3c_lcd->fix.smem_len, s3c_lcd->screen_base, s3c_lcd->fix.smem_start);
    iounmap(lcd_regs);
    iounmap(gpbcon);
    iounmap(gpccon);
    iounmap(gpdcon);
    iounmap(gpgcon);
    framebuffer_release(s3c_lcd);
}

module_init(lcd_init);
module_exit(lcd_exit);
```


## Makefile

``` makefile
obj-m       := lcd.o
KERN_SRC    := /home/draapho/share/jz2440/kernel/linux-2.6.22.6/
PWD         := $(shell pwd)

modules:
    make -C $(KERN_SRC) M=$(PWD) modules

clean:
    make -C $(KERN_SRC) M=$(PWD) clean
```

## 测试

这个测试比较复杂, 需要去掉自带的LCD驱动, 重新编译和烧录内核.

``` bash
# Ubuntu 主机端
# pwd = ./linux-2.6.22.6_no_lcd  复制一个新的内核源码目录

$ make clean
$ make menuconfig                       # 去掉原来的S3C2410驱动程序
# -> Device Drivers
# -> Graphics support
# <M> S3C2410 LCD framebuffer support
# 改为 M, 因为我们需要编译出里面的 "/drivers/video/cfb*.ko" 三个文件

$ make uImage
$ make modules
$ cp ./drivers/video/cfb*.ko ~/share/jz2440/drivers/lcd/    # 拷贝到lcd驱动目录

# 烧录新的uImage
# 重启开发板进入uboot烧录界面, 按k准备烧录内核. 略过不表
$ sudo dnw ./arch/arm/boot/uImage

# pwd = ~/share/jz2440/drivers/lcd/     # lcd驱动目录
$ make modules                          # 生成lcd.ko


# 开发板端
# pwd = ./share/jz2440/drivers/lcd/    # lcd驱动源码目录, nfs文件
$ insmod cfbcopyarea.ko
$ insmod cfbfillrect.ko
$ insmod cfbimgblt.ko
$ insmod lcd.ko
# 如果 /etc/inittab 已经增加过 tty1::askfirst:-/bin/sh 这么一行, 屏幕就会显示终端信息了.

# pwd = ./share/jz2440/drivers/input_keys/KERN_SRC  # input_keys源码路径, nfs文件
$ insmod input_keys.ko
# 按下 S4 输入Enter, 使能屏幕终端(即tty1),
# 依次按下 S2, S3, S4, 就是输入了ls指令, 屏幕上会列出文件列表.

# 开发板端, 其它测试方法
echo hello > /dev/tty1  // 可以在LCD上看见hello, tty1会用到 fbcon.c文件
cat lcd.ko > /dev/fb0   // 花屏
```


# 参考资料
- [Framebuffer兩三事-Test On QT2410](http://daydreamer.idv.tw/rewrite.php/read-42.html)
- [常见的Linux内核中内存分配函数](http://blog.sina.com.cn/s/blog_4770ef020101oy2e.html) 看最后一张图


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***