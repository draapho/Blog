---
title: Yocto 的安装与体验
date: 2017-12-15
categories: embedded linux
tags: [linuxembedded linux, yocto]
description: 如题.
---

# 前言

Yocto的简介就不抄写了, 反正我光看介绍并不明白Yocto到底是干吗的.
但应该确确实实让定制和开发嵌入式Linux系统变得更方便, 招聘要求里会Yocto都是加分项.
所以决定动手实践一下, 先有个感性认识再说.

下文基本按照官网的 [Yocto Project Quick Start](https://www.yoctoproject.org/docs/current/yocto-project-qs/yocto-project-qs.html) 步骤而来.

# 第一步, 安装 Yocto Project

安装 Yocto Project 有两个方法:
- 使用 CROPS (CROss PlatformS), 直观的说, 就是基于Docker平台进行安装
    - 我并没有采用这种方法, 因为手头已经有现成的Ubuntu系统了
    - Docker相关内容, 可以参考我的笔记 [Docker 初学笔记](https://draapho.github.io/2017/02/23/1708-docker/)
- 第二个方法就是基于Linux系统安装
    - 此文基于 Ubuntu 16.04 32bit 桌面版
    - 基本要求: 50G的硬盘空间, 建议预留100G
    - 支持主流Linux系统, 如 Fedora, CentOS, Debian, Ubuntu
    - Git 1.8.3.1或以上版本
    - tar 1.27或以上版本
    - python 3.4.0或以上版本


``` bash
# Ubuntu, 安装软件
$ sudo apt-get update
$ sudo apt-get install gawk wget git-core diffstat unzip texinfo gcc-multilib \
    build-essential chrpath socat cpio python python3 python3-pip python3-pexpect \
    xz-utils debianutils iputils-ping libsdl1.2-dev xterm

# 确认一下软件版本
$ git --version
git version 2.7.4
$ tar --version
tar (GNU tar) 1.28
$ python3
Python 3.5.2
>>> exit()

# 如果没有装好, 可单独安装
$ sudo apt install git
$ sudo apt install tar
$ sudo apt install python3
```

这样就准备好了安装环境. 然后安装 Yocto Project

``` bash
# 创建一下yocto目录, 整个项目就放在此目录下面
$ mkdir ~/yocto
$ cd ~/yocto

# git获取工程
$ git clone git://git.yoctoproject.org/poky
...
Checking connectivity... done.

# 下载完成后, 有个poky文件夹.
# 如果是从别处下载再拷贝进Ubuntu的, 可能需要改个权限
# 因为后面的bitbake命令不允许已root用户操作.
$ sudo chmod -R +777 poky/
```


# 第二步, 定制Linux镜像文件

安装好 Yocto Project 后, 就需要体验一把定制Linux镜像

```
# pwd = ~/yocto/poky/

# 创建一个git分支, 基于此分支制作自己的Linux镜像
$ sudo git checkout -b rocko origin/rocko
$ git branch
  master
* rocko

# 执行脚本, 创建了一些默认配置
$ source oe-init-build-env
You can now run 'bitbake <target>'
Common targets are:
    core-image-minimal
    core-image-sato
    meta-toolchain
    meta-ide-support
# 显示后续操作的说明, 并自动进入 build 目录

# pwd = ~/yocto/poky/build
$ ls conf/
# 三个.conf文件, 教程简单介绍了一下 local.conf 里的 MACHINE 和 PACKAGE_CLASSES
$ vim conf/local.conf
# 看一下配置文件, 有个直观感受. 先用默认值, 不去修改

$ bitbake core-image-sato
# 第一次的话, 会非常非常慢, 下载源码加编译, 可能花费几个小时...

# 烘焙(bitbake)好image后, 在虚拟环境QEMU下看看效果
$ runqemu qemux86
```

至此, 体验完成. 实际硬件环境的流程基本一致, 就是还要考虑烧录和启动的问题.
这是嵌入式Linux开发的基本能力, 略过不表.


# ~~一些弯路~~

第一个弯路是python版本问题, 造成安装软件失败
直接运行python, 默认是2.7. 然后想着需要改成3.5版本的.
按照网上教程, 修改python软链接, 但会导致apt安装软件失败.
原因是有些软件依赖于python2.7, 改为3.5后, 安装过程会发生语法错误.
具体可参考 [linux软件的安装和管理](https://draapho.github.io/2017/11/26/1736-linux-apt/) 的 `X not fully installed or removed`

``` bash
$ ll /usr/bin/python*
lrwxrwxrwx 1 root root       9 Nov 24 07:18 /usr/bin/python -> python2.7*
$ sudo rm /usr/bin/python
$ sudo ln -s /usr/bin/python3.5 /usr/bin/python
$ ll /usr/bin/python*
lrwxrwxrwx 1 root root       9 Nov 24 07:18 /usr/bin/python -> python3.5*
$ python
Python 3.5.2 (default, Nov 23 2017, 16:37:01)

# 这样改完以后, 再去安装 libsdl1.2-dev 会报错! 解决方法是改回来...
```

第二个弯路是安装虚拟机的时候, 只给了20G的空间. 扩盘的方法如下:
[扩大Vmware虚拟机中Ubuntu系统磁盘空间的方法](https://lzw.me/a/vmware-ubuntu-disk-space.html), 建议直接用可视化的软件

```
$ sudo apt install gparted
$ sudo gparted

# 重启后自动挂载, 可以格式化并重命名为 extend
# 自动挂载路径为 /media/user-name/extend, 没有重命名的话, 是一长串ID
$ sudo chmod +777 /media/draapho/extend
$ sudo ln -s /media/draapho/extend ~/share/extend
# 改下权限, 建立软连接方便操作.
# 由于空间要求, yocto项目就放在这个盘里面.
```





# 参考资料
- [Yocto Project Quick Start](https://www.yoctoproject.org/docs/current/yocto-project-qs/yocto-project-qs.html)
- [使用 Yocto Project 构建自定义嵌入式 Linux 发行版](https://www.ibm.com/developerworks/cn/linux/l-yocto-linux/index.html)
- [在MIPS平台上如何使用Yocto框架来定制嵌入式Linux发行版](http://www.sohu.com/a/134506616_468740), 里面有个视频, 介绍了yocto的好处
- [基于Yocto Project的嵌入式应用设计](http://www.eeskill.com/article/id/2761)