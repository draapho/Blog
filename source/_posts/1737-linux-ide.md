---
title: LinK+, 一款Linux内核开发IDE
date: 2017-11-27
categories: embedded linux
tags: [linuxembedded linux, ide]
---


# 前言
LinK+ 是一款在linux下基于eclipse开发的免费的Linux内核以及驱动开发软件.
和大名顶顶的 Source Insight 相比, 只有优点, 没有缺点!
可惜的是, 这个软件在国外知名度也不高. 国内更是没人介绍过这一款软件.

软件的现状是: 开发者似乎已经停止更新, 设想中支持的ARM架构也没有下文. 因此不支持嵌入式的编译和仿真.
好再我的主要目标就是方便的阅读源码, 找到函数调用关系, 这些都是eclipse的强项, 无需担心.

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
# 下载好LinK+IDE的文件, LinK+IDE-linux.gtk.x86.tar.gz.tar.gz
tar –xzvf LinK+IDE-linux.gtk.x86.tar.gz.tar.gz
./linkplus
# 安装成功的话, 就能运行了.
```

然后, LinK+IDE 的升级和插件不用看了. 很久没更新过了.

# 阅读源码
- 将嵌入式内核源码先编译好.
- LinK+IDE里, 新建工程->Linux Kernel Development(LinK+)
- 选择 Kernel Compilation Project
- 写入项目名称, 选择 `Link to Existing Kernel Source Code`, 然后选择内核源码目录.
- 架构就选x86吧. ARM不支持的.
- 完成以后, 似乎宏定义部分有问题, 大多数的函数跳转就能直接用了.

# 写驱动
- LinK+IDE里, 新建工程->Linux Kernel Development(LinK+)
- 选择 Device Driver Project
- 写好驱动名称, 驱动路径, 作者, 开源证书类型
- Kernel Version 要去掉 `Use Host Machine Kernel`, 选择我们已经编译好的嵌入式内核源码路径
- X86架构 (ARM不支持), 
- 下面两步可以根据需求自己选择驱动框架, LinK+会自动生成有框架的.c和.h文件.
- 驱动下面, 所有的跳转都可用, 包括宏定义.
- 完美!

----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***
