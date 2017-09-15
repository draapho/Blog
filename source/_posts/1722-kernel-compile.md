---
title: kernel之编译体验
date: 2017-09-01
categories: embedded linlux
tags: [embedded linux, kernel]
---


# 总览
- [嵌入式linux环境搭建-jz2440开发板](https://draapho.github.io/2017/02/21/1707-jz2440-env/), 回顾一下s3c2440的地址分配
- [uboot之makefile分析](https://draapho.github.io/2017/07/07/1719-uboot-makefile/)
- [uboot之源码分析](https://draapho.github.io/2017/08/25/1720-uboot-source/)
- [uboot之定制指令](https://draapho.github.io/2017/08/30/1721-uboot-modify/)
- [kernel之编译体验](https://draapho.github.io/2017/09/01/1722-kernel-compile/)
- [kernel之Makefile分析](https://draapho.github.io/2017/09/14/1724-kernel-makefile/)
- [kernel之内核启动分析](https://draapho.github.io/2017/09/15/1725-kernel-launch/)

本文使用 linux-2.6.22.6 内核, 使用jz2440开发板.


# 解压缩和打补丁

``` bash
# ubuntu shell

tar xjvf linux-2.6.22.6.tar.bz2             # 解压kernel源码
cd linux-2.6.22.6                           # 进入kernel源码目录
patch -p1 < ../linux-2.6.22.6_jz2440.patch  # 打补丁文件, p1表忽略patch文件内的1层目录

# pwd = linux-2.6.22.6
mv ../4.3寸LCD_mach-smdk2440.c arch/arm/mach-s3c2440/mach-smdk2440.c    # 替换为4.3寸屏源码
```

# 生成配置文件 ".config"

整个嵌入式linux系统的配置, 其根源就是这么一个 ".config" 文件.
然后编译时, 会通过makefile变量和C语言的宏定义来实现模块的使能, 禁止或生成为`.ko`模块.

## 生成".config"
生成`.config`配置文件有三种方法:
- 直接使用 `make menuconfig` 进行配置
    - 配置项太多了, 基本不会直接用这种方式
- 基于默认配置自行修改
    - 确保 `pwd` 路径在kernel源码路径下: `./linux-2.6.22.6/`
    - `find -name "*defconfig"`, 查找默认配置文件
    - 可以找到, 最相关的配置文件为 `./arch/arm/configs/s3c2410_defconfig`
    - `make s3c2410_defconfig`, 加载这个默认配置.
    - 注意最后一句 "configuration written to .config", 因此最终生成的就是一个 `.config` 文件
    - `make menuconfig` 根据需求, 部分修改配置 `.config` 文件.
    - 如果遇到错误提示 `fatal error: curses.h:`. 安装 `sudo apt-get install libncurses5-dev libncursesw5-dev`
- 使用厂家提供的配置文件
    - jz2440 提供的配置文件名为 `config_ok`
    - `cp config_ok .config` 直接改名为 `.config` 文件即可.
    - `make menuconfig`, 一样可以再自己定制配置.


## 修改".config"

执行 `make menuconfig` 后, 有个简单的用户界面. 关键操作如下:
- `上下左右`键进行移动, `Enter`键进入子菜单.
- 按两边 `ESC` 返回上一级, 或退出界面.
- `蓝色高亮字母` 为快捷键, 按了直接跳到那一行
- `Y` 表示需要加载这个模块
- `N` 表示不要加载这个模块
- `M` 表示将此模块生成 `.ko` 文件, 可动态加载.
- `?` 显示当前行的帮助信息, 帮助页按 `上下` 或 `jk` 进行翻页
- `/` 搜索关键字


# 分析配置过程

从 ".config" 文件出发, 分析查看该文件如何影响 Makefile 文件以及C语言的宏定义.

## ".config" 文件

使用 `vim .config` 查看该文件, 可知其基本格式为 `CONFIG_XXX=`
- `# CONFIG_XXX is not set` 此项被配置为 `N`, 不编译
- `CONFIG_XXX=y` 此项被配置为 `Y`, 直接编译进内核
- `CONFIG_XXX=m` 此项被配置为 `M`, 编译为`.ko`文件, 供动态加载
- `CONFIG_LOCALVERSION=""` 此项为字符串, 也可能是数值

我们以 `CONFIG_DM9000` 为例, 进行搜索. 忽略一些其他的配置文件, 关键的文件有如下几个:
- `include/linux/autoconf.h:129:   #define CONFIG_DM9000 1`
    - 这是个C语言的头文件, 很明显是给C语言代码调用的.
    - 该文件由Makefile调用 `./scripts/kconfig/` 内的脚本自动生成.
    - 对于 `y` `m` 的配置项, 宏定义为 `1`
    - 对于 `n` 的配置项, 不进行宏定义
- `include/config/auto.conf:128:   CONFIG_DM9000=y`
    - 这个文件是给 Makefile 调用的, 里面的值全部被认为是Makefile变量.
    - 该文件由Makefile调用 `./scripts/kconfig/` 内的脚本自动生成.
    - 对于 `y` `m` 以及其它值的配置项, 照抄一遍 `.config` 里的内容
    - 对于 `n` 的配置项, 无定义!
- `drivers/net/Makefile:197:   obj-$(CONFIG_DM9000) += dm9dev9000c.o`
    - 子目录下的 Makefile 会被顶层的 Makefile 包含
    - 由`auto.conf`文件可知`$(CONFIG_DM9000)=y`
    - 所以此句等同于 `obj-y += dm9dev9000c.o`
    - 同理, 被设置成 `m` 的变量就会有 `obj-m += xxx.o`
    - 如果配置项被设为 `n`, 则变量为空, 替换后为 `obj- += xxx.o`, 会被直接忽略
    - Makefile 最后就通过 `obj-y` 或 `obj-m` 来识别配置, 编译模块.
- `.config:588:   CONFIG_DM9000=y`
    - `./.config` 配置文件. 一切配置的源头文件.



# 编译和烧录内核

## 编译内核
``` bash
cp config_ok .config                        # 加载厂家默认配置
make clean                                  # 清空
make uImage                                 # 编译获得内核image

# 可能在make时, 提示如下错误信息. 原因是新版的make对老的Makefile规则不兼容
Makefile:1449: *** mixed implicit and normal rules.  Stop.

vim Makefile
    # 416行      config %config: scripts_basic outputmakefile FORCE
    #   改为 ->  %config: scripts_basic outputmakefile FORCE
    # 1449行     / %/: prepare scripts FORCE
    #   改为 ->  %/: prepare scripts FORCE
    # 保存后重新编译即可.
```

## 使用 nfs 烧录

如果配置好网路, 建议使用 nfs 进行烧录
``` bash
# 开发板 uboot
# 要使用nfs功能, 必须正确设置uboot的ip地址
# 将 .../linux-2.6.22.6/arch/arm/boot/uImage 拷贝到 /jz2440/

# kernel: 在OpenJTAG> 提示符下
nfs 30000000 10.0.0.98:/jz2440/uImage       # nfs 加载 kernel 固件到ram中 (0x30000000是sdram的地址)
nand erase kernel                           # 擦除 falsh 的 kernel 区
nand write.jffs2 30000000 kernel            # 烧录 kernel (ram->flash)
```

## 使用 dnw 烧录
**确保链接了开发板的串口和usb口, 并把usb口关联到Ubuntu上.**

``` bash
# 开发板 uboot

# 打开 jz2440 开发板串口终端, 启动时输入空格键, 进入如下菜单
##### 100ask Bootloader for OpenJTAG #####
[n] Download u-boot to Nand Flash
[o] Download u-boot to Nor Flash            # 如果是Nand Flash启动的话，这个菜单项没有
[k] Download Linux kernel uImage
[j] Download root_jffs2 image
[y] Download root_yaffs image
[d] Download to SDRAM & Run
[z] Download zImage into RAM
[g] Boot linux from RAM
[f] Format the Nand Flash
[s] Set the boot parameters
[b] Boot the system
[r] Reboot u-boot
[q] Quit from menu

Enter your selection: k                     # 输入k, 烧录 kernel
USB host is connected. Waiting a download.  # 提示连接成功



# 切换到 Ubuntu 终端, 输入
# pwd = ./linux-2.6.22.6                    # 确保在 kernel 源码路径下
sudo dnw ./arch/arm/boot/uImage             # 输入dnw指令, 指明烧录文件
# DNW usb device found!                     # 开始烧录
```




----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
