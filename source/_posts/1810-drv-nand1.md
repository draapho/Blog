---
title: 驱动之NAND Flash框架
date: 2018-01-24
categories: embedded linux
tags: [embedded linux, driver]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之块设备-框架](https://draapho.github.io/2018/01/22/1809-drv-blk/)
- [驱动之NAND Flash框架](https://draapho.github.io/2018/01/24/1810-drv-nand1/)
- [驱动之NAND Flash源码](https://draapho.github.io/2018/01/25/1811-drv-nand2/)
- [驱动之NOR Flash](https://draapho.github.io/2018/01/26/1812-drv-nor/

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.




# NAND Flash 基础知识

## NAND 和 NOR Flash的比较

| NOR FLASH                                | NAND FLASH                               |
| ---------------------------------------- | ---------------------------------------- |
| 接口时序同SRAM,易使用                            | 地址/数据线复用，数据位较窄                           |
| 读取速度较快                                   | 读取速度较慢                                   |
| 擦除速度慢，以64-128KB的块为单位                     | 擦除速度快，以8－32KB的块为单位                       |
| 写入速度慢                                    | 写入速度快                                    |
| 随机存取速度较快，支持XIP(eXecute In Place，芯片内执行)，适用于代码存储。在嵌入式系统中，常用于存放引导程序、根文件系统等。 | 顺序读取速度较快，随机存取速度慢，适用于数据存储(如大容量的多媒体应用)。在嵌入式系统中，常用于存放用户文件系统等。 |
| 单片容量较小，1-32MB                            | 单片容量较大，8-128MB，提高了单元密度                   |
| 最大擦写次数10万次                               | 最大擦写次数100万次                              |


## 硬件接口和时序

看相关数据手册, 以jz2440v3开发板为例:
- `K9F2G08U0C.pdf` NAND Flash 数据手册
- `S3C2440A_UserManual_Rev13.pdf` CPU 数据手册



NAND Flash的硬件引脚基本固定, 下面列出各个引脚的含义

| 缩写          | 英文原意                 | 说明               |
| ----------- | -------------------- | ---------------- |
| I/O         | data Inputs/Outputs  | 数据收发, 8bit或16bit |
| CLE         | Command Latch Enable | 传的是指令, 高电平有效     |
| ALE         | Address Latch Enable | 传的是地址, 高电平有效     |
| _CE 或 nCE   | Chip Enable          | 片选信号, 低电平有效      |
| _RE 或 nRE   | Read Enable          | 读数据, 低电平有效       |
| _WE 或 nWE   | Write Enable         | 写数据, 低电平有效       |
| R/_B 或 R/nB | Ready/Busy           | 空闲/忙信号, 忙为低电平    |



查看三星S3C2440数据手册 `NAND Flash Controller` 章节可知, 已将nand flash的时序操作打包成了寄存器操作.
u-boot里面, 可以使用 `md` `mw` 直接对memroy进行操作. 因此可在u-boot下面直接用指令来操作nand flash的时序
- `md`, Memory Display. 显示指定内存地址的内容. `.b`表Byte, 字节. `.w`表Word, 2字节. `.l`表Long, 4字节.
- `mw`, Memory Write. 写入内容到指定内存地址. `.b`表Byte, 字节. `.w`表Word, 2字节. `.l`表Long, 4字节.


| 指令   | 物理操作                       | S3C2440 寄存器操作 | u-boot 直接操作对应的寄存器地址                |
| ---- | -------------------------- | ------------- | ---------------------------------- |
| 片选   | _CE低                       | NFCONT bit1=0 | md.l 读一下, mw.l 0x4E000004 回写bit1=0 |
| 发命令  | CLE高, ALE低, I/O命令值, _WE高变低 | NFCMMD=命令值    | mw.b 0x4E000008 命令值                |
| 发地址  | ALE高, CLE低, I/O地址值, _WE高变低 | NFADDR=地址值    | mw.b 0x4E00000C 地址值                |
| 发数据  | CLE低, ALE低, I/O数据值, _WE高变低 | NFDATA=数据值    | mw.b 0x4E000010 数据值                |
| 读数据  | CLE低, ALE低, _RE高变低, 取I/O值  | 数据值=NFDATA    | md.b 0x4E000010 1                  |


## 读写实验

``` bash
# 开发板 uboot 命令行, 最好是从 NAND Flash 启动的uboot.

# 1. 读取 ID, 查看 K9F2G08U0C 数据手册 5.5 Read ID 时序图.
md.l 0x4E000004 1           # 读取 NFCONT 寄存器值. 1表示长度, 就读一个数据. 默认值是16
mw.l 0x4E000004 1           # 置 bit1=0 后, 回写
mw.b 0x4E000008 0x90        # 发命令 NFCMMD=0x90
mw.b 0x4E00000C 0x00        # 发地址 NFADDR=0x00
md.b 0x4E000010 1           # 读数据 NFDATA, 应该得到 ec
md.b 0x4E000010 1           # 继续读 NFDATA, 应该得到device code, da
md.b 0x4E000010 1           # 继续读 NFDATA, 应该得到device code, 10
md.b 0x4E000010 1           # 继续读 NFDATA, 应该得到device code, 15 (这里返回了95, 先不管)
md.b 0x4E000010 1           # 继续读 NFDATA, 应该得到device code, 44
# 这里不能使用指令 md.b 0x4E000010 5 读取5个字节. 因为其含义是读 0x4E000010-0x4E000014 的寄存器值, 必然是错的.
mw.b 0x4E000008 0xff        # 发RESET命令 NFCMMD=0xFF


# 2. 读取0地址的数据, 查看 K9F2G08U0C 数据手册 5.1 Page Read 时序图
nand dump 0                 # 先用nand指令直接读取nand flash的页, 后面在用寄存器操作的方式读一遍来对比
17 00 00 ea 14 f0 9f e5  14 f0 9f e5 14 f0 9f e5
......

md.l 0x4E000004 1           # 读取 NFCONT 寄存器值. 1表示长度, 就读一个数据. 默认值是16
mw.l 0x4E000004 1           # 置 bit1=0 后, 回写
mw.b 0x4E000008 0x00        # 写命令 NFCMMD=0x00
mw.b 0x4E00000C 0x00        # 写地址 NFADDR=0x00
mw.b 0x4E00000C 0x00        # 写地址 NFADDR=0x00
mw.b 0x4E00000C 0x00        # 写地址 NFADDR=0x00
mw.b 0x4E00000C 0x00        # 写地址 NFADDR=0x00
mw.b 0x4E00000C 0x00        # 写地址 NFADDR=0x00
# 这款nand总线是8位, 时序图要求5个周期. 由2字节的列地址和3字节的行地址组成.
mw.b 0x4E000008 0x30        # 读命令 NFCMMD=0x30
md.b 0x4E000010 1           # 读数据 NFDATA
......                      # 重复多次这个指令, 譬如16次
md.b 0x4E000010 1           # 读数据 NFDATA, 得到的数据应该和 nand dump 0 的一样
# 16此返回值应该和 nand dump 的结果一样: 17 00 00 ea 14 f0 9f e5  14 f0 9f e5 14 f0 9f e5
# 这里不能使用指令 md.b 0x4E000010 16 读取16个字节. 因为其含义是读 0x4E000010-0x4E000020 的寄存器值, 必然是错的.
mw.b 0x4E000008 0xff        # 发RESET命令 NFCMMD=0xFF
```

# NAND Flash 系统框架

![nand1](https://draapho.github.io/images/1810/nand1.jpg)

![nand2](https://draapho.github.io/images/1810/nand2.png)


``` c
// 由Linux系统启动时的打印信息, 可以抓取到 NAND FLASH 相关的初始化信息和分区信息.
// 可得 "S3C24XX NAND Driver, ..." 搜索后, 定位到文件 "/drivers/mtd/nand/s3c2410.c"
// mtd: Memory Technology Device. 记忆体技术设备, 也就是 nand/nor flash.

// -----> /drivers/mtd/nand/s3c2410.c
s3c2410_nand_init                                               // 看驱动文件, 从 module_init 开始
    platform_driver_register(&s3c2440_nand_driver);             // 很明显用了 platform 框架

    // -----> /arch/arm/plat-s3c24xx/common-smdk.c              // 这里是 platform 框架的 device 配置
    smdk_machine_init
        s3c_device_nand.dev.platform_data = &smdk_nand_info;
        platform_add_devices(smdk_devs);                        // 找到了 platform 的 devices 端.
        // 这里看下 smdk_nand_info, smdk_devs的s3c_device_nand 就都明白了. 配置nand的名称和参数.
    // -----> 结束, common-smdk.c

// 看完了platform框架, 匹配后就是调用probe函数. 几次跳转后, 最终调用:
s3c24xx_nand_probe
    struct s3c2410_platform_nand *plat = to_nand_plat(pdev);    // 取出了 smdk_nand_info 的配置信息
    s3c2410_nand_inithw                                         // 初始化硬件, 如时序
    s3c2410_nand_init_chip                                      // 初始化通讯, 如缓冲区, 寄存器值
    nand_scan                                                   // 开始通讯, 检查 nand flash

    // -----> /drivers/mtd/nand/nand_base.c                     // NAND FLASH 操作的通用文件
    nand_scan
        nand_scan_ident                                         // 第一阶段的初始化, 检查flash硬件
            nand_set_defaults                                   // nand 通信使用默认参数
            nand_get_flash_type                                 // 获取第一块 nand 的ID值
                nand_flash_ids                                  // 常用的 nand flash 表. 可见内核都支持了
            printk(KERN_INFO "%d NAND chips detected\n", i);    // 接了多块nand的话, 必须是同型号的
            mtd->size = i * chip->chipsize;                     // 总容量 = nand数量*单片容量
        nand_scan_tail                                          // 第二阶段的初始化工作, 软件设置
    // -----> 结束, nand_base.c

    s3c2410_nand_add_partition                                  // 分区工作
        add_mtd_device
        // -----> /drivers/mtd/mtdcore.c                        // mtd 设备核心
        // add_mtd_partitions 最终也调用了 add_mtd_device
        add_mtd_device
            not = list_entry(this, struct mtd_notifier, list);  // struct mtd_notifier 结构体是关键
            not->add(mtd);                                      // 调用了add
            // 搜索 mtd_notifier 查看来源, 可知:
            // 实际调用了 mtd_notify_add         // -----> drivers/mtd/mtdchar.c
            // 实际调用了 blktrans_notify_add    // -----> drivers/mtd/mtd_blkdevs.c
        // -----> 结束, mtdcore.c
// -----> 结束, s3c2410.c



// -----> drivers/mtd/mtdchar.c                                 // 将mtd设备挂载成字符设备
static struct mtd_notifier notifier;                            // .add = mtd_notify_add
mtd_notify_add
    class_device_create("mtd%d")                                // mtd字符设备, 可读写
    class_device_create("mtd%dro")                              // mtd只读字符设备
init_mtdchar                                                    // mtdchar.c 的 module_init
    register_chrdev(MTD_CHAR_MAJOR, "mtd", &mtd_fops)           // 注册为字符设备
// -----> 结束, mtdchar.c 完成了字符设备的核心步骤.



// -----> drivers/mtd/mtd_blkdevs.c                             // 将mtd设备挂载成块设备
static struct mtd_notifier blktrans_notifier;                   // .add = blktrans_notify_add
blktrans_notify_add
    tr = list_entry(this, struct mtd_blktrans_ops, list);       // 一样的, 搜索 mtd_blktrans_ops
    tr->add_mtd(tr, mtd);
    // 可以找到两个文件有初始化, 很明显是块设备读写还是只读的区别. 选取 /drivers/mtd/mtdblock.c
    // 实际调用了 mtdblock_add_mtd

    // -----> /drivers/mtd/mtdblock.c
    static struct mtd_blktrans_ops mtdblock_tr;                 // .add_mtd = mtdblock_add_mtd
    mtdblock_add_mtd
        add_mtd_blktrans_dev
            alloc_disk                                          // 分配 gendisk
            add_disk                                            // 注册为块设备
    init_mtdblock                                               // mtdblock.c 的 module_init
        register_mtd_blktrans
            register_blkdev                                     // 获得主设备号
            blk_init_queue                                      // 设置缓冲队列
    // -----> 结束, mtdblock.c 完成了块设备的核心步骤.
// -----> 结束, mtd_blkdevs
```


# 参考资料
[Linux操作系统下 NAND FLASH驱动程序框架](http://www.cnblogs.com/TaigaCon/archive/2012/11/17/2775057.html)
[Linux MTD子系统 _从模型分析到Flash驱动模板](http://www.linuxidc.com/Linux/2017-03/142206.htm)
[LINUX NAND FLASH驱动程序框架分析](http://blog.sina.com.cn/s/blog_6683e49d0100o18j.html)



----------

***原创于 [DRA&PHO](https://draapho.github.io/)***