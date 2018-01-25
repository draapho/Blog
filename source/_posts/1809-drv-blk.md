---
title: 驱动之块设备-框架
date: 2018-01-22
categories: embedded linux
tags: [embedded linux, driver]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之块设备-框架](https://draapho.github.io/2018/01/22/1809-drv-blk/)
- [驱动之nand flash](https://draapho.github.io/2018/01/24/1810-drv-nand/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.


# 块设备的驱动框架

## 驱动框架

![block.png](https://draapho.github.io/images/1809/block.png)

![block_fun.png](https://draapho.github.io/images/1809/block_fun.png)

- `ll_rw_block`: Low Level Read/Write block device
- `submit_bh`: submit Buffer Head
- `submit_bio`: submit Block IO (Input/Output)
- `elv_merge`: elevator merge. 用电梯算法合并数据


## 硬盘基础概念

块设备为了兼容机械结构的硬盘, 使用了一些硬盘特有的概念.

![Platter.jpg](https://draapho.github.io/images/1809/Platter.jpg)

![Cylinder.png](https://draapho.github.io/images/1809/Cylinder.png)

- `存储容量 = 磁头数 x 柱面数 x 扇区数 x 512(扇区字节数)`
- `存储容量 = 柱面大小 x 柱面数`
- `柱面大小 = 磁头数 x 扇区数 x 512(扇区字节数)`

| 英语        | 中文   | 说明               |
| --------- | ---- | ---------------- |
| Disk      | 磁盘   | 就是硬盘             |
| Platter   | 圆盘   | 硬盘的盘片            |
| Head      | 磁头   | 盘片有2面: 2磁头/圆盘    |
| Track     | 磁道   | 圆盘被分割为多个同心圆, 即磁道 |
| Sector    | 扇区   | 磁道被分割后的扇形区域      |
| Cylinder  | 柱面   | 由多个圆盘的同一磁道构成     |
| Partition | 分区   | 软件概念, 以柱面为单位     |

## 参考资料

- [Linux 0.11 源码阅读笔记-设备驱动程序](https://draapho.github.io/2017/02/01/1704-linux-source4/)
- [Linux-块设备驱动之框架详细分析(详解)](http://blog.csdn.net/zdy0_2004/article/details/78206395)
- [Linux块设备驱动](http://blog.csdn.net/hustfoxy/article/details/8723178)
- [硬盘的存储原理和内部架构](http://blog.chinaunix.net/uid-23069658-id-3413957.html)
- [计算机机械硬盘的结构和工作原理](http://www.bijishequ.com/detail/193530)
- [磁盘的组成](http://www.dongcoder.com/detail-473552.html)
- [磁盘结构简介](http://www.cnblogs.com/joydinghappy/articles/2511948.html)


# 块设备驱动范例

块设备驱动的实现更为简单. Linux内核做掉了大部分工作, 驱动层只需要专注于硬件的块读写功能.
而且其框架相对固定, 不像字符设备有多种不同的框架组合.



可以参考内核里的两个文件
- `drivers\block\xd.c` 用于 XT hard disk.
- `drivers\block\z2ram.c` ram disk.
- 给出的源码没有做返回值判断, **实际使用时务必参考上面的范例实现错误处理**.



基本步骤如下:
1. 分配gendisk: `alloc_disk`
2. 设置
    2.1 分配/设置缓冲队列. `blk_init_queue`
    2.2 设置gendisk其他信息, 用于提供硬件属性, 如容量
3. 硬件初始化操作
4. 注册: `add_disk`



## ramblock.c
``` c
#include <linux/major.h>
#include <linux/vmalloc.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/blkdev.h>
#include <linux/hdreg.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

#define DEVICE_NAME "RAMDISK"
#define RAMBLOCK_SIZE (1024*1024)

static int major;
static struct gendisk *ramblock_disk;
static request_queue_t *ramblock_queue;
static DEFINE_SPINLOCK(ramblock_lock);
static unsigned char *ramblock_buf;

// 分区需要知道"硬盘"的几何结构(geometry), 这里虚拟一下即可.
static int ramblock_getgeo(struct block_device *bdev, struct hd_geometry *geo)
{
    geo->heads     = 2;                                     // 磁头数=盘面数*2
    geo->cylinders = 32;                                    // 柱面数
    geo->sectors   = RAMBLOCK_SIZE/2/32/512;                // 扇区数. 利用公式: 存储容量=磁头数x柱面数x扇区数x512
    return 0;
}

static struct block_device_operations ramblock_fops = {
    .owner  = THIS_MODULE,
    .getgeo = ramblock_getgeo,
};

// 实现扇区的读写操作
static void do_ramblock_request(request_queue_t * q)
{
    static int r_cnt = 0;
    static int w_cnt = 0;
    struct request *req;

    while ((req = elv_next_request(q)) != NULL) {           // 取出要处理的数据(连续的扇区数据, 即簇)
        unsigned long offset = req->sector*512;             // 读写的目标地址
        unsigned long len = req->current_nr_sectors*512;    // 长度

        if (rq_data_dir(req) == READ) {                     // 读操作
            printk("do_ramblock_request read %d\n", ++r_cnt);
            memcpy(req->buffer, ramblock_buf+offset, len);  // 直接读 ramblock_buf
        } else {                                            // 写操作
            printk("do_ramblock_request write %d\n", ++w_cnt);
            memcpy(ramblock_buf+offset, req->buffer, len);  // 直接写 ramblock_buf
        }
        end_request(req, 1);                                // 告知操作完成
    }
}

static int ramblock_init(void)
{
    /* 1. 分配一个gendisk结构体 */
    ramblock_disk = alloc_disk(16);                         // 次设备号个数, 也是允许的最大分区个数

    /* 2. 设置 */
    /* 2.1 分配/设置缓冲队列 */
    ramblock_queue = blk_init_queue(do_ramblock_request, &ramblock_lock);
    ramblock_disk->queue = ramblock_queue;

    /* 2.2 设置其他属性: 比如容量 */
    major = register_blkdev(0, DEVICE_NAME);                // cat /proc/devices 查看块设备
    ramblock_disk->major       = major;                     // 主设备号
    ramblock_disk->first_minor = 0;                         // 次设备号起始值
    sprintf(ramblock_disk->disk_name, "ramblock");
    ramblock_disk->fops        = &ramblock_fops;
    set_capacity(ramblock_disk, RAMBLOCK_SIZE / 512);       // 设置扇区的数量, 不是字节数

    /* 3. 硬件初始化操作 */
    ramblock_buf = kzalloc(RAMBLOCK_SIZE, GFP_KERNEL);

    /* 4. 注册 */
    add_disk(ramblock_disk);
    return 0;
}

static void ramblock_exit(void)
{
    del_gendisk(ramblock_disk);                     // 对应 add_disk
    put_disk(ramblock_disk);                        // 对应 blk_init_queue
    blk_cleanup_queue(ramblock_queue);              // 对应 blk_init_queue
    unregister_blkdev(major, DEVICE_NAME);          // 对应 register_blkdev
    kfree(ramblock_buf);                            // 安全起见, 最后释放buf
}

module_init(ramblock_init);
module_exit(ramblock_exit);
```

## Makefile

``` makefile
obj-m       := ramblock.o
KERN_SRC    := /home/draapho/share/jz2440/kernel/linux-2.6.22.6/
PWD         := $(shell pwd)

modules:
    make -C $(KERN_SRC) M=$(PWD) modules

clean:
    make -C $(KERN_SRC) M=$(PWD) clean
```

## 测试

``` bash
# Ubuntu主机端
# pwd = ~/share/jz2440/drivers/drv_blk/         # 块设备驱动目录
$ make modules                                  # 生成 ramblock.ko


# 开发板端, 开始测试
# pwd = ~/share/jz2440/drivers/drv_blk/         # 块设备驱动目录, nfs
$ insmod ramblock.ko
 ramblock:do_ramblock_request read 1
 unknown partition table                        # ramblock_buf 全是0, 所以显示无效分区表.

$ ls /dev/ramblock*                             # 可以看到 ramblock 设备了
$ cat /proc/devices
254 RAMDISK                                     # register_blkdev产生的块设备信息

$ mkdosfs /dev/ramblock                         # 格式化. 没有mkfs指令, 用mkdosfs
$ mount /dev/ramblock /tmp                      # 挂载为 /tmp

$ vi /tmp/test                                  # 在ramblock_disk里读写文件
do_ramblock_request read 43                     # 退出后, 只是读取块, 然后在缓冲区修改. 没有真正写入!
$ sync                                          # 多等一会, 或者输入sync同步指令, 开始写入磁盘
do_ramblock_request write 6
do_ramblock_request write 7 ......

$ cp ramblock.c /tmp/                           # 随便拷贝一个文件
# 没有打印 do_ramblock_request write 说明文件还没有被真正写入磁盘
$ sync                                          # 多等一会, 或者输入sync同步指令, 开始写入磁盘
do_ramblock_request write 11
do_ramblock_request write 12 ......

$ ls /tmp                                       # 显示 ramblock 里的文件
ramblock.c  test
$ umount /tmp                                   # 卸载 /tmp
do_ramblock_request write 16 ......             # 如果有未写入的数据, 此时会写入.
$ ls /tmp                                       # 这时候, tmp文件夹就是空的了.

$cat /dev/ramblock > ./ramblock.bin             # 把整个磁盘打包成文件. 当前路径是ubuntu的nfs
do_ramblock_request read ......

# 然后切换到 Ubuntu主机端
$ sudo mount -o loop ramblock.bin /mnt          # -o loop 表示挂载指定文件, 挂载到/mnt目录下
$ ls /mnt                                       # 显示了之前 ramblock 里的内容.
ramblock.c  test
$ sudo umount /mnt

# 切换到 开发板端
$ mkdir /ramdisk
$ mount /dev/ramblock /ramdisk                  # 重新挂载为 /ramdisk
$ ls /ramdisk                                   # 显示 ramblock 里的文件
ramblock.c  test
$ df                                            # 可以查看文件系统信息.
Filesystem           1k-blocks      Used Available Use% Mounted on
/dev/ramblock             1004         6       998   1% /ramdisk

$ umount /ramdisk                               # 卸载ramdisk, 否则无法卸载驱动
$ rmdir /ramdisk
$ rmmod ramblock                                # 卸载驱动, 里面数据就没有了!
# 观察打印信息 do_ramblock_request 可得: 块设备操作都是批量的读或者批量的写.
# 这是由电梯算法实现的, 能大大提高硬盘的物理读写速度, 减缓由磁盘操作造成的速度下降


# 开发板端, 开始做fdisk分区测试 (分区指令需要 geometry 信息)
$ insmod ramblock.ko
$ ls /dev/ramblock*                             # 查看设备
/dev/ramblock                                   # 没有分区, 只有一个总的磁盘设备
$ fdisk /dev/ramblock
m                                               # m for help
n p Partition number: 1 cylinder value: 1-8     # 增加一个主分区
n p Partition number: 2 cylinder value: 9-32    # 再增加一个主分区
p                                               # 查看设置的分区情况
w                                               # 执行上述配置

$ ls /dev/ramblock* -l                          # 再次查看设备, b表示块设备
brw-rw----    1 0        0        254,   0 Jan  1 00:01 /dev/ramblock   # 整个磁盘设备
brw-rw----    1 0        0        254,   1 Jan  1 00:01 /dev/ramblock1  # 分区一
brw-rw----    1 0        0        254,   2 Jan  1 00:01 /dev/ramblock2  # 分区二

$ mkdosfs /dev/ramblock1                        # 格式化
$ mkdosfs /dev/ramblock2
$ mkdir /mnt/ramdisk1                           # 创建挂载文件点
$ mkdir /mnt/ramdisk2
$ mount /dev/ramblock1 /mnt/ramdisk1            # 挂载
$ mount /dev/ramblock2 /mnt/ramdisk2
# 做一些操作, 如读写/拷贝文件...
$ mkdosfs /dev/ramblock                         # 危险操作!!! 依旧能格式化整个磁盘.

$ umount /mnt/ramdisk1
$ umount /mnt/ramdisk2
$ rmdir /mnt/ramdisk1
$ rmdir /mnt/ramdisk2
```

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***