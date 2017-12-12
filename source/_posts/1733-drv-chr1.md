---
title: 驱动之字符设备-框架
date: 2017-11-22
categories: embedded linux
tags: [embedded linux, driver]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之字符设备-框架](https://draapho.github.io/2017/11/22/1733-drv-chr1/)
- [驱动之基于LinK+设计按键驱动](https://draapho.github.io/2017/11/30/1740-drv-chr2/)
- [驱动之基于中断设计按键驱动](https://draapho.github.io/2017/12/07/1741-drv-chr3/)
- [驱动之poll机制](https://draapho.github.io/2017/12/11/1742-drv-chr4/)
- [驱动之异步通知](https://draapho.github.io/2017/12/12/1743-drv-chr5/)
- [驱动之同步互斥阻塞](https://draapho.github.io/2017/12/13/1744-drv-chr6/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.


# linux 架构概念
![Linux_kernel_System_Call_Interface_and_glibc.png](https://draapho.github.io/images/1733/Linux_kernel_System_Call_Interface_and_glibc.png)

![Linux_kernel_Layer.JPG](https://draapho.github.io/images/1733/Linux_kernel_Layer.JPG)

- 一个操作系统需要软硬件分离. 应用端无需关注底层硬件的实现.
- Linux采用的接口就是 GNU C Library 标准, 下面简称C库.
    - 譬如 `open` `read` `write`
- 应用程序和C库运行在芯片的用户空间 (权限受限, 保证安全).
- 当应用程序调用C库, C库会使用 `SWI` 汇编指令触发异常, 切换到内核空间.
- 内核空间的对外接口是 **System Call Interface**, 下面简称系统调用
    - 譬如 `sys_open` `sys_read` `sys_write`
- 触发系统调用后, Linux内核会根据框架结构自动去调用对应的驱动.
- 编写驱动时, 需要了解的是Linux各个驱动的实现框架.
    - 譬如 `led_open` `led_read` `led_write`
- 最后一点, **Linux下一切皆文件, 文件即节点(inode)**. 所以驱动也是一个个文件节点.

## 参考资料
- [Linux 0.11 源码阅读笔记-总览](https://draapho.github.io/2017/01/23/1704-linux-source/)
- [Linux 0.11 源码阅读笔记-设备驱动程序](https://draapho.github.io/2017/02/01/1704-linux-source4/)
- [The GNU C Library (glibc) Documentation](https://www.gnu.org/software/libc/documentation.html)

**重点推荐**
- [The Linux man-pages project](https://www.kernel.org/doc/man-pages/) Library部分就是GNUC库的函数说明
- [Linux Kernel API](https://www.fsl.cs.sunysb.edu/kernel-api/) Linux内核API函数说明

# 字符设备的驱动框架

- 实现 `led_open` `led_write` `led_read` 等函数
- 定义一个 `file_operations` 结构体, 设置好对应的函数指针
    - `/include/linux/fs.h` 下包含了此结构
- 实现一个初始化函数, 并调用 `register_chrdev` 注册定义好的 `file_operations`
    - `/include/linux/fs.h` 下包含了此函数
    - 源码位于 `/fs/chr_dev.c`, 使用 `EXPORT_SYMBOL` 让内核函数可以调用它.
- 使用 `module_init` 指定好初始化函数.
- 内核在加载驱动时, 会先自动调用初始化函数. 初始化函数做相关的注册工作
- 这样, 系统调用就能找到最终要执行的函数了.

## 一些概念
- 主设备号. 可以人工指定, 也可以由系统动态分配. 理解为设备类型的id即可.
- 子设备号. 譬如一个led灯的驱动设备, 可以实现多个led的控制. 子设备号可以提供针对特定的led进行控制
    - 譬如: 0表示控制所有led, 1表示led1, 2表示led2...
- mdev. 根据动态驱动模块的信息自动创建设备节点.
- 地址映射. 这是与单片机的区别. 单片机操作寄存器可以直接使用物理地址. 但linux下使用的是虚拟地址!
    - 地址转换使用 `ioremap` `iounmap` 函数.
    - 一般的芯片商也会提供操作寄存器的函数, 譬如 `s3c2410_gpio_setpin`
- 用户空间和内核空间. 两个空间的资源不能直接相互访问.
    - 驱动程序内经常要用 `copy_to_user` 以及 `copy_from_user`

# 人工绑定设备号

## 驱动代码 drv_leds.c

``` c
// ~/jz2440/driver/drv_leds/drv_leds.c

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/device.h>
#include <asm/uaccess.h>

#define DEVICE_NAME "drv_leds"      // 设备类型名称, cat /proc/devices 可以看到
#define LED_MAJOR   111             // 主设备号
#define BUFF_LEN    5               // 缓存大小. 这里定小一点便于测试      

// ===== 驱动的硬件实现部分, 和单片机类似 =====

int drv_leds_open(struct inode *inode, struct file *file) 
{
    printk("drv_leds_open\n");
    return 0;
}

ssize_t drv_leds_write(struct file *file, const char __user *data, size_t len, loff_t *ppos) 
{

    char buff[BUFF_LEN];
    int i, l;
    
    printk("drv_leds_write: ");
    do {
        l = len<BUFF_LEN? len:BUFF_LEN;
        copy_from_user(buff, data, l);                      // 一点点拷贝, 避免溢出
        data += l;
        for (i=0; i<l; i++)
            printk("%c", buff[i]);
        len -= l;
    } while (len>0);

    printk("\n");
    return len;
}

// 此结构体指定了C库的文件操作函数需要调用的底层驱动的函数名.
static struct file_operations drv_leds_fops = {
    .owner  =   THIS_MODULE,        // 这是一个宏，指向编译模块时自动创建的__this_module变量. 和平台相关
    .open   =   drv_leds_open,     
    .write  =   drv_leds_write,
};


// ===== 加载和卸载内核时, 指定要调用的函数 =====
int drv_leds_init(void) 
{
    register_chrdev(LED_MAJOR, DEVICE_NAME, &drv_leds_fops);// 注册驱动, 包含了函数指针
    printk(DEVICE_NAME " initialized\n");                   // 调试用
    return 0;
}

void drv_leds_exit(void) 
{
    unregister_chrdev(LED_MAJOR, DEVICE_NAME);
    printk(DEVICE_NAME " deinitialized\n");     
}

module_init(drv_leds_init);
module_exit(drv_leds_exit);


// ===== 描述驱动程序的一些信息，不是必须的 =====
MODULE_AUTHOR("draapho");
MODULE_VERSION("0.1.0");
MODULE_DESCRIPTION("First Driver for LED");
MODULE_LICENSE("GPL");
```

## Makefile

``` Makefile
# ~/jz2440/driver/drv_leds/Makefile

KERN_DIR = ~/jz2440/kernel/linux-2.6.22.6
# 这是交叉编译, 需要指定嵌入式linux内核地址

all:
	make -C $(KERN_DIR) M=`pwd` modules 
# pwd 表示当前目录, 即驱动代码所在的目录
# 驱动目录并不需要放在内核目录下面.

clean:
	make -C $(KERN_DIR) M=`pwd` modules clean
	rm -rf modules.order

obj-m	+= drv_leds.o
```


## 测试代码, drv_leds_test.c

``` c
// ~/jz2440/driver/drv_leds/drv_leds_test.c

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) 
{
    int fd;

    fd = open("/dev/xxx", O_RDWR);      // 这里设备名字并不重要, 设备和驱动的关联方式是主设备号!
    if (fd < 0) 
        printf("can't open!\n");
    else if (argc >=2) {
        int i;
        for (i=1; i<argc; i++)
        write(fd, argv[i], strlen(argv[i]));
    } else {
        printf("./drv_led_test <str1> [str2]\n");
    }
    return 0;
}
```

## 编译加载并测试

``` bash
# ===== Ubuntu主机端, 编译驱动 =====
# pwd = drv_leds.c所在的目录.
$ make clean
$ make                                  # 编译驱动
# 成功后, 生成 drv_leds.ko 动态库

$ cp drv_leds.ko ~/jz2440/fs_first/     # 先直接放到文件系统根目录下了.
# 嵌入式端最好用网络的方式加载文件系统, 这样就不用重新烧录文件系统了, 便于调试!

# ===== 嵌入式Linux端, 加载驱动 =====
# pwd = /
$ insmod drv_leds.ko                    # 加载模块
drv_leds initialized                    # 打印的调试信息
$ cat /proc/devices                     # 查看设备信息
Character devices:
111 drv_leds                            # 应该能找到这一项

# ===== Ubuntu主机端, 编译测试源码 =====
# pwd = drv_leds_test.c所在的目录.
$ arm-linux-gcc -o drv_leds_test drv_leds_test.c    # 编译应用程序
$ cp drv_leds_test ~/jz2440/fs_first/               # 先直接放到文件系统根目录下了.

# 如果此时直接在嵌入式端运行 ./drv_leds_test
# 会显示 can't open! 因为不存在文件 /dev/xxx 

# ===== Ubuntu主机端, 创建文件节点 ======
$ mknod /dev/xxx c 111 0
# 创建设备xxx文件, c-字符设备, 111-主设备号(关联到了drv_les驱动设备), 0-子设备号(先随便写)

# ===== 嵌入式Linux端, 测试驱动 =====
$ ./drv_leds_test 123
drv_leds_open
drv_leds_write: 123
```


# 自动化实现

## 驱动代码 drv_leds.c

``` c
// ~/jz2440/driver/drv_leds/drv_leds.c

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/device.h>
#include <asm/io.h>
#include <asm/arch/regs-gpio.h>
#include <asm/hardware.h>
#include <asm/uaccess.h>


#define DEVICE_NAME "drv_leds"                      // 设备类型名称, cat /proc/devices 可以看到

static int major;                                   // 存储自动分配的主设备号
static struct class *leds_class;                    // 类, 供mdev用, ls /sys/class/ 可以看到
static struct class_device	*leds_class_devs[4];    // 类下设备, ls /sys/class/class_name 可以看到

static unsigned long gpio_base;                     // gpio 寄存器基础地址

#define GPIO_OFFSET(addr) ((addr) - 0x56000000)
#define GPFCON  (*(volatile unsigned long *)(gpio_base + GPIO_OFFSET(0x56000050)))
#define GPFDAT  (*(volatile unsigned long *)(gpio_base + GPIO_OFFSET(0x56000054)))


// ===== 驱动的硬件实现部分, 和单片机类似 =====

static int drv_leds_open(struct inode *inode, struct file *file) 
{
    int minor = MINOR(inode->i_rdev);
    
    // 初始化对应的LED
    if ((minor == 1) || (minor == 0)) {             // led1 或 leds
        GPFCON &= ~(0x3<<(4*2));                    // GPF4 配置为输出
        GPFCON |= (1<<(4*2));
        GPFDAT |= (1<<4);                           // 关灯
    }      
    if ((minor == 2) || (minor == 0)) {             // led2 或 leds
        GPFCON &= ~(0x3<<(5*2));                    // GPF5 配置为输出
        GPFCON |= (1<<(5*2));
        GPFDAT |= (1<<5);     
    }      
    if ((minor == 3) || (minor == 0)) {             // led3 或 leds
        // GPFCON &= ~(0x3<<(6*2));                    // GPF6 配置为输出
        // GPFCON |= (1<<(6*2));
        // GPFDAT |= (1<<6);    
        s3c2410_gpio_cfgpin(S3C2410_GPF6, S3C2410_GPF6_OUTP);   
        s3c2410_gpio_setpin(S3C2410_GPF6, 1);       // 另外一种方法
    }      
    printk("drv_leds_open\n");
    return 0;
}

static ssize_t drv_leds_write(struct file *file, const char __user *data, size_t len, loff_t *ppos) 
{
    int minor = MINOR(file->f_dentry->d_inode->i_rdev);
    char val;
    
    copy_from_user(&val, data, 1);
    
    // 操作对应的LED
    if ((minor == 1) || (minor == 0)) {             // led1 或 leds
        if (val)
            GPFDAT &= ~(1<<4);                      // 开灯
        else
            GPFDAT |= (1<<4);                       // 关灯
    }      
    if ((minor == 2) || (minor == 0)) {             // led2 或 leds
        if (val)
            GPFDAT &= ~(1<<5);   
        else   
            GPFDAT |= (1<<5);    
    }      
    if ((minor == 3) || (minor == 0)) {             // led3 或 leds        
        // if (val)
            // GPFDAT &= ~(1<<6);    
        // else   
            // GPFDAT |= (1<<6);
        s3c2410_gpio_setpin(S3C2410_GPF6, !val);     // 另外一种方法
    }
    printk("drv_leds_write, led%d=%d\n", minor, val);
    return len;
}

// 此结构体指定了C库的文件操作函数需要调用的底层驱动的函数名.
static struct file_operations drv_leds_fops = {
    .owner  =   THIS_MODULE,        // 这是一个宏，指向编译模块时自动创建的__this_module变量. 和平台相关
    .open   =   drv_leds_open,     
    .write  =   drv_leds_write,
};


// ===== 加载和卸载内核时, 指定要调用的函数 =====
static int drv_leds_init(void) 
{
    int minor;

    // 获取寄存器起始地址的虚拟地址值. 其它寄存器基于此值再用偏移量.
    gpio_base = ioremap(0x56000000, 0xD0);
    if (!gpio_base) {
        return -EIO;
    }
    
    // 注册驱动, 指定主设备号
//    minor = register_chrdev(LED_MAJOR, DEVICE_NAME, &s3c24xx_leds_fops);
//    if (minor < 0) {
//        printk(DEVICE_NAME " can't register major number\n");
//        return minor;
//    }

    // 注册驱动, 0表示动态分配主设备号
    major = register_chrdev(0, DEVICE_NAME, &drv_leds_fops);    
    
    // 生成系统设备信息, 供mdev自动创建设备节点使用
	leds_class = class_create(THIS_MODULE, "leds");             // 创建 leds 类
	if (IS_ERR(leds_class))
		return PTR_ERR(leds_class);
    
    // 创建 leds 类下面的设备. 0表示所有led, 名称为 leds
    leds_class_devs[0] = class_device_create(leds_class, NULL, MKDEV(major, 0), NULL, "leds");
	
    // 1-3 表示3个独立的led, 名称为 led1, led2, led3
    for (minor = 1; minor < 4; minor++) {
		leds_class_devs[minor] = class_device_create(leds_class, NULL, MKDEV(major, minor), NULL, "led%d", minor);
		if (unlikely(IS_ERR(leds_class_devs[minor])))
			return PTR_ERR(leds_class_devs[minor]);
	}
    
    printk(DEVICE_NAME " initialized\n");                       // 调试用
    return 0;
}

static void drv_leds_exit(void) 
{
    int minor;

	for (minor = 0; minor < 4; minor++) {                       
		class_device_unregister(leds_class_devs[minor]);        // 删除设备节点
	}
	class_destroy(leds_class);                                  // 删除设备类
    
    unregister_chrdev(major, DEVICE_NAME);                      // 卸载驱动
    iounmap(gpio_base);
    printk(DEVICE_NAME " deinitialized\n");     
}

module_init(drv_leds_init);
module_exit(drv_leds_exit);


// ===== 描述驱动程序的一些信息，不是必须的 =====
MODULE_AUTHOR("draapho");
MODULE_VERSION("0.1.1");
MODULE_DESCRIPTION("First Driver for LED");
MODULE_LICENSE("GPL");
```

## Makefile

``` Makefile
# ~/jz2440/driver/drv_leds/Makefile

KERN_DIR = ~/jz2440/kernel/linux-2.6.22.6
# 这是交叉编译, 需要指定嵌入式linux内核地址

all:
	make -C $(KERN_DIR) M=`pwd` modules 
# pwd 表示当前目录, 即驱动代码所在的目录
# 驱动目录并不需要放在内核目录下面.

clean:
	make -C $(KERN_DIR) M=`pwd` modules clean
	rm -rf modules.order

obj-m	+= drv_leds.o
```


## 测试代码, drv_leds_test.c

``` c
// ~/jz2440/driver/drv_leds/drv_leds_test.c

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>

/*
  *  ledtest <dev> <on|off>
  */
void print_usage(char *file)
{
    printf("Usage:\n");
    printf("%s <dev> <on|off>\n",file);
    printf("eg. \n");
    printf("%s /dev/leds on\n", file);
    printf("%s /dev/leds off\n", file);
    printf("%s /dev/led1 on\n", file);
    printf("%s /dev/led1 off\n", file);
}

int main(int argc, char **argv)
{
    int fd;
    char* filename;
    char val;

    if (argc != 3) {                        // 输入错误, 打印帮助信息
        print_usage(argv[0]);
        return 0;
    }

    filename = argv[1];

    fd = open(filename, O_RDWR);            // 打开设备
    if (fd < 0) {
        printf("error, can't open %s\n", filename);
    } else if (!strcmp("on", argv[2])) {    // 亮灯
        val = 1;
        write(fd, &val, 1);
    } else if (!strcmp("off", argv[2])) {   // 灭灯
        val = 0;
        write(fd, &val, 1);
    } else {
        print_usage(argv[0]);
    }

    return 0;
}
```

## 编译加载并测试

``` bash
# ===== Ubuntu主机端, 编译驱动 =====
# pwd = drv_leds.c所在的目录.
$ make clean
$ make                                  # 编译驱动
# 成功后, 生成 drv_leds.ko 动态库

$ cp drv_leds.ko ~/jz2440/fs_first/     # 先直接放到文件系统根目录下了.
# 嵌入式端最好用网络的方式加载文件系统, 这样就不用重新烧录文件系统了, 便于调试!

# ===== 嵌入式Linux端, 加载驱动 =====
# pwd = /
$ insmod drv_leds.ko                    # 加载模块
drv_leds initialized                    # 打印的调试信息
$ cat /proc/devices                     # 查看设备信息
Character devices:
252 drv_leds                            # 应该能找到这一项, 自动分配的主设备号252

# 需要配置好 mdev. 才支持insmod后自动生成设备节点.
$ ls -l /dev/led1                       # 查看自动加载的设备节点 led1. 其它3个同理查看
crw-rw----  1 0     0       252, 1  时间信息    /dev/led1
$ cd /sys/class/                        # 查看设备的类
$ ls
leds                                    # 可以找到这一项
$ ls leds/                              # 查看类下面的设备
led1 led2 led3 leds
$ cat leds/led1/dev                     # 查看设备信息
252:1                                   # 主设备号252(自动分配的), 次设备号为1
$ rmmod drv_leds.ko                     # 移除驱动
drv_leds deinitialized                  # 打印的调试信息
$ ls /dev/led1                          # 会告知文件或目录不存在
$ ls /sys/class                         # leds 已经不见了! 说明mdev把这个设备节点自动卸载掉了.
$ insmod drv_leds.ko                    # 加载一下, 为测试做准备

# ===== Ubuntu主机端, 编译测试源码 =====
# pwd = drv_leds_test.c所在的目录.
$ arm-linux-gcc -o drv_leds_test drv_leds_test.c    # 编译应用程序
$ cp drv_leds_test ~/jz2440/fs_first/               # 先直接放到文件系统根目录下了.

# ===== 嵌入式Linux端, 测试驱动 =====
$ ./drv_leds_test                       # 显示使用方法
$ ./drv_leds_test /dev/leds on          # LED全开
$ ./drv_leds_test /dev/led2 off         # 关LED2
```




----------

***原创于 [DRA&PHO](https://draapho.github.io/)***