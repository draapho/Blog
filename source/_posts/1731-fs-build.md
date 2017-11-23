---
title: fs之创建文件系统
date: 2017-11-03
categories: embedded linux
tags: [embedded linux, fs]
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

# 要构建一个最小的linux根文件系统
- `dev/console`, linux内核的标准IO接口
- `dev/null`, 相当于一个NULL文件
- init进程, 即 `bin/busybox`
- `etc/inittab` 配置文件, (可以省略, busybox会调用其默认值)
- 配置文件里指定的应用程序或脚本, 如 `/etc/init.d/rcS` `bin/sh`
- C语言库 `lib/`

在 [fs之Busybox的编译与使用](https://draapho.github.io/2017/11/02/1730-fs-busybox/) 一文中,
已经将busybox安装到指定目录 `~/jz2440/fs_first/`,
接下来, 基于此目录, 继续完善嵌入式linux的最小文件系统

## 创建 `dev/console` `dev/null` 文件
`dev/console` 用于标准输入输出
`dev/null` 空设备, 用于丢弃不需要的输出流, 或提供空输入.

``` bash
# pwd = ~/jz2440/fs_first/

$ ll /dev/console /dev/null
# 查看现有系统的这两个文件的详情
crw------- 1 root root 5, 1 Sep  5 00:01 /dev/console
# c表示字符设备, 5为主设备号, 1为次设备号
crw-rw-rw- 1 root root 1, 3 Sep  5 00:01 /dev/null
# c表示字符设备, 1为主设备号, 3为次设备号

$ mkdir dev
$ cd dev        # 进入 ~/jz2440/fs_first/dev/ 目录

$ sudo mknod console c 5 1
$ sudo mknod null c 1 3
# 仿照现有的文件系统内容, 创建 console 和 null 两个节点文件

$ ll            # pwd=~/jz2440/fs_first/dev/
drwxrwxr-x 2 draapho draapho 4096 Nov  3 11:01 ./
drwxrwxr-x 6 draapho draapho 4096 Nov  3 11:00 ../
crw-r--r-- 1 root    root    5, 1 Nov  3 11:00 console
crw-r--r-- 1 root    root    1, 3 Nov  3 11:01 null

# 至此, 创建 /dev/console 以及 /dev/null 完成.
```

## 创建 `etc/inittab` 文件
`etc/inittab` 供busybox初始化时调用的配置文件


``` bash
# pwd = ~/jz2440/fs_first/

$ mkdir etc
$ vim etc/inittab
# 输入 "console::askfirst:-/bin/sh", 保存退出
$ cat etc/inittab
console::askfirst:-/bin/sh
# "-/bin/sh" 前面的-, 提示让busybox开启一个账户登陆终端.
# 由源码函数 ash_main() 代码可知当检测到 - 时, 赋值isloginsh = 1

# 至此, 创建 etc/inittab 完成.
```

## 安装C库
务必使用 `gcc-3.4.5-glibc-2.3.6` 这个版本的C库
在 [嵌入式linux环境搭建3-Ubuntu16.04](https://draapho.github.io/2017/02/20/1706-linux-ubuntu16/) 中,
已经将这个库安装到了 `/usr/local/` 目录下.

``` bash
$ cd /usr/local/gcc-3.4.5-glibc-2.3.6/arm-linux/lib
$ ll
# 查看解压后的库文件, 针对 arm-linux的库
...
-rwxr-xr-x  1 draapho draapho  112886 Jan 22  2008 ld-2.3.6.so*
lrwxrwxrwx  1 draapho draapho      11 Jan 22  2008 ld-linux.so.2 -> ld-2.3.6.so*
drwxr-xr-x  2 draapho draapho    4096 Jan 22  2008 ldscripts/
-rwxr-xr-x  1 draapho draapho   17586 Jan 22  2008 libanl-2.3.6.so*
-rw-r--r--  1 draapho draapho   13094 Jan 22  2008 libanl.a
lrwxrwxrwx  1 draapho draapho      11 Jan 22  2008 libanl.so -> libanl.so.1*
lrwxrwxrwx  1 draapho draapho      15 Jan 22  2008 libanl.so.1 -> libanl-2.3.6.so*
...
# ".a" 表示静态库, ".so"表示动态库, 还有很多动态库的软连接.
# 我们只需要拷贝动态库和动态库的软连接即可.

$ mkdir ~/jz2440/fs_first/lib
$ cp *.so* ~/jz2440/fs_first/lib/ -d
# 拷贝动态库到最小文件系统下面. "-d" 表示只需要拷贝连接. cp指令默认会拷贝连接到的内容.

$ cd ~/jz2440/fs_first/
$ ll lib
# 查看一下拷贝结果.
# 至此, 创建 lib/ C库完成.
```

# 制作并烧录yaffs2映像文件
直接说结论, 一般文件系统都会放到 nand flash 里,
所以会使用 mkyaffs2image 工具将目录文件生成为 yaffs2 格式文件系统,
最后烧录进 nand flash 的 root 分区即可.

linux下的大多数工具都需要下载源码再自己编译, 譬如这里的 mkyaffs2image.
对于这类软件的安装, 我一般归到环境搭建里面去.
可以参考 [嵌嵌入式linux环境搭建3-Ubuntu16.04](https://draapho.github.io/2017/02/20/1706-linux-ubuntu16/)


## flash和文件系统比较
- jffs2: Journalling Flash FileSystem V2
    - 主要用于**NOR FLASH**, 基于MTD驱动层.
    - 缺点是当文件系统已满或接近满时，因为垃圾收集的关系而使jffs2的运行速度大大放慢
    - jffs不适合用于NAND闪存
- yaffs： Yet Another Flash File System
    - 针对**NAND FLASH**而设计的一种日志型文件系统. 直接提供了API对FLASH进行操作.
    - 与jffs2相比, 减少了数据压缩等功能, 所以速度更快, 挂载时间更短, 内存占用较小.
    - yaffs 仅支持小页(512 Bytes), yaffs2 可支持大页(2KB)的NAND闪存. yaffs2也优化了性能.
    - 大多数情况, 嵌入式系统推荐使用 yaffs2
- Cramfs: Compressed ROM File System
    - 一种**只读**的压缩文件系统。它也基于MTD驱动程序.
    - 按页单独压缩, 可以随机页访问. 高压缩比, 可节省Flash空间.
    - 速度快，效率高，其只读的特点有利于保护文件系统免受破坏，提高了系统的可靠性.
- NOR FLASH vs NAND FLASH

| NOR FLASH                                | NAND FLASH                               |
| ---------------------------------------- | ---------------------------------------- |
| 接口时序同SRAM,易使用                            | 地址/数据线复用，数据位较窄|
| 读取速度较快                                   | 读取速度较慢 |
| 擦除速度慢，以64-128KB的块为单位                     | 擦除速度快，以8－32KB的块为单位|
| 写入速度慢                                    | 写入速度快|
| 随机存取速度较快，支持XIP(eXecute In Place，芯片内执行)，适用于代码存储。在嵌入式系统中，常用于存放引导程序、根文件系统等。 | 顺序读取速度较快，随机存取速度慢，适用于数据存储(如大容量的多媒体应用)。在嵌入式系统中，常用于存放用户文件系统等。 |
| 单片容量较小，1-32MB                            | 单片容量较大，8-128MB，提高了单元密度 |
| 最大擦写次数10万次                               | 最大擦写次数100万次|

## 制作yaffs2映像文件

``` bash
$ cd ~/jz2440/
$ mkyaffs2image fs_first fs_first.yaffs2
# 进入文件系统所在的上级目录, 然后制作镜像

$ ll
-rw------- 1 draapho draapho 8750016 Nov  3 12:23 fs_first.yaffs2
# 查看制作结果
```

## 烧录yaffs2映像文件
``` bash
# 开发板 uboot
# 打开 jz2440 开发板串口终端, 启动时输入空格键, 进入如下菜单
##### 100ask Bootloader for OpenJTAG #####
...
[y] Download root_yaffs image
...
Enter your selection: y                     # 输入k, 烧录 root_yaffs
USB host is connected. Waiting a download.  # 提示连接成功

# 切换到 Ubuntu 终端, 输入
cd ~/jz2440/
sudo dnw fs_first.yaffs2                    # 输入dnw指令, 指明烧录文件
# DNW usb device found!                     # 开始烧录

# 开发板重启后, 就能启动终端输入指令操作了.
```

# 进一步完善linux根文件系统

上面只是完成了linux文件系统的基础功能.
要实现更高级的功能, 我们需要更为复杂全面的文件系统.

## 创建 `proc` 文件

proc目录即process的简写, 可以让ps指令查看linux的进程.
知道 `/proc` 的基本作用和使用方法以后, 我们需要把这些功能整合到文件系统里面.
为了循序渐进的说明, 下面展示了三种方法, 常用的就是第三种.

### ~~开发板人工实现~~
``` bash
# 开发板终端

$ ps
PID  Uid        VSZ Stat Command
ps: can't open '/proc': No such file or directory
# 譬如执行ps指令, 就会提示没有找到 /proc 目录

# 我们先手工实现一下
# pwd=/
$ mkdir proc
$ mount -t proc none /proc
# 创建 proc 目录, 并挂载到此目录. -t 为指定挂载类型为 proc.

$ ps
  PID  Uid        VSZ Stat Command
    1 0          3088 S   init
  ...
# 这样, ps指令就能看到进程了.

$ cd /proc
$ ls
1              745            diskstats      locks          sys
...
$ cd 1          # 进入目录1
$ ls -l fd      # 查看目录fd (file descriptor)
lrwx------    1 0        0              64 Jan  1 00:10 0 -> /dev/console
lrwx------    1 0        0              64 Jan  1 00:10 1 -> /dev/console
lrwx------    1 0        0              64 Jan  1 00:10 2 -> /dev/console
# 可以看到init进程的三个文件描述符, 分别对应了 标准输入, 标准输出, 标准错误.
```


### ~~集成到文件系统, 直接 mount ~~

``` bash
# Linux主机, Ubuntu终端

# 创建 proc 文件
$ cd ~/jz2440/fs_first/
$ mkdir proc

# 增加初始化脚本
$ vim etc/inittab
# 新增一行 "::sysinit:/etc/init.d/rcS" 用作运行脚本
$ cat etc/inittab
console::askfirst:-/bin/sh
::sysinit:/etc/init.d/rcS

# 创建脚本, 执行挂载指令
$ mkdir etc/init.d
$ vim etc/init.d/rcS
# 加入脚本语句 "mount -t proc none /proc" 挂载proc目录
$ cat etc/init.d/rcS
mount -t proc none /proc
$ chmod +x etc/init.d/rcS
# 加上可执行的权限

# 这样, 嵌入式linux完成启动后, 会运行init进程.
# - init进程运行 /etc/inittab 内的指令
# - 就会运行 /etc/init.d/rcS 脚本
# - 最终运行 mount -t proc none /proc 指令
```

### 集成到文件系统, 使用 `mount -a`

一般的, linux需要mount多个文件, 因此使用更为通用的 `mount -a` 指令,
然后去读取 `/etc/fstab` 文件内的配置项.

``` bash
# Linux主机, Ubuntu终端

# 创建 proc 文件, tmp 文件
$ cd ~/jz2440/fs_first/
$ mkdir proc
$ mkdir tmp         # 临时文件目录, 顺便一起做掉

# 增加初始化脚本
$ vim etc/inittab
# 新增一行 "::sysinit:/etc/init.d/rcS" 用作运行脚本
$ cat etc/inittab
console::askfirst:-/bin/sh
::sysinit:/etc/init.d/rcS

# 创建脚本, 执行挂载指令
$ mkdir etc/init.d
$ vim etc/init.d/rcS
# 加入脚本语句 "mount -a" 挂载proc目录
$ cat etc/init.d/rcS
mount -a
$ chmod +x etc/init.d/rcS
# 加上可执行的权限

# 创建挂载指令的配置文件
$ vim etc/fstab
# 创建 fstab 配置文件, 输入必要的内容, 见cat的结果
$ cat etc/fstab
#dev    dir     type    options         dump    fsck
proc    /proc   proc    defaults        0       0
tmpfs   /tmp    tmpfs   defaults        0       0
# 这里加载proc, 顺便把临时文件的加载也做了
```

此时. 可以使用 mkyaffs2image 生成镜像文件并烧录, 测试一下.

### fstab文件的简单说明

- dev, 要挂接的设备
    - 譬如: `/dev/hd2` `/dev/mtdblock1`
    - 对于 proc, 直接忽略此字段. 可以是任意值
    - 对于NFS文件系统, 此字段为 `<host>:<dir>`
- mount-point, 挂载点, 即一个目录文件
- type, 文件系统类型
    - 如 jffs, yaffs, ext2, nfs
    - 也可以是auto, 对DVD, usb等设备会非常有用
    - proc, tmpfs 等是特殊的文件类型, 都有特定功能.
- options, 挂接参数.
    - 一般用 defaults 就行
    - 参考[fstab (简体中文)](https://wiki.archlinux.org/index.php/Fstab_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))
- dump和fsck, 文件系统的备份和检查
    - 嵌入式系统一般都禁用, 设置为0

## 使用 mdev 自动生成文件
udev是Linux的设备管理器。它主要的功能是管理/dev目录底下的设备节点
busybox提供了udev的简化版本mdev, 其作用是在系统启动或动态加载驱动时, 自动生成节点文件.

在busybox源码里, 可以找到 `busybox-1.7.0\docs\mdev.txt`. 关键步骤如下:
- `mount -t sysfs sysfs /sys`
- `echo /bin/mdev > /proc/sys/kernel/hotplug`
- `mdev -s`
- `mount -t tmpfs mdev /dev`
- `mkdir /dev/pts`
- `mount -t devpts devpts /dev/pts`

由于我们使用的是 `mount -a`, 因此具体步骤稍有修改

``` bash
# Linux主机, Ubuntu终端
# pwd = ~/jz2440/fs_first/

$ mkdir sys
$ vim etc/fstab
# 修改fstab, 按要求增加 /sys /dev.
$ cat etc/fstab
#dev    dir     type    options         dump    fsck
proc    /proc   proc    defaults        0       0
tmpfs   /tmp    tmpfs   defaults        0       0
sysfs   /sys    sysfs   defaults        0       0
tmpfs   /dev    tmpfs   defaults        0       0

# 增加初始化指令到 etc/init.d/rcS
$ vim etc/init.d/rcS
# 修改rcS, mdev的要求增加指令
$ cat etc/init.d/rcS
mount -a
mkdir /dev/pts
mount -t devpts devpts /dev/pts
echo /sbin/mdev > /proc/sys/kernel/hotplug
mdev -s
# 不存在 /bin/mdev, busybox实际把它放在了 /sbin/mdev 下面.

# 这样, 嵌入式linux完成启动后, 会运行init进程.
# - init进程运行 /etc/inittab 内的指令
# - 然后调用 /etc/init.d/rcS 脚本
# - 依次执行rcS脚本内的指令, 
# - 执行"mount -a"时, 会根据 /etc/fstab 的配置挂载文件系统.
```

完成烧录后, 使用 `ls /dev`, 就会看到自动生成了非常多的设备文件.
至此, 一个最小linux文件系统制作完成了.

# 制作 jffs2 映像文件
jffs2 是一个压缩的文件系统, 所以体积几乎比yaffs2小一半.
多用于 NOR FLASH

## 生成 jffs2 工具
``` bash
# mtd-utils-05.07.23.tar.bz2 可生成jffs2工具

# 首先需要压缩库zlib-1.2.3的支持
$ tar xzf zlib-1.2.3.tar.gz
$ cd zlib-1.2.3
$ ./configure --shared --prefix=/usr 
# 配置为动态库, 放入/usr目录下
$ make
$ sudo make install

# 然后编译 mkfs.jffs2
$ tar xjf mtd-utils-05.07.23.tar.bz2
$ cd mtd-utils-05.07.23/util
$ make
$ sudo make install

# 测试一下是否装好了
$ mkfs.jffs
```

## 制作 jffs2 映像文件
``` bash
$ cd ~/jz2440/
$ mkfs.jffs -n -s 2048 -e 128KiB -d fs_first -o fs_first.jffs2
# -n            不要再每个擦除块上都加上清除标记
# -s 2048       指定Flash页大小
# -e 128KiB     指定Flash块大小(最小擦除单位)
# -d fs_first   文件系统目录
# -0 fs_first.jffs2 目标文件
```

至此, jffs2 格式的映像文件制作完成.

## 烧录 jffs2 映像文件
``` bash
# 开发板 uboot
# 打开 jz2440 开发板串口终端, 启动时输入空格键, 进入如下菜单
##### 100ask Bootloader for OpenJTAG #####
...
[j] Download root_jffs2 image
...
Enter your selection: j                     # 输入k, 烧录 root_jffs2
USB host is connected. Waiting a download.  # 提示连接成功

# 切换到 Ubuntu 终端, 输入
cd ~/jz2440/
sudo dnw fs_first.yaffs2                    # 输入dnw指令, 指明烧录文件
# DNW usb device found!                     # 开始烧录

# 切换到, 开发板 uboot, q退出菜单进入命令行模式
# 由于linux会自动识别为yaffs2格式, 因此还需要设置一下uboot环境变量, 指定文件系统的类型.
$ set bootargs noinitrd console=ttySAC0 root=/dev/mtdblock3 rootfstype=jffs2 init=/linuxrc
$ saveenv

# 开发板重启后, 就能启动终端输入指令操作了.
```



# 参考资料
- [嵌入式系统文件系统比较 jffs2, yaffs, cramfs, romfs, ramdisk, ramfs/tmpfs （转）](http://www.cnblogs.com/zelos/archive/2011/03/27/1996766.html)
- [Cramfs、JFFS2、YAFFS2的全面对比](http://blog.csdn.net/daofengdeba/article/details/7721340)
- [fstab (简体中文)](https://wiki.archlinux.org/index.php/Fstab_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***