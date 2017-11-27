---
title: uboot之makefile分析
date: 2017-07-07
categories: embedded linux
tags: [embedded linux, uboot, jz2440]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [jz2440分区及启动的基础概念](https://draapho.github.io/2017/11/24/1735-jz2440-basic/)
- [uboot之makefile分析](https://draapho.github.io/2017/07/07/1719-uboot-makefile/)
- [uboot之源码分析](https://draapho.github.io/2017/08/25/1720-uboot-source/)
- [uboot之定制指令](https://draapho.github.io/2017/08/30/1721-uboot-modify/)

本文基于 u-boot-1.1.6, 使用jz2440开发板. 若要使用最新的u-boot版本见: [u-boot官网](http://www.denx.de/wiki/U-Boot/WebHome)  [u-boot下载](ftp://ftp.denx.de/pub/u-boot/)

# u-boot 编译过程
1. 解压缩 u-boot-1.1.6
2. 打补丁 针对特定开发板发布的补丁. 打补丁方法
   `uboot目录下$ patch -p1 < ../补丁文件`  p1表示忽略补丁目标目录的第一层
3. 配置 `make 100ask24x0_config`
4. 编译: `make`, 获取 `u-boot.bin` 文件
5. 烧录, 多种方式, 可以用jlink烧录到 NOR Flash 中

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
  
# u-boot的README

要了解 u-boot 的架构和设计思路, 建议先看自带的 `README` 文件. 重要信息如下:
- `include/configs/<board_name>.h`  板级配置头文件
- `make NAME_config`                加载配置, 准备编译
- `make` or `make all`              编译生成bin文件
- `Monitor Commands - Overview:`    u-boot 指令概览
- `Environment Variables:`          u-boot 环境变量
- `Linux HOWTO:`                    编译linux uImage
- `Boot Linux:`                     u-boot 启动Linux相关设置

自己设置板级配置的步骤: (位于 README line 2375)
1.  Add a new configuration option for your board to the toplevel
    "Makefile" and to the "MAKEALL" script, using the existing
    entries as examples. Note that here and at many other places
    boards and other names are listed in alphabetical sort order. Please
    keep this order.
2.  Create a new directory to hold your board specific code. Add any
    files you need. In your board directory, you will need at least
    the "Makefile", a "<board>.c", "flash.c" and "u-boot.lds".
3.  Create a new configuration file "include/configs/<board>.h" for
    your board
3.  If you're porting U-Boot to a new CPU, then also create a new
    directory to hold your CPU specific code. Add any files you need.
4.  Run "make <board>_config" with your new name.
5.  Type "make", and you should get a working "u-boot.srec" file
    to be installed on your target system.
6.  Debug and solve any problems that might arise.


# u-boot的Makefile

分析 `100ask24x0` 即jz2440板子的Makefile实现. Linux下可以使用grep搜索.
``` bash
# pwd = u-boot-1.1.6 文件夹下
grep -n 100ask24x0 ./Makefile       # 在Makefile文件下查找 100ask24x0, 并显示行号
grep -nr 100ask24x0 *               # 当前目录递归查找 100ask24x0
grep -nwr 100ask24x0 *              # w=word, 100ask24x0 作为一个单词查找
grep -nd skip 100ask24x0 *          # 仅在当前目录查找, 不显示子目录信息

# 特别强大的一条指令, 可针对指定文件搜索指定关键字!
# 先用find找出所有的Makefile文件, 然后在Makefile文件内查找 uImage 关键字.
find ./ -name "Makefile" | xargs grep -nw --color "uboot"
```

## 'make 100ask24x0_config' 指令分析

`make 100ask24x0_config` 其指令结构和 `make clean` 是一样的. 
因此在 Makefile 里找到 `100ask24x0_config` 为目标的行即可:
``` bash
1886    100ask24x0_config	:	unconfig    
1887	    @$(MKCONFIG) $(@:_config=) arm arm920t 100ask24x0 NULL s3c24x0

# 目标为 100ask24x0_config, 没有依赖
# 执行 make 100ask24x0_config 后, 实际运行的就是第二行的指令
# 找到并替换里面的变量:
#   MKCONFIG	:= $(SRCTREE)/mkconfig
#   SRCTREE		:= $(CURDIR)
#   $(@:_config=) 其中 $(@) 表示目标, 即 `100ask24x0_config:_config=空`, 最终得到 `100ask24x0`
# 整句替换下来的指令就变成了:
    ./mkconfig 100ask24x0 arm arm920t 100ask24x0 NULL s3c24x0
```

因此, 我们需要去当前文件夹下查找 `mkconfig` 这个脚本文件.
下面直接删减成最终执行的样子, 前面加上原来的行号便于学习比较
``` bash
# 输入为: ./mkconfig 100ask24x0 arm arm920t 100ask24x0 NULL s3c24x0
# 对应的变量:  $0        $1      $2   $3       $4        $5    $6

# 打印信息
23  BOARD_NAME="$1"                             # BOARD_NAME=100ask24x0
28  "Configuring for ${BOARD_NAME} board..."    # Configuring for 100ask24x0 board...

# 重新创建一系列的软链接:
46  cd ./include
47  rm -f asm
48  ln -s asm-$2 asm                            # asm->asm-arm, 建立一个软连接, 使用asm-arm
51  rm -f asm-$2/arch                           # asm-arm/arch
56  ln -s ${LNPREFIX}arch-$6 asm-$2/arch        # LNPREFIX. 因此 asm-arm/arch->arch-s3c24x0
60  rm -f asm-$2/proc
61	ln -s ${LNPREFIX}proc-armv asm-$2/proc      # asm-arm/proc->proc-armv, 

# 创建 config.mk 文件
67  echo "ARCH   = $2" >  config.mk             # >  新建, "ARCH   = arm"
68  echo "CPU    = $3" >> config.mk             # >> 追加, "CPU    = arm920t"
69  echo "BOARD  = $4" >> config.mk             # >> 追加, "BOARD  = 100ask24x0"
71  [ "$5" ] && [ "$5" != "NULL" ] && echo "VENDOR = $5" >> config.mk   # $5 = NULL, 不写VENDOR字段
73  [ "$6" ] && [ "$6" != "NULL" ] && echo "SOC    = $6" >> config.mk   # "SOC = s3c24x0"
# 可以使用 `cat ./include/config.mk` 查看该文件的内容.

# 创建 config.h 文件. 为了 `#include <configs/100ask24x0.h>`
82  > config.h                                                      # >  新建 config.h
84  echo "/* Automatically generated - do not edit */" >>config.h   # >> 追加写入
85  echo "#include <configs/$1.h>" >>config.h                       # >> 追加写入, $1=100ask24x0
# 可以使用 `cat ./include/config.h` 查看该文件的内容.
```

## 'make' 指令分析

`make` 实际上执行的是 `make all`, Makefile 中比较重要的几行为:
```
116 # load ARCH, BOARD, and CPU configuration
117 include $(OBJTREE)/include/config.mk
118 export	ARCH CPU BOARD VENDOR SOC
# ./include/config.mk 这个文件由 `make 100ask24x0_config` 指令生成, 可获得如下变量
# ARCH   = arm
# CPU    = arm920t
# BOARD  = 100ask24x0
# SOC    = s3c24x0

164 include $(TOPDIR)/config.mk
# u-boot-1.1.6 根目录下的配置文件, 里面有一些变量的定义

169 OBJS  = cpu/$(CPU)/start.o
193 LIBS  = lib_generic/libgeneric.a
194 LIBS += board/$(BOARDDIR)/lib$(BOARD).a
195 LIBS += cpu/$(CPU)/lib$(CPU).a
197 LIBS += cpu/$(CPU)/$(SOC)/lib$(SOC).a
199 LIBS += lib_$(ARCH)/lib$(ARCH).a
# 加载几个板级参数相关的变量值. 特别注意 start.o 这个文件, 是整个u-boot最先运行的文件

239 ALL = $(obj)u-boot.srec $(obj)u-boot.bin $(obj)System.map $(U_BOOT_NAND)
241 all:		$(ALL)
# `make` 指令的入口就在这里. 可以根据 ALL 目标后面的依赖开始看这个 make 的过程

262 $(obj)u-boot:		depend version $(SUBDIRS) $(OBJS) $(LIBS) $(LDSCRIPT)
263		    UNDEF_SYM=`$(OBJDUMP) -x $(LIBS) |sed  -n -e 's/.*\(__u_boot_cmd_.*\)/-u\1/p'|sort|uniq`;\
264		    cd $(LNDIR) && $(LD) $(LDFLAGS) $$UNDEF_SYM $(__OBJS) \
265             --start-group $(__LIBS) --end-group $(PLATFORM_LIBS) \
266             -Map u-boot.map -o u-boot
# 比较重要的一个指令. 可以运行 `make`, 在最后会看到这条指令的展开式, 用这种倒推的方式比较方便. 其展开如下:

make[1]: Leaving directory '/home/draapho/jz2440/uboot/u-boot-1.1.6/common'
# 这句不重要, 但这句的位置很明显, 所以写在这里了.

UNDEF_SYM=`arm-linux-objdump -x lib_generic/libgeneric.a board/100ask24x0/lib100ask24x0.a cpu/arm920t/libarm920t.a cpu/arm920t/s3c24x0/libs3c24x0.a lib_arm/libarm.a fs/cramfs/libcramfs.a fs/fat/libfat.a fs/fdos/libfdos.a fs/jffs2/libjffs2.a fs/reiserfs/libreiserfs.a fs/ext2/libext2fs.a net/libnet.a disk/libdisk.a rtc/librtc.a dtt/libdtt.a drivers/libdrivers.a drivers/nand/libnand.a drivers/nand_legacy/libnand_legacy.a drivers/usb/libusb.a drivers/sk98lin/libsk98lin.a common/libcommon.a |sed  -n -e 's/.*\(__u_boot_cmd_.*\)/-u\1/p'|sort|uniq`;\
# 整个语句有点复杂, 用了一系列管道指令, 将最终结果赋值给 UNDEF_SYM 这么一个变量
# 对 "UNDEF_SYM=`$(OBJDUMP) -x $(LIBS) |sed  -n -e 's/.*\(__u_boot_cmd_.*\)/-u\1/p'|sort|uniq`;\" 的展开
# 其中 "board/100ask24x0/lib100ask24x0.a cpu/arm920t/libarm920t.a cpu/arm920t/s3c24x0/libs3c24x0.a lib_arm/libarm.a" 就是对 $(LIBS) 的展开
  
cd /home/draapho/jz2440/uboot/u-boot-1.1.6 && 
# "cd $(LNDIR) &&" 的展开, 进入 u-boot-1.1.6 目录. 

arm-linux-ld -Bstatic -T /home/draapho/jz2440/uboot/u-boot-1.1.6/board/100ask24x0/u-boot.lds -Ttext 0x33F80000  $UNDEF_SYM cpu/arm920t/start.o \
# "$(LD) $(LDFLAGS) $$UNDEF_SYM $(__OBJS) \" 的展开
# $(LD) 就是 arm-linux-ld 链接指令. 其中 "LD	= $(CROSS_COMPILE)ld", 定义在 "./config.mk", $(CROSS_COMPILE) 在 Makefile 下面. 
# $(LDFLAGS) 给出了链接指令的参数, 定义在 "./config.mk", 形式为 "LDFLAGS += -Bstatic -T $(LDSCRIPT) -Ttext $(TEXT_BASE) $(PLATFORM_LDFLAGS)"
# 根据 "cpu/arm920t/start.o", 可以知道 start.s 的文件位置, 便于以后查看. (由u-boot.lds可知, 这是u-boot第一个运行的代码段)
# !!! 其中 $(LDSCRIPT) 和 $(TEXT_BASE) 很重要 !!!
    # "LDSCRIPT := $(TOPDIR)/board/$(BOARDDIR)/u-boot.lds", 定义在 "./config.mk". 可以查看链接脚本
    # "TEXT_BASE = 0x33F80000", 定义在 "./board/100ask24x0/config.mk". 这个参数明显是板级相关的. 也可以使用 0x33F80000 来搜索.

                --start-group lib_generic/libgeneric.a board/100ask24x0/lib100ask24x0.a cpu/arm920t/libarm920t.a cpu/arm920t/s3c24x0/libs3c24x0.a lib_arm/libarm.a fs/cramfs/libcramfs.a fs/fat/libfat.a fs/fdos/libfdos.a fs/jffs2/libjffs2.a fs/reiserfs/libreiserfs.a fs/ext2/libext2fs.a net/libnet.a disk/libdisk.a rtc/librtc.a dtt/libdtt.a drivers/libdrivers.a drivers/nand/libnand.a drivers/nand_legacy/libnand_legacy.a drivers/usb/libusb.a drivers/sk98lin/libsk98lin.a common/libcommon.a --end-group -L /usr/local/gcc-3.4.5-glibc-2.3.6/bin/../lib/gcc/arm-linux/3.4.5 -lgcc \
                -Map u-boot.map -o u-boot
# 依旧属于 arm-linux-ld 的指令, 这里就是对 "$(__LIBS)" 和 "$(PLATFORM_LIBS)" 的展开, 忽略这一段, 对理解没有影响.
```

## 'u-boot.lds' 链接脚本分析

根据对 Makefile 的分析, 可以知道uboot代码的偏移地址被设置成了 `-Ttext 0x33F80000` 这么一个值.
其含义就是, **给u-boot的代码段分配的空间位于SDRAM最顶部的512K.**
jz2440使用的SDRAM大小为 64M, 即 0x400_0000, 预留512K (0x8_0000)给u-boot代码, 得到地址 0x3F8_0000. 
因为 s3c24x0 给SDRAM分配的地址是从 0x3000_0000 开始的, 所以有了 0x33F8_0000 这么一个值. 

链接脚本 `./board/100ask24x0/u-boot.lds` 也很重要. 从中可以知道u-boot整个代码段的分配情况. 下面来分析一下:
链接脚本的作用就是安排目标文件在可执行文件中的顺序, 便于链接器生成最终的可执行文件.
```
OUTPUT_FORMAT("elf32-littlearm", "elf32-littlearm", "elf32-littlearm")
/*OUTPUT_FORMAT("elf32-arm", "elf32-arm", "elf32-arm")*/
OUTPUT_ARCH(arm)
ENTRY(_start)
SECTIONS
{
    // . 表示当前位置, 设置当前位置为 0. 实际物理地址需要加上偏移量 0x33F80000
	. = 0x00000000;

	. = ALIGN(4);                   // 4字节对齐
	.text      :                    // 代码段
	{
	  cpu/arm920t/start.o	(.text) // 第一段代码放 start.s
      board/100ask24x0/boot_init.o (.text)  // 第二段代码放 boot_init.c (非必须)
	  *(.text)                      // 其它的代码段
	}

	. = ALIGN(4);
	.rodata : { *(.rodata) }        // 只读数据段, RO段

	. = ALIGN(4);
	.data : { *(.data) }            // 数据段, RW段

	. = ALIGN(4);
	.got : { *(.got) }              // uboot自定义, 非标准段

	. = .;
	__u_boot_cmd_start = .;         // 赋值 __u_boot_cmd_start, 命令段起始位置
	.u_boot_cmd : { *(.u_boot_cmd) }// uboot 命令段, uboot通过宏定义, 将命令放在该段
	__u_boot_cmd_end = .;           // 赋值 __u_boot_cmd_end, 命令段结束位置

	. = ALIGN(4);
	__bss_start = .;                // 赋值 __bss_start
	.bss : { *(.bss) }              // bss 段
	_end = .;                       // 赋值 _end
}

```


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***