---
title: uboot之源码分析
date: 2017-08-25
categories: embedded linlux
tags: [embedded linux, uboot]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [jz2440分区及启动的基础概念](https://draapho.github.io/2017/11/24/1735-jz2440-basic/)
- [uboot之makefile分析](https://draapho.github.io/2017/07/07/1719-uboot-makefile/)
- [uboot之源码分析](https://draapho.github.io/2017/08/25/1720-uboot-source/)
- [uboot之定制指令](https://draapho.github.io/2017/08/30/1721-uboot-modify/)

本文基于 u-boot-1.1.6, 使用jz2440开发板. 若要使用最新的u-boot版本见: [u-boot官网](http://www.denx.de/wiki/U-Boot/WebHome)  [u-boot下载](ftp://ftp.denx.de/pub/u-boot/)

# u-boot功能:
- 本质是单片机程序
- 硬件相关初始化
  - 关看门狗
  - 初始化时钟
  - 初始化SDRAM
  - 从Flash读取内核
- 最终目的: 启动内核
- 为开发方便, 还支持:
  - 烧写flash
  - 网卡
  - USB
  - 串口

![uboot-start](https://draapho.github.io/images/1720/uboot-start.png)
  
  
# 查看内存地址分配
可以使用指令 `readelf -s u-boot | grep _start` 查看uboot的内存地址分配
```
$ readelf -s u-boot|grep _start
    63: 33f80118     0 NOTYPE  LOCAL  DEFAULT    1 _start_armboot
   218: 33fb0798     4 OBJECT  LOCAL  DEFAULT   10 mem_malloc_start
   906: 33fb5a0c     4 OBJECT  LOCAL  DEFAULT   10 bin_start_address
  1303: 33f9f274    88 FUNC    LOCAL  DEFAULT    1 setup_start_tag
  1507: 33f80000     0 NOTYPE  GLOBAL DEFAULT    1 _start   // 等同于 config.mk 中的 TEXT_BASE值
  1657: 33f80044     0 NOTYPE  GLOBAL DEFAULT    1 _armboot_start
  1776: 33f80048     0 NOTYPE  GLOBAL DEFAULT    1 _bss_start
  1869: 33fb06ac     0 NOTYPE  GLOBAL DEFAULT  ABS __bss_start
  2038: 33fb016c     0 NOTYPE  GLOBAL DEFAULT  ABS __u_boot_cmd_start
```

![uboot-ram](https://draapho.github.io/images/1720/uboot-ram.gif)

# 一 汇编初始化, start.s

由链接脚本 `./board/100ask24x0/u-boot.lds` 可知, 
uboot启动后, 首先执行的就是 `cpu/arm920t/start.s`

``` asm
41 .globl _start                        // 程序入口
42 _start:	b       reset               // 跳转到reset执行

75 _TEXT_BASE:                          // _TEXT_BASE值, 可知等同于 _start
76	    .word	TEXT_BASE               // 赋值
79 _armboot_start:                      // _armboot_start 值等同于 TEXT_BASE
80	    .word _start                    // 赋值 _start 给 _armboot_start

122 reset:                      
124 /* set the cpu to SVC32 mode */     // 1. 将CPU设置为SVC32管理模式
131 /* turn off the watchdog */         // 2. 关闭看门狗
150 /* mask all IRQs ... - default */   // 3. 关中断

                                        // 4. 初始化SDRAM
174 #ifndef CONFIG_SKIP_LOWLEVEL_INIT     // 一个宏定义开关
175 	adr	r0, _start                    // 读取当前地址, 如果是从nand flash启动, 这段代码被自动拷贝到片内4K RAM, 初始地址为0
                                          // 反之, 如果代码是直接复制到SDRAM中并运行(如调试器), 则_start和_TEXT_BASE值相等
176 	ldr	r1, _TEXT_BASE                // TEXT_BASE 由 "./board/100ask24x0/config.mk" 赋值为 0x33F80000
                                          // 可在linux用指令 "grep -nr TEXT_BASE *" 搜索
177 	cmp     r0, r1                    // 比较两个值. 不等的话, 说明片外SDRAM还没有被初始化过
178 	blne	cpu_init_crit             // 初始化片外SDRAM的控制 (关MMU, 初始化存储控制器)
179 #endif

182 stack_setup:                        // 5. 设置栈指针, 栈指针向下递减, 推指针向上递增.
183 	ldr	r0, _TEXT_BASE		          // 从 _TEXT_BASE 开始分配空间. _TEXT_BASE	上面是uboot代码段
184 	sub	r0, r0, #CFG_MALLOC_LEN	      // uboot 自己用的 malloc 堆空间
185 	sub	r0, r0, #CFG_GBL_DATA_SIZE    // 全局变量, 保存uboot系统参数的预留空间
187 #ifdef CONFIG_USE_IRQ
188 	sub	r0, r0, #(CONFIG_STACKSIZE_IRQ+CONFIG_STACKSIZE_FIQ)    // IRQ 以及 FIQ, 中断模式的栈
189 #endif
190 	sub	sp, r0, #12		            // 再减去12字节后, 就是sp栈指针的起始位置

193 bl clock_init                       // 6. 初始化系统时钟, 设置为400MHz

197 relocate:                           // 7. 拷贝代码. 把uboot代码从nand/nor flash拷贝到片外 SDRAM 中

219 clear_bss:                          // 8. 清bss. 将未初始化过的全局变量设为0. Block Started by Symbol     

261 _start_armboot:	.word start_armboot // 9. 调用 start_armboot, c语言函数.
```

# 二 板级初始化, board.c

`grep -nwr start_armboot *`, 找出 `start_armboot` 源码文件和行号.
可知, 其位于 `./lib_arm/board.c` 的236行.

``` c
216 init_fnc_t *init_sequence[] = {...};    // 初始化函数组

236 void start_armboot (void) {
248     gd = (gd_t*)(_armboot_start - CFG_MALLOC_LEN - sizeof(gd_t));
        // 实际指向的就是 CFG_GBL_DATA_SIZE 段, 下面是清零, 对应的结构体是 gd_t

258     for (init_fnc_ptr = init_sequence; *init_fnc_ptr; ++init_fnc_ptr) {}
        // 依次调用初始化函数, 如果返回值为0, 则初始化失败, 系统出错!
        // 在init的过程中, 相关的函数对 gd_t 内容赋值.

266     size = flash_init ();               // 初始化nor flash
267     display_flash_config (size);

297     mem_malloc_init (_armboot_start - CFG_MALLOC_LEN);  // 堆地址的初始化

301     nand_init();	                    // 初始化 nand flash

310     env_relocate ();                    // 加载uboot的环境变量

...     // 网卡, devices_init, 显示终端, 控制台, 其它驱动等等 初始化, 略过不表

403     main_loop ();                       // 初始化结束, 跳转到 main.c 文件的 void main_loop(void)
407 }
```

# 三 识别终端指令, main.c
`grep -nr "main_loop (void)" *`, 可找到 `./common/main.c` 的301行 main_loop
整个文件的最核心指令就是 run_command(), 即识别和运行指令函数.

``` c
301 void main_loop (void) {

404     s = getenv ("bootdelay");           // 获取 bootdelay 环境变量
405     bootdelay = s ? (int)simple_strtol(s, NULL, 10) : CONFIG_BOOTDELAY;

432     s = getenv ("bootcmd");             // 加载 bootcmd 环境变量, 此变量为linux加载和启动指令
436     if (bootdelay >= 0 && s && !abortboot (bootdelay)) {    // 倒计时结束, 自动加载linux
443         printf("Booting Linux ...\n");  // 终端打印信息
444         run_command (s, 0);             // 运行 bootcmd 的指令.
454     }

        // abortboot 函数内会判断倒计时, 并获取按键操作, 只有 ' ' 空格才能跳出启动
        // 457-467行不会运行, 因为没有宏定义 CONFIG_MENUKEY
478     run_command("menu", 0);             // 执行 "menu" 指令, 打印jz2440定制的菜单信息

488     for (;;) {                          // 死循环, 等待终端输入指令
497         len = readline (CFG_PROMPT);    // 读取终端输入, 提示符为 "OpenJTAG> "
521         rc = run_command (lastcommand, flag);   // 执行输入的指令
527     }
529 } 

        // 指令数据结构被放在 __u_boot_cmd 段内, 对应的指令函数可以在 ./common/cmd_***.c 内找到
1280    int run_command (const char *cmd, int flag) {
1361        if ((cmdtp = find_cmd(argv[0])) == NULL) {...}      // 查找指令是否存在
1391        if ((cmdtp->cmd) (cmdtp, flag, argc, argv) != 0) {} // 调用指令函数
1403    }         
```

# 四 加载和启动linux

## bootcmd 指令分析

在uboot命令行下, 输入 `printenv` 可以查看uboot的环境变量
可以找到如下信息
```
bootcmd=nand read.jffs2 0x30007FC0 kernel; bootm 0x30007FC0
    // 启动指令分为了两条:
    // 1. nand read.jffs2 0x30007FC0 kernel
        // 从 nand flash 的 kernel 分区读取数据, 放到地址 0x30007FC0 处(SDRAM)
    // 2. bootm 0x30007FC0
        // 从 0x30007FC0 启动linux

bootdelay=2
    // 启动延时参数为2S
    // 因此uboot的环境变量可以是参数设置, 也可以是命令行, 命令行的本质是字符串
```

## flash 分区信息

可以通过 "./include/configs/100ask24x0.h" 中的 MTDPARTS_DEFAULT 来分析获得flash分区情况
``` c
#define MTDPARTS_DEFAULT "mtdparts=nandflash0:256k@0(bootloader)," \
                            "128k(params)," \
                            "2m(kernel)," \
                            "-(root)"
// nandflash0: 分区位于 nandflash 上
// 256k@0(bootloader), 第一个分区从0地址开始, 占用256k, 分区名称 bootloader
// 128k(params), 第二个分区紧邻第一个分区, 占用128K, 分区名称 params
// 2m(kernel), 第三个分区紧邻第二个分区, 占用2m字节, 分区名称 kernel
// -(root), 剩余的空间全部分配给第四个分区, 名称为 root
```

也可以在uboot下, 使用 "mtdparts" 可以查看 flash 的分区情况
``` bash
OpenJTAG> mtdparts
 #: name                size            offset          mask_flags
 0: bootloader          0x00040000      0x00000000      0
 1: params              0x00020000      0x00040000      0
 2: kernel              0x00200000      0x00060000      0
 3: root                0x0fda0000      0x00260000      0
```

## 加载linux内核

执行 `nand read.jffs2 0x30007FC0 kernel` 指令, 源码在 `./common/cmd_nand.c` 的 do_nand 函数
- jffs2 是读取的格式, 但此处并非是指 kernel 是jffs2格式. jffs2方式无需块对齐和页对齐, 提高通用性.
- 可知 kernel 分区大小为 0x200000 (2M), 起始地址为 0x60000
- 所以整条指令等价于: nand read.jffs2 0x30007FC0(目标地址) 0x60000(源地址) 0x200000(字节大小)

``` c
    // nand     read.jffs2  0x30007FC0  kernel 
    // argv[0]  argv[1]     argv[2]     argv[3]

166 int do_nand(cmd_tbl_t * cmdtp, int flag, int argc, char *argv[]) {
316     if (strncmp(cmd, "read", 4) == 0 || strncmp(cmd, "write", 5) == 0) {
322         addr = (ulong)simple_strtoul(argv[2], NULL, 16);                    // 目标地址 addr = 0x30007FC0
326         if (arg_off_size(argc - 3, argv + 3, nand, &off, &size) != 0) {...} // 获取源地址以及长度
            // arg_off_size 中, 如果发现导入的参数是分区名字, 就会调用 find_dev_and_part() 来获取改分区的地址和长度
            // 最终会将源地址以及长度放入 &off, &size 中
336         opts.buffer = (u_char*) addr;                                       // sdram, 直接就是一片buffer
337         opts.length = size;
338         opts.offset = off;
340         ret = nand_read_opts(nand, &opts);                                  // 读取nand到buffer中
416     printf(" %d bytes %s: %s\n", size, read ? "read" : "written", ret ? "ERROR" : "OK"); // 打印进度
419     return ret == 0 ? 0 : 1;                        返回读取结果
511 }
```

## 启动linux内核

执行 `bootm 0x30007FC0` 指令, 源码在 `./common/cmd_bootm.c` 的 do_bootm 函数
- 设置 0x30007FC0 这个奇怪的值, 是有原因的. 简而言之, 是为了避免拷贝内核两次, 加快启动速度
- kernel 最后编译时的指令是 `make uImage`, 因此其格式是 uImage
- 相比于纯压缩文件 zImage 的内核文件, uImage 在 zImage之前加上了长度为 0x40 的头部信息 (image_header_t)
- 0x30007FC0 + 0x40 = 0x30008000, 正好就是 uImage 头部信息要求的加载地址.
- 而 0x30008000 这个地址, 是有linux源码在 `Makefile` 里写死的. 可搜索关键字 `zreladdr-y` 和 `ZRELADDR`
``` c

149 image_header_t header;              // uImage的头部信息, 占用0x40字节
        // ih_load, Data Load Address,   加载地址, 如果发现加载地址不对, do_bootm会重新移动内核文件到此地址
        // ih_ep,   Entry Point Address, 入口地址, 跳转到此地址开始执行linux内核

    // bootm    0x30007FC0
    // argv[0]  argv[1]
153 int do_bootm (cmd_tbl_t *cmdtp, int flag, int argc, char *argv[]) {
163     image_header_t *hdr = &header;                              // 指针 hdr 指向头部信息
171     addr = simple_strtoul(argv[1], NULL, 16);                   // 获取地址, 0x30007FC0
183     memmove (&header, (char *)addr, sizeof(image_header_t));    // 读取头部信息
229     data = addr + sizeof(image_header_t);                       // data为linux内核起始地址
321     if(ntohl(hdr->ih_load) == data) {
322         printf ("   XIP %s ... ", name);                        // 一致, 不用移动了
323     } else {
340         memmove ((void *) ntohl(hdr->ih_load), (uchar *)data, len);     // 否则, 把内核移动到加载地址
342     }
418     do_bootm_linux  (cmdtp, flag, argc, argv, addr, len_ptr, verify);   // 启动linux
477 }
```

`do_bootm_linux` 函数位于 `./lib_arm/armlinux.c`, 
**注意**, cmd_bootm.c文件内的那个do_bootm_linux不会被调用, 因为没有宏定义 CONFIG_PPC

``` c
79  void do_bootm_linux (...) {
    // 此函数主要做两件事情:
    // 1. uboot 需要告诉内核一些系统参数 (内存大小, 终端波特率等等)
    // 2. 跳转到入口地址, 启动内核
85    	void (*theKernel)(int zero, int arch, uint params);         // linux启动函数
86      image_header_t *hdr = &header;                              // uImage 头部信息
87      bd_t *bd = gd->bd;                                          // 处于 CFG_GBL_DATA_SIZE 段内
90      char *commandline = getenv ("bootargs");                    // 获取 bootargs 参数
        
93      theKernel = (void (*)(int, int, uint))ntohl(hdr->ih_ep);    // ih_ep, 即linux入口地址

235     setup_start_tag (bd);                                       // 一系列的TAG参数设置, 准备传递给linux
        // 对jz2440, TAG地址是 0x30000100. 
        // 在 "./board/100ask24x0/100ask24x0.c" 中, gd->bd->bi_boot_params = 0x30000100;
237	    setup_serial_tag (&params);
240	    setup_revision_tag (&params);
243	    setup_memory_tags (bd);
246	    setup_commandline_tag (bd, commandline);                    // 告知linux文件系统的位置
250	    setup_initrd_tag (bd, initrd_start, initrd_end);
253	    setup_videolfb_tag ((gd_t *) gd);
255	    setup_end_tag (bd);                                         // 参数设置结束

259     printf ("\nStarting kernel ...\n\n");
270     theKernel (0, bd->bi_arch_number, bd->bi_boot_params);      // 调用入口地址, 传入参数, 启动linux
271 }
```

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***