---
title: 嵌入式linux环境搭建1-Ubuntu14.04
date: 2017-02-18
categories: embedded linux
tags: [embedded linux, environment]
---


# 环境及结论

- 大环境的搭建思路可参考[嵌入式linux环境搭建-主机端](https://draapho.github.io/2017/02/16/1705-linux-env/)
  - gateway ip `10.0.0.138`
  - PC windows: win10 64bit, ip `10.0.0.98`
  - PC linux(最终版本): ubuntu server 16.04 32 bit, ip `10.0.0.100`
  - Embedded Linux: jz2440v3 ip `10.0.0.111`
- 探索嵌入式linux环境搭建的各方案可行性.
- 使用环境: Ubuntu 14.04.5 LTS 32bit 桌面版 (安装在win10的虚拟机内)
- 成功验证了win10作为NFS服务器. 两个linux作为NFS客户端, 三者文件共享的方案
- 最终遇到了gcc编译器的坑, 就决定换到CentOS系统练练手.
- 在win 10 下使用虚拟机安装在win10下, 略过不表.
- 实验结论:
  - win10(非企业版)下, 没有找到nfs客户端. 因此没法使用 **ubuntu做NFS服务器** 的方案
  - ubuntu下安装samba来支持windows文件共享, 失败告终. 因此没法使用 **ubuntu使用samba来支持windows文件共享** 的方案
  - linux不允许把NFS挂载过来的文件再使用NFS服务共享出去. 因此没法使用 **交叉使用上述方案**
  - 还好, 最终 **windows做NFS服务器** 成功了

# 安装必要的软件

``` bash
# 查看 make 和 gcc 工具 (非交叉编译用)
make -v                     # GNU Make 3.81
gcc -v                      # gcc version 4.8.4
```


# 设置静态IP
个人更喜欢用静态IP, 这样putty的设置更直观方便.
如果要使用动态IP, 可以设置 windwos 的 HaneWIN, 用`-range`来指定nfs客户端的网址段

刚开始怎么样都不能上外网, 突然按照下面的顺序就好了... 原因不明
``` bash
sudo vim /etc/network/interfaces
    # ===== 文件内容, 大致修改如下: =====
    auto lo
    iface lo inet loopback

    auto eth0

    iface eth0 inet static
    address  10.0.0.100
    netmask  255.255.255.0
    gateway  10.0.0.138
    dns-nameservers   8.8.8.8  10.0.0.138
    # ===== 结束修改, 保存退出vim =====

sudo reboot
```

# 安装nfs服务(服务器/客户端)

最终方案里, windows下用了HaneWIN 做NFS服务器, 虚拟机ubuntu下安装客户端就可以了.
这里为了做实验, nfs服务器和客户端都安装了, 可以参考:
[How To Set Up an NFS Mount on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-14-04)


## nfs 客户端的安装

``` bash
# 安装 nfs 客户端软件
sudo apt-get update
sudo apt-get install nfs-common

# 建立空文件夹用于挂载nfs
sudo mkdir -p /mnt/nfs/study
sudo mkdir -p /mnt/nfs/work

# 开机自动挂载(参考文章中的客户端自动挂载方法没有起作用)
sudo vim /etc/rc.local
    # ===== 文件内容, 加入如下两句 =====
    sudo mount 10.0.0.98:/study /mnt/nfs/study
    sudo mount 10.0.0.98:/work /mnt/nfs/work
    # ===== 结束修改, 保存退出vim =====

# 建立软连接(快捷方式), 可忽略此步骤
sudo ln -s /mnt/nfs/study /home/user/study
sudo ln -s /mnt/nfs/work /home/user/work
```

## ~~nfs 服务器的安装~~

实际上没有用到linux的nfs服务器功能, 最终用的是windows下的HaneWIN给开发板提供的nfs服务!!!
因为最后测试下来, **linux不允许把NFS挂载过来的文件再使用NFS服务共享出去**.

``` bash
# 虚拟机ubuntu 安装服务器, 供开发板端使用nfs.
apt-get install nfs-kernel-server
sudo vim /etc/exports
    # ===== 文件内容, 末尾加入如下语句 =====
    # 加入要共享的文件夹, 一个文件夹一行即可
    # 注意! 由windows 共享过来的目录无法再由ubuntu共享出去
    /home/draapho 10.0.0.*(rw,no_root_squash,async,no_subtree_check)
    # ===== 结束修改, 保存退出vim =====

# 重启服务
sudo exportfs -a
sudo /etc/init.d/nfs-kernel-server restart
```

## ~~其它实验~~
win10(非企业版)下, 没有找到nfs客户端. 因此无法让linux当nfs服务器, win10做nfs客户端.
ubuntu下安装samba来支持windows文件共享, 失败告终


# 安装ssh服务, 用putty远程登录

``` bash
# 安装ssh服务
sudo apt-get update
sudo apt-get install openssh-server
# 如果有依赖包冲突, 执行如下指令
sudo apt-get install openssh-client=1:6.6p1-2ubuntu1

# 查看是否已经运行
sudo ps -e | grep ssh
# 启动服务
sudo service ssh start
```

# 安装 u-boot-tools 工具

安装 u-boot-tools, 内核编译后生成uImage使用.
``` bash
# 安装 mkimage
sudo apt-get install u-boot-tools
# 验证
mkimage -V
```


# 安装 mkyaffs2image 工具

该工具用于制作文件系统镜像文件
文件系统烧录到开发板flash时需要使用镜像文件

``` bash
sudo cp mkyaffs2image /bin/                         # 拷贝到bin
sudo chmod +x /bin/mkyaffs2image                    # 增加可执行权限
mkyaffs2image                                       # 测试是否可用
```


# 安装及使用交叉编译工具gcc

在 arm-linux-gcc 4.3.2 上走的比较远, 结果证明遇到坑了!
建议不要尝试最新版本的编译器, 老老实实使用开发板提供的 `gcc-3.4.5-glibc-2.3.6` 编译器版本.

## ~~安装 arm-linux-gcc 4.3.2~~
``` bash
# 直接拷贝解压 arm-linux-gcc-4.3.2.tar.bz2
# 事后证明, gcc-4.3.2 不能正确编译(但能成功编译)2440的linux内核和驱动
sudo tar xjvf arm-linux-gcc-4.3.2.tar.bz2 -C /usr/local/

# 添加路径到环境变量
sudo vim /etc/bash.bashrc
    # ===== 文件内容, 末尾加入如下语句 =====
    if [ -d /usr/local/arm/4.3.2 ] ; then
        PATH=/usr/local/arm/4.3.2/bin:"${PATH}"
    fi
    # ===== 结束修改, 保存退出vim =====

# 测试安装结果
source /etc/bash.bashrc                             # 不重启更新PATH
echo $PATH                                          # 查看PATH
arm-linux-gcc -v                                    # 测试是否安装成功
```


如果希望sudo超级账户也能用 make 指令 (没有测试过)

``` bash
sudo -s                                             # 登录超级账户
vi /etc/profile                                     # 打开profile
    # ===== 文件内容, 末尾加入如下语句 =====
    export PATH=$PATH:/usr/local/arm/4.3.2/bin
    # ===== 结束修改, 保存退出vim =====
```

## ~~遇到问题并解决, 结果是坑~~

下面列出使用 `arm-linux-gcc 4.3.2` 编译u-boot遇到问题时的解决方法
所谓顺利, 是因为没有报错, 生成的文件可以烧录, 启动.
加上引号, 是因为最后证明这些生成文件是有问题的, 会导致整个嵌入式系统某些部分无法正常工作.
最后在编译测试驱动用的C文件时, 编译出来的可执行文件在开发板上不可执行,
才想到可能是编译器问题而尝试着换回到 3.4.5 版本. 并连同内核全部重新编译了.
换回去后, 之前一度认为的源码有问题的fs也能成功加载了, 真是个巨坑...

``` bash
# 如果用gcc 4.3.2, 则版本太新, 编译错误. 可以使用自带的arm-none-linux-gnueabi
# 解决方法如下:
# 修改Makefile文件中的PLATFORM_LIBS, 将:
PLATFORM_LIBS += -L $(shell dirname `$(CC) $(CFLAGS) -print-libgcc-file-name`) -lgcc
# 修改成:
PLATFORM_LIBS += -L $(shell dirname `$(CC) $(CFLAGS) -print-libgcc-file-name`) -lgcc -lc -L /usr/local/arm/4.3.2/arm-none-linux-gnueabi/libc/armv4t/usr/lib

# 修改 cpu /arm920t/config.mk 文件, 将:
PLATFORM_CPPFLAGS +=$(call cc-option,-mapcs-32,-mabi=apcs-gnu)
PLATFORM_RELFLAGS +=$(call cc-option,-mshort-load-bytes,$(call cc-option,-malignment-traps,))
# 修改成:
PLATFORM_CPPFLAGS +=$(call cc-option,)
PLATFORM_RELFLAGS +=$(call cc-option,$(call cc-option,))

# 重新make, 即可生成 u-boot.bin
```


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***