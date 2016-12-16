---
title: linux 系统文件及磁盘指令
date: 2016-12-15
categories: linux
tags: [linux, command]
---

# linux 系统文件简要说明

FHS是Filesystem Hierarchy Standard的简称.FHS定义了两层规范:
第一层是/目录下各个主要目录应该放什么文件数据, 例如/etc应该放配置文件,/bin与/sbin则应该放置可执行文件等.
第二层则是针对/usr和/var这两个目录的子目录来定义,例如/var/log放置系统登录文件,/usr/share放置共享数据等.
单一文件或目录的最大允许文件名为255个字符,包含完整路径的文件名或目录名最大允许为4096个字符.


| 目录                                      | 说明                                       | 文件内容                                     |
| --------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| `/`                                     | root, 根目录                                | 一般建议只有目录,不要直接放文件. `/etc` `/bin` `/sbin` `/dev` `/lib` 必须与 `/` 同一分区 |
| `/bin`, `/usr/bin`, `/usr/local/bin`    | Essential command **bin**aries, 普通用户可执行的二进制文件 | 如 `ls` `mv` `cat` 等指令                    |
| `/boot`                                 | Static files of the **boot** loader,  启动时用到的文件 | 包括 vmlinuz (就是kernel), grub (开机管理)       |
| `/dev`                                  | **Dev**ice files, 设备文件                   | 任何设备与接口都是以文件的型态存放在此目录下. 分为`字符设备`和`块设备`   |
|                                         | `/dev/null`                              | 空设备                                      |
|                                         | `/dev/tty*`                              | 串口设备                                     |
|                                         | `/dev/hd[a-d][1-63]`                     | IDE 硬盘                                   |
|                                         | `/dev/sd[a-p][1-20]`                     | SCSI硬盘,U盘                                |
|                                         | `/dev/cdrom`                             | CDROM                                    |
|                                         | `/dev/fd[0-1]`                           | 软盘                                       |
|                                         | `/dev/lp[0-2]`                           | 并口打印机                                    |
|                                         | `/dev/mouse`                             | 鼠标                                       |
|                                         | 常见`sda1-3`(主分区),~~`sda4`~~(扩展分区),`sda5..`(逻辑分区) | 分析:硬盘支持4个主分区,1个扩展分区(占用主分区),16个逻辑分区(SCSI硬盘). 扩展分区文件名不显示. |
| `/etc`                                  | **Etc**etera, 杂项都在此处! 偏系统设置              | 系统启动(`/etc/init` `/etc/init.d`), 账号密码(`/etc/passwd` `/etc/shadow`), 开机预设值(`/etc/sysconfig/*`) |
| `/home`                                 | User **home** directories, 用户的家目录        | 放置用户自有的数据, 如音乐图片等                        |
| `/lib` `/usr/lib` `/usr/local/lib`      | Essential shared **lib**raries and kernel modules, 系统使用的函式库的目录 | `/lib/modules` 放着kernel的相关模块             |
| `/lost+found`                           | 系统异常时,会将一些遗失的片段放于此目录                     |                                          |
| `/mnt`                                  | **Mount** point for mounting a file system temporarily, 默认挂载点文件的目录 | 通常软盘挂在`/mnt/floppy`下,光盘挂在`/mnt/cdrom`下   |
| `/media`                                | Contains mount points for replaceable **media** | `/media`目录功能与`/mnt`类似                    |
| `/opt`                                  | Add-on application software packages, 主机自行安装软件默认放置的目录 | 以前较多情况放置在`/usr/local`目录下                 |
| `/proc`                                 | Virtual directory for system information, 虚拟档案系统. 数据都在内存当中,不占用硬盘空间. | 主要包括系统核心,接口设备状态,网络状态. 比较重要的档案例: `/proc/cpuinfo` `/proc/dma` `/proc/interrupts` `/proc/ioports` `/proc/net/*` 等 |
| `/root`                                 | Home directory for the **root** user 系统管理员的家目录。 | 一般与根目录`/`在同一分区下                          |
| `/sbin`, `/usr/sbin`, `/usr/local/sbin` | Essential system binaries,**S**uper user **bin**aries, 放置系统管理员才会动用到的执行指令 | 如： `fdisk` `mke2fs` `fsck` `mkswap` `mount` 等 |
| `/sys`                                  | Virtual directory for system information (2.6 kernels) |                                          |
| `/srv`                                  | Data for **services** provided by the system, 一些服务启动之后，这些服务所需要取用的数据目录 | 如WWW 服务器需要的网页就可放在`/srv/www`内             |
| `/tmp`                                  | **Temp**orary files, 这是让一般用户或是正在执行的程序暂时放置文件的目录 | 这个目录任何人都能够存取的，所以需要定期清理                   |
| `/usr`                                  | **U**nix **S**hared **R**esources        | 此目录下包含系统的主要程序,图形界面文件,额外的函式库、本机自行安装的软件，以及共享的目录与文件等 |
|                                         | `/usr/bin,/usr/sbin`                     | 可执行的档案放置目录                               |
|                                         | `/usr/include`                           | c/c++等程序语言的头文件放置目录                       |
|                                         | `/usr/lib`                               | 各应用软件的函数库档案放置目录                          |
|                                         | `/usr/local`                             | 本机自行安装及升级软件默认放置的目录                       |
|                                         | `/usr/local/bin`                         | 自行安装及升级软件后的可执行文件目录                       |
|                                         | `/usr/share`                             | 共享文件放置的目录, 如帮助文档(doc,man)                |
|                                         | `/usr/src`                               | Linux系统相关的程序代码放置目录                       |
|                                         | `/usr/src/linux`                         | 为Linux Kernel的源码                         |
|                                         | `/usr/X11R6`                             | X Window System 所需的执行文件放置目录              |
| `/var`                                  | **Var**iable data                        | 主要放置系统执行过程中经常变化的文件                       |
|                                         | `/var/cache`                             | 程序文件在运作过程中的一些缓存数据                        |
|                                         | `/var/lib`                               | 程序执行中，使用到的数据库文件放置的目录                     |
|                                         | `/var/log`                               | 登录文件放置的目录(如/var/log/messages)            |
|                                         | `/var/run`                               | 某些程序或是服务启动后,会放置PID在此处                    |
|                                         | `/var/spool`                             | 是一些数据队列存放的目录,作用为缓冲                       |



# linux系统分区建议

| 挂载目录    | 说明                        | 类型   | 台式机      | 嵌入式            |
| ------- | ------------------------- | ---- | -------- | -------------- |
| `/boot` | 启动程序等                     | ext4 | 100MB    | 50MB           |
| `/`     | 根目录                       | ext4 | 1GB-5GB  | 150-250MB      |
| `swap`  | 虚拟内存                      | swap | 0/2*ram  | 看情况            |
| `/usr`  | 放置系统应用程序                  | ext4 | 5GB-20GB | 1-5GB          |
| `/opt`  | 放置大型或测试软件, **建议用户软件都放此处** | ext4 | 10-50GB  | 使用`/usr/local` |
| `/tmp`  | 临时文件                      | ext4 | 500M     | 50-100M        |
| `/var`  | 放置经常变化的文件                 | ext4 | 1GB      | 300-500M       |
| `/home` | 用户家目录                     | ext4 | 100G/自定义 | 看情况            |



# linux磁盘常用指令

| 指令                                       | 说明                             |
| ---------------------------------------- | ------------------------------ |
| `df`                                     | **disk free**, 查看磁盘相关信息        |
| ...... **`df -Th`**                      | 查看磁盘容量信息                       |
| ...... **`df -iTh`**                     | 查看磁盘inode信息                    |
| `du`                                     | **disk usage**, 查看磁盘文件使用情况     |
| ...... **`du -h`**                       | 列出当前文件夹下所有文件的容量                |
| ...... **`du -sh file_dir`**             | 列出指定文件的容量                      |
| `fdisk`                                  | **format disk**, 磁盘查看及分区       |
| ...... **`fdisk -l`**                    | 查看整个系统的分区情况                    |
| ...... **`fdisk /dev/sda6`**             | 对指定磁盘进行配置(进入fdisk命令行模式)        |
| `mkfs`                                   | **make filesystem**, 分区格式化     |
| ...... **`mkfs -t ext4 /dev/sda6`**      | 格式化sda6分区格式为ext4               |
| `fsck`                                   | **filesystem check**, 分区检验和修复  |
| ...... **`unmount /dev/sda6`**           | 要检查的分区必须先umount                |
| ...... **`fsck -y -t ext4 /dev/sda6`**   | 对sda6分区进行检验和修复                 |
| `mount`                                  | **mount** 查看和挂载分区              |
| ...... **`mkdir /mnt/sda_data`**         | 必须先创建挂载点文件夹                    |
| ...... **`mount -t ext4 /dev/sda6 /mnt/sda_data`** | 挂载指定设备sda6到文件夹                 |
| `umount`                                 | **umount**, 取消挂载点              |
| ...... **`umount /dev/sda6` **           | 两种写法都可以                        |
| ...... **`umount /mnt/sda_data`**        | 两种写法都可以                        |
| `quato`                                  | **quato**, 管理普通用户的分区配额,多用于服务器. |


# mount常见用法及开机自动挂载

## 挂载U盘
- 插入U盘, 用 `fdisk -l` 或 `ll /dev/` 下查看U盘的硬件名称, 如 `sda11`
- 在mnt下建立usb目录 `mkdir /mnt/usb`
- 挂载U盘  `mount -t vfat /dev/sda11 /mnt/usb`
- 卸载U盘  `umount /mnt/usb`
- 拔出U盘
- 删除mnt目录  `rm -fr /mnt/usb`

## 挂载fat32分区
`mount -t vfat -o iocharset=cp936 /dev/sda6 /mnt/fat32`

## 挂载ntfs分区
`mount -t ntfs -o iocharset=uft8 /dev/sda6 /mnt/ntfs`

## 挂载光驱
`mount -t iso9660 /dev/hdc /mnt/cdrom`

## 重载分区为可读写
将根目录改为可读写,系统维护时使用
`mount -n -o remount,rw /`

## 自动挂载分区
通过修改 `/etc/fstab` 实现. 根据规则自行添加行即可.
```
# <file system>   <mount point> <type> <options> <dump> <pass>
# <分区>           <挂载点>      <类型>  <配置>     <备份>  <检查>

# 以下是通过分区唯一的uuid进行挂载,优点是可绑定指定分区
# 获取uuid指令: `ll /dev/disk/by-uuid/`
  UUID=xxxx-xxxx  /             ext4   errors=..  0     1
  UUID=xxxx-xxxx  /boot         ext4   defaults   0     2
  UUID=xxxx-xxxx  /home         ext4   defaults   0     2

# 以下是通过设备文件名进行挂载,优点是直观
# 查看设备文件名指令: `sudo fdisk -l`  (sudo,获取管理员权限)
  /dev/sda5       /mnt/data     ext4   defaults   0     2
```







----------

***原创于 [DRA&PHO](https://draapho.github.io/)***