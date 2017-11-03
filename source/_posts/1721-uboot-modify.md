---
title: uboot之定制指令
date: 2017-08-30
categories: embedded linlux
tags: [embedded linux, uboot]
---

# 总览
- [嵌入式linux环境搭建](https://draapho.github.io/2017/02/16/1705-linux-env/)
- [嵌入式linux环境搭建-jz2440开发板](https://draapho.github.io/2017/02/21/1707-jz2440-env/)
- [uboot之makefile分析](https://draapho.github.io/2017/07/07/1719-uboot-makefile/)
- [uboot之源码分析](https://draapho.github.io/2017/08/25/1720-uboot-source/)
- [uboot之定制指令](https://draapho.github.io/2017/08/30/1721-uboot-modify/)
- [kernel之编译体验](https://draapho.github.io/2017/09/01/1722-kernel-compile/)
- [kernel之Makefile分析](https://draapho.github.io/2017/09/14/1724-kernel-makefile/)
- [kernel之内核启动分析](https://draapho.github.io/2017/09/15/1725-kernel-launch/)
- [fs之Busybox的编译与使用](https://draapho.github.io/2017/11/02/1730-fs-busybox/)
- [fs之创建文件系统](https://draapho.github.io/2017/11/03/1731-fs-build/)

本文基于 u-boot-1.1.6, 使用jz2440开发板. 若要使用最新的u-boot版本见: [u-boot官网](http://www.denx.de/wiki/U-Boot/WebHome)  [u-boot下载](ftp://ftp.denx.de/pub/u-boot/)


# hello world

1. 新建文件 `./common/cmd_hello.c`, 按照其他 cmd_XXX 文件内容, 依样画葫芦即可.
2. 打开文件 `./common/Makefile`, 在 `COBJS = ...` 一行, 加入 `cmd_hello.o` 即可.
3. Linux主机下, `make` 指令重新编译 u-boot, 并生成 `u-boot.bin` 文件
4. 烧录并执行, 测试新指令即可, 譬如在uboot命令行下, 输入 `hello DRA&PHO`.

``` c
#include <common.h>
#include <command.h>

int do_hello (cmd_tbl_t *cmdtp, int flag, int argc, char *argv[]) {
    int i;

    printf ("hello world!, %d\n", argc);
    for (i=0; i<argc; i++) {
        printf("argv[%d]: %s\n", i, argv[i]);
    }
}


U_BOOT_CMD(
    hello,  CFG_MAXARGS,    1,  do_hello,
    "hello   - print hello world and arguments\n",
    "[arg [arg ...]]\n    - print hello and arguments\n"
    "\ttest purpose, learn to write uboot command\n"
);
```


# 源码分析

我们用倒推法, 从关键的 `U_BOOT_CMD` 宏定义开始分析.
找到其宏定义所在的文件 `./include/command.h`

```c
39  struct cmd_tbl_s {
40      char        *name;      /* Command Name         */          // 指令名称
41      int     maxargs;    /* maximum number of arguments  */      // 参数最大数量
42      int     repeatable; /* autorepeat allowed?      */          // 空格键是否可自动重复指令
44      int     (*cmd)(struct cmd_tbl_s *, int, int, char *[]);     // 指令函数
45      char        *usage;     /* Usage message    (short) */      // 短帮助说明
47      char        *help;      /* Help  message    (long)  */      // 长帮助说明
53  };
55  typedef struct cmd_tbl_s    cmd_tbl_t;

57  extern cmd_tbl_t  __u_boot_cmd_start;
58  extern cmd_tbl_t  __u_boot_cmd_end;
    // 这两个变量不存在与任何的C或者汇编文件中, 其来源于 "./board/100ask24x0/u-boot.lds" 链接脚本里面

93  #define Struct_Section  __attribute__ ((unused,section (".u_boot_cmd")))
    // 指定变量存放的段位置, 由链接脚本决定.

97  #define U_BOOT_CMD(name,maxargs,rep,cmd,usage,help) \
98  cmd_tbl_t __u_boot_cmd_##name Struct_Section = {#name, maxargs, rep, cmd, usage, help}

    // 已 U_BOOT_CMD(hello,  CFG_MAXARGS, 1, do_hello, ...); 为例, 展开后为
    cmd_tbl_t __u_boot_cmd_hello __attribute__ ((unused,section (".u_boot_cmd"))) = {
    // 这个变量结构被指定存放在 ".u_boot_cmd" 段内
        hello,                                                      // 指令名称 hello
        CFG_MAXARGS,                                                // 参数最大数量
        1,                                                          // 可重复指令
        do_hello,                                                   // 指令函数
        "hello   - print hello world and arguments\n",              // 短帮助说明
        "..."                                                       // 长帮助说明
    }
```

清楚了指令的结构体存放方式后, 需要考虑uboot是如何识别输入的指令, 并执行其指定的函数 `do_XXX`
这个文件位于 `./common/command.c`

``` c
346 cmd_tbl_t *find_cmd (const char *cmd) {
360     for (cmdtp = &__u_boot_cmd_start;                           // 在".u_boot_cmd"段内查找指令
361          cmdtp != &__u_boot_cmd_end;
362          cmdtp++) {
363          if (strncmp (cmd, cmdtp->name, len) == 0) {
364             if (len == strlen (cmdtp->name))
365                 return cmdtp;   /* full match */
367             cmdtp_temp = cmdtp; /* abbreviated command ? */
368             n_found++;
369         }
370     }
371     if (n_found == 1) {         /* exactly one match */
372         return cmdtp_temp;
373     }
376 }
```

此时, 通过查找 find_cmd 函数, 发现被多次调用, 其中一条路径是指令自动完成, 此处忽略.
可以发现它也被 `./common/main.c` 的 `run_command` 调用了

``` c
301  void main_loop (void) {
        // 源码分析中, 已经分析到此函数. 用于自动启动kernel, 或者等待终端输入指令并执行
488     for (;;) {                                  // 死循环, 等待终端输入
497         len = readline (CFG_PROMPT);            // 读取整行, 会存放到 console_buffer 中
501         strcpy (lastcommand, console_buffer);   // 赋值给 lastcommand, 譬如 hello 指令
521         rc = run_command (lastcommand, flag);   // 执行 lastcommand
527     }
529  }

1280 int run_command (const char *cmd, int flag) {
1361    if ((cmdtp = find_cmd(argv[0])) == NULL) {...}          // 查找指令
1391    if ((cmdtp->cmd) (cmdtp, flag, argc, argv) != 0) {...}  // 执行指令函数, 譬如调用 do_hello
1403 }
```

至此, 指令部分的实现分析完成. 再倒过来总结一下:
- main_loop 中, 终端等待用户输入指令, 譬如 "hello"
- run_command 先查找指令是否存在, 调用find_cmd
- find_cmd 会在 ".u_boot_cmd" 段内查找指令是否存在
- 因此, 增减指令很简单, 只有两个关键点:
    - 使用 `U_BOOT_CMD` 宏定义, 定义好指令结构, 编译器会自动存放进".u_boot_cmd" 段
    - 实现指令函数. 习惯上将其命名为 "do_XXX", 如 "do_hello".
- 指令存在的话, 执行指令函数, 即通过 (cmdtp->cmd) (cmdtp, flag, argc, argv) 的形式调用 do_hello
- 执行完成后, 继续死循环等待下一条输入


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
