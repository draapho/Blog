---
title: Ubuntu下配置支持Windows访问的samba共享
date: 2017-07-06
categories: embedded linux
tags: [uboot, embedded linux, error]
---


# 背景

家用电脑, 环境的搭建思路可参考[嵌入式linux环境搭建-主机端](https://draapho.github.io/2017/02/16/1705-linux-env/)

单位电脑, 没有使用nfs共享文件.
用的环境是: VMware Ubuntu 16.04 + Windows 7 + VMware 文件共享
尝试编译uboot时, 弹出一个错误提示

> ln: creating symbolic link XXXXXX : Operation not supported


问题根源和解决方法:
出现这类问题，主要是由于在编译的时候，要用ln去建立一些软链接，而这些文件是从Windows中，通过VMWare虚拟机共享进Linux的，Windows不支持软链接，所以，编译会报错。
解决办法就是，在VMWare下的Linux中，建立Samba服务， 然后新创建新samba用户和文件夹，然后在windows中就可以访问到该文件夹了。

相比于nfs共享文件, 唯一的缺点是: 文件存放在虚拟机中, 需要始终打开虚拟机才能在windows下访问文件. 因此文件的备份和修复也稍微麻烦一点. 优点是, 不需要付费软件.



--------------------------------------------

下文转载自 [Ubuntu下配置支持Windows访问的samba共享](http://blog.csdn.net/i_chips/article/details/19191957)

--------------------------------------------

# 一、安装Ubuntu samba服务器

``` bash
$ sudo apt-get install samba
$ sudo apt-get install smbclient # Linux客户端测试用
```

# 二、创建samba配置文件

1. 备份原配置文件
``` bash
$ sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
```

2. 创建共享目录
``` bash
$ sudo mkdir -p /home/share
# 一般来说，该目录的权限为755，将其改为777之后，Owner之外的其他用户才有权限写入。
$ sudo chmod 777 /home/share
```

3. 修改配置文件
``` bash
$ sudo vim /etc/samba/smb.conf

# ===== 文件内容, 在smb.conf最后添加： =====
[share]
    path = /home/share
    browseable = yes
    writable = yes
    comment = smb share test
# ===== 结束修改, 保存退出vim =====
```

另外，总结一下常见的samba配置及说明：

```
[share]                           # 该共享的共享名
    comment = smb share test  # 该共享的备注
    path = /home/share        # 共享路径
    allow hosts = host(subnet) # 设置该Samba服务器允许的工作组或者域
    deny hosts = host(subnet) # 设置该Samba服务器拒绝的工作组或者域
    available = yes|no        # 设置该共享目录是否可用
    browseable = yes|no       # 设置该共享目录是否可显示
    writable = yes|no         # 指定了这个目录缺省是否可写，也可以用readonly = no来设置可写
    public = yes|no           # 指明该共享资源是否能给游客帐号访问，guest ok = yes其实和public = yes是一样的
    user = user, @group       # user设置所有可能使用该共享资源的用户，也可以用@group代表group这个组的所有成员，不同的项目之间用空格或者逗号隔开
    valid users = user, @group # 指定能够使用该共享资源的用户和组
    invalid users = user, @group # 指定不能够使用该共享资源的用户和组
    read list = user, @group  # 指定只能读取该共享资源的用户和组
    write list = user, @group # 指定能读取和写该共享资源的用户和组
    admin list = user, @group # 指定能管理该共享资源（包括读写和权限赋予等）的用户和组
    hide dot files = yes|no   # 指明是否像UNIX那样隐藏以“.”号开头的文件
    create mode = 0755        # 指明新建立的文件的属性，一般是0755
    directory mode = 0755     # 指明新建立的目录的属性，一般是0755
    sync always = yes|no      # 指明对该共享资源进行写操作后是否进行同步操作
    short preserve case = yes|no # 指明是否区分文件名大小写
    preserve case = yes|no    # 指明是否保持大小写
    case sensitive = yes|no   # 指明是否对大小写敏感，一般选no，不然可能引起错误
    mangle case = yes|no      # 指明混合大小写
    default case = upper|lower # 指明缺省的文件名是全部大写还是小写
    force user = testuser     # 强制把建立文件的属主是谁。如果我有一个目录，让guest可以写，那么guest就可以删除，如果我用force user= testuser强制建立文件的属主是testuser，同时限制create mask = 0755，这样guest就不能删除了
    wide links = yes|no       # 指明是否允许共享外符号连接，比如共享资源里面有个连接指向非共享资源里面的文件或者目录，如果设置wide links = no将使该连接不可用
    max connections = 100     # 设定最大同时连接数
    delete readonly = yes|no  # 指明能否删除共享资源里面已经被定义为只读的文件
```

# 三、创建samba用户

注意，创建samba用户之前，必须先确保有一个同名的linux用户，否则samba用户会创建失败。
``` bash
$ sudo smbpasswd -a $USER
```

# 四、重启samba服务
``` bash
$ sudo service smbd restart
```

# 五. 客户端访问测试

1. Linux客户端访问测试
``` bash
$ smbclient -L //localhost/share
```

2. Windows客户端访问测试
    可以访问如下地址 `\\Linux的IP或者主机名\share`

3. 我一般会把虚拟机端Linux的IP搞成静态地址, 这样远程登录也更方便
``` bash
$ ifconfig                          # 查看IP信息
$ sudo vim /etc/network/interfaces

    # ===== 文件内容, 大致修改如下: =====
    auto lo
    iface lo inet loopback
    auto eth0

    iface eth0 inet static          # 使用静态地址
    address  192.168.0.100          # 设置静态地址
    netmask  255.255.255.0
    gateway  192.168.0.1            # 网关
    dns-nameservers   8.8.8.8  192.168.0.1 
    # ===== 结束修改, 保存退出vim =====
```

如果public = no，此时需要输入samba用户密码；
如果public = yes，则作为nobody用户直接访问。
另外，在Windows客户端使用 `net use * /del /y` 这条命令可以清理访问缓存。

--------------------------------------------

转载自 [Ubuntu下配置支持Windows访问的samba共享](http://blog.csdn.net/i_chips/article/details/19191957)