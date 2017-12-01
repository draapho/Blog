---
title: 驱动之基于LinK+设计按键驱动
date: 2017-11-30
categories: embedded linux
tags: [linuxembedded linux, drv]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之字符设备-框架](https://draapho.github.io/2017/11/22/1733-drv-chr1/)
- [驱动之基于LinK+设计按键驱动](https://draapho.github.io/2017/11/30/1740-drv-chr2/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.


上文[驱动之字符设备-框架](https://draapho.github.io/2017/11/22/1733-drv-chr1/)是根据jz2440教程书写的. 整个过程比较繁杂.
在此期间, 搜索了一下Linux内核开发工具, 寻得一款非常好用的 Link+IDE, 安装配置见 [LinK+, 一款Linux内核开发IDE](https://draapho.github.io/2017/11/27/1737-linux-ide/).
这款软件可以自动生成Linux驱动开发的软件模板, 可以大大减少工作量, 提高效率!
因此, 此文基于LinK+的生成的驱动框架, 对按键驱动进行开发.


# 使用LinK+生成驱动模板

打开 LinK+IDE, 新建工程, 选择 `Linux Kernel Development(LinK+)` 下面的 `Device Driver Project`
然后如图配置即可.

![LinKDriverWizard1.JPG](https://draapho.github.io/images/1740/LinKDriverWizard1.JPG)

![LinKDriverWizard2.JPG](https://draapho.github.io/images/1740/LinKDriverWizard2.JPG)

确定后, LinK+IDE会自动生成代码, 基于这个代码模板, 去实现按键功能函数即可.

**注意** 自动生成的模板中, 函数`device_create`和linux-2.6.22.6不兼容, 需要去掉最后一个NULL!
不修改的话, 编译时有个警告, 尝试加载模块时会报错: 
`Unable to handle kernel NULL pointer dereference at virtual address 00000000`


# 驱动源码

## drv_key.c

``` c
/*
===============================================================================
Driver Name		:		drv_key
Author			:		DRAAPHO
License			:		GPL
Description		:		LINUX DEVICE DRIVER PROJECT
===============================================================================
*/

#include"drv_key.h"

#define DRV_KEY_N_MINORS 4
#define DRV_KEY_FIRST_MINOR 0
#define DRV_KEY_NODE_NAME "key"
#define DRV_KEY_BUFF_SIZE 1

MODULE_LICENSE("GPL");
MODULE_AUTHOR("DRAAPHO");

int drv_key_major=0;
dev_t drv_key_device_num;
struct class *drv_key_class;

typedef struct privatedata {
	int nMinor;
	char buff[DRV_KEY_BUFF_SIZE];
	struct cdev cdev;
	struct device *drv_key_device;
} drv_key_private;

drv_key_private devices[DRV_KEY_N_MINORS];

static int drv_key_open(struct inode *inode,struct file *filp)
{
	/* TODO Auto-generated Function */
	drv_key_private *priv = container_of(inode->i_cdev ,
									drv_key_private ,cdev);
	filp->private_data = priv;

	if ((priv->nMinor == 0) || (priv->nMinor == 1))
		s3c2410_gpio_cfgpin(S3C2410_GPF0, S3C2410_GPF0_INP);
	if ((priv->nMinor == 0) || (priv->nMinor == 2))
		s3c2410_gpio_cfgpin(S3C2410_GPF2, S3C2410_GPF2_INP);
	if ((priv->nMinor == 0) || (priv->nMinor == 3))
		s3c2410_gpio_cfgpin(S3C2410_GPG3, S3C2410_GPG3_INP);

	PINFO("minor=%d\n", priv->nMinor);
	PINFO("In char driver open() function\n");
	return 0;
}					

//static int drv_key_release(struct inode *inode,struct file *filp)
//{
//	/* TODO Auto-generated Function */
//	drv_key_private *priv;
//	priv=filp->private_data;
//
//	PINFO("In char driver release() function\n");
//	return 0;
//}

static ssize_t drv_key_read(struct file *filp, 
	char __user *ubuff,size_t count,loff_t *offp)
{
	/* TODO Auto-generated Function */
	int n=0;
	char key_vals[3]={0};
	drv_key_private *priv;
	priv = filp->private_data;

	if ((priv->nMinor == 0) || (priv->nMinor == 1))
		key_vals[0] = !s3c2410_gpio_getpin(S3C2410_GPF0);
	if ((priv->nMinor == 0) || (priv->nMinor == 2))
		key_vals[1] = !s3c2410_gpio_getpin(S3C2410_GPF2);
	if ((priv->nMinor == 0) || (priv->nMinor == 3))
		key_vals[2] = !s3c2410_gpio_getpin(S3C2410_GPG3);
	copy_to_user(ubuff, key_vals, sizeof(key_vals));

//	PINFO("In char driver read() function\n");
	return n;
}

static const struct file_operations drv_key_fops= {
	.owner				= THIS_MODULE,
	.open				= drv_key_open,
//	.release			= drv_key_release,
	.read				= drv_key_read,
};

static int __init drv_key_init(void)
{
	/* TODO Auto-generated Function Stub */

	int i;
	int res;

	res = alloc_chrdev_region(&drv_key_device_num,DRV_KEY_FIRST_MINOR,DRV_KEY_N_MINORS ,DRIVER_NAME);
	if(res) {
		PERR("register device no failed\n");
		return -1;
	}
	drv_key_major = MAJOR(drv_key_device_num);
	drv_key_class = class_create(THIS_MODULE , DRIVER_NAME);
	if(!drv_key_class) {
		PERR("class creation failed\n");
		return -1;
	}

	for(i=0;i<DRV_KEY_N_MINORS;i++) {
		drv_key_device_num= MKDEV(drv_key_major ,DRV_KEY_FIRST_MINOR+i);
		cdev_init(&devices[i].cdev , &drv_key_fops);
		cdev_add(&devices[i].cdev,drv_key_device_num,1);

		devices[i].drv_key_device  = 
				// BE CARE, device_create has different parameters...
//				device_create(drv_key_class , NULL ,drv_key_device_num ,
//							NULL ,DRV_KEY_NODE_NAME"%d",DRV_KEY_FIRST_MINOR+i);
				device_create(drv_key_class , NULL ,drv_key_device_num ,
							DRV_KEY_NODE_NAME"%d",DRV_KEY_FIRST_MINOR+i);
		if(!devices[i].drv_key_device) {
			class_destroy(drv_key_class);
			PERR("device creation failed\n");
			return -1;
		}
		devices[i].nMinor = DRV_KEY_FIRST_MINOR+i;
	}

	PINFO("INIT\n");
	return 0;
}

static void __exit drv_key_exit(void)
{	
	/* TODO Auto-generated Function Stub */

	int i;
	PINFO("EXIT\n");

	for(i=0;i<DRV_KEY_N_MINORS;i++) {
		drv_key_device_num= MKDEV(drv_key_major ,DRV_KEY_FIRST_MINOR+i);

		cdev_del(&devices[i].cdev);

		device_destroy(drv_key_class ,drv_key_device_num);

	}
	class_destroy(drv_key_class);
	unregister_chrdev_region(drv_key_device_num ,DRV_KEY_N_MINORS);	

}

module_init(drv_key_init);
module_exit(drv_key_exit);
```

## drv_key.h

``` c
#define DRIVER_NAME "drv_key"
#define PDEBUG(fmt,args...) printk(KERN_DEBUG"%s:"fmt,DRIVER_NAME, ##args)
#define PERR(fmt,args...) printk(KERN_ERR"%s:"fmt,DRIVER_NAME,##args)
#define PINFO(fmt,args...) printk(KERN_INFO"%s:"fmt,DRIVER_NAME, ##args)
#include<linux/cdev.h>
#include<linux/device.h>
#include<linux/fs.h>
#include<linux/init.h>
#include<linux/kdev_t.h>
#include<linux/module.h>
#include<linux/types.h>
#include<linux/uaccess.h>
#include <asm/arch/regs-gpio.h>
#include <asm/hardware.h>
```

## Makefile

``` makefile
obj-m		:= drv_key.o 
KERN_SRC	:= /home/draapho/share/kernel/linux-2.6.22.6/
PWD			:= $(shell pwd)

modules:
	make -C $(KERN_SRC) M=$(PWD) modules

install:
	make -C $(KERN_SRC) M=$(PWD) modules_install
	depmod -a

clean:
	make -C $(KERN_SRC) M=$(PWD) clean
```

## 测试文件 drv_key_test.c

``` c
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>

void print_usage(char *file)
{
    printf("Usage:\n");
    printf("%s <dev>\n",file);
    printf("eg. \n");
    printf("%s /dev/key0\n", file);
    printf("%s /dev/key1\n", file);
}
int main(int argc, char **argv)
{
    int fd;
    char* filename;
    char val;
    if (argc != 2) {                        // 输入错误, 打印帮助信息
        print_usage(argv[0]);
        return 0;
    }
    filename = argv[1];
    fd = open(filename, O_RDWR);            // 打开设备
    if (fd < 0) {
        printf("error, can't open %s\n", filename);
    } else {
    	char key_vals[3];
    	int cnt = 0;

    	while(1) {
        	read(fd, key_vals, sizeof(key_vals));
    		if (key_vals[0] || key_vals[1] || key_vals[2]) {
    			printf("%04d key pressed: %d %d %d\n", cnt++, key_vals[0], key_vals[1], key_vals[2]);
    		}
    		usleep(100);
    	}
    }
    return 0;
}
```

# 编译并测试

## Ubuntu主机端

``` bash
# 主机端, 编译源码
# pwd = /home/draapho/share/drv/drv_key/KERN_SRC    # 驱动源码路径, share是nfs共享文件夹

# 编译驱动
$ make clean
$ make modules                  # LinK+的Makefile使用的是 make modules 而不是 make all

# 编译测试代码
$ arm-linux-gcc drv_key_test.c -o drv_key_test
```


## 开发板端

开发环境上, 开发板烧录好内核, 使用nfs挂载共享文件. 所以无需任何文件传输的步骤.
开发环境的具体配置可参考: [基于DHCP建立嵌入式Linux开发环境](https://draapho.github.io/2017/11/28/1738-dhcp-env/)

``` bash
# 开发板端, 测试模块加载情况
# pwd = /home/draapho/share/drv/drv_key/KERN_SRC    # 驱动源码路径, share是nfs共享文件夹

$ insmod drv_key.ko     # 加载模块
drv_key:INIT

$ cat /proc/devices     # 查看设备
249 drv_key
250 drv_key
251 drv_key
252 drv_key

$ ls /dev/key*          # 查看设备节点               
/dev/key0  /dev/key1  /dev/key2  /dev/key3

$ ls /sys/class/drv_key/            # 查看设备的类
key0  key1  key2  key3
$ cat /sys/class/drv_key/key3/dev   # 查看设备号
249:3

$ rmmod drv_key.ko      # 移除模块
drv_key:EXIT
```

下面进行按键测试

``` bash
# 开发板端, 测试驱动功能
# pwd = /home/draapho/share/drv/drv_key/KERN_SRC    # 驱动源码路径, share是nfs共享文件夹

$ insmod drv_key.ko     # 加载模块

# key0->all, key1->s2, key2->s3, key3->s4
$ ./drv_key_test /dev/key0          # 检测所有按键 
drv_key:minor=0                     # 打印信息
drv_key:In char driver open() function

# jz2440开发板按下按键, 就会打印按键信息. 1表示按下. 0表示松开.
# 按ctrl+c 终止进程

$ ./drv_key_test /dev/key0 &        # 后台运行
$ top                               # 查看系统资源情况
# 可以看到 ./drv_key_test /dev/key0 进程表现还不错. %MEM=2% %CPU=0%

$ kill <PID>                        # 杀掉指定进程
# 这是因为我在测试代码的死循环里加了100ms的延时, 去掉usleep这行, 再测的话会变成:
# %CPU=99%
```

结论: 这种方式的按键驱动是有巨大风险的, 因为其性能取决于应用层怎么写, 这是不可接受的!
实际开发中, 按键多半采用中断或poll方式.


# 驱动框架的比较

LinK+自动生成的框架和jz2440教程的框架主要有如下区别:
- `alloc_chrdev_region` or `register_chrdev_region` vs `register_chrdev`
    - 本质上没啥区别, 都会调用 `__register_chrdev_region()`
    - [字符设备 register_chrdev_region()、alloc_chrdev_region() 和 register_chrdev()](http://blog.csdn.net/freenaut/article/details/4298174)
- `device_create` vs `class_device_create`
    - 似乎是历史遗留问题, `device_create` 函数用于替换 `class_device_create`.
    - [class_create(),class_device_create()或device_create()自动创建设备文件结点](http://blog.csdn.net/yuzaipiaofei/article/details/6790689)
- 子设备号Minor获取上的区别.
    - 使用 private_data 更符合linux的规范

总体而言, jz2440的教程使用的框架比较老, LinK+使用的框架更合适高版本的linux内核.



----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***