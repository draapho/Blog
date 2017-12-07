---
title: 基于DHCP建立嵌入式Linux开发环境
date: 2017-11-28
categories: embedded linux
tags: [linuxembedded linux, env]
---


# 总览

- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [嵌入式linux环境搭建-主机端](https://draapho.github.io/2017/02/16/1705-linux-env/)
- [嵌入式linux环境搭建-jz2440开发板](https://draapho.github.io/2017/02/21/1707-jz2440-env/)
- [基于DHCP建立嵌入式Linux开发环境](https://draapho.github.io/2017/11/28/1738-dhcp-env/)

之前的环境搭建都是基于静态IP的. 但有些网络不方便设置静态IP, 而必须使用动态IP.
针对这种情况, 介绍一下Windows主机, Ubuntu主机, 以及开发板全部使用DHCP动态IP的方法.

# 主机端
Ubuntu安装好后, 默认就是dhcp分配动态IP地址.
那么在windows端的Putty, 我们需要使用Ubuntu的hostname, 而不是其IP地址即可.

方法很简单. Ubuntu的bash终端下面
``` bash
$ hostname
ubuntu

# 或者
$ uname -n
ubuntu
```

Windows下查看主机名
我的电脑->属性, `电脑名称`就是主机名
或者cmd终端下面, 输入 `ipconfig -all`
第一行就是 `Host Name`.

这样putty端直接使用 `hostname` 或者 `user@hostname` 就可以使用ssh远程登录了.


# 开发板DHCP

开发板要支持dhcp比较复杂一点. 
基本思路如下:
- 嵌入式linux启动后, 自动启动dhcp联网.
- 嵌入式linux安装nfs client, 挂载Ubuntu上的nfs文件.
- 内核和文件系统需要烧录到开发板.
- 此方法适用于开发驱动和应用层软件. 
- 新版本的uboot肯定支持dhcp, 但老版本的不确定, 不去吃螃蟹了.
- 有兴趣的参考 [
Using DHCP Client in U-Boot for Loading Linux Images via Network](https://www.emcraft.com/som/using-dhcp)

## 编译内核

首先需要内核支持更多的网络特性.

``` bash
# pwd = linux-2.6.22.6
cp config_ok .config
make menuconfig

# 进行如下配置
Networking  --->    
    [*] Networking support         
        Networking options  --->             
        <* > Packet socket                 # 使能CONFIG_PACKET, socket包           
        [ * ]     IP: DHCP support         # 使能DHCP           
        [ * ] Network packet filtering framework (Netfilter)  --->  # 使能 
        # 后面子选项可不选
# 保存并退回到终端

make clean
make uImage
```

然后烧录新的内核到开发板. 
- 内核的编译和烧录可参考 [kernel之编译体验](https://draapho.github.io/2017/09/01/1722-kernel-compile/)
- 如果内核没有支持上述特性, 后面执行udhcpc时会报错: `Address family not supported by protocol`

## ~~编译Busybox~~

jz2440提供的文件系统包含udhcpc命令, 所以不用重新配置编译了. 
**可跳过此步骤**.


如果要自己做, 注意勾选下面的选项(有的版本默认支持dhcp指令)

``` bash
Busybox Settings  --->  
    Busybox Library Tuning  ---> 
    [*]   Tab completion                # 指令自动填充, 非常必要的属性, 默认关闭...
        
Networking Utilities  --->           
    [] udhcp Server (udhcpd)            # 在此不作服务端，故不选。生成udhcpd命令    
    [*] udhcp Client (udhcpc)           # 生成udhcpc命令   
```

针对嵌入式系统, 由于是交叉编译, Busybox编译和安装有特别的要求, 可参考:
- [fs之BusyBox的使用与编译](https://draapho.github.io/2017/11/02/1730-fs-busybox/)

## 完善文件系统

自己构建文件系统也很麻烦. 可以参考 [fs之创建文件系统](https://draapho.github.io/2017/11/03/1731-fs-build/)


我是基于jz2440提供的 `fs_mini_mdev` 修改后, 使其支持dhcp的
busybox包含的udhcpc没有提供运行脚本, 直接运行会报错:
`udhcpc: exec /usr/share/udhcpc/default.script: No such file or directory`


因此对整个文件系统的改造有如下步骤
- 建立udhcpc要用的default.script
- 加入可执行属性
- 启动自动执行udhcpc指令

``` bash
# pwd = fs_mini_mdev_dhcp/

mkdir -p ./usr/share/udhcpc/     # 自动建立多层目录
vim ./usr/share/udhcpc/default.script

# ===== 打开vim, 写入如下内容 =====
#!/bin/sh
[ -z "$1" ] && echo "Error: should be called from udhcpc" && exit 1

RESOLV_CONF="/etc/resolv.conf"
[ -n "$broadcast" ] && BROADCAST="broadcast $broadcast"
[ -n "$subnet" ] && NETMASK="netmask $subnet"
 
case "$1" in
  deconfig)
    /sbin/ifconfig $interface 0.0.0.0
    ;;
 
  renew|bound)
    /sbin/ifconfig $interface $ip $BROADCAST $NETMASK
 
    if [ -n "$router" ] ; then
      echo "deleting routers"
      while route del default gw 0.0.0.0 dev $interface ; do
        :
      done
 
      for i in $router ; do
        route add default gw $i dev $interface
      done
    fi
 
    echo -n > $RESOLV_CONF
    [ -n "$domain" ] && echo search $domain >> $RESOLV_CONF
    for i in $dns ; do
      echo adding dns $i
      echo nameserver $i >> $RESOLV_CONF
    done
    ;;
esac
 
exit 0
# ===== wq保存文件, 退出 =====

chmod +x ./usr/share/udhcpc/default.script       # 加入可执行属性

vim ./etc/init.d/rcS             # 开机自动执行udhcpc. S是大写!
# ===== 打开vim, 修改/增加如下内容 =====
# ifconfig eth0 192.168.1.17
ifconfig eth0 up
udhcpc eth0
# 上述两行放在最前面. 这样才能成功自动挂载nfs

# ===== wq保存文件, 退出 =====


vim ./etc/fstab
# ===== 打开vim, 增加如下内容 =====

# 文件最后加入这样一句nfs模板, 便于日后修改
# 192.168.1.111:/home/share /mnt/share nfs rsize=1024,wsize=1024,timeo=14,intr,nolock 0 0
# ===== wq保存文件, 退出 =====



# 制作文件系统
# pwd = fs_mini_mdev_dhcp/..
mkyaffs2image fs_mini_mdev_dhcp fs_mini_mdev_dhcp.yaffs2
```

上述工作完成后, 烧录到开发板即可. 详情可参考:[fs之创建文件系统](https://draapho.github.io/2017/11/03/1731-fs-build/)


## 开发板测试
烧录好内核和文件系统后, 开机测试一下.
注意, udhcpc比较傻, 如果不能联网, 开机就会死在 `Sending discover...`
成功启动后, 使用 `ifconfig` 就可以看到dhcp自动分配的ip地址了.


所以也有人用别的方式实现dhcp. 我没有尝试, 列在这里供参考
- [成功移植DHCP客户端到mini2440](http://www.linuxidc.com/Linux/2011-05/36038.htm), 用的 dhclient 指令
- [jz2440自动获取ip地址](https://wenku.baidu.com/view/bca0c470e418964bcf84b9d528ea81c758f52ed1.html), 源码编译udhcpc, 估计里面会有 default.script 文件.


# 开发板挂载nfs

主机端 nfs环境搭建参考: [Ubuntu 16.04安装配置NFS](https://draapho.github.io/2017/11/29/1739-ubuntu-nfs/)


在开发板上挂载服务器共享的目录
``` bash
# pwd = / 
$ mkdir mnt/share          # 挂载点
$ ln -s mnt/share share    # 创建软连接

$ mount -t nfs -o nolock 192.168.1.100:/home/share /mnt/share/
$ df -h                     # 查看挂载的文件系统.
$ ls share                  # 查看一下是否可以看到共享内容了.
```


每次开机敲一长串 mount 指令也挺麻烦的, 进一步偷懒, 让它开机自启动.
``` bash
# 开发板终端, 修改fstab, 让 mount -a 自动加载nfs
$ vi /etc/fstab
# ===== 打开vi, 修改/增加如下内容 =====
192.168.1.111:/home/share /mnt/share nfs rsize=1024,wsize=1024,timeo=14,intr,nolock 0 0
# ===== wq保存文件, 退出 =====

$ mount -a                  # 重新加载
$ df -h                     # 查看挂载的文件系统.
$ ls share                  # 查看一下是否可以看到共享内容了.
```

下次重启就能自动加载nfs了. **如果加载失败, 看看是不是主机动态IP变掉了**.
jz2440启动后, 加载nfs失败时, 需要等待一段时间才能进入终端界面! 

## 使用hostname
这里, 最理想的情况是使用 hostname 而不是IP地址.
但网上搜索了一下, 没有找到让jz2440支持hostname的方法.
动态IP也不会更换的太频繁, 所以是一个可以忍受的缺点, 就不去深究了.
关键点是 `/etc/resolv.conf`, 应该可以由udhcpc自动生成内容的...
找了如下相关信息:
- [linux根文件系统 /etc/resolv.conf 文件详解](http://blog.csdn.net/mybelief321/article/details/10049429)
- [linux系统2440开发板域名解析问题](http://www.voidcn.com/article/p-yruxiyxx-nk.html)
- [JZ2440开发笔记（4）——设置静态IP](http://www.cnblogs.com/zjzsky/p/3559367.html)



# 参考资料
- [ubuntu永久修改主机名](http://blog.csdn.net/ruglcc/article/details/7802077)
- [BusyBox 應用 – udhcpc](http://felix-lin.com/linux/busybox-%E6%87%89%E7%94%A8-udhcpc/)
- [jz2440自动获取ip地址](https://wenku.baidu.com/view/bca0c470e418964bcf84b9d528ea81c758f52ed1.html)
- [Linux NFS Mount Entry In fstab ( /etc/fstab ) With Example](https://linoxide.com/file-system/example-linux-nfs-mount-entry-in-fstab-etcfstab/)
- [ubuntu下 mini2440的NFS挂载【终极版】](http://blog.sina.com.cn/s/blog_76c545390100sscr.html)

----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***
