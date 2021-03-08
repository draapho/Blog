---
title: LinK+, 一款Linux内核开发IDE
date: 2017-11-27
categories: embedded linux
tags: [linuxembedded linux, ide]
description: 如题.
---


# 前言
LinK+ 是一款在linux下基于eclipse开发的免费的Linux内核以及驱动开发软件.
这个软件在国外知名度也不高. 国内更是没人介绍过这一款软件.
软件的现状是: 开发者似乎已经停止更新, 设想中支持的ARM架构也没有下文. 因此不支持嵌入式的仿真.
**我主要用它来查看内核源码, 开发驱动, 能快速的搭建好驱动架构, 支持内核函数跳转查看! 自动生成Makefile.**

网址如下: [Linux Kernel Programming IDE (LinK+)](https://sourceforge.net/projects/linkplustest/)


# 安装

根据用户手册, 有多种安装方法. 使用最简单的 LinK+IDE方式.
下载 32bit, 因为我用的是32位的Ubuntu.
- [点这里, 下载页面](https://sourceforge.net/projects/linkplustest/files/installers/)
- [安装和使用手册](http://sourceforge.net/projects/linkplustest/files/documentation/LinK%2B_UserManual_Rev4.pdf)

**说明一下 LinK+ UserManual 里面的 `-`横杠都是错误的, 终端无法识别!**
然后按照说明安装如下依赖的软件.

``` bash
# 安装最新版 openjdk, 向下兼容jdk6即可.
sudo apt-get install openjdk-8-jdk

# 安装open ssh
sudo apt-get install openssh-client openssh-server

# 其它依赖的软件
sudo apt-get install libqt4-dev
sudo apt-get install libncurses5
sudo apt-get install qemu
sudo apt-get install bridge-utils iptables dnsmasq


# 安装 LinK+IDE
# 下载好LinK+IDE的文件, LinK+ IDE-linux.gtk.x86.tar.gz.tar.gz
tar -xzvf LinK+\ IDE-linux.gtk.x86.tar.gz.tar.gz
./linkplus
# 安装成功的话, 就能运行了.
```

然后, LinK+IDE 的升级和插件不用看了. 很久没更新过了.


# Kernel源码的编译和阅读

先确定linux内核源码可以在终端下成功编译.
新建Makefile工程
![link.JPG](https://draapho.github.io/images/1737/link1.JPG)


选择源码路径, 工具链使用Makefile自己的, 所以选`<none>`
![link.JPG](https://draapho.github.io/images/1737/link2.JPG)


选中项目, 然后在菜单里取消自动编译, 最后选择项目属性
![link.JPG](https://draapho.github.io/images/1737/link3.JPG)


设定编译指令, `make` 即可
![link.JPG](https://draapho.github.io/images/1737/link5.JPG)


设定指令目标. 内核使用 `uImage`, 驱动使用 `make modules`
![link.JPG](https://draapho.github.io/images/1737/link6.JPG)


如果需要设置更多的指令目标, 用如下方式. Create是设置, Build是执行
![link.JPG](https://draapho.github.io/images/1737/link7.JPG)


设置自定义目标
![link.JPG](https://draapho.github.io/images/1737/link8.JPG)


好了, 如果这样直接 `Make Targets`->`Build...`->`uImage`, 会编译失败.
原因是Eclipse下面无法正确识别Makefile下面的CROSS_COMPILE路径.
见 [Ubuntu下基于Eclipse去调用Makefile交叉编译Uboot](
https://www.crifan.com/ubuntu_eclipse_cross_compile_uboot_based_on_makefile/)
需要将其改为绝对路径. 打开内核源码根目录下的 `Makefile`, 187行, 修改如下:

``` makefile
# CROSS_COMPILE ?= arm-linux-
CROSS_COMPILE   ?= /usr/local/gcc-3.4.5-glibc-2.3.6/bin/arm-linux-
```


再次在eclipse下尝试编译, 就成功了. 看Console的输出, 获得uImage文件
```
Kernel: arch/arm/boot/Image is ready
Kernel: arch/arm/boot/zImage is ready
Image arch/arm/boot/uImage is ready
```

但Ecilpse依旧会显示很多警告和错误. 原因不明, 查的如下资料:
- [What is kernel section mismatch?](https://stackoverflow.com/questions/8563978/what-is-kernel-section-mismatch)
- [解决编译kernel出现WARNING:Section mismatch(es)](http://www.linuxdiyf.com/linux/24369.html)

先忽略这些错误警告, 但此时, 有些函数依旧不能正常跳转. 原因是 `.\include\linux\autoconf.h` 没有被其它头文件包含, 里面的宏定义linux源码无法识别. 解决办法是我们自己把这些宏定义加入eclipse的SYMBOLS. 手工一个个加入不现实, 我写了一个python代码, 把linux下的config自动转为eclipse可识别的XML格式:
**[下载config2xml](https://github.com/draapho/Blog/tree/master/_blog_stuff/linux/config2xml.py)**


将这个文件放在linux源码根目录下, 配置好`.config` 文件. 然后在终端运行它
``` bash
# pwd = linux内核源码根目录
$ python config2xml.py
Generate ../eclipse_SYMBOLS.xml successfully...
```

成功后, 会在上层目录生成 `eclipse_SYMBOLS.xml` 这么一个文件.
然后回到eclipse里面, 将其导入. 如图:
![link.JPG](https://draapho.github.io/images/1737/link9.JPG)

另外, 为方便跳转, 可以在eclipse下面把linux源码下不相关的平台代码排除掉.
![link.JPG](https://draapho.github.io/images/1737/link4.JPG)

最后, 需要把项目的index索引重建一下才能正确跳转. 重建耗时较长.
![link.JPG](https://draapho.github.io/images/1737/link10.JPG)


**至此内核源码的C语言部分已经能成功的跳转查看了.汇编部分可以用eclipse的搜索功能.**


# 写驱动

需要先在工程里加载好Kernel源码!
然后参考 **[驱动之基于LinK+设计按键驱动](https://draapho.github.io/2017/11/30/1740-drv-chr2/)**



大致步骤如下:

- LinK+IDE里, 新建工程->Linux Kernel Development(LinK+)
- 选择 Device Driver Project
- 写好驱动名称, 驱动路径, 作者, 开源证书类型
- Kernel Version 要去掉 `Use Host Machine Kernel`, 选择我们已经编译好的嵌入式内核源码路径
- X86架构 (ARM不支持),
- 下面两步可以根据需求自己选择驱动框架, LinK+会自动生成有框架的.c和.h以及Makefile文件.
- 驱动下面, 所有的跳转都可用, 可以非常方便的查看函数和宏定义.
- 可以使用eclipse去编译, 设置一个 `modules` 目标就可以了.


# Eclipse交叉编译说明

这个方法的核心是不用Eclipse自己的编译工具链. 所有的编译工具都由Makefile内指定了.
所以, 这个也适用于编译查看u-boot源码.
如果是应用层代码, 那么就需要自己写Makefile指定编译工具了.
另外一个方法是, 另外下载一个 `Eclipse IDE for C/C++`, 单独为应用层代码配置一个环境.



可参考:
- [Linux下搭建树莓派交叉编译环境](http://www.linuxidc.com/Linux/2016-09/135062.htm)
- [Linux + Eclipse 配置交叉编译环境](http://www.cnblogs.com/lazygunner/archive/2011/11/30/2269726.html)
- [配置eclipse linux嵌入式 集成开发环境（编译部分）详细](http://blog.csdn.net/tianzhihen_wq/article/details/41872365)
- [eclipse在windows下的arm交叉编译环境搭建](http://m.itboth.com/d/BzIRZz/windows-eclipse-arm)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***