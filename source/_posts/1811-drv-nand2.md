---
title: 驱动之NAND Flash源码
date: 2018-01-25
categories: embedded linux
tags: [embedded linux, driver]
description: 如题.
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之块设备-框架](https://draapho.github.io/2018/01/22/1809-drv-blk/)
- [驱动之NAND Flash框架](https://draapho.github.io/2018/01/24/1810-drv-nand1/)
- [驱动之NAND Flash源码](https://draapho.github.io/2018/01/25/1811-drv-nand2/)
- [驱动之NOR Flash](https://draapho.github.io/2018/01/26/1812-drv-nor/)
- [驱动之网卡驱动](https://draapho.github.io/2018/02/06/1813-drv-net/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.


# 源码

由 **nand flash 系统框架** 分析可知, Linux内核系统以及完成了Nand Flash设备的绝大部分的核心工作.
因此Nand Flash驱动真正要做的工作主要就是:
- 分配并初始化 `nand_chip` 结构体
- 初始化硬件
- 调用 `nand_scan`
- 调用 `add_mtd_partitions`


可以参考内核文件的相关源码, 学着写.
- `drivers\mtd\nand\at91_nand.c`
- `drivers\mtd\nand\s3c2410.c`



流程如下图:
![nand3](https://draapho.github.io/images/1810/nand3.jpg)

## s3c_nand.c

``` c
#include <linux/slab.h>
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/mtd/mtd.h>
#include <linux/mtd/nand.h>
#include <linux/mtd/partitions.h>
#include <linux/clk.h>

#include <asm/io.h>
#include <asm/arch/regs-nand.h>
#include <asm/arch/nand.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

struct s3c_nand_regs {                              // 2440芯片NAND Flash相关寄存器
    unsigned long nfconf  ;                         // 物理地址 0x4E000000
    unsigned long nfcont  ;
    unsigned long nfcmd   ;
    unsigned long nfaddr  ;
    unsigned long nfdata  ;
    unsigned long nfeccd0 ;
    unsigned long nfeccd1 ;
    unsigned long nfeccd  ;
    unsigned long nfstat  ;
    unsigned long nfestat0;
    unsigned long nfestat1;
    unsigned long nfmecc0 ;
    unsigned long nfmecc1 ;
    unsigned long nfsecc  ;
    unsigned long nfsblk  ;
    unsigned long nfeblk  ;
};


static struct nand_chip *s3c_nand;                  // NAND Flash操作的核心结构体
static struct mtd_info *s3c_mtd;                    // 给两个系统函数使用的结构体
static struct s3c_nand_regs *s3c_nand_regs;

static struct mtd_partition s3c_nand_parts[] = {    // 分区信息
    [0] = {
        .name   = "bootloader",
        .size   = 0x00040000,
        .offset = 0,
    },
    [1] = {
        .name   = "params",
        .offset = MTDPART_OFS_APPEND,
        .size   = 0x00020000,
    },
    [2] = {
        .name   = "kernel",
        .offset = MTDPART_OFS_APPEND,
        .size   = 0x00200000,
    },
    [3] = {
        .name   = "root",
        .offset = MTDPART_OFS_APPEND,
        .size   = MTDPART_SIZ_FULL,
    }
};

// 不能用Linux默认的片选函数(nand_set_defaults), 自己根据数据手册写一下.
static void s3c2440_select_chip(struct mtd_info *mtd, int chipnr)
{
    if (chipnr == -1) {
        s3c_nand_regs->nfcont |= (1<<1);            // NFCONT bit1=1, 取消片选
    } else {
        s3c_nand_regs->nfcont &= ~(1<<1);           // NFCONT bit1=0, 使能片选
    }
}

static void s3c2440_cmd_ctrl(struct mtd_info *mtd, int dat, unsigned int ctrl)
{
    if (ctrl & NAND_CLE) {
        s3c_nand_regs->nfcmd = dat;                 // NFCMMD=dat, 发送命令
    } else {
        s3c_nand_regs->nfaddr = dat;                // NFADDR=dat, 发送地址
    }
}

static int s3c2440_dev_ready(struct mtd_info *mtd)
{
    return (s3c_nand_regs->nfstat & (1<<0));        // NFSTAT bit0=0, Busy else Ready
}

static int s3c_nand_init(void)
{
    struct clk *clk;

    /* 1. 分配nand_chip 和 mtd_info 结构体 */
    s3c_nand = kzalloc(sizeof(struct nand_chip), GFP_KERNEL);
    s3c_mtd = kzalloc(sizeof(struct mtd_info), GFP_KERNEL);

    // 获得寄存器的虚拟地址. 0x4E000000是这些寄存器的起始物理地址
    s3c_nand_regs = ioremap(0x4E000000, sizeof(struct s3c_nand_regs));


    /* 2. 设置nand_chip */
    /* nand_chip 需要提供 NAND Flash 操作的基本函数. 通用的函数已经由 nand_set_defaults 设置好了.
     * 需要自己设置的函数主要有: 片选,发指令,发地址,发数据,读数据,判断状态的功能
     */
    s3c_nand->select_chip = s3c2440_select_chip;    // 片选函数
    s3c_nand->cmd_ctrl    = s3c2440_cmd_ctrl;       // 发送指令/地址
    s3c_nand->IO_ADDR_R   = &s3c_nand_regs->nfdata; // 读数据的虚拟地址
    s3c_nand->IO_ADDR_W   = &s3c_nand_regs->nfdata; // 发数据的虚拟地址
    s3c_nand->dev_ready   = s3c2440_dev_ready;      // 芯片Busy/Ready的状态反馈
    s3c_nand->ecc.mode    = NAND_ECC_SOFT;          // ECC校验方式. 软件或硬件.


    /* 3. 硬件相关的设置: 根据NAND FLASH的手册设置时间参数 */
    // 使能NAND控制器的时钟
    clk = clk_get(NULL, "nand");                    // 由名称"nand"获得时钟
    clk_enable(clk);                                // 实际上就是 CLKCON bit[4]=1

    // 设置 NFCONF 寄存器. 由启动的打印信息可获得 HCLK=100MHz, 设置时序要求.
#define TACLS    0  // 发出CLE/ALE之后多长时间才发出nWE信号, 从NAND手册可知CLE/ALE与nWE可以同时发出,所以TACLS=0
#define TWRPH0   1  // nWE的脉冲宽度, HCLK x ( TWRPH0 + 1 ), 从NAND手册可知它要>=12ns, 所以TWRPH0>=1
#define TWRPH1   0  // nWE变为高电平后多长时间CLE/ALE才能变为低电平, 从NAND手册可知它要>=5ns, 所以TWRPH1>=0
    s3c_nand_regs->nfconf = (TACLS<<12) | (TWRPH0<<8) | (TWRPH1<<4);

    // 设置 NFCONT 寄存器. BIT1=1, 取消片选. BIT0=1, 使能NAND控制器
    s3c_nand_regs->nfcont = (1<<1) | (1<<0);


    /* 4. 使用: nand_scan */
    s3c_mtd->owner = THIS_MODULE;
    s3c_mtd->priv  = s3c_nand;
    nand_scan(s3c_mtd, 1);                          // 识别NAND FLASH, 构造mtd_info. 硬件只有1块NAND Flash.


    /* 5. add_mtd_partitions
     * 增加 add_mtd_partitions 函数后,
     * 内核必须去掉自带的NAND Flash驱动, 从NFS启动系统.
     * 确认要做这个实验的时候, 再取消下面的注释, 编译测试
     * 如果不需要分区, 只需调用 add_mtd_device(s3c_mtd);
     */
    // add_mtd_partitions(s3c_mtd, s3c_nand_parts, 4);  // 告知分区要求, 调用 add_mtd_partitions

    return 0;
}

static void s3c_nand_exit(void)
{
    del_mtd_partitions(s3c_mtd);
    iounmap(s3c_nand_regs);
    kfree(s3c_mtd);
    kfree(s3c_nand);
}

module_init(s3c_nand_init);
module_exit(s3c_nand_exit);
```

## Makefile

``` makefile
obj-m       := s3c_nand.o
KERN_SRC    := /home/draapho/share/jz2440/kernel/linux-2.6.22.6/
PWD         := $(shell pwd)

modules:
    make -C $(KERN_SRC) M=$(PWD) modules

clean:
    make -C $(KERN_SRC) M=$(PWD) clean
```

## 测试1

源码没有调用 `add_mtd_partitions` 时, 简单测试一下NAND Flash是否正常工作了.

``` bash
# Ubuntu 主机端
# pwd = ~/share/jz2440/drivers/nand/            # NAND flash驱动目录
$ make modules                                  # 生成s3c_nand.ko, 忽略 s3c_nand_parts 没有使用的警告信息

# 开发板端, 开始测试
# pwd = ~/share/jz2440/drivers/nand/            # NAND flash驱动目录, nfs
$ insmod s3c_nand.ko                            # 加载驱动
NAND device: Manufacturer ID: 0xec, Chip ID: 0xda (Samsung NAND 256MiB 3,3V 8-bit)
Scanning device for bad blocks
......
# 打印信息正确识别了 Nand Flash, 说明底层操作都成功了.
```

## 测试2

源码调用 `add_mtd_partitions` 时, 测试过程比较复杂.
1. 卸载内核自带的NAND Flash驱动
2. 导致无法从本地Flash启动, 必须设置为从nfs启动
3. 从nfs启动后, 加载 s3c_nand.ko 驱动.
4. 使用工具 `mtd-utils` 格式化 NAND Flash
5. 格式化后, 就能挂载测试了.
6. 恢复原来的开发环境.


**这个实验我没有实际去做, 设置和恢复都太麻烦. 而且正常的开发过程是不会这样去操作的.**
下面给出实验步骤:


``` bash
# 1. 卸载内核自带的NAND Flash驱动
# Ubuntu 主机端
# pwd = ./linux-2.6.22.6_custom  复制一个新的内核源码目录

$ make clean
$ make menuconfig                               # 去掉自带的HID USB驱动程序
# -> Device Drivers
#   -> Memory Technology Device (MTD) support
#     -> NAND Device Support
#       < > NAND Flash support for S3C2410/S3C2440 SoC  # 取消内置的NAND Flash驱动

$ make uImage
# 烧录新的uImage
# 重启开发板进入uboot烧录界面, 按k准备烧录内核. 略过不表
$ sudo dnw ./arch/arm/boot/uImage


2. 导致无法从本地Flash启动, 必须设置为从nfs启动.
# 可参考 "嵌入式linux环境搭建-jz2440开发板" 一文
# 开发板, uboot命令行下
# 要使用nfs功能, 必须正确设置uboot的ip地址, 并且Ubuntu端正确设置了nfs

printenv                                        # 看下现有的uboot环境, 记好bootargs, 恢复的时候要用的.
# bootargs=noinitrd root=/dev/mtdblock3 init=/linuxrc console=ttySAC0
set bootargs noinitrd root=/dev/nfs nfsroot=10.0.0.98:/fs ip=10.0.0.111:10.0.0.98:10.0.0.138:255.255.255.0::eth0:off init=/linuxrc console=ttySAC0
# (简化ip: 'set bootargs noinitrd root=/dev/nfs nfsroot=10.0.0.98:/fs ip=10.0.0.111 init=/linuxrc console=ttySAC0' 也可以工作)
save        # 保存修改
reset       # 重启.

# 参数简要说明:
# 'root=/dev/nfs' 加载nfs文件系统
# 'nfsroot=10.0.0.98:/fs' nfs文件系统的来源, 此处是由Ubuntu当nfs服务器, 共享出/fs文件夹
# 'ip=10.0.0.111:10.0.0.98:10.0.0.138:255.255.255.0::eth0:off' 分别表示:
#  ip= 开发板ip : nfs服务器ip: 网关ip : 子网掩码 :: 开发板网口 : off


3. 从nfs启动后, 加载 s3c_nand.ko 驱动.
# Ubuntu 主机端
# pwd = ~/share/jz2440/drivers/nand/            # NAND flash驱动目录
$ make modules                                  # 生成s3c_nand.ko

# 开发板端, 开始测试
# pwd = ~/share/jz2440/drivers/nand/            # NAND flash驱动目录, nfs
$ insmod s3c_nand.ko                            # 加载驱动
NAND device: Manufacturer ID: 0xec, Chip ID: 0xda (Samsung NAND 256MiB 3,3V 8-bit)


4. 使用工具 mtd-utils 格式化 NAND Flash
# Ubuntu 主机端, 需要先编译mtd-utils
$ tar xjf mtd-utils-05.07.23.tar.bz2
$ cd mtd-utils-05.07.23/util
$ vim Makefile
    # ===== 文件内容, 修改如下内容: =====
    #CROSS=arm-linux-   # 需要交叉编译, 取消注释
    CROSS=arm-linux-
    # ===== 结束修改, 保存退出vim =====
$ make
# 拷贝可执行文件到挂载的nfs文件系统的bin目录下
$ cp flash_erase flash_eraseall /home/draapho/share/jz2440/nfs/fs_mini_mdev/bin


5. 格式化后, 就能挂载测试了.
# 开发板端 bash
$ ls -l /dev/mtd*                               # 查看一下分区情况, 有0-3共四个分区
# 应该是用 "flash_eraseall /dev/mtd1" 格式化 "params" 分区, 恢复起来最方便.
$ flash_eraseall /dev/mtd3                      # 格式化 root分区 (用的字符设备), 文件格式为yaffs
$ mount -t yaffs /dev/mtdblock3 /tmp            # 以yaffs格式挂载 root分区
$ ls /tmp                                       # 应该只有一个 lost+found 文件.
# 然后可以对这个分区进行文件创建, 读写的操作了.


6. 恢复原来的开发环境
# 开发板 uboot:
# 破坏了root区的话, 就恢复root区, 重新烧写文件系统到flash就行了. 猜测使用 params 区做测试是没有影响的.
# 烧录原来的 uImage 到 kernel.
# 改回 uboot 的 bootargs 参数
# 重启, 从NAND Flash正常启动.
```


# 参考资料
[Linux操作系统下 NAND FLASH驱动程序框架](http://www.cnblogs.com/TaigaCon/archive/2012/11/17/2775057.html)



----------

***原创于 [DRA&PHO](https://draapho.github.io/)***