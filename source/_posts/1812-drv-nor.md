---
title: 驱动之NOR Flash
date: 2018-01-26
categories: embedded linux
tags: [embedded linux, driver]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之块设备-框架](https://draapho.github.io/2018/01/22/1809-drv-blk/)
- [驱动之NAND Flash框架](https://draapho.github.io/2018/01/24/1810-drv-nand1/)
- [驱动之NAND Flash源码](https://draapho.github.io/2018/01/25/1811-drv-nand2/)
- [驱动之NOR Flash](https://draapho.github.io/2018/01/26/1812-drv-nor/)
- [驱动之网卡驱动](https://draapho.github.io/2018/02/06/1813-drv-net/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.



# NOR Flash 基础知识

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


## 硬件接口

看相关数据手册, 以jz2440v3开发板为例:
- `MX29LV160DBTI-70G.pdf` NOR Flash 数据手册
- `S3C2440A_UserManual_Rev13.pdf` CPU 数据手册


![nor1.png](https://draapho.github.io/images/1812/nor1.JPG)


注意几点:
- NOR Flash 的特性和RAM一样, 可以直接用物理地址来操作.
    - 当开发板以NOR Flash启动时, 0开始的地址就是指向NOR Flash的.
- NOR Flash 数据位宽有两种接法, 16bit 和 8bit. jz2440用的16bit接法
    - 因此, 用uboot测试时, 需要使用 `mw.w` `md.w` 来操作内存地址
    - `mw` Memory Write. uboot下的写内存指令
    - `md` Memory Display. uboot下的读内存指令
    - 使用16bit接法时, CPU的地址线0是不接的. 因而指令上有个错位.
    - 譬如: jz2440发出 (555h<<1), NOR Flash才能收到555h这个地址.
- NOR Flash 有两种模式, jedec, cfi
    - jedec, 无法直接从芯片内读取详细信息, 需要根据芯片ID软件查表.
    - cfi, Common Flash Interface, 可以直接查询芯片详细信息.
    - 目前大多数 NOR Flash 都支持 cfi 规范.



## 读写实验

``` bash
# 开发板 uboot 命令行, 确保是从 NOR Flash 启动的uboot!

# 读取 ID. 2440的A1接到NOR的A0，所以2440发出的地址全部要左移一位
mw.w aaa aa             # Addr = 555<<1
mw.w 554 55             # Addr = 2AA<<1
mw.w aaa 90             # Addr = 555<<1
md.w 0 1
# 显示 00c2, Manifacture ID
md.w 2 1                # Addr = 1<<1
# 显示 2249, 表示型号 MX29LV160DB
mw.w 0 f0               # Reset Mode, 退出读ID
```

# NOR Flash 系统框架

## 系统自带驱动

``` bash
# Ubuntu 主机端
# pwd = ./linux-2.6.22.6

$ make clean
$ make menuconfig                                       # 增加对NOR Flash的支持
# -> Device Drivers
#   -> Memory Technology Device (MTD) support
#     -> Mapping drivers for chip access
#       <M> CFI Flash device in physical memory map     # CFI NOR Flash, 直接做物理映射就可以了
#       (0x0) Physical start address of flash mapping   # 物理基地址, 从0开始的
#       (0x2000000) Physical length of flash mapping    # 要映射的长度, 就是芯片的大小
#       (2)   Bank width in octets (NEW)                # 数据线位宽, 2就是2字节,  16bit

# 比较 .config 会发现多了如下配置. 从而可以找到文件 "drivers/mtd/chips/phram.c"
# CONFIG_MTD_PHYSMAP=m
# CONFIG_MTD_PHYSMAP_START=0
# CONFIG_MTD_PHYSMAP_LEN=0x2000000
# CONFIG_MTD_PHYSMAP_BANKWIDTH=2

$ make modules                                          # 会生成 physmap.ko
cp ./drivers/mtd/maps/physmap.ko ~/share/jz2440/drivers/nor/


# 开发板端, 开始测试
# pwd = ~/share/jz2440/drivers/nor/                     # NOR flash驱动目录, nfs
$ ls /dev/mtd*                                          # 查看一下mtd现有设备
$ insmod physmap.ko                                     # 加载驱动
$ ls /dev/mtd*                                          # 增加了若干mtd设备
$ cat /proc/mtd
```

## 框架分析


其基本框架和 NAND Flash 是一样的

![nor2.png](https://draapho.github.io/images/1812/nor2.png)


下面, 分析一下 CFI NOR Flash 的内核代码框架

``` c
// -----> /drivers/mtd/maps/physmap.c
module_init(physmap_init)
    platform_driver_register(&physmap_flash_driver);    // 上来就是自己玩platform框架
    platform_device_register(&physmap_flash);

# 匹配后, 自然是调用probe函数
physmap_flash_probe
    probe_type = rom_probe_types;                       // "cfi_probe" "jedec_probe" 都是用于NOR Flash的
    do_map_probe(*probe_type, &info->map);

    // -----> /drivers/mtd/chips/chipreg.c
    do_map_probe
        drv = get_mtd_chip_driver(name);
            list_entry(pos, typeof(*this), list)        // this 是 mtd_chip_driver 类型
        drv->probe(map);
        // 搜索 mtd_chip_driver 查看来源. 可以猜出和文件 cfi_probe.c 有关.
        // 实际调用了 cfi_probe      // -----> drivers/mtd/chips/cfi_probe.c
    // -----> 结束, chipreg.c

    // add_mtd_partitions                               // 有分区则进行分区, 最终也会调用 add_mtd_device
    add_mtd_device                                      // 添加mtd设备
    // 然后就会跳到 mtdcore.c 后面和 NAND Flash 一样了. 或参考下面的一个例子
    // 最终会去注册 字符设备 和 块设备
// -----> 结束, physmap.c


// -----> drivers/mtd/chips/cfi_probe.c
static struct mtd_chip_driver cfi_chipdrv;              // .probe = cfi_probe
cfi_probe
    mtd_do_chip_probe(map, &cfi_chip_probe);            // 识别cfi设备

    // -----> drivers/mtd/chips/gen_probe.c
    mtd_do_chip_probe
        genprobe_ident_chips
            cp->probe_chip                              // 调用 cfi_chip_probe.probe_chip
            // 实际调用函数 cfi_probe_chip
        check_cmd_set                                   // 初始化 mtd_info 结构体
    // -----> 结束, gen_probe.c

cfi_probe_chip
    cfi_send_gen_cmd                                    // 发送CFI指令, 获取芯片信息
// -----> 结束, cfi_probe.c


// drivers/mtd/chips/jedec_probe.c 有 jedec_probe. 用于jedec设备
// drivers/mtd/chips/map_rom.c 有 map_rom_probe. 应该是用于CPU内置的ROM.
```

这样就比较清楚了, 整个Linux代码尽可能的做到功能上的(代码上没有完全做到)分层分离.
大框架下有小框架. 譬如 NOR Flash 属于整个MTD大框架的一部分. 但其内部也有自己的一套小框架.

在 NOR Flash 这个例子里面,
将通用的底层驱动代码放在文件 `/drivers/mtd/maps/physmap.c`
然后probe时, 具体的硬件操作被拆分三个部分 `cfi_probe.c` `jedec_probe.c` `map_rom.c`
由于probe里面也有共性的东西, 又被提炼成 `gen_probe.c` 放在一起.



最后, 看一个最简单的例子, ram模拟mtd设备. 将底层硬件相关操作减到了最少.
这个RAM mtd设备和 NAND/NOR Flash 平级, 挂在 `mtdcore.c` 下.
``` c
// -----> /drivers/mtd/devices/phram.c
module_param_call(phram, phram_setup, NULL, NULL, 000);         // 由uboot传递参数进来
phram_setup
    register_device(name, start, len);
        new->mtd.XXX = XXX;                                     // 初始化 mtd_info 结构体
        add_mtd_device                                          // 添加 mtd设备

        // -----> /drivers/mtd/mtdcore.c                        // mtd 设备核心
        add_mtd_device
            not = list_entry(this, struct mtd_notifier, list);  // struct mtd_notifier 结构体是关键
            not->add(mtd);                                      // 调用了add
            // 搜索 mtd_notifier 查看来源, 可知:
            // 实际调用了 mtd_notify_add         // -----> drivers/mtd/mtdchar.c
            // 实际调用了 blktrans_notify_add    // -----> drivers/mtd/mtd_blkdevs.c
        // -----> 结束, mtdcore.c

//可见, 核心内容就是 初始化mtd_info结构体, 然后 add_mtd_device
// -----> 结束, phram.c


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



# 源码

## s3c_nor.c

``` c

/*
 * 参考 drivers\mtd\maps\physmap.c
 */

#include <linux/module.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/device.h>
#include <linux/platform_device.h>
#include <linux/mtd/mtd.h>
#include <linux/mtd/map.h>
#include <linux/mtd/partitions.h>
#include <asm/io.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

static struct map_info *s3c_nor_map;
static struct mtd_info *s3c_nor_mtd;

static struct mtd_partition s3c_nor_parts[] = {             // 复杂一点, 做一个分区信息
    [0] = {
        .name   = "bootloader_nor",
        .size   = 0x00040000,
        .offset = 0,
    },
    [1] = {
        .name   = "root_nor",
        .offset = MTDPART_OFS_APPEND,
        .size   = MTDPART_SIZ_FULL,
    }
};

static int s3c_nor_init(void)
{
    /* 1. 分配map_info结构体 */
    s3c_nor_map = kzalloc(sizeof(struct map_info), GFP_KERNEL);;

    /* 2. 设置: 物理基地址(phys), 大小(size), 位宽(bankwidth), 虚拟基地址(virt) */
    s3c_nor_map->name = "s3c_nor";
    s3c_nor_map->phys = 0;                                              // 对应的物理地址
    s3c_nor_map->size = 0x2000000;                                      // NOR的容量
    s3c_nor_map->bankwidth = 2;                                         // 数据线位宽, 单位字节
    s3c_nor_map->virt = ioremap(s3c_nor_map->phys, s3c_nor_map->size);  // 对应的虚拟地址
    simple_map_init(s3c_nor_map);

    /* 3. 使用: 调用NOR FLASH协议层提供的函数来识别 */
    printk("use cfi_probe\n");
    s3c_nor_mtd = do_map_probe("cfi_probe", s3c_nor_map);               // 直接去调用 .probe = cfi_probe
    if (!s3c_nor_mtd) {
        printk("use jedec_probe\n");
        s3c_nor_mtd = do_map_probe("jedec_probe", s3c_nor_map);         // 失败, 尝试 jedec 模式
    }

    if (!s3c_nor_mtd) {
        iounmap(s3c_nor_map->virt);
        kfree(s3c_nor_map);
        return -EIO;
    }

    /* 4. add_mtd_partitions */
    add_mtd_partitions(s3c_nor_mtd, s3c_nor_parts, 2);                  // 里面调用 add_mtd_device

    return 0;
}

static void s3c_nor_exit(void)
{
    del_mtd_partitions(s3c_nor_mtd);
    iounmap(s3c_nor_map->virt);
    kfree(s3c_nor_map);
}

module_init(s3c_nor_init);
module_exit(s3c_nor_exit);
```

## Makefile

``` makefile
obj-m       := s3c_nor.o
KERN_SRC    := /home/draapho/share/jz2440/kernel/linux-2.6.22.6/
PWD         := $(shell pwd)

modules:
    make -C $(KERN_SRC) M=$(PWD) modules

clean:
    make -C $(KERN_SRC) M=$(PWD) clean
```

## 测试

``` bash
# Ubuntu 主机端
# pwd = ~/share/jz2440/drivers/nor/         # NOR flash驱动目录
$ make modules                              # 生成s3c_nor.ko

# 开发板端, 开始测试
# pwd = ~/share/jz2440/drivers/nor/         # NOR flash驱动目录, nfs
$ ls /dev/mtd*                              # 查看现有的mtd设备
$ insmod s3c_nor.ko                         # 加载驱动
$ ls /dev/mtd*                              # 查看新增的mtd设备
$ flash_eraseall -j /dev/mtd5               # 格式化为 jffs2, 注意新增的不一定是mtd5
$ mount -t jffs2 /dev/mtdblock5 /mnt        # 挂载这个设备到 /mnt
# 在 /mnt 下进行文件的创建和操作, 测试该文件系统.


# 如果没有 flash_eraseall 指令, 则需要编译mtd格式化工具 mtd-utils
# Ubuntu 主机端
$ tar xjf mtd-utils-05.07.23.tar.bz2
$ cd mtd-utils-05.07.23/util
$ vim Makefile
    # ===== 文件内容, 修改如下内容: =====
    #CROSS=arm-linux-   # 需要交叉编译, 取消注释
    CROSS=arm-linux-
    # ===== 结束修改, 保存退出vim =====
$ make

# 开发板端
# 通过nfs拷贝到bin目录下即可.
# pwd = ./mtd-utils-05.07.23/util           # nfs文件
$ cp flash_erase flash_eraseall /bin
```


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***