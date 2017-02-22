---
title: 嵌入式linux环境搭建
date: 2017-02-16
categories: embedded linux
tags: [embedded linux, environment]
---

# 嵌入式linux开发环境搭建思路

1. PC windows 所有资料存在windows目录下, 所有操作在windows环境下. NFS设置可参考:
   - [Windows NFS 环境搭建](https://draapho.github.io/2016/10/03/1606-WinSoft-cloud/)
2. PC linux 装在虚拟机里, 提供交叉编译环境. 其环境搭建可参考:
   - 第一次尝试, 失败告终, ~~[嵌入式linux环境搭建1-Ubuntu14](https://draapho.github.io/2017/02/18/1706-linux-ubuntu14/)~~
   - 第二次尝试, 失败告终, ~~[嵌入式linux环境搭建2-CentOS7](https://draapho.github.io/2017/02/19/1706-linux-centos7/)~~
   - 第三次尝试, 成功! [嵌入式linux环境搭建1-Ubuntu16](https://draapho.github.io/2017/02/20/1706-linux-ubuntu16/)
3. Embedded linux 固化uboot, kernel, 使用nfs加载文件系统. 其参数设置可参考:
   - [嵌入式linux-jz2440环境搭建](https://draapho.github.io/2017/02/21/1707-jz2440-env/)


整个环境的搭建思路基于尽可能少的文件传输, 系统切换操作, 以便提高效率. 可以选择的方案有NFS方案, windows文件共享方案.
细化下去有:
- windows做NFS服务器
- ubuntu做NFS服务器
- ubuntu使用samba来支持windows文件共享
- 交叉使用上述方案.

一些列折腾之后, 最后顺利基于hanewin, win10作为NFS服务器. 两个linux作为NFS客户端, 三者文件共享.
而且使用这个方案还有一个好处, 开发文件都存放在熟悉的windows环境下, 修改/维护/备份都很方便.


## PC windows, win10
ip addr: `10.0.0.98`
gateway: `10.0.0.138`

1. 配置为静态IP. `10.0.0.98`
2. 当NFS服务器, 向PC linux和Embedded linux, u-boot提供NFS服务.
   使用了hanewin, 注意使能 nfs version2 以及权限设置 (-mapall:0:0)
3. 虚拟机安装 PC linux
4. 烧录工具, jlink, OpenJtag, dnw, 网络传输.
   早期需要使用. 开发到应用层就可以不用了.
   用基于nfs的网络传输, 放弃使用dnw.
5. 使用putty, 远程登录控制 PC linux.
   文本编辑器建议用vim
6. 使用串口, 可用putty 或 TeraTerm, 远程登录控制 Embedded linux,
   文本编辑器只能用vi
7. PC windows的环境搭建可参考:
   设置IP, 安装虚拟机属于常规内容, 按下不表.
   NFS服务器 HaneWIN 的配置见 **[Windows 软件系列-基于NFS的家庭网](https://draapho.github.io/2016/10/03/1606-WinSoft-cloud/)**
   其中 `Exports` 内容如下:

``` bash
# for linux
E:\My_Study\linux -name:study -mapall:0:0 10.0.0.100
E:\My_Work\linux -name:work -mapall:0:0 10.0.0.100

# for embedded linux.
E:\My_Study\linux\jz2440\ -name:jz2440 -mapall:0:0 -range 10.0.0.1 10.0.0.111

# for loading file system, should be no limit, root account
# E:\My_Study\linux\jz2440\nfs\fs_qtopia -name:fs -mapall:0:0 10.0.0.111
# E:\My_Study\linux\jz2440\nfs\fs_mini_mdev -name:fs -mapall:0:0 10.0.0.111
# E:\My_Study\linux\jz2440\nfs\fs_mini -name:fs -mapall:0:0 10.0.0.111
# please choose one:

E:\My_Study\linux\jz2440\nfs\fs_mini_mdev -name:fs -mapall:0:0 10.0.0.111
```


## PC linux ubuntu serve 16.04 32bit
ip addr: `10.0.0.100`
gateway: `10.0.0.138`

1. 配置为静态IP. (弄不好就是无法上外网. 这里折腾半天)
2. 安装NFS客户端. 开机mount NFS文件
3. 安装SSH服务, 以便在windows下使用putty
4. 安装交叉编译工具并测试
   arm-linux-gcc 3.4.5 (对于2440系列, 别用新版本, 不停的有坑)
   u-boot-tools
   mkyaffs2image
5. PC linux的环境搭建可参考:
   - 第一次尝试, 失败告终, ~~[嵌入式linux环境搭建1-Ubuntu14](https://draapho.github.io/2017/02/18/1706-linux-ubuntu14/)~~
   - 第二次尝试, 失败告终, ~~[嵌入式linux环境搭建2-CentOS7](https://draapho.github.io/2017/02/19/1706-linux-centos7/)~~
   - 第三次尝试, 成功! [嵌入式linux环境搭建1-Ubuntu16](https://draapho.github.io/2017/02/20/1706-linux-ubuntu16/)


## Embedded Linux jz2440v3
ip addr: `10.0.0.111`
gateway: `10.0.0.138`

1. 用 jlink 或 openJtag **烧录u-boot**
   - u-boot的编译
   - 需要工具jlink或OpenJtag, 一般开发板都会事先烧录好

2. 基于u-boot, 用dnw或网络传输 **烧录内核文件**
   - 最后成功使用nfs, 在u-boot下烧录内核文件. 彻底放弃dnw, 接线也更简洁.
   - 注意hanewin不支持多层文件夹!!!
   - ~~dnw 需要在window下安装驱动, win7/win10下支持不好. win10 有数字签名问题 (重启即失效)~~
   - ~~dnw 在虚拟机下的linux没有尝试成功, 因为我用的hyper-v虚拟机, 要连接到物理usb太麻烦.~~
   - ~~网络传输我这边表现很不稳定, 而且操作上也比dnw繁琐.~~
   - ~~我最终使用的是 windows 下的dnw. 因为只是烧录内核的时候需要使用.~~

3. 基于u-boot, 更改 **file system** 的加载方式为nfs系统, 并自动加载
   ``` bash
   # 以jz2440的u-boot为例, 进入u-boot命令行模式, 将其设置为nfs加载file system
   set bootargs noinitrd root=/dev/nfs nfsroot=10.0.0.98:/fs ip=10.0.0.111:10.0.0.98:10.0.0.138:255.255.255.0::eth0:off init=/linuxrc console=ttySAC0
   # (简化ip: 'set bootargs noinitrd root=/dev/nfs nfsroot=10.0.0.98:/fs ip=10.0.0.111 init=/linuxrc console=ttySAC0' 也可以工作)
   # (默认值: 'set bootargs noinitrd root=/dev/mtdblock3 init=/linuxrc console=ttySAC0')
   save        # 保存修改
   reset       # 重启.
   ```

4. jz2440的环境搭建可参考:
   - [嵌入式linux-jz2440环境搭建](https://draapho.github.io/2017/02/21/1707-jz2440-env/)



# 折腾记

## 实验过程

1. 之前玩过NAS, 所以有现成的hanewin让windows做NFS服务器.
2. Ubuntu上安装 nfs-common, 顺利加载NFS文件. 编译了u-boot和kernel, 一切正常
3. 开发板手动挂载nfs, 也成功了
4. 开发板开机通过nfs挂载文件系统时, 各种permssion deny.
5. 明显权限问题, 退回到ubuntu下, 尝试在ubuntu下也做个NFS服务器, 然后windows再倒过来加载.
6. 发现在ubuntu下, 不能把加载过来的NFS文件再次通过NFS分享出去, 应该是出于安全考虑, 没有深入追究.
7. 被第五条思路折腾了挺久, 最后是因为win10专业版下没有找到能做NFS客户端的软件而放弃.
8. 折腾一圈后, 又想到windows共享文件方法, 结果Ubuntu 14.04安装Samba提示依赖错误, 搜索半天网络, 没有解决. 按下不表.
9. 返璞归真, 在ubuntu下老老实实修改权限为777, 编译文件系统, 烧录测试... 结果开发板开机依旧提示错误...
10. 一天后, 理了理思路, 再分析. 应该还是权限问题没跑, 要么chmod, 要么uid, gid问题. 毕竟是windows下NFS传过来的文件.
11. 开始研究hanewin的权限问题, 翻到官网的说明, 确实有几个参数可以设置用户和权限.
12. 一通假设加穷举后, 顺利解决用户和权限问题. 再回到开发板开机通过nfs挂载文件系统, 终于成功了, 而且还是最理想的只需要windows当NFS服务器即可.
13. 期间还因为使用的arm-linux-gcc 4.3.2 版本, 编译成功, 加载部分fs可以运行, 部分fs有问题.一度以为是有些fs源码有问题, 多个问题交织在一起, 所以排错过程就显得异常痛苦迷茫了.
14. 嵌入式开发的起步阶段, 基本就是想打主线游戏, 但不停的有分支任务, 分支任务的分支打断你, 让人直直的想骂这tmd是谁设计的鬼游戏, 还让不让人玩下去...
15. 我想说, 只有保持着对主线好奇, 不忘要打败大boss的初心, 并在分支任务中寻求一点满足感, 才能坚持下去.


## ~~编译器的巨坑~~

刚开始用了 arm-linux-gcc 4.3.2, 编译u-boot时遇到了第一个坑, 还给解决了.
于是"顺利"使用 arm-linux-gcc 4.3.2 编译了u-boot, kernel, led驱动程序.
所谓顺利, 是因为没有报错, 生成的文件可以烧录, 启动.
加上引号, 是因为最后证明这些生成文件是有问题的, 会导致整个嵌入式系统某些部分无法正常工作.
最后在编译测试驱动用的C文件时, 编译出来的可执行文件在开发板上不可执行,
才想到可能是编译器问题而尝试着换回到 3.4.5 版本. 并连同内核全部重新编译了.
换回去后, 之前一度认为的源码有问题的fs也能成功加载了, 真是个巨坑...


下面列出使用 `arm-linux-gcc 4.3.2` 编译u-boot遇到问题时的解决方法 (**巨坑的开始**):

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

最后, 对于 arm-linux-gcc 版本问题, 又研究了一下. 应该说不是新版本不能用, 而是需要设置.
对应编译原理之类的基本不懂, 暂时也没有时间去验证, 此处写出来提供一个思路, 感觉是可行的.
关键点有这么几个.
- 要使用 arm-none-linux-gnueabi
- 要指定arm架构 -
- 指定使用的库

这个在上面uboot的例子也能看出一二了. 在网上还有人提到:
``` bash
# 编译 hello.c 时, 需要用如下命令
arm-none-linux-gnueabi-gcc -o hello hello.c -static # 特别指明了 static不能省略!
# 配置Makefile时, 需要指明arm架构
CC="arm-none-linux-gnueabi-gcc -march=armv4t"
# 指定交叉编译工具
export CROSS_COMPILE=/usr/local/arm-2008q3/bin/arm-none-linux-gnueabi-
# 最后, 还是没明白 arm-linux-gcc 和 arm-none-linux-gnueabi-gcc的区别.
# 因为打开 arm-linux-gcc 4.3.2 bin下的 arm-linux-gcc 可以看到如下内容:
exec arm-none-linux-gnueabi-gcc -march=armv4t $*
```

找到二篇详细说明的, 放上链接
[arm交叉编译器gnueabi、none-eabi、arm-eabi、gnueabihf、gnueabi区别](http://www.veryarm.com/296.html)
[arm-none-linux-gnueabi交叉工具链安装,介绍，区别总结](http://blog.csdn.net/u013467442/article/details/44197725)


# 新技术 [Docker](https://docs.docker.com/)

Linux下的环境搭建一直让人比较痛苦, 这也直接使得 `Docker` 优势尽显. 
简单研究了一下Docker, 这个方案是可行的! 
可参考 [Docker 初学笔记](https://draapho.github.io/2017/02/23/1708-docker/)

基于Docker的ARM交叉编译环境, 已经有人在做了.
- [dockcross/dockcross](https://github.com/dockcross/dockcross), 但S3C2440是ARM9, 采用的ARMv4架构
- [HOW TO USE DOCKER TO CROSS COMPILE FOR RASPBERRY PI](http://hackaday.com/2016/09/01/how-to-use-docker-to-cross-compile-for-raspberry-pi-and-more/)



----------

***原创于 [DRA&PHO](https://draapho.github.io/)***