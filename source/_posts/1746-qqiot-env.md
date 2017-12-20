---
title: 嵌入式linux环境搭建-QQ物联
date: 2017-12-18
categories: embedded linux
tags: [linux, embedded linux]
---

# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [嵌入式linux环境搭建-QQ物联](https://draapho.github.io/2017/12/18/1746-qqiot-env/)
- [QQ物联基础概念及绑定分析](https://draapho.github.io/2017/12/20/1747-qqiot-conception/)

为学习QQ物联而搭建的jz2440开发环境.
需要升级交叉编译环境, 然后编译和烧录
使用如下软件版本:
- u-boot-1.1.6
- linux-3.4.2
- arm-linux-gcc-4.3.2


另可参考:
- [嵌入式linux环境搭建-主机端](https://draapho.github.io/2017/02/16/1705-linux-env/), 搭建Ubuntu开发环境
- [嵌入式linux环境搭建-jz2440开发板](https://draapho.github.io/2017/02/21/1707-jz2440-env/), 基于2.6.22内核的编译和烧录
- [基于DHCP建立嵌入式Linux开发环境](https://draapho.github.io/2017/11/28/1738-dhcp-env/), 修改jz2440的内核和文件系统以支持DHCP


# 安装交叉编译工具链

新的linux内核需要用 arm-linux-gcc-4.3.2 这个版本的交叉编译.
对已安装的arm-linux-gcc-3.4.5, 无需删除, 但需要从环境变量中去除.
因此整个过程需要安装新软件, 重新设置一下Ubuntu的环境变量

``` bash
# ubuntu shell

# 直接拷贝解压 arm-linux-gcc-4.3.2.tar.bz2, 提供的压缩包包含了路径 /usr/local/arm/4.3.2
$ sudo tar xjf arm-linux-gcc-4.3.2.tar.bz2 -C /
# 添加路径到环境变量, 记得去掉 gcc-3.4.5-glibc-2.3.6
$ sudo vim /etc/bash.bashrc
    # ===== 文件内容, 末尾加入如下语句 =====
    # if [ -d /usr/local/gcc-3.4.5-glibc-2.3.6 ] ; then
    #   PATH=/usr/local/gcc-3.4.5-glibc-2.3.6/bin:"${PATH}"
    # fi
    if [ -d /usr/local/arm/4.3.2 ] ; then
        PATH=/usr/local/arm/4.3.2/bin:"${PATH}"
    fi
    # ===== 结束修改, 保存退出vim =====
# 如果直接修改 /etc/environment 文件也可以.

# 测试安装结果
$ source /etc/bash.bashrc                           # 不重启更新PATH
$ echo $PATH                                        # 查看PATH
$ arm-linux-gcc -v                                  # 测试是否安装成功
gcc version 4.3.2
```

# uboot的编译和烧录

## 编译uboot

``` bash
# ubuntu shell

tar xjvf u-boot-1.1.6.tar.bz2               # 解压uboot源码
cd u-boot-1.1.6                             # 进入uboot源码目录
patch -p1 < ../u-boot-1.1.6_20161226_all.patch 
make clean
make 100ask24x0_config                      # uboot config文件
make                                        # uboot 编译, 得到u-boot.bin文件
```

## 烧录uboot

``` bash
# 开发板 uboot
# 打开 jz2440 开发板串口终端, 启动时输入空格键, 进入如下菜单
##### 100ask Bootloader for OpenJTAG #####
[n] Download u-boot to Nand Flash
...
Enter your selection: n / o                 # 输入n 或者 o, 烧录uboot
USB host is connected. Waiting a download.  # 提示连接成功

# 切换到 Ubuntu 终端, 输入
# pwd = ./u-boot-1.1.6                      # 确保在 uboot 源码路径下
sudo dnw u-boot.bin                         # 使用dnw烧录uboot
```

## 设置uboot

如果希望通过uboot直接加载nfs文件系统, 还需进行如下设置

``` bash
# 开发板 uboot
# 设置ip地址, 在OpenJTAG> 提示符下
set ipaddr 10.0.0.111           # 设置开发板的ip地址
set serverip 10.0.0.138
save                            # 保存
printenv                        # 打印环境变量, 查看设置结果

set bootargs noinitrd root=/dev/nfs nfsroot=10.0.0.98:/fs ip=10.0.0.111:10.0.0.98:10.0.0.138:255.255.255.0::eth0:off init=/linuxrc console=ttySAC0
# (简化ip: 'set bootargs noinitrd root=/dev/nfs nfsroot=10.0.0.98:/fs ip=10.0.0.111 init=/linuxrc console=ttySAC0' 也可以工作)
save        # 保存修改
reset       # 重启. (稍后再重启, 先修改好 filesystem 内的初始化文件)
# 参数简要说明:
# 'root=/dev/nfs' 加载nfs文件系统
# 'nfsroot=10.0.0.98:/fs' nfs文件系统的来源, 此处是由win10当nfs服务器, 共享出/fs文件夹
# 'ip=10.0.0.111:10.0.0.98:10.0.0.138:255.255.255.0::eth0:off' 分别表示:
#  ip= 开发板ip : nfs服务器ip: 网关ip : 子网掩码 :: 开发板网口 : off
```

# kernel的编译和烧录

## 编译kernel

``` bash
# ubuntu shell

tar xjvf linux-3.4.2.tar.bz2                # 解压kernel源码
cd linux-3.4.2                              # 进入kernel源码目录
patch -p1 < ../linux-3.4.2_20161226_all.patch  # 打补丁文件, p1表忽略patch文件内的1层目录

make clean                                  # 清空 (先清空再在SI内查看)
cp config_jz2440 .config                    # 设置config文件, 此配置文件已支持dhcp
make uImage                                 # 编译获得内核image
```

编译时, 遇到一个错误: `Can't use 'defined(@array)' (Maybe you should just omit the defined()?) at kernel/timeconst.pl line 373.`
参考 [Linux kernel 编译问题记录](http://sunyongfeng.com/201701/programmer/linux/kernel_compile_fail.html). 原因是perl版本升级了.
将 `if (!defined(@val))` 改为 `if (!@val)` 再次编译就可以了.


## 烧录kernel

``` bash
# 开发板 uboot
# 打开 jz2440 开发板串口终端, 启动时输入空格键, 进入如下菜单
##### 100ask Bootloader for OpenJTAG #####
[k] Download Linux kernel uImage
...
Enter your selection: k                     # 输入k, 烧录 kernel
USB host is connected. Waiting a download.  # 提示连接成功


# 切换到 Ubuntu 终端, 输入
# pwd = ./linux-2.6.22.6                    # 确保在 kernel 源码路径下
sudo dnw ./arch/arm/boot/uImage             # 输入dnw指令, 指明烧录文件
# DNW usb device found!                     # 开始烧录
```

# filesystem的制作和烧录

**注意**, QQ物联的应用, 文件系统必须烧录到nand flash中, 而不能采用NFS的方式加载.

## 制作 filesystem

``` bash
# ubuntu shell
sudo tar xjvf fs_mini_mdev_new_auto_wifi.tar.bz2        # 解压缩
mkyaffs2image fs_mini_mdev_new fs_mini_mdev_new.yaffs2  # 生成文件系统
```

## 烧录 filesystem

``` bash
# 开发板 uboot
# 打开 jz2440 开发板串口终端, 启动时输入空格键, 进入如下菜单
##### 100ask Bootloader for OpenJTAG #####
[y] Download root_yaffs image
...
Enter your selection: y                     # 输入k, 烧录 root_yaffs
USB host is connected. Waiting a download.  # 提示连接成功


# 切换到 Ubuntu 终端, 输入
sudo dnw fs_mini_mdev_new.yaffs2            # 输入dnw指令, 指明烧录文件
# DNW usb device found!                     # 开始烧录
# 这样就成功把文件系统烧录到 jz2440 开发板中了.
```

# ~~查看分区~~

- bootloader, 512k
- params, 128k
- kernel, 4m
- rootfs, 剩下的空间

``` bash
# 开发板 uboot, 进入命令行模式
> printenv
mtdparts=mtdparts=nandflash0:512k@0(bootloader),128k(params),4m(kernel),-(root)


# ubuntu端, kernel 源码下
$ vim arch/arm/mach-s3c24xx/common-smdk.c
# 查看 smdk_default_nand_part 可知分区情况
static struct mtd_partition smdk_default_nand_part[] = {
        [0] = {
                .name   = "bootloader",
                .size   = SZ_512K,
                .offset = 0,
        },
        [1] = {
                .name   = "params",
                .offset = MTDPART_OFS_APPEND,
                .size   = SZ_128K,
        },
        [2] = {
                .name   = "kernel",
                .offset = MTDPART_OFS_APPEND,
                .size   = SZ_4M,
        },
        [3] = {
                .name   = "rootfs",
                .offset = MTDPART_OFS_APPEND,
                .size   = MTDPART_SIZ_FULL,
        }
};
```


# 配置网络, 支持nfs

## 实现dhcp功能

为了正常使用udhcpc, 还需要对文件系统稍加修改. 如下工作即可以在开发板端做, 也可以先在文件系统上做好, 然后编译烧录进开发板

``` bash
# 开发板bash

# udhcpc需要一个脚本文件, 否则无法完整实现dhcp功能. (测试了一下, 这个版本没有脚本也不报错, 但无法正常使用!)
mkdir -p /usr/share/udhcpc/     # 自动建立多层目录
vi /usr/share/udhcpc/default.script
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
chmod +x /usr/share/udhcpc/default.script       # 加入可执行属性

# 然后测试一下
ifconfig eth0 up
udhcpc eth0
# 如果没有脚本文件, 只能获得IP地址, 没有dns的信息!
ifconfig
# 能看到IP地址, 广播地址, 子网掩码信息
ping 192.168.1.100
# 能ping通ubuntu主机
```

## 开机自动挂载nfs

要使用nfs, Ubuntu主机首先必须支持nfs. 主机端配置详情见 [Ubuntu 16.04安装配置NFS](https://draapho.github.io/2017/11/29/1739-ubuntu-nfs/)
使用 `ifconfig` 查看主机IP地址, `vim /etc/exports` 查看共享目录

``` bash
# jz2440开发板
vi /etc/init.d/rcS             # 开机自动执行udhcpc. S是大写!
# ===== 打开vim, 修改/增加如下内容 =====
#ifconfig eth0 192.168.1.17

ifconfig eth0 up
udhcpc eth0
# 上述两行放在最前面. 这样才能成功自动挂载nfs
# ===== wq保存文件, 退出 =====

vi /etc/fstab
# ===== 打开vim, 增加如下内容 =====
# 文件最后加入这样一句nfs模板, 便于日后修改
# 192.168.1.100:/home/draapho/share /mnt/share nfs rsize=1024,wsize=1024,timeo=14,intr,nolock 0 0
# ===== wq保存文件, 退出 =====

mkdir /mnt/share                # 创建挂载点
mount -a                        # 不重启挂载, 测试一下
```

# 编译并测试驱动模块

默认提供的驱动关联了 `/work/system/linux-3.4.2`作为内核关联.
另外, 可以把编译好的驱动拷贝到jz2440 flash中, 统一放在 `/lib/modules/3.4.2` 目录下面.

``` bash
# jz2440开发板
mkdir -p /lib/modules/3.4.2

# Ubuntu端firstdrvtest.c 
sudo mkdir -p /work/system/
firstdrvtest.c 
```

## LED驱动

``` bash
# Ubuntu端
# pwd = ./jz2440/first_drv                  # nfs共享文件
make
arm-linux-gcc firstdrvtest.c -o firstdrvtest


# jz2440开发板
# pwd = /mnt/share/.../jz2440/first_drv     # nfs共享文件
cp first_drv.ko /lib/modules/3.4.2/
ls /lib/modules/3.4.2/                      # 查看拷贝结果
insmod first_drv.ko
lsmod                                       # 列出已加载模块
./firstdrvtest on                           # 测试
./firstdrvtest off
```

## 按键驱动

``` bash
# Ubuntu端
# pwd = ./jz2440/7th_buttons_all                # nfs共享文件
make
arm-linux-gcc buttons_test.c -o buttons_test


# jz2440开发板
# pwd = /mnt/share/.../jz2440/7th_buttons_all   # nfs共享文件
cp buttons.ko /lib/modules/3.4.2/
ls /lib/modules/3.4.2/                          # 查看拷贝结果
insmod buttons.ko
lsmod                                           # 列出已加载模块
./buttons_test                                  # 测试
```


## LCD驱动

``` bash
# Ubuntu端
# pwd = ./jz2440/10th_lcd                       # nfs共享文件, 屏幕驱动
cp lcd_4.3.c lcd.c                              # jz2440, 用的4.3寸屏
make
# pwd = ./jz2440/fb_test                        # nfs共享文件, 屏幕测试
make


# jz2440开发板
# pwd = /mnt/share/.../jz2440/10th_lcd          # nfs共享文件, 屏幕驱动
cp lcd.ko /lib/modules/3.4.2/
ls /lib/modules/3.4.2/                          # 查看拷贝结果
insmod lcd.ko
lsmod                                           # 列出已加载模块
# pwd = /mnt/share/.../jz2440/fb_test           # nfs共享文件, 屏幕测试
./fb_test                                       # 测试, 显示用法
ls /dev/fb*                                     # 显示设备
./fb_test /dev/fb0                              # 测试指定设备
```
