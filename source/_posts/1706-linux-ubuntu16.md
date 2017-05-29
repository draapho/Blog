---
title: 嵌入式linux环境搭建3-Ubuntu16.04
date: 2017-02-20
categories: embedded linux
tags: [embedded linux, environment]
---



# 环境及结论

- 大环境的搭建思路可参考[嵌入式linux环境搭建](https://draapho.github.io/2017/02/16/1705-linux-env/)
  - gateway ip `10.0.0.138`
  - PC windows: win10 64bit, ip `10.0.0.98`
  - PC linux(最终版本): ubuntu server 16.04 32 bit, ip `10.0.0.100`
  - Embedded Linux: jz2440v3 ip `10.0.0.111`
- 使用环境: Ubuntu server 16.04 32bit (安装在win10的虚拟机内)
- 在经历了两次失败后, 成功搭建了整个环境. 服务器版去掉了UI, 给虚拟机用很好.
- 补充一点, 刚开始用的是 ubuntu server 16.04 64 bit, 也遇到点问题.
  由于是要做交叉编译的开发环境, 所以 PC linux 和 embedded linux 用一样的带宽才好.


# apt-get使用摘要
- 软件升级: `sudo apt-get update`
- 普通安装: `apt-get install softname1 softname2 ...`
- 修复安装： `apt-get -f install softname1 softname2...`  (-f Atemp to correct broken dependencies)
- 重新安装： `apt-get --reinstall install softname1 softname2...`
- 移除式卸载(保留配置)： `apt-get remove softname1 softname2 ...`
- 清除式卸载(删除配置)： `apt-get --purge remove softname1 softname2...`
  或 `apt-get purge sofname1 softname2...`


# 安装必要的软件

``` bash
# 安装 make
sudo apt-get install make
make -v                     # GNU Make 4.1

# 安装gcc, 非交叉编译用
sudo apt-get install gcc
gcc -v                      # gcc version 5.4.0

# 设置时区
sudo dpkg-reconfigure tzdata
```


# ~~安装32bit兼容库~~

不要安装 64bit 的ubuntu作为交叉编译的linux环境. 我最后换回到了32bit

``` bash
sudo apt-get install ia32-libs      # 提示不可用, 替代方案如下
sudo apt-get install lib32ncurses5
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

# 可装完ssh服务再重启. 然后验证putty是否可用.
sudo reboot
```


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

# 重启后, 验证是否能用putty功能
sudo reboot
```


# nfs 客户端的安装

参考: [How To Set Up an NFS Mount on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-14-04)

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
cd /home/user/
sudo ln -s /mnt/nfs/study study
sudo ln -s /mnt/nfs/work work
```


# 安装交叉编译工具gcc

老老实实使用开发板提供的 `gcc-3.4.5-glibc-2.3.6` 编译器版本.

``` bash
# 直接拷贝解压 gcc-3.4.5-glibc-2.3.6.tar.bz2
sudo tar xjf arm-linux-gcc-3.4.5-glibc-2.3.6.tar.bz2 -C /usr/local/

# 添加路径到环境变量
sudo vim /etc/bash.bashrc
    # ===== 文件内容, 末尾加入如下语句 =====
    if [ -d /usr/local/gcc-3.4.5-glibc-2.3.6 ] ; then
        PATH=/usr/local/gcc-3.4.5-glibc-2.3.6/bin:"${PATH}"
    fi
    # ===== 结束修改, 保存退出vim =====

# 测试安装结果
source /etc/bash.bashrc                             # 不重启更新PATH
echo $PATH                                          # 查看PATH
arm-linux-gcc -v                                    # 测试是否安装成功
```


# 安装 u-boot-tools 工具

安装 u-boot-tools, 内核编译后生成uImage使用.
``` bash
# 安装 mkimage
sudo apt-get install u-boot-tools
# 验证
mkimage -V              # mkimage version 2016.01+dfsg1-2ubuntu1
```


# 安装 mkyaffs2image 工具

该工具用于制作文件系统镜像文件
文件系统烧录到开发板flash时需要使用镜像文件

``` bash
sudo cp mkyaffs2image /bin/                         # 拷贝到bin
sudo chmod +x /bin/mkyaffs2image                    # 增加可执行权限
mkyaffs2image                                       # 测试是否可用
```


----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***