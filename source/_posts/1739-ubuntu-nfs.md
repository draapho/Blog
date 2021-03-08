---
title: Ubuntu 16.04安装配置NFS
date: 2017-11-29
categories: linux
tags: [linux, nfs]
description: 如题.
---

转载自 [Ubuntu 16.04安装配置NFS](http://blog.topspeedsnail.com/archives/908)
**略有改动和增加**

--------------------------------------------

NFS允许用户通过网络分享目录和文件，客户端用户可以像操作本地文件一样操作服务端文件。

# NFS服务端

安装nfs-kernel-server：

``` bash
$ sudo apt install nfs-kernel-server
```

# NFS客户端

安装 nfs-common：

``` bash
$ sudo apt install nfs-common
```

# 服务端创建共享目录

客户端通过远程挂载的方式访问服务端共享目录，为了说明两种不同的文件权限，我会使用不同的选项创建两个共享目录。

- 默认情况下客户端不允许在NFS共享目录上执行root操作，如：更改文件所有权等。
- 但是有时用户需要用root权限操作NFS共享目录，这可以通过配置实现。

## 创建默认配置的共享目录

创建一个目录：
``` bash
$ sudo mkdir -p /var/nfs/sharedir
```

更改目录权限：
``` bash
$ sudo chown nobody:nogroup /var/nfs/sharedir
```

## 以root权限共享home目录

配置NFS：

```
$ sudo vim /etc/exports
```

如下格式
```
/var/nfs/sharedir   *(rw,sync,no_subtree_check)
/home               *(rw,sync,no_root_squash,no_subtree_check)

# 要限制客户端IP
# /var/nfs/sharedir 122.111.222.111(rw,sync,no_subtree_check)
# /home             122.111.222.111(rw,sync,no_root_squash,no_subtree_check)
```

下面是一些NFS共享的常用参数说明：

参数| 说明
---|---
rw          | 可读写的权限
ro           |    只读的权限
no_root_squash | 权限不压缩, 远程客户端拥有root权限. (不安全, 但嵌入式要用!)
root_squash | 权限压缩, 远程客户端root权限压缩成为匿名使用者(默认)
sync | 资料同步写入到内存与硬盘当中
async | 资料会先暂存于内存当中，而非直接写入硬盘
hide | 不共享子目录
no_hide | 共享子目录
subtree_check | 共享子目录时, 检查父目录的权限(默认)
no_subtree_check | 共享子目录时, 不检查父目录的权限

重启nfs-kernel-server：
``` bash
$ sudo systemctl restart nfs-kernel-server
```
如果开启了防火墙，打开NFS的2049端口。

查看共享文件情况
``` bash
$ showmount -e
/home *
```


# 客户端挂载共享目录

**此方法不适用于嵌入式Linux!**

创建两个挂载点：

``` bash
$ sudo mkdir -p /nfs/sharedir
$ sudo mkdir -p /nfs/home
```

挂载远程共享目录：

``` bash
$ sudo mount nfs_server_ip:/var/nfs/sharedir /nfs/sharedir
$ sudo mount nfs_server_ip:/home /nfs/home
```

查看挂载点：

``` bash
$ df -h
Filesystem                       Size  Used Avail Use% Mounted on
udev                             861M     0  861M   0% /dev
...
192.168.0.100:/var/nfs/sharedir   29G  4.5G   23G  17% /nfs/sharedir
192.168.0.100:/home               29G  4.5G   23G  17% /nfs/home
```
现在你可以使用共享目录了。


使用完之后不要忘了卸载：
``` bash
$ sudo umount /nfs/home
$ sudo umount /nfs/sharedir
```


# 开机自动挂载NFS共享目录

编辑fstab文件：
``` bash
$ sudo vim /etc/fstab
```

添加如下两行：
```
your_nfs_server_Ip:/var/nfs/sharedir    /nfs/sharedir   nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0
your_nfs_server_Ip:/home                /nfs/home       nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0
```

或者使用hostname
```
nfs_server_hostname:/var/nfs/sharedir   /nfs/sharedir   nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0
nfs_server_hostname:/home               /nfs/home       nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0
```


------------------------------------------------------

转载自 [Ubuntu 16.04安装配置NFS](http://blog.topspeedsnail.com/archives/908)
