---
title: 面试之嵌入式Linux
date: 2018-05-08
categories: interview
tags: [interview]
description: 面试题集.
---

# 总览
- [逻辑|这样表达，事半功倍](https://draapho.github.io/2017/05/04/1714-expression/)
- [面试之常规问题](https://draapho.github.io/2018/01/10/1805-interview-general/)
- [面试之嵌入式C语言](https://draapho.github.io/2018/05/07/1816-interview-c/)
- [C语言知识巩固](https://draapho.github.io/2017/05/17/1715-c/)
- [面试之嵌入式Linux](https://draapho.github.io/2018/05/08/1817-interview-linux/)
- [面试之面向对象](https://draapho.github.io/2022/08/10/2206-interview-oop/)
- [设计模式概要](https://draapho.github.io/2022/08/11/2207-design-patterns/)

我个人面试经验极少, 但这种能力都是需要培养的. 此系列总结一下面试中常见的技能要点. 侧重于技术面的准备.


# common
## Q: What Is The Difference Between Microprocessor And Microcontroller?
Microcontroller is a self-contained system with peripherals, memory and a processor that can be used as embedded system.

Microprocessor is managers of the resources (I/O, memory) which lie outside of its architecture.

## Q: Difference btwn Process and Thread
the threads are a part of a process
Process has a self-contained execution environment, each process has its own memory space. just can use IPC to communication
Threads share resources, which helps in efficient communication between threads.

## Q: What is thread safety? What is re-entrancy?
线程安全的概念比较直观，一般来说，一个函数被称为线程安全的，当且仅当被多个并发线程反复调用时，它会一直产生正确的结果.
可重入函数一定是线程安全的. 但线程安全的函数不一定是可重入的.

对于可重入函数, 有如下要求:
- 不使用全局变量或静态变量；
- 不使用用malloc或者new开辟出的空间；
- 不调用不可重入函数；


## Q: Explain Interrupt Latency And How Can We Decrease It?
- Interrupt latency basically refers to the time span an interrupt is generated and it being serviced by an appropriate routine defined, usually the interrupt handler.
- External signals, some condition in the program or by the occurrence of some event, these could be the reasons for generation of an interrupt.
- Interrupts can also be masked so as to ignore them even if an event occurs for which a routine has to be executed.
- Following steps could be followed to reduce the latency
    - ISRs being simple and short.
    - Interrupts being serviced immediately
    - Avoiding those instructions that increase the latency period.
    - Also by prioritizing interrupts over threads.
    - Avoiding use of inappropriate APIs.


## Q: What is Top half & bottom half of a kernel?
Sometimes to handle an interrupt, a substantial amount of work has to be done. But it conflicts with the speed need for an interrupt handler.
To handle this situation, Linux splits the handler into two parts: Top half and Bottom half.
- The top half is the routine that actually responds to the interrupt.
- The bottom half on the other hand is a routine that is scheduled by the upper half to be executed later at a safer time.

All interrupts are enabled during execution of the bottom half. The top half saves the device data into the specific buffer, schedules bottom half and exits. The bottom half does the rest. This way the top half can service a new interrupt while the bottom half is working on the previous.


## Q: List Out Various Uses Of Timers In Embedded System?
- Real Time Clock (RTC) for the system
- Initiating an event after a preset time delay
- Initiating an event after a comparison of preset times
- Capturing the count value in timer on an event
- Between two events finding the time interval
- Time slicing for various tasks
- Time division multiplexing
- Scheduling of various tasks in RTOS

## Q: Significance of watchdog timer in Embedded Systems.
The watchdog timer is a timing device with a predefined time interval. During that interval, some event may occur or else the device generates a time out signal. It is used to reset to the original state whenever some inappropriate events take place which can result in system malfunction. It is usually operated by counter devices.

## Q: Difference between RISC and CISC processor.

RISC (Reduced Instruction Set Computer) could carry out a few sets of simple instructions simultaneously. Fewer transistors are used to manufacture RISC, which makes RISC cheaper. RISC has uniform instruction set and those instructions are also fewer in number. Due to the less number of instructions as well as instructions being simple, the RISC computers are faster. RISC emphasise on software rather than hardware. RISC can execute instructions in one machine cycle.

CISC (Complex Instruction Set Computer) is capable of executing multiple operations through a single instruction. CISC have rich and complex instruction set and more number of addressing modes. CISC emphasise on hardware rather that software, making it costlier than RISC. It has a small code size, high cycles per second and it is slower compared to RISC.


## Q: What is RTOS? What is the difference between hard real-time and soft real-time OS?
The scheduler in a Real Time Operating System (RTOS) is designed to provide a predictable execution pattern. In an embedded system, a certain event must be entertained in strictly defined time.
To meet real time requirements, the behaviour of the scheduler must be predictable. This type of OS which have a scheduler with predictable execution pattern is called Real Time OS(RTOS).

A Hard real-time system strictly adheres to the deadline associated with the task. If the system fails to meet the deadline, even once, the system is considered to have failed.
In case of a soft real-time system, missing a deadline is acceptable. In this type of system, a critical real-time task gets priority over other tasks and retains that priority until it completes.


## Q: What type of scheduling is there in RTOS?
RTOS uses pre-emptive scheduling. In pre-emptive scheduling, the higher priority task can interrupt a running process and the interrupted process will be resumed later.

## Q: What is priority inversion? What is priority inheritance?
If two tasks share a resource, the one with higher priority will run first. However, if the lower-priority task is using the shared resource when the higher-priority task becomes ready, then the higher-priority task must wait for the lower-priority task to finish. In this scenario, even though the task has higher priority it needs to wait for the completion of the lower-priority task with the shared resource. This is called priority inversion.

Priority inheritance is a solution to the priority inversion problem. The process waiting for any resource which has a resource lock will have the maximum priority. This is priority inheritance. When one or more high priority jobs are blocked by a job, the original priority assignment is ignored and execution of critical section will be assigned to the job with the highest priority in this elevated scenario. The job returns to the original priority level soon after executing the critical section.

## Q: What is job of preprocessor, compiler, assembler and linker?
The preprocessor commands are processed and expanded by the preprocessor before actual compilation.

After preprocessing, the compiler takes the output of the preprocessor and the source code, and generates assembly code.

Once compiler completes its work, the assembler takes the assembly code and produces an assembly listing with offsets and generate object files.

The linker combines object files or libraries and produces a single executable file. It also resolves references to external symbols, assigns final addresses to functions and variables, and revises code and data to reflect new addresses.

## Q: How you will debug the memory issues?
- First of all, double check the code source. Make sure already paired using `kmalloc` `kfree` and `vmalloc` `vfree`
- `free -m` to monitor memory using status.
- `kmemleak` to log the possible problem
- oom or panic information from kernel
- Intercept all functions that allocate and deallocate memory.

## Q: Debugging techniques
`GDB`, printk, led, `/var/log/`



# hardware

## Q: What Does Dma Address Will Deal With?
DMA address deals with physical addresses. It is a device which directly drives the data and address bus during data transfer. So, it is purely physical address.

## Q: What is virtual memory?
Virtual memory is a technique that allows processes to allocate memory in case of physical memory shortage using automatic storage allocation upon a request.
The advantage of the virtual memory is that the program can have a larger memory than the physical memory. It allows large virtual memory to be provided when only a smaller physical memory is available.

Virtual memory can be implemented using paging.
A paging system is quite similar to a paging system with swapping. When we want to execute a process, we swap it into memory. Here we use a lazy swapper called pager rather than swapping the entire process into memory. When a process is to be swapped in, the pager guesses which pages will be used based on some algorithm, before the process is swapped out again. Instead of swapping whole process, the pager brings only the necessary pages into memory. By that way, it avoids reading in unnecessary memory pages, decreasing the swap time and the amount of physical memory.

## Q: What is kernel paging? What is page frame?
Paging is a memory management scheme by which computers can store and retrieve data from the secondary memory storage when needed in to primary memory. In this scheme, the operating system retrieves data from secondary storage in same-size blocks called pages. The paging scheme allows the physical address space of a process to be non continuous. Paging allows OS to use secondary storage for data that does not fit entirely into physical memory.

A page frame is a block of RAM that is used for virtual memory. It has its page frame number. The size of a page frame may vary from system to system, and it is in the power of 2 in bytes. Also, it is the smallest length block of memory in which an operating system maps memory pages.

## Q: Virtual Address, Linear Address, Physical Address
32-bit CPU 3GB for user layer, 1GB for kernel layer
`kmalloc` apply the physical address directly, so it is continuous but size limination
`vmalloc` apply the virtual memory, in physical it is not continuous. need MMU to translate to physical memory.
Virtual Address -- Segment(GDT LDT) -- Linear Address -- Paging (4 layer Page Directory, Page Table) -- Physical Address

## Q:How to decide whether given processor is using little endian format or big endian format ?

``` c
#include <stdio.h>

int check_for_endianness()
{
  unsigned int x = 1;
  char *c = (char*) &x;
  return (int)*c;
}
```

## Q: nand vs nor flash
- 使用复杂 vs 使用简单(same as sram)
- 读取慢 vs 读取快
- 写入快 vs 写入慢
- 顺序读取快, 随机存取慢 vs 随机存取快
- 容量大 vs 容量小
- 擦写次数多 vs 擦写次数少
- yaffs2 vs jffs2
- 存放引导程序, 参数区 vs 用户文件, 多媒体文件

## Q: Definition and difference between Hardware interrupt, Software Interrupt, Exception, Trap and Signals?
- Hardware Interrupts: may arrive anytime, typically IO interrupts.
- Exception: may only arrive after the execution of an instruction, for example when the cpu try to devide a number by 0 or a page fault
- Trap is a kind of exceptions, whose main purpose is for debugging
- Software Interrupt occurs at the request of the programmer. They are used to implement system calls, and handled by the CPU as trap.
- Signals are part of the IPC, not belong to interrupts or exceptions.

## Q: Explain MMU in Linux
Paged memory management unit. Translation of virtual memory addresses to physical addresses

## Q: What are high memory and low memory on Linux
- The High Memory is the segment of memory that user-space programs can address. It cannot touch Low Memory.
- Low Memory is the segment of memory that the Linux kernel can address directly.
- If the kernel must access High Memory, it has to map it into its own address space first.
- `copy_from_user(&val, data, 1);`

## Q: How to register an interrupt handler?
- `request_irq(IRQ_ID, handler_irq, ...);`
- `irqreturn_t handler_irq(int irq, void *dev_id)` can get the IRQ_ID from `int irq`


# kernel

## Q: Linux驱动的一些基本概念
- 主设备号. 可以人工指定, 也可以由系统动态分配. 理解为设备类型的id即可.
- 子设备号. 譬如一个led灯的驱动设备, 可以实现多个led的控制. 子设备号可以提供针对特定的led进行控制
- mdev. 根据动态驱动模块的信息自动创建设备节点.
- 地址映射. 这是与单片机的区别. 单片机操作寄存器可以直接使用物理地址. 但linux下使用的是虚拟地址!
    - 地址转换使用 `ioremap` `iounmap` 函数.
    - 一般的芯片商也会提供操作寄存器的函数, 譬如 s3c2410_gpio_setpin
- 用户空间和内核空间. 两个空间的资源不能直接相互访问.
    - 驱动程序内经常要用 `copy_to_user` 以及 `copy_from_user`

## Q: Linux 调度机制
- 轮转调度算法(Round Robin), 先来先服务(FIFC)策略, have a time slice
- 优先级调度算法(Priority): preemptive(抢占式), static priority, dynamic priority
- Linux Sheduler:
    - pick next, staircase scheduler.
    - using dynamic priority, and time slice
    - rt_proirity(实时任务): SCHED_FIFO (just priority), SCHED_RR (time_slice)

## Q: linux android 启动流程
- hardware bootloader, can load specific flash address to ram and run automatically
- uboot stage1 (start.s): 底层硬件初始化(register), copy stage2 code to ram, init stack, data segment
- uboot stage2 (main.c): 硬件初始化(flash, ui, net), load kernel image, copy parameter to specific address for linux
- kernel: decompress image, read parameter from uboot, init hardware(register, MMU, paging table)
- load filesystem, init environment(`etc/inittab`, `etc/init.d/rcS`, `bin/sh`)
- load dymatical drivers, run user application
- Then for android:
    - zygote (由 Linux init 启动)
    - Dalvik VM
    - SyetemServers
    - Managers
    - Launcher

## Q: linux file system
- Linux下一切皆文件, 文件即inode.
- 索引过程为: 目录inode->目录名/文件名->对应inode->具体内容
- BusyBox 是linux下的一个应用程序, 集成了最常用的Linux命令和工具.
- 最小文件系统 `dev/console` `dev/null` init进程`bin/busybox` `etc/inittab` C库 `lib/` 系统程序或脚本 `/etc/init.d/rcS` `bin/sh`
- mdev: 动态加载驱动时, 自动生成节点文件 `/dev`
- file format yaffs2 for nand, jffs2 for nor

## Q: What do you understand about Linux Kernel and can you edit it?
Linux Kernel is the component that manages the hardware resources for the user and that provides essential services and interact with the user commands.
Linux Kernel is an open source software and free, and it is released under General Public License so we can edit it and it is legal.


## Q: What are the different types of Kernels? Explain
We can build kernels by many different types, but 3 of the types of kernels are most commonly used: monolithic, microkernel and hybrid.

- Microkernel: This type of kernel only manages CPU, memory, and IPC. This kind of kernel provides portability, small memory footprint and also security.

- Monolithic Kernel: Linux is a monolithic kernel. So, this type of kernel provides file management, system server calls, also manages CPU, IPC as well as device drivers. It provides easier access to the process to communicate and as there is not any queue for processor time, so processes react faster.

- Hybrid Kernel: In this type of kernels, programmers can select what they want to run in user mode and what in supervisor mode. So, this kernel provides more flexibility than any other kernel but it can have some latency problems.

## Q: Linux operating system components
- Kernel: Linux is a monolithic kernel
- System Library: GNU C Library. Library plays a vital role because application programs access Kernels feature using system library.
- System Utility: System Utility performs specific and individual level tasks.


## Q: Where is password file located in Linux and how can you improve the security of password file?
This is an important question that is generally asked by the interviewers.
User information along with the passwords in Linux is stored in `/etc/passwd` that is a compatible format. But this file is used to get the user information by several tools. Here, security is at risk. So, we have to make it secured.

To improve the security of the password file, instead of using a compatible format we can use **shadow password format**.

So, in shadow password format, the password will be stored as single “x” character which is not `/etc/passwd`. This information is stored in another file instead with a file name `/etc/shadow`. So, to enhance the security, the file is made word readable and also, this file is readable only by the root user. Thus security risks are overcome to a great extent by using the shadow password format.



## Q: Explain system calls used for process management?
There are some system calls used in Linux for process management.
These are as follows:

- `Fork()`: It is used to create a new process
- `Exec()`: It is used to execute a new process
- `Wait()`: It is used to make the process to wait
- `Exit()`: It is used to exit or terminate the process
- `Getpid()`: It is used to find the unique process ID
- `Getppid()`: It is used to check the parent process ID
- `Nice()`: It is used to bias the currently running process property


## Q:Guess the output
``` c
main() {
    fork();
    fork();
    fork();
    printf("hello world\n");
}
```
It will print “hello world' 8 times.
The main() will print one time and creates 3 children, let us say Child_1, Child_2, Child_3. All of them printed once.
The Child_3 will not create any child.
Child2 will create one child and that child will print once.
Child_1 will create two children, say Child_4 and Child_5 and each of them will print once.
Child_4 will again create another child and that child will print one time.
A total of eight times the printf statement will be executed.

## Q: What is the difference between static linking and dynamic linking ?
In static linking, all the library modules used in the program are placed in the final executable file making it larger in size. This is done by the linker. If the modules used in the program are modified after linking, then re-compilation is needed. The advantage of static linking is that the modules are present in an executable file. We don't want to worry about compatibility issues.

In case of dynamic linking, only the names of the module used are present in the executable file and the actual linking is done at run time when the program and the library modules both are present in the memory. That is why, the executables are smaller in size. Modification of the library modules used does not force re-compilation. But dynamic linking may face compatibility issues with the library modules used.

## Q: How a user mode is transferred to kernel mode? Difference between kernerl/user space
using System call
kernel mode: can do anything, cpu run in full function
user mode: safty purpose, cpu function is liminated.
kernel 访问用户层数据: `copy_to_user` `copy_from_user`


## Q: Main difference between Tasklets and workqs?
- Tasklets:
    - are old (around 2.3 I believe)
    - have a straightforward, simple API
    - are designed for low latency
    - cannot sleep
- Work queues:
    - are more recent (introduced in 2.5)
    - have a flexible API (more options/flags supported)
    - are designed for higher latency
    - can sleep


## Q: Do you know panic and oops errors in kernel crash?
Oops is a way to debug kernel code, and there are utilities for helping with that.
A kernel panic means the system cannot recover and must be restarted.
However, with an Oops, the system can usually continue. You can configure klogd and syslogd to log oops messages to files, rather than to std out.

## Q: What is the name and path of the main system log?
By default, the main system log is `/var/log/messages`.
This file contains all the messages and the script written by the user. By default, all scripts are saved in this file. This is the standard system log file, which contains messages from all system software, non-kernel boot issues, and messages that go to `dmesg`.
`dmesg` is a system file that is written upon system boot.
`dmesg | less` to review boot messages.

## Q: Explain what happens when an insmod is done an module
insmod is a user space utility to load a module into Linux kernel. It calls init_module system call to do the work.
init_module loads the kernel module in ELF format into kernel address space. Each section of the ELF are read and mapped using vmalloc().
Use of vmalloc is because kernel modules can be big and kernel might not have contiguous physical memory to accommodate for module text and data.

Each .ko has a struct module section. This has relocatable address of init and exit routines (ones specified in module_init and module_exit). This goes as a separate section in ELF. Once all the relevant sections are loaded in memory, kernel calls init routine of the module.

## Q: How will you insert a module statically in to linux kernel.
Using makefile `obj-y`. By the way `obj-m` will generate `.ko` file.
``` makefile
obj-y += mymodule.o
mymodule-objs := src.o other.o
```

## Q: what is a device driver and write a simple driver
``` c
#include <linux/xxx.h>
#include <asm/xxx.h>

#define DEVICE_NAME "drv_leds"                      // 设备类型名称, cat /proc/devices 可以看到

static int major;                                   // 存储自动分配的主设备号
static struct class *leds_class;                    // 类, 供mdev用, ls /sys/class/ 可以看到
static struct class_device  *leds_class_devs[4];    // 类下设备, ls /sys/class/class_name 可以看到

// ===== 驱动的硬件实现部分, 和单片机类似 =====

static int drv_leds_open(struct inode *inode, struct file *file)
{
    int minor = MINOR(inode->i_rdev);

    // 初始化对应的LED
    gpio_init(minor);
    printk("drv_leds_open\n");
    return 0;
}

static ssize_t drv_leds_write(struct file *file, const char __user *data, size_t len, loff_t *ppos)
{
    int minor = MINOR(file->f_dentry->d_inode->i_rdev);
    char val;
    copy_from_user(&val, data, 1);

    // 操作对应的LED
    gpio_set(minor);
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
    // gpio_base = ioremap(0x56000000, 0xD0);

    // 注册驱动, 0表示动态分配主设备号
    major = register_chrdev(0, DEVICE_NAME, &drv_leds_fops);

    // 生成系统设备信息, 供mdev自动创建设备节点使用
    leds_class = class_create(THIS_MODULE, "leds");             // 创建 leds 类
    if (IS_ERR(leds_class))
        return PTR_ERR(leds_class);

    // 0-3 表示4个独立的led, 名称为 led0, led1, led2, led3
    for (minor = 0; minor < 4; minor++) {
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

    // iounmap(gpio_base);
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



# IPC

## Q: How many types of IPC mechanism you know?
- Named pipes or FIFO
- Semaphores
- Shared memory
- Message queue
- Socket

## Q: Explain What Is Semaphore?
A semaphore is an abstract datatype or variable that is used for controlling access, by multiple processes to a common resource in a concurrent system such as multiprogramming operating system.

Semaphores are commonly used for two purposes:
- To share a common memory space
- To share access to files

Semaphores are of two types:
- Binary semaphore: It can have only two values (0 and 1). The semaphore value is set to 1 by the process in charge, when the resource is available.
- Counting semaphore: It can have value greater than one. It is used to control access to a pool of resources.

## Q: What is difference between binary semaphore and mutex?
- Mutual exclusion and synchronization can be used by binary semaphore while mutex is used only for mutual exclusion.
- A mutex can be released by the same thread which acquired it. Semaphore values can be changed by other thread also.
- From an ISR, a mutex can not be used.
- The advantage of semaphores is that, they can be used to synchronize two unrelated processes trying to access the same resource.
- Semaphores can act as mutex, but the opposite is not possible.

## Q: What is spin lock?
If a resource is locked, a thread that wants to access that resource may repetitively check whether the resource is available. During that time, the thread may loop and check the resource without doing any useful work. Suck a lock is termed as spin lock.

## Q: Explain Whether We Can Use Semaphore Or Mutex Or Spinlock In Interrupt Context In Linux Kernel?
Mutex cannot be used for interrupt context in Linux Kernel.
Semaphore only can use `sema_post` in interrupt handler.
Spinlocks can be used for locking in interrupt context.

## Q: What is shared memory?
Shared memory is the fastest interprocess communication mechanism. The operating system maps a memory segment in the address space of several processes, so that several processes can read and write in that memory segment without calling operating system functions. However, we need some kind of synchronization between processes that read and write shared memory.


## Q: How to come out of deadlock?
The most common error causing deadlock is self deadlock or recursive deadlock:
- a thread tries to acquire a lock it is already holding.
- Recursive deadlock is very easy to program by mistake.

Here are some simple guidelines for locking.
- Try not to hold locks across long operations like I/O where performance can be adversely affected.
- Don't hold locks when calling a function that is outside the module and that might reenter the module.
- In general, start with a coarse-grained approach, identify bottlenecks, and add finer-grained locking where necessary to alleviate the bottlenecks. Most locks are held for short amounts of time and contention is rare, so fix only those locks that have measured contention.
- When using multiple locks, avoid deadlocks by making sure that all threads acquire the locks in the same order.

## Q: 生产者, 消费者写法
``` c
struct goods
{
    int id;
    struct goods *next;
};
pthread_mutex_t m;
pthread_cond_t has_product;
struct goods *head;

void *producer(void *argv)
{
    struct goods *p = NULL;
    while (1)
    {
        pthread_mutex_lock(&m);
        p = malloc(sizeof(struct goods));
        p->id = rand() % 100;
        p->next = head;
        head = p;
        printf("produce %d\n", p->id);
        pthread_mutex_unlock(&m);
        pthread_cond_signal(&has_product);
        //printf("produce %d\n", p->id);
        sleep(rand() % 2);
    }
    return (void *)0;
}

void *comsumer(void *argv)
{
    struct goods *p = NULL;
    while (1)
    {
        pthread_mutex_lock(&m);
        //思考：pthread_cond_wait()的作用？
        while (NULL == head)
            pthread_cond_wait(&has_product, &m);
        p = head;
        head = head->next;
        printf("comsume %d\n", p->id);
        pthread_mutex_unlock(&m);
        //printf("comsume %d\n", p->id);
        free(p);
        sleep(rand() % 2);
    }
    return (void *)0;
}

// 开启两个线程作为生产者，三个线程作为消费者
int main(void)
{
    int i;
    //初始化条件变量和互斥量
    pthread_mutex_init(&m, NULL);
    pthread_cond_init(&has_product, NULL);
    head = NULL;
    pthread_t pro[2], com[3];
    for (i = 0; i < 2; i++)
        pthread_create(&pro[i], NULL, producer, NULL);
    for (i = 0; i < 3; i++)
        pthread_create(&com[i], NULL, comsumer, NULL);
    for (i = 0; i < 2; i++)
        pthread_join(pro[i], NULL);
    for (i = 0; i < 3; i++)
        pthread_join(com[i], NULL);
    //销毁条件变量和互斥量
    pthread_mutex_destroy(&m);
    pthread_cond_destroy(&has_product);
    return 0;
}
```



# bash command

## Q: How can I redirect both stderr and stdin at once?
command `> file.log 2>&1` : Redirect stderr to "where stdout is currently going". In this case, that is a file opened in append mode. In other words, the `&1` reuses the file descriptor which stdout currently uses.

## Q: what is `/proc` entry and how it is useful
Virtual directory for system information, 虚拟档案系统. 数据都在内存当中,不占用硬盘空间.
主要包括系统核心,接口设备状态,网络状态.
比较重要的档案例: `proc/cpuinfo`  `/proc/interrupts`  `/proc/ioports`


## How can we edit a file without opening in Linux?
`sed` command is used to edit a file without opening.
`sed` command is used to modify or change the contents of a file.

``` bash
# For example, we have a text file with below content
> cat file.txt

# replace “sed” with “vi”
>sed ‘s/sed/vi/’ file.txt
```

## Q: How can you find out how much memory Linux is using?
`cat /proc/meminfo`

## Q: Explain grep command and its use.
`grep` command in Linux is used to search a specific pattern. Grep command will help you to explore the string in a file or multiple files.

``` bash
grep ‘word’ filename
grep ‘word’ file1 file2 file3
command | grep ‘string’

# For example,

grep “smith” passwd
grep “smith” passwd shadow
netstat -an | grep 8083
cat /etc/passwd | grep smith
```

## Q: Explain file content commands along with the description.
- `head`: to check the starting of a file.
- `tail`: to check the ending of the file. It is the reverse of head command.
- `cat`: used to view, create, concatenate the files.
- `more`: used to display the text in the terminal window in pager form.
- `less`: used to view the text in the backward direction and also provides single line movement.



# 参考
- [Linux Embedded systems Interview Questions & Answers](https://www.wisdomjobs.com/e-university/linux-embedded-systems-interview-questions.html)
- [Linux Device Driver,Embedded C Interview Questions](http://linuxdevicedrivercinterviewqs.blogspot.com.au/)

