---
title: kernel之内核启动分析
date: 2017-09-15
categories: embedded linux
tags: [embedded linux, kernel]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [kernel之编译体验](https://draapho.github.io/2017/09/01/1722-kernel-compile/)
- [kernel之Makefile分析](https://draapho.github.io/2017/09/14/1724-kernel-makefile/)
- [kernel之内核启动分析](https://draapho.github.io/2017/09/15/1725-kernel-launch/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.

# 内核引导阶段 `head.S`
由 [uboot之源码分析](https://draapho.github.io/2017/08/25/1720-uboot-source/) 可知, uboot最后调用的函数是
- `theKernel (0, bd->bi_arch_number, bd->bi_boot_params)`, 会把一些板级参数传递给linux内核使用.

由 [kernel之Makefile分析](https://draapho.github.io/2017/09/14/1724-kernel-makefile/) 可知, 两个重要的文件如下:
- 第1个文件: `arch/arm/kernel/head.S`
- 链接脚本: `arch/arm/kernel/vmlinux.lds`

`head.S` 主要完成了如下工作.

![内核引导阶段](https://draapho.github.io/images/1725/stage1.JPG)

- `__lookup_machine_type` 会将 theKernel 传入的单板类型与内核支持的单板类型逐一比较.
- `.arch.info.init` 这一个段存放的就是内核支持的单板类型.
    - 定义在 `./arch/arm/kernel/vmlinux.lds`
    - `__lookup_machine_type` 会对该段进行轮询
    - 该段的数据结构为 `machine_desc`, 定义在 `./include/asm-arm/mach/arch.h`
    - `arch.h` 文件还宏定义了 `MACHINE_START` `MACHINE_END`,
        调用该宏定义, 就会将相关数据放在 `.arch.info.init` 段内
- `./arch/arm/mach-s3c2440/mach-smdk2440.c:` 内调用了 `MACHINE_START(S3C2440, "SMDK2440")`
    - kernel下 `grep -nr MACH_TYPE_S3C2440` 可知 MACH_TYPE_S3C2440 的值为 362
    - uboot下 `grep -nr bi_arch_number` 可知其值为 MACH_TYPE_S3C2440, 即 362
    - 这样, kernel就能确定是支持当前的开发板的. (当前的开发板信息由uboot提供给kernel)

# 内核启动第二阶段 `init/main.c`

`head-common.S` 调用 `start_kernel` 后, 代码会转到 `init/main.c`, 使用的是C语言.

![内核启动第二阶段](https://draapho.github.io/images/1725/stage2.JPG)


从 `start_kernel` 开始, 函数的基本调用关系如下:
- `setup_arch(&command_line);` 读取uboot传过来的TAG参数
    - 位于 `./arch/arm/kernel/setup.c` 770 行
    - uboot 的 `setup_memory_tags` 存放内存大小
    - uboot 的 `setup_commandline_tag` 告知linux挂载文件系统的命令行
    - uboot 的 `/board/100ask24x0/100ask24x0.c` 中, `gd->bd->bi_boot_params = 0x30000100`
    - 使用了 `machine_desc` 结构体, `.boot_params = S3C2410_SDRAM_PA + 0x100`, 其值就是 `0x30000100`
    - 至此, uboot存放在内存中的TAG参数, 就能被内核读取出来了.
    - 此函数还会把挂载文件系统的命令赋值给 `boot_command_line`, 后续会去处理.
    - `parse_cmdline` 会去处理放在 `early_param.init` 段的指令.
- `parse_early_param`, 此函数会把 `boot_command_line`传递给`do_early_param`让其执行挂载文件系统的指令.
    - `do_early_param`
        - 搜索 `.init.setup` 段, 调用有early标记的函数 (大多只是设置一下参数)
- `unknown_bootoption` (使用 parse_args 先检查参数后再执行该函数)
    - `obsolete_checksetup`
        - 搜索 `.init.setup` 段, 调用非early标记的函数 (大多只是设置一下参数)
- `rest_init`, 去做剩余的初始化工作
    - `kernel_thread(kernel_init, NULL, CLONE_FS | CLONE_SIGHAND);` 首先就是创建一个线程来做初始化工作
        - `kernel_init` 会调用 `prepare_namespace`
            - 在 `do_mounts.c` 文件下 `prepare_namespace` 调用 `mount_root`
            - 目的就是挂载文件系统.
        - 挂载完文件系统后, 调用 `init_post`, 尝试执行第一个应用程序(下述应用程序不会再返回)
            - `run_init_process(execute_command);`
            - `run_init_process("/sbin/init");`
            - `run_init_process("/etc/init");`
            - `run_init_process("/bin/init");`
            - `run_init_process("/bin/sh");`
- 以默认的启动指令为例 `"root=/dev/hda1 ro init=/bin/bash console=ttySAC0"`
            - `__setup("root=", root_dev_setup);` 位于 `./init/do_mounts.c`
            - `__setup("init=", init_setup);` 位于 `./init/main.c`
            - `__setup("console=", console_setup);` 位于 `./kernel/printk.c`
            - 以上命令对应的函数都会由 `obsolete_checksetup` 函数来调用. 主要是设置好相关参数.

``` c
// ./init/main.c

497 asmlinkage void __init start_kernel(void) {
520     tick_init();
521     boot_cpu_init();
522     page_address_init();
524     printk(linux_banner);                           // 打印linux版本信息
525     setup_arch(&command_line);                      // 读取uboot传过来的TAG参数
                                                        // 搜索 "early_param.init" 段, 并调用相关函数
526     setup_command_line(command_line);               // 复制一下 command_line.

544     printk(KERN_NOTICE "Kernel command line: %s\n", boot_command_line); // 打印文件系统挂载命令
545     parse_early_param();                            // 最终会搜索 ".init.setup" 段, 调用有early标记的函数
546     parse_args("Booting kernel", static_command_line, __start___param,
547        __stop___param - __start___param,            // 搜索 "__param" 段
548        &unknown_bootoption);                        // 最终会搜索 ".init.setup" 段, 调用非early标记的函数

575     console_init();                                 // 控制终端初始化

636     rest_init();                                    // 剩余部分的初始化
637 }

466 void __init parse_early_param(void) {
475     strlcpy(tmp_cmdline, boot_command_line, COMMAND_LINE_SIZE);
        // parse_args 会先检查参数, 最后调用函数, 此处是do_early_param,
        // 参数为 boot_command_line 启动命令, 由uboot传递进来. 实际不会在此处执行.
476     parse_args("early options", tmp_cmdline, NULL, 0, do_early_param);
478 }

450 static int __init do_early_param(char *param, char *val) {
454     for (p = __setup_start; p < __setup_end; p++)   // 遍历 ".init.setup" 段
455         if (p->early && strcmp(param, p->str) == 0) // 在段内找了匹配boot_command_line的命令, 则执行
456             if (p->setup_func(val) != 0)
463 }

258 static int __init unknown_bootoption(char *param, char *val) {
274     if (obsolete_checksetup(param))                 // 调用 obsolete_checksetup
313 }

190 static int __init obsolete_checksetup(char *line) {
195     p = __setup_start;                              // 遍历 ".init.setup" 段
196     do {
199         if (p->early) {                             // 有early标记, 跳过.
210         } else if (p->setup_func(line + n))         // 执行指令对应的函数
214     } while (p < __setup_end);24
217 }

426 static void noinline __init_refok rest_init(void) {
        kernel_thread(kernel_init, NULL, CLONE_FS | CLONE_SIGHAND); // 创建一个初始化用的线程
        schedule();                                     // 调度
447 }

787 static int __init kernel_init(void * unused) {
828         prepare_namespace();                        // 调用 mount_root, 加载文件系统
836     init_post();                                    // 执行应用程序
838 }

748 static int noinline init_post(void) {               // 执行应用程序
756     if (sys_open((const char __user *) "/dev/console", O_RDWR, 0) < 0)      
                                                        // 尝试打开终端设备, 文件0->printf
757         printk(KERN_WARNING "Warning: unable to open an initial console.\n");
759	    (void) sys_dup(0);                              // 赋值文件0, 生成文件1->scanf
760	    (void) sys_dup(0);                              // 赋值文件0, 生成文件2->err
        // 以上四句作用为设置标准输入输出流, (printf, scanf, err)
        
744 	if (execute_command) {
745	    	run_init_process(execute_command);
746		    printk(KERN_WARNING "Failed to execute %s.  Attempting "
747					"defaults...\n", execute_command);
748  	}
        // 传入的启动参数内有 "init=" 启动程序, 则执行! 执行成功的话不会再返回这里!

779     run_init_process("/sbin/init");
780     run_init_process("/etc/init");
781     run_init_process("/bin/init");
782     run_init_process("/bin/sh");
        // 没有配置过启动指令, 依次尝试上述四个默认程序. 某一个执行成功后就不会再返回!
        
784     panic("No init found.  Try passing init= option to kernel.");
        // 执行首个应用程序失败, 打印内核错误信息!
785 }
```

``` bash
# 我们擦除开发板文件系统后, 来看一下打印出来的启动信息

OpenJTAG> nand erase root           # uboot 下, 擦除root块
OpenJTAG> reset                     # uboot 下, 重启系统

Booting Linux ...
NAND read: device 0 offset 0x60000, size 0x200000
## Booting image at 30007fc0 ...
...
Starting kernel ...
...
Kernel command line: noinitrd root=/dev/mtdblock3 init=/linuxrc console=ttySAC0
loop: module loaded
...
Creating 4 MTD partitions on "NAND 256MiB 3,3V 8-bit":
0x00000000-0x00040000 : "bootloader"
0x00040000-0x00060000 : "params"
0x00060000-0x00260000 : "kernel"
0x00260000-0x10000000 : "root"
...
VFS: Mounted root (yaffs filesystem).
...
Kernel panic - not syncing: No init found.  Try passing init= option to kernel.
# 此句就是由./init/main.c文件784行打印出来的. 因为没有文件系统, 第一个应用程序执行失败!
```

如果正常启动, 会打印如下信息, 可知第一个应用程序名字是 `BusyBox`, 然后启动了 `/bin/sh`!!!
`init started: BusyBox v1.7.0 (2008-01-22 10:04:09 EST)`
`starting pid 764, tty '': '/etc/init.d/rcS'`
`Please press Enter to activate this console.`
`starting pid 770, tty '/dev/s3c2410_serial0': '/bin/sh'`


# 初始化中用到的段 `vmlinux.lds`

## `.init.setup` 段分析

在 `./arch/arm/kernel/vmlinux.lds` 中有这么一个段
`*(.init.setup)`, 其头尾为 `__setup_start` `__setup_end`

这一个段存放着需要通过读取命令行来执行的初始化工作, 内核称之为 `unknow_xxx`
定义在此段的变量通过两个宏定义实现 `__setup` 以及 `early_param`
简单理解的话, `early_param` 是需要先执行的命令行, `__setup` 则稍后执行.

``` c
# ./include/linux/init.h

148 struct obs_kernel_param {
149     const char *str;
150     int (*setup_func)(char *);
151     int early;
152 };

160 #define __setup_param(str, unique_id, fn, early)            \
161     static char __setup_str_##unique_id[] __initdata = str; \
162     static struct obs_kernel_param __setup_##unique_id  \
163         __attribute_used__              \
164         __attribute__((__section__(".init.setup"))) \
165         __attribute__((aligned((sizeof(long)))))    \
166         = { __setup_str_##unique_id, fn, early }

171 #define __setup(str, fn)                    \
172     __setup_param(str, fn, fn, 0)

179 #define early_param(str, fn)                    \
180     __setup_param(str, fn, fn, 1)
```

先来分析 `__setup(str, fn)` 这么一个宏定义, 它设置的就是命令行队列, 将字符串关联到函数.
- `unique_id` 就是fn的函数地址
- 存放在 `.init.setup` 段内.
- 与数据结构 `obs_kernel_param` 相关. 保存的就是 str, fn, 以及early三个变量.
- 通过这样一种结构, 可以很方便的使用字符串来调用指定的函数.
- `grep -nwr __setup ./arch/arm` 可找到 `__setup("tft=", qt2410_tft_setup);`, 很明显就是用来初始化屏幕的.
- 在 `./init/do_mounts.c`里, 还能找到 `__setup("root=", root_dev_setup)`, 是用来挂载文件系统的.

然后看 `early_param(str, fn)` 宏定义.
- `__setup` 是一样的.
- 只是将标记 `early` 赋值为1. 表示需要较早执行的初始化工作, 一般为更底层的驱动
- arm 架构几乎没有用到 `early_param` 的地方, 搜索的话, 可以看到 pci 的初始化就用到了 `early_param`

## `early_param.init` 段

和 `.init.setup` 段类似, 其定义在
`./include/asm-arm/setup.h`, 220行.
关联的宏定义为 `__early_param`, 初始化如 `initrd=` `mem=` 之类的命令
`grep -nwr __early_param` 进行查询, 结果不多的.
搜索 `grep -nwr __early_begin`, 可知, 其处理函数为 `parse_cmdline`

## `__param` 段
该段主要用于给驱动模块的初始化. 设置参数使用.
定义在 `./include/linux/moduleparam.h`, 72 行
其调用位于 `./init/main.c` 的 `parse_args` (`grep -nwr __start___param`)
关联的宏定义为 `module_param_call` `module_param_named` `module_param` 以及 `module_param_string`
查阅后, 可以发现全部是和驱动模块有关的.

# linux下的分区
jz2440的启动参数为 `root= /dev/mtdblock3`,
linux下没有分区表的概念, 这里分区是在内核源码里写死的.
可见 `./arch/arm/plat-s3c24xx/common-smdk.c` 的118行, `smdk_default_nand_part`
它分配了4个的分区:

|分区 | 对应mtdblock | size                        |
|--------|----------|--------                     |
| `bootloader`|  mtdblock0 |    0x00040000        |
| `params`    | mtdblock1  |   0x00020000         |
| `kernel`    | mtdblock2  | 0x00200000           |
| `root`      | mtdblock3  | MTDPART_SIZ_FULL     |



# 更多参考
- [ linux kernel的cmdline参数解析原理分析](http://blog.csdn.net/skyflying2012/article/details/41142801)
- [深入淺出 start_kernel](https://danielmaker.github.io/blog/linux/inside_start_kernel.html)
- [嵌入式Linux中基于MTD的文件系统的结构框架图](http://blog.sina.com.cn/s/blog_5d9051c00100ij93.html)
- [u-boot中分区和内核MTD分区关系](http://blog.csdn.net/yusiguyuan/article/details/9471577)

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***