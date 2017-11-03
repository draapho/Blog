---
title: kernel之Makefile分析
date: 2017-09-14
categories: embedded linlux
tags: [embedded linux, kernel]
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

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.


# Makefile 概览
`.\linux-2.6.22.6\Documentation\kbuild\makefiles.txt` 详细介绍了 kernel 的 makefile用法.
建议完整过一遍, 它对如何配置, 生成配置, 编译过程有完整的阐述.

Makefile分为5个部分:
- `Makefile`, 位于kernel根目录, 顶层Makefile. 最终目的是编译内核, 生成 `vmlinux` 和 `modules`.
- `.config`, kernel配置文件, 已在 [kernel之编译体验](https://draapho.github.io/2017/09/01/1722-kernel-compile/)分析过生成方式和过程
- `arch/$(ARCH)/Makefile`, 芯片架构相关的Makefile
- `scripts/Makefile.*`, Makefile的规则和脚本
- `kbuild Makefiles`, 即各子目录下的`Makefile`, 最终都会被顶层Makefile调用的.


`obj-y`, 表示需要编译进内核, 其形式很简单
- `obj-$(CONFIG_DM9000) += dm9dev9000c.o`, 含变量的形式.
- `obj-y += dm9dev9000c.o`, 替换变量后的直观形式.


`obj-m`, 表示需要编译为`.ko`模块. 有三种形式

``` makefiles
# 单文件编译为模块, 变量$(CONFIG_ISDN_PPP_BSDCOMP)为m
obj-$(CONFIG_ISDN_PPP_BSDCOMP) += isdn_bsdcomp.o

# 多文件编译为模块, 变量$(CONFIG_ISDN)为m
# 目标模块名称 isdn.ko
obj-$(CONFIG_ISDN) += isdn.o
# 关联相关源文件, 使用 xxx-objs. $(LD) 链接命令会链接如下文件.
isdn-objs := isdn_net_lib.o isdn_v110.o isdn_common.o

# 多文件可配置, 编译为模块. 可使用 xxx-$(CONFIG_) 来配置
# $(CONFIG_EXT2_FS) 为m, 即需要生成 ext2.ko 模块文件
obj-$(CONFIG_EXT2_FS)        += ext2.o
# 必须的关联文件有如下两个, 此处效果等同于 ext2-objs := balloc.o bitmap.o
ext2-y                       := balloc.o bitmap.o
# 另外一个文件则根据配置决定是否编译进模块. 其值为 y 或者空.
ext2-$(CONFIG_EXT2_FS_XATTR) += xattr.o
```

`lib-y` 编译为库文件. 形如 `lib-y := checksum.o delay.o`
一般仅用于 `lib/` 以及 `arch/*/lib-y` 目录下面

另外还有一些 `EXTRA_CFLAGS`, `EXTRA_AFLAGS`, `EXTRA_LDFLAGS`, `EXTRA_ARFLAGS` 的 flag配置
此处略过不表.


# linux下关键字搜索技巧

由于有多个Makefile, 变量也分布在不同的文件中, 所以阅读起来比较麻烦.
此处再重复列举一下linux下的搜索技巧

``` bash
grep -n 100ask24x0 ./Makefile       # 在Makefile文件下查找 100ask24x0, 并显示行号
grep -nr 100ask24x0 *               # 当前目录递归查找 100ask24x0
grep -nwr 100ask24x0 *              # w=word, 100ask24x0 作为一个单词查找
grep -nd skip 100ask24x0 *          # 仅在当前目录查找, 不显示子目录信息

# 特别强大的一条指令, 可针对指定文件搜索指定关键字!
# 先用find找出所有的Makefile文件, 然后在Makefile文件内查找 uImage 关键字.
find ./ -name "Makefile" | xargs grep -nw --color "uImage"
```


# Makefile整体分析


``` makefile
    # 顶层Makefile, 位于 "./linux-2.6.22.6/Makefile"
    # 这里就不按文件顺序排列, 而按照分析Makefile的逻辑顺序排列了.

186 ARCH		?= arm                  # arm 架构
187 CROSS_COMPILE	?= arm-linux-       # 指定编译器

192 KCONFIG_CONFIG	?= .config          # 指定配置文件

284 LD		= $(CROSS_COMPILE)ld        # 指定一些列指令
285 CC		= $(CROSS_COMPILE)gcc

    # 编译时, 我们使用 make uImage, 因为需要uImage格式.
    # 但过程和 make all 是一样的, 都需要生成 vmlinux 
484 all: vmlinux                       # 直接make, 就是生成vmlinux

581 # Build vmlinux. 可以看一行开始的注释, 说明了vmlinux的依赖结构

    # 找到了 vmlinux 这个目标有关的依赖文件, 逐一扩展来看
745 vmlinux: $(vmlinux-lds) $(vmlinux-init) $(vmlinux-main) $(kallsyms.o) FORCE
    # kernel/kallsyms.c

608 vmlinux-init := $(head-y) $(init-y)
609 vmlinux-main := $(core-y) $(libs-y) $(drivers-y) $(net-y)
611 vmlinux-lds  := arch/$(ARCH)/kernel/vmlinux.lds
    # vmlinux-lds:= arch/arm/kernel/vmlinux.lds
    # 此文件由 vmlinux.lds.S 在make时自动生成!

434 init-y		:= init/
435 drivers-y	:= drivers/ sound/
436 net-y		:= net/
437 libs-y		:= lib/
438 core-y		:= usr/
562 core-y		+= kernel/ mm/ fs/ ipc/ security/ crypto/ block/

573 init-y		:= $(patsubst %/, %/built-in.o, $(init-y))
574 core-y		:= $(patsubst %/, %/built-in.o, $(core-y))
575 drivers-y	:= $(patsubst %/, %/built-in.o, $(drivers-y))
576 net-y		:= $(patsubst %/, %/built-in.o, $(net-y))
577 libs-y1		:= $(patsubst %/, %/lib.a, $(libs-y))
578 libs-y2		:= $(patsubst %/, %/built-in.o, $(libs-y))
579 libs-y		:= $(libs-y1) $(libs-y2)

    # patsubst 是makefile内的字符串替换函数, 替换结果为:
    # init-y    := init/built-in.o
    # core-y    := usr/built-in.o kernel/built-in.o mm/built-in.o fs/built-in.o ... (略)
    # drivers-y := drivers/built-in.o sound/built-in.o
    # net-y     := net/built-in.o
    # libs-y    := lib/lib.a lib/built-in.o
    
    # find ./ -name "Makefile" | xargs grep -nw --color "head-y"
    # 查出 head-y 位于 "./arch/arm/Makefile" 以及 "./arch/arm/kernel/Makefile" 内
    # head-y	:= arch/arm/kernel/head.S arch/arm/kernel/init_task.c, 分析见 架构文件内的Makefile.
    

    
    # 此句就是执行指令, 将上述相关文件打包生成vmlinux二进制内核文件. 太难懂, 先略过.
745 vmlinux: $(vmlinux-lds) $(vmlinux-init) $(vmlinux-main) $(kallsyms.o) FORCE
749	$(call if_changed_rule,vmlinux__)
750	$(Q)$(MAKE) -f $(srctree)/scripts/Makefile.modpost $@
751	$(Q)rm -f .old_version
```

``` makefile
    # 架构文件内的 Makefile, 位于 "./arch/arm/Makefile"

    # 查找 .config 文件可知, CONFIG_MMU=y
26  ifeq ($(CONFIG_MMU),)       # CONFIG_MMU不为空, 条件不成立
27  MMUEXT		:= -nommu
28  endif                       # 因此 $(MMUEXT) 为空

94  head-y		:= arch/arm/kernel/head$(MMUEXT).o arch/arm/kernel/init_task.o
    # head-y	:= arch/arm/kernel/head.S arch/arm/kernel/init_task.c
    # 至于 "./arch/arm/kernel/Makefile" 内的head-y, 猜测是为 extra-y 服务的, 不去追究.
    
    # make uImage时, 也需要先生成 vmlinux. 事实上, uImage格式只是比vmlinux多64字节的头.
227 zImage Image xipImage bootpImage uImage: vmlinux
```


至此, 为生成vmlinux的原材料都已经分析完成, 就看如何执行指令了.
但是, 由Makefile进行分析的话, 需要去看一系列的脚本文件, 工作量太大, 也难以理解.
我们倒过来分析, 直接执行 `make uImage V=1`, 查看编译指令是否和分析的一致.

``` bash
# pwd = ./linux-2.6.22.6
make uImage             # 生成 uImage, 如有必要, 先 make clean
rm vmlinux              # 删除目标文件vmlinux
make uImage V=1         # 查看生成vmlinux时, 详细的编译指令

# 可以在执行结果中, 找到这么一行:
# arm-linux-ld -EL  -p --no-undefined -X -o vmlinux -T arch/arm/kernel/vmlinux.lds 
# arch/arm/kernel/head.o arch/arm/kernel/init_task.o  init/built-in.o 
# --start-group  usr/built-in.o  arch/arm/kernel/built-in.o  arch/arm/mm/built-in.o  arch/arm/common/built-in.o  arch/arm/mach-s3c2410/built-in.o  arch/arm/mach-s3c2400/built-in.o  arch/arm/mach-s3c2412/built-in.o  arch/arm/mach-s3c2440/built-in.o  arch/arm/mach-s3c2442/built-in.o  arch/arm/mach-s3c2443/built-in.o  arch/arm/nwfpe/built-in.o  arch/arm/plat-s3c24xx/built-in.o  kernel/built-in.o  mm/built-in.o  fs/built-in.o  ipc/built-in.o  security/built-in.o  crypto/built-in.o  block/built-in.o  arch/arm/lib/lib.a  lib/lib.a  arch/arm/lib/built-in.o  lib/built-in.o  drivers/built-in.o  sound/built-in.o  net/built-in.o 
# --end-group .tmp_kallsyms2.o

# 分析如下:
    # "arm-linux-ld"                    链接命令
    # "-o vmlinux"                      目标文件
    # "-T arch/arm/kernel/vmlinux.lds"  指定链接脚本
    # 一系列的 ".o" 文件, 就是前文分析出的相关文件, 能一一对应的.
```

# 链接指令的工作方式

链接指令的工作方式为, 根据链接脚本的要求对每个文件内的段按顺序排放. 相同的段, 则按照指令的文件顺序排放.
譬如: lds 一开始的段位 `.text.head` 和 `.init`. 那么以 head.o 和 init_task.o 为例, 其排放顺序为
```
# .text.head 段开始
head.text.head          # 第一个文件的 .text.head 段
init_task.text.head     # 第二个文件的 .text.head 段
# .text.head 段结束

# .init 段开始
head.init               # 第一个文件的 .init 段
init_task.init          # 第二个文件的 .init 段
# .init 段结束

# 这样, 链接指令就会把各文件打包生成一个最终的二进制文件, 名称为 vmlinux
```

为分析内核启动过程, 重要的信息如下:
- 第1个文件: `arch/arm/kernel/head.S`
- 链接脚本:  `arch/arm/kernel/vmlinux.lds`


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***