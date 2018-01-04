---
title: 驱动之同步互斥阻塞
date: 2017-12-13
categories: embedded linux
tags: [linuxembedded linux, drv]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [驱动之字符设备-框架](https://draapho.github.io/2017/11/22/1733-drv-chr1/)
- [驱动之基于LinK+设计按键驱动](https://draapho.github.io/2017/11/30/1740-drv-chr2/)
- [驱动之基于中断设计按键驱动](https://draapho.github.io/2017/12/07/1741-drv-chr3/)
- [驱动之poll机制](https://draapho.github.io/2017/12/11/1742-drv-chr4/)
- [驱动之异步通知](https://draapho.github.io/2017/12/12/1743-drv-chr5/)
- [驱动之同步互斥阻塞](https://draapho.github.io/2017/12/13/1744-drv-chr6/)
- [驱动之定时器按键防抖](https://draapho.github.io/2018/01/04/1801-drv-chr7/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.
硬件具备唯一性, 因此某一时刻应该只有一个应用程序能对驱动进行操作.


# 原子操作

**原子操作指的是在执行过程中不会被别的进程或中断所打断的操作**
底层实现就是 `raw_local_irq_save` `raw_local_irq_restore`, 保存中断并禁止, 操作完成后, 恢复.

``` c
// 常用的原子操作函数
atomic_t v = ATOMIC_INIT(0);            // 定义原子变量v并初始化为0
atomic_read(atomic_t *v);               // 返回原子变量的值
atomic_inc(atomic_t *v);                // 原子变量增加1
atomic_dec(atomic_t *v);                // 原子变量减少1
atomic_dec_and_test(atomic_t *v);       // 自减操作后测试其是否为0，为0则返回true，否则返回false

// 更多宏定义可参考 /linux/include/asm/atomic.h
```

## drv_sem.c
源码基于 [驱动之基于中断设计按键驱动](https://draapho.github.io/2017/12/07/1741-drv-chr3/), 部分修改而来
只显示新增和修改的部分. 这样更直观易懂.

``` c
#include"drv_sem.h"                                 // 头文件改一下
#define DRV_KEY_INT_NODE_NAME "drv_sem"             // 名称改一下

atomic_t canopen = ATOMIC_INIT(1);                  // 定义原子变量canopen并初始化为1

static int drv_key_int_open(struct inode *inode,struct file *filp)
{
	int ret;
    
    if (!atomic_dec_and_test(&canopen)) {           // 新增的原子操作判断 
        atomic_inc(&canopen);                       // 打开失败, 恢复到0
        return -EBUSY;
    }
    
    ......

    // 因为这一句的存在, 就算没有原子操作 应用程序无法调用此驱动多次. 先注释掉.
	// if (ret) return -EINVAL;                        
	// else return 0;
    return 0;                                       // 为了测试, 直接返回0.
}

static int drv_key_int_release(struct inode *inode,struct file *filp)
{
	......
    
    atomic_inc(&canopen);                           // 恢复原子操作为1
	return 0;
}
```

## drv_sem.h

``` c
#define DRIVER_NAME "drv_sem"       // 名称改一下
```

## Makefile

``` makefile
obj-m		:= drv_sem.o            # 目标名称改一下
```

## 测试文件 test_drv_sem.c

``` c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>

int main(int argc, char **argv)
{
	int fd;
	unsigned char keys_val;

	fd = open("/dev/drv_sem0", O_RDWR);
	if (fd < 0) {
		printf("can't open!\n");
		return -1;
	}

	while (1) {
		read(fd, &keys_val, 1);
		printf("keys_val=0x%x, pid=%d\n", keys_val, getpid());
	}
	
	return 0;
}
```

## 编译并测试
``` bash
# ubuntu主机端, 编译驱动和测试文件
# pwd = /home/draapho/share/drv/drv_sem/KERN_SRC    # 驱动源码路径, share是nfs共享文件夹

$ make clean
$ make modules
$ arm-linux-gcc test_drv_sem.c -o test_drv_sem

# jz2440端
$ insmod drv_sem.ko
drv_sem:INIT

$ ./test_drv_sem &      # 第一次运行
$ top
789   779 0        S     1312   2%   0% ./test_drv_sem
# 显示当前进程信息.
$ ./test_drv_sem &      # 第二次运行
can't open!             # 打开文件失败
$ top
789   779 0        S     1312   2%   0% ./test_drv_sem
# 依旧只有一个处于睡眠状态的测试程序.
```


# 信号量

信号量是用于保护临界区的一种常用方法, 只有得到信号量进程才能执行临界区代码.
与原子操作不同的是, 当获取不到信号量是, **进程进入休眠等待状态!**
一但其他进程释放信号量, 该进程获得信号量后, 会恢复运行.

``` c
//定义信号量
struct semaphore sem;                       // 信号量
static DECLARE_MUTEX(lock);                 // 定义互斥锁

//初始化信号量
void sema_init (struct semaphore *sem, int val);
void init_MUTEX(struct semaphore *sem);     // 初始化为0

//获得信号量
void down(struct semaphore * sem);
int down_interruptible(struct semaphore * sem); 
int down_trylock(struct semaphore * sem);

//释放信号量
void up(struct semaphore * sem);
```

## drv_sem.c
源码基于 [驱动之基于中断设计按键驱动](https://draapho.github.io/2017/12/07/1741-drv-chr3/), 部分修改而来
只显示新增和修改的部分. 这样更直观易懂.

``` c
#include"drv_sem.h"                                 // 头文件改一下
#define DRV_KEY_INT_NODE_NAME "drv_sem"             // 名称改一下

atomic_t canopen = ATOMIC_INIT(1);                  // 定义原子变量canopen并初始化为1
static DECLARE_MUTEX(key_lock);                     // 定义互斥锁 

static int drv_key_int_open(struct inode *inode,struct file *filp)
{
	int ret;

#if 0
    if (!atomic_dec_and_test(&canopen)) {           // 新增的原子操作判断 
        atomic_inc(&canopen);                       // 打开失败, 恢复到0
        return -EBUSY;
    }
#else
    down(&key_lock);                                // 获取信号量
#endif
    
    ......

    // 因为这一句的存在, 就算没有原子操作 应用程序无法调用此驱动多次. 先注释掉.
	// if (ret) return -EINVAL;                        
	// else return 0;
    return 0;                                       // 为了测试, 直接返回0.
}

static int drv_key_int_release(struct inode *inode,struct file *filp)
{
	......
    
#if 0
    atomic_inc(&canopen);                           // 恢复原子操作为1
#else
    up(&key_lock);                                  // 释放信号量
#endif
	return 0;
}
```

其它文件 `drv_sem.h` `Makefile` `test_drv_sem.c` 和原子操作的部分一样. 不用修改

## 编译并测试
``` bash
# ubuntu主机端, 编译驱动和测试文件
# pwd = /home/draapho/share/drv/drv_sem/KERN_SRC    # 驱动源码路径, share是nfs共享文件夹

$ make clean
$ make modules
$ arm-linux-gcc test_drv_sem.c -o test_drv_sem

# jz2440端
$ insmod drv_sem.ko
drv_sem:INIT

$ ./test_drv_sem &      # 第一次运行
$ top
789   779 0        S     1312   2%   0% ./test_drv_sem
# 显示当前进程信息.
$ ./test_drv_sem &      # 第二次运行
# 并不会显示 can't open!, 此进程实际上在等待获取信号量
$ top
789   779 0        S     1312   2%   0% ./test_drv_sem
791   779 0        D     1308   2%   0% ./test_drv_sem
# 789 是第一个进程, 处于S, 可中断的睡眠状态, 在等待按键中断
# 791 是第二个进程, 处于D, 不可中断的睡眠状态, 在等待获取信号量

$ kill 789
$ top                   # 结束第一个进程, 再看进程表
791   779 0        S     1308   2%   0% ./test_drv_sem
# 791 是第二进程, 获取信号量成功后开始运行, 处于S状态.
```

# 阻塞和非阻塞

- 阻塞操作
    - 系统默认就是阻塞操作
    - 是指在执行设备操作时若不能获得资源则挂起进程，直到满足可操作的条件后再进行操作。
    - 被挂起的进程进入休眠状态，被从调度器的运行队列移走，直到等待的条件被满足。
- 非阻塞操作
    - 使用宏定义 `O_NONBLOCK`
    - 进程在不能进行设备操作时并不挂起，它或者放弃，或者不停地查询，直至可以进行操作为止。

    
## drv_sem.c
源码基于 [驱动之基于中断设计按键驱动](https://draapho.github.io/2017/12/07/1741-drv-chr3/), 部分修改而来
只显示新增和修改的部分. 这样更直观易懂.

``` c
#include"drv_sem.h"                                 // 头文件改一下
#define DRV_KEY_INT_NODE_NAME "drv_sem"             // 名称改一下

atomic_t canopen = ATOMIC_INIT(1);                  // 定义原子变量canopen并初始化为1
static DECLARE_MUTEX(key_lock);                     // 定义互斥锁 

static int drv_key_int_open(struct inode *inode,struct file *filp)
{
	int ret;

#if 0
    if (!atomic_dec_and_test(&canopen)) {
        atomic_inc(&canopen); 
        return -EBUSY;
    }
#else
    if (filp->f_flags & O_NONBLOCK) {               // 非阻塞
        if (down_trylock(&key_lock))                // 尝试获取信号量
            return -EBUSY;
    } else {
        down(&key_lock);                            // 获取信号量, 阻塞
    }
#endif
    
    ......

    // 因为这一句的存在, 就算没有原子操作 应用程序无法调用此驱动多次. 先注释掉.
	// if (ret) return -EINVAL;                        
	// else return 0;
    return 0;                                       // 为了测试, 直接返回0.
}

static ssize_t drv_key_int_read(struct file *filp,  // 读取函数也需要修改一下!
    char __user *ubuff,size_t count,loff_t *offp)
{
    ......
    if (count != 1)
        return -EINVAL;
    
    if (filp->f_flags & O_NONBLOCK) {               // 非阻塞
        if (!ev_press)                              // 无按键, 立刻返回
            return -EAGAIN;
    } else {
        // ev_press, 用于判断是否可以让当前进程睡眠(让出CPU, 进程切换)
        wait_event_interruptible(key_waitq, ev_press);      // 阻塞
    }

    ev_press = 0;                                           // 运行后, 立刻清零
    if (copy_to_user(ubuff, &keys_val, 1)) {                // 传回按键值
        return -EFAULT;
    }
    return 1;
}

static int drv_key_int_release(struct inode *inode,struct file *filp)
{
	......
    
#if 0
    atomic_inc(&canopen);                           // 恢复原子操作为1
#else
    up(&key_lock);                                  // 释放信号量
#endif
	return 0;
}
```

文件 `drv_sem.h` `Makefile` 和信号量的部分一样. 不用修改
阻塞是open函数的默认值, 其测试就不写了, 因为之前写的按键驱动测试都是阻塞的.

## 测试文件 unblock_drv_sem.c

``` c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>

int main(int argc, char **argv)
{
	int ret, fd;
	unsigned char keys_val;

	fd = open("/dev/drv_sem0", O_RDWR | O_NONBLOCK);    // O_NONBLOCK 非阻塞
	if (fd < 0) {
		printf("can't open!\n");
		return -1;
	}

	while (1) {
		ret = read(fd, &keys_val, 1);                   // 读取函数是否阻塞取决于open函数
		printf("keys_val=0x%x, ret=%d\n",keys_val,ret);
        sleep(3);
	}
	
	return 0;
}
```

## 编译并测试
``` bash
# ubuntu主机端, 编译驱动和测试文件
# pwd = /home/draapho/share/drv/drv_sem/KERN_SRC    # 驱动源码路径, share是nfs共享文件夹

$ make clean
$ make modules
$ arm-linux-gcc unblock_drv_sem.c -o unblock_drv_sem

# jz2440端
$ insmod drv_sem.ko
drv_sem:INIT

$ ./unblock_drv_sem &       # 第一次运行
key_val=0x0, ret=-1         # 无按键, 返回值 -EAGAIN
key_val=0x0, ret=-1         # 无按键, 返回值 -EAGAIN
key_val=0x1, ret=1          # 有按键, 返回值为1
$ top
789   779 0        S     1312   2%   0% ./unblock_drv_sem
# 显示当前进程信息.
$ ./unblock_drv_sem &      # 第二次运行
# 显示 can't open!, 非阻塞进程, 尝试获取信号量失败后, 返回给应用程序 -EBUSY
$ top
789   779 0        S     1312   2%   0% ./unblock_drv_sem
# 依旧只有一个789进程
```
