---
title: fs之BusyBox的使用与编译
date: 2017-11-02
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

# 什么是BusyBox
BusyBox 是linux下的一个应用程序, 集成了最常用的Linux命令和工具.
在jz2440开发板里, **BusyBox是内核成功启动后, 调用的第一个应用程序.**
启动jz2440开发板, 在终端内输入如下指令, 可以发现系统指令都是BusyBox的软链接.

``` bash
# 开发板终端
$ ls -l /bin/ls
lrwxrwxrwx    1 1000     1000            7 Jan 22  2008 /bin/ls -> busybox
$ ls -l /bin/cp
lrwxrwxrwx    1 1000     1000            7 Jan 22  2008 /bin/cp -> busybox

$ ls -l /linuxrc
lrwxrwxrwx    1 1000     1000           11 Jan 22  2008 /linuxrc -> bin/busybox
$ ls -l /sbin/init
lrwxrwxrwx    1 1000     1000            7 Jan 22  2008 /sbin/init -> ../bin/busybox
$ ls -l /bin/sh
lrwxrwxrwx    1 1000     1000            7 Jan 22  2008 /bin/sh -> busybox
```

# BusyBox的使用

内核启动后, 调用的第一个应用程序就是BusyBox. 而BusyBox的职责如下:
- 读取配置文件, `/etc/inittab`
- 解析配置文件, `<id>:<runlevels>:<action>:<process>`  
    - 指定程序, `<process>`
    - 何时执行, `<action>`
- 执行程序


## 启动BusyBox
由 [kernel之内核启动分析](https://draapho.github.io/2017/09/15/1725-kernel-launch/) 可知, 
`start_kernel` 函数最后会尝试调用: `run_init_process(execute_command);`, 由uboot的传入execute_command.
查看uboot的bootargs环境变量, `init=/linuxrc`, 所以会执行 `run_init_process("/linuxrc")`
由于 `/linuxrc` 是 `/bin/busybox` 的软连接, 所以最终调用了busybox.

如果调用失败, 会依次尝试如下指令, 但这些指令都是busybox的软连接, 等同于调用了busybox指令
- `run_init_process("/sbin/init");`, busybox的软连接
- `run_init_process("/etc/init");`, 指令不存在
- `run_init_process("/bin/init");`, 指令不存在
- `run_init_process("/bin/sh");`, busybox的软连接

BusyBox 源码大致的函数调用关系:
- `init_main`, busybox的入口
    - `parse_inittab`, 准备分析配置文件
        - `file=fopen(INITTAB, "r")`, 打开配置文件 `/etc/inittab`
        - `new_init_action`, 创建并链表化 init_action 结构.
    - `run_actions(SYSINIT)`, 初始化工作, 最早被执行
        - `waitfor(a,0)`, 等待执行完成
        - `delete_init_action(a)`, 从 init_action_list 链表中删除, 不会再被执行了
    - `run_actions(WAIT)`, 等待执行完成
        - 同 `run_actions(SYSINIT)`
    - `run_actions(ONCE)`, 执行一次且不会等待执行完成.
        - `run(a)`, 执行指令, 不会等待执行完成
        - `delete_init_action(a)`, 从链表中删除
    - `run_actions(RESPAWN)`, 如果子进程终止, 那么会重新孵化(调用执行).
    - `run_actions(ASKFIRST)`, 相比于RESPAWN, 要求用户按键确认.

## BusyBox使用说明
查看busybox源码, `busybox-1.7.0/examples/inittab` 文件内有较为详细的说明.
关键内容如下:
- 配置文件格式: `<id>:<runlevels>:<action>:<process>`
- `<id>`, 指定tty终端. 非强制, 会在前面加上 `/dev/` 变成 `/dev/<id>`
    - 譬如 `tty2`, 实际运行的终端是 `/dev/tty2`
    - 如果没有值的话, 对应的文件会是 `/dev/null`
- `<runlevels>`, 忽略
- `<action>`, 包括:
    - `sysinit`, 用作系统初始化, 执行指令并等待完成
    - `respawn`, 执行指令, 如果子线程终止, 会被重新孵化/执行
    - `askfirst`, 功能同 `respawn`, 只是需要用户按键确认
    - `wait`, 执行指令并等待完成
    - `once`, 执行指令不等待.
    - `restart`, `ctrlaltdel`, `shutdown`, 由linux内核信号量传递而来. 执行指令并等待.
- `<process>`, 要执行的应用程序或者脚本
- 如果BusyBox没有找到 `/etc/inittab` 文件, 则会自动加载如下应用程序:
    - `::sysinit:/etc/init.d/rcS`, 系统初始化时, 调用rcS脚本
    - `::askfirst:/bin/sh`, 询问后, 运行终端
    - `::ctrlaltdel:/sbin/reboot`, 按键重启
    - `::shutdown:/sbin/swapoff -a`, 关机时要做的事
    - `::shutdown:/bin/umount -a -r`, 关机时要做的事
    - `::restart:/sbin/init`, 重启后要做的事
- jz2440的 `/etc/inittab` 内容如下
    - `::sysinit:/etc/init.d/rcS`, 初始化配置
    - `s3c2410_serial0::askfirst:-/bin/sh`, 指定串口运行终端
    - `::ctrlaltdel:/sbin/reboot`, 特定按键重启
    - `::shutdown:/bin/umount -a -r`, 关机时要做的事

# BusyBox的编译

BusyBox的编译和安装可以查看源码内提供的 `INSRALL` 文件. 编译方法和过程和内核是类似的.
在linux主机ubuntu下进行交叉编译:

``` bash
tar -xjf busybox-1.7.0.tar.bz2      # 解压
cd busybox-1.7.0/                   # 进入目录, pwd=./busybox-1.7.0
make menuconfig                     # 会弹出UI配置界面

# 如果报错: *** mixed implicit and normal rules: deprecated syntax
# 修改makefile相关的行:
# config %config: 修改为 %config:
# / %/: 修改为 %/
```

BusyBox的配置项也非常多, 在此就不深入研究了. 
需要注意的是, 因为这里是交叉编译. 所以编译前, 需要修改BusyBox的编译工具链.
因为没有在Menuconfig界面里找到, 所以通过Makefile文件直接修改

``` bash
# pwd=./busybox-1.7.0
vim Makefile

# vim 界面
# 使用 :/COMPILE 找到 CROSS_COMPILE 配置项, 修改为
CROSS_COMPILE   ?= arm-linux-
# 使用 :wq 保存退出

make                # 编译

# 安装, 不能使用 make install, 否则Linux主机Ubuntu的命令就会被破坏掉!
mkdir ~/jz2440/fs_first                         # 创建一个filesystem, 实验用
make CONFIG_PREFIX=~/jz2440/fs_first install    # 安装到指定目录
# 再次强调, 这里是交叉编译, 不能直接用 make install. 否则linux主机的系统就被破坏了.

# 查看 fs_first 目录
# 可以看到全部都是常用的linux指令, 存放在 /bin /sbin /usr/bin /usr/sbin 目录下面.
cd ~/jz2440/fs_first/
total 20
drwxrwxr-x 5 name group 4096 Nov  2 15:46 ./
drwxrwxrwx 7 name group 4096 Nov  2 15:44 ../
drwxrwxr-x 2 name group 4096 Nov  2 15:46 bin/
lrwxrwxrwx 1 name group   11 Nov  2 15:46 linuxrc -> bin/busybox*
drwxrwxr-x 2 name group 4096 Nov  2 15:46 sbin/
drwxrwxr-x 4 name group 4096 Nov  2 15:46 usr/
```

这样, BusyBox编译就完成了.
然后, 就可以考虑构建linux的文件系统了

要构建一个最小的linux根文件系统, 至少需要如下文件:
- `dev/console`, linux内核的标准IO接口 
- `dev/null`, 相当于一个NULL文件
- init进程, 即 `bin/busybox`
- `etc/inittab` 配置文件, (可以省略, busybox会调用其默认值)
- 配置文件里指定的应用程序或脚本, 如 `/etc/init.d/rcS` `bin/sh`
- C语言库 `lib/`


# 更多资料
- [busybox 详解](http://blog.csdn.net/kyokowl/article/details/6921640)
- 嵌入式Linux应用开发完全手册, 第17章BusyBox相关部分

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***