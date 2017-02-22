---
title: Windows 软件系列-基于NFS的家庭网
date: 2016-10-3
categories: windows
tags: [windows, NFS, Hyper-V, NAS, freefilesync]
---


# 家庭网设想

## 理想的云
- 理想的家庭网是由NAS做数据中心, 是家里的云
- 需要使用千兆网来支持数据分享(如视频流)
- 考虑到设备多样性, 可使用多种分享模式, 如NFS, windows共享服务等等
- 理想很丰满, 现实很骨干. 由于预算, 稳定性, 易用性等问题, 多半会用折中方案
- 可以看看混乱的方案推荐: [如何实现一个简单的家庭云存储（NAS）系统？](https://www.zhihu.com/question/20791825)

## 现实的云
- 理想之所以遥远, 往往是因为没有明确需求, 导致什么都想要! 所以, 先明确需求
  - NAS是用来折腾和看电影的(电影存在硬盘上, 能在沙发上和床上观影).
  - 日常资料还是存储在本地硬盘比较便捷
  - 有安全需求, 要备份或镜像本地资料到家庭云(**双设备备份**, 相比NAS的各种RAID, 一大优势是**防偷**)
  - 做嵌入式开发, 需要在windows上装linux虚拟机, 然后数据共享
  - 关键数据出问题时, 在可靠和有把握的环境下来恢复数据.
- 给出最终使用的方案. 折腾记就不写在此文了.
  - 使用 Intel NUC 作为桌面主机和云服务器. 小巧, 够用(不玩游戏), 省电.
  - 使用 Hyper-V 安装 家用NAS 和 Ubuntu.
  - 另有嵌入式linux开发板, 投影仪, 手机等设备需要和云交换数据.
  - 使用 [HaneWIN][hanewin] 向其它设备提供NFS服务
  - 使用 [freefilesync][ffs] 备份资料到移动硬盘(和理想中的备份方式差好多...)


# [HaneWIN][hanewin]

- [HaneWIN][hanewin] 2017年开始是免费软件了. 非常适合做win下的nfs服务器
- 需要支持嵌入式linux端的NFS(只支持NFS v2), 配置见图:
![haneWIN_NFS](https://draapho.github.io/images/1606/haneWIN_NFS.PNG)
- 务必使用`UTF-8 character set`
![haneWIN_Server](https://draapho.github.io/images/1606/haneWIN_Server.PNG)
- 重点说一下`Exports`这一块, 即把文件通过NFS分享出去.
![haneWIN_Exports](https://draapho.github.io/images/1606/haneWIN_Exports.PNG)
  - `E:\Downloads -name:Downloads 10.0.0.99`
    就是把本地`Downloads`文件夹分享给`ip=10.0.0.99`的机器, 对外名称为`Downloads`
  - `-mapall:0:0` 是提供给linux端root权限. (这句最短? 花了一周时间才实验成功啊...)
  - `-range 10.0.0.1 10.0.0.111` 是设置ip范围, 这里是从`10.0.0.1`-`10.0.0.111`
  - 语法规则不多, 详见[官网说明](https://www.hanewin.net/doc/nfs/nfsd.htm). 可用参数如下:
    ```
    # The following options are supported:
    -name:<sharename>   assigns a name to the exported path as an alternate name for mounting.
    -alldirs    allows the host(s) to mount at any point within the filesystem.
    -umask:<mask>   set the umask for group and world permissions on the filesystem, default 022
    -readonly   limits access to reading
    -public Enables WebNFS access.
    -lowercase  maps all file names to lowercase, otherwise case is preserved.
    -exec   forces in access rights the x bit for all files.
    -mapall:<uid>[:<gid>]   all Unix user-ids and group-ids are mapped to the specified user-id and group-id.
    -maproot:<uid>[:<gid>]  the Unix super user root is mapped to the specified user-id, group-id. Without a mapping entry root will be mapped to user and group nobody.
    -range  IP adresses are interpreted in pairs as from-to ranges enabling client access from all addresses in a range (more flexible than the unix -net -mask options).
    ```
  - 再举几个例子:
    ```
    # exports example
    c:\ftp -range 192.168.1.1 192.168.1.10
    c:\public -public -readonly
    c:\tools -readonly 192.168.1.4
    ```
- 如果NFS被成功加载, 那么会在`Mounts`页显示出来
![haneWIN_Mounts](https://draapho.github.io/images/1606/haneWIN_Mounts.PNG)
- 参考
  - [GEN8折腾日记-第三方NFS工具 hanewin 设置(需登录)](http://www.nasyun.com/thread-25086-1-1.html)
  - [GEN8折腾日记-第三方NFS工具 hanewin 设置(百度文库)](http://wenku.baidu.com/view/c78baefefad6195f302ba665.html)
  - [群晖加载Windows NFS文件](https://www.chiphell.com/thread-1240623-1-1.html)


# Hyper-V

- 从Win8开始, Hyper-V是Windows自带的软件.
- 启用Hper-V, `控制面板`->`程序和功能`->`启用或关闭Windows功能`->`Hyper-V`
![HyperV_Enable](https://draapho.github.io/images/1606/HyperV_Enable.PNG)
- 设置虚拟网络
![HyperV_NIC1](https://draapho.github.io/images/1606/HyperV_NIC1.PNG)
![HyperV_NIC2](https://draapho.github.io/images/1606/HyperV_NIC2.PNG)
- 新建虚拟机
![HyperV_Install1](https://draapho.github.io/images/1606/HyperV_Install1.png)
![HyperV_Install2](https://draapho.github.io/images/1606/HyperV_Install2.png)
![HyperV_Install3](https://draapho.github.io/images/1606/HyperV_Install3.png)
- 安装Ubuntu 32位服务器版本, 用于交叉编译. (另一个备选方案是用cygwin)
- 安装家用NAS, 用于多设备(投影仪, 平板, 手机)看硬盘上的影片.


# NAS和智能路由器

## 两者的区别
- NAS, Network Attached Storage. 家用的话, 大多定位于多媒体观赏和数据备份两个核心功能.
- 专做NAS的厂家, [Synology(群晖)](https://www.synology.com/) 和 [QNAP(威联通)](https://www.qnap.com/) 比较有名
- 智能路由器, 从小米路由器到airport extreme.
- 两者区别的话, 就是一个更专业, 一个更娱乐.
  所谓专业, 就是更多的权限设置和管理(对用户不友好), 更多的功能, 更高的安全要求.
  所谓娱乐, 就是傻瓜易上手, 能用好用为主要需求.
  简而言之, 一个是专业单反, 一个是傻瓜机, 然后有一些就是处于中间位置的微单...

## 需求分析
- 大多数的家庭, 对此类产品的第一要求就是**好用**. 只有Geek一类的人需要**好玩**.
- NAS在宣传上, 必然会强调数据安全, 列出诸如支持多种RAID这种让非专业人士云里雾里的概念.
- 而普通家庭最大的数据安全问题就是数据过于集中, 防偷防意外损坏之类的风险防范反而不足了.
- 因此, 家用云市场应该侧重于易于配置和使用. 家庭的数据安全问题不是靠一台专业NAS设备就能解决的.
- 结论: 在家用市场, 智能路由器有更好的市场前景.

## 数据安全
- 家庭环境的话, 建议用移动硬盘备份关键资料(即RAID1), 然后分开存储, 当然也可以基于SFTP等服务自动备份. 这样可以做到物理上相对独立, 而且因为用的是RAID1, 数据出问题后的恢复也非常简单.
- 中小企业就需要用到稍微专业一点的NAS才比较好了. 话说, 很多本土企业对数据安全这一块很不上心啊...
- 推荐完全免费的同步软件[freefilesync][ffs], 买块硬盘, 家用足够了.

## 个人推荐
- 听说过家庭云, 不知道具体需求, 买个便宜的小米路由器先体验体验.
- 苹果爱好者直接上 airport extreme, 二千元可以给手机平板太多额外的存储空间了.
- 想要玩NAS的, 可以先用虚拟机装了体验一下效果.
- 如果买专业的NAS, 推荐直接用企业入门级产品QNAP的`TS-251`或`TS-253 Pro`,内置虚拟机, 可玩性很高.
- 群晖的机器不太推荐, 因为数据的存储格式很奇怪, 万一出点问题自己一点办法也没有!
- 组装机也不是太推荐, 因为功耗美观服务都要考虑进去.


# 同步软件[freefilesync][ffs]

- [freefilesync][ffs]是一款完全免费的同步软件, 可以完全媲美GoodSync
- 支持sftp, 所以也可以通过网络自动备份数据
- 家庭用户使用RAID1, 即关键资料双硬盘完整备份, 然后分开存放就足够了.


# 远程开机

如果是7x24小时开机当服务器用, 则不用考虑这一块. 远程开机是针对虚拟机和组装机用户说的.

## LAN唤醒
- LAN唤醒需要主板的支持, 不支持无线网络, 必须使用有线. 新一点的机器一般都能支持.
- 启用主板的WOL功能
  - 开机进入BIOS, 寻找`wake on lan``resume on lan``power on PME``power on by PCI-E device``Power on by Onboard LAN`等与电源管理和唤醒有关的选项并使能
- 设置网卡驱动
  - `设备管理器`->`网络适配器`->选择有线网卡设备->右键`属性`->在`高级`和`电源管理`标签下->启用`唤醒模式``唤醒魔包``幻数据包``唤醒计算机`之类的选项
- 配置 WIN10 WOL(Wake on Lan 远程唤醒) 最大的坑就是要关闭 "启用快速启动(推荐)", 而默认是打开的. 另外, 
  - `控制面板`->`硬件和声音`->`电源选项`->左边栏`选择电源按钮的功能`->弹出`系统设置`页面->`关机设置`->~~`启用快速启动(推荐)`~~
- 电脑非正常关机后, 是无法远程唤醒的.
- 建议分级测试.
  1. 可以先确定bios配置正确. 配置好bios, 进入winPE之类的系统, 选择关机, 看WOL是否起作用.
  2. 然后进入win10配置网卡的相关选项, 然后让机器进入睡眠模式, 看WOL是否起作用.
  3. 最后win10关机, 测试WOL是否起作用.
  4. "启用快速启动(推荐)", 位于 控制面板\硬件和声音\电源选项\唤醒时需要密码(系统设置)\关机设置.
  5. 注意: bios设置内关于PCI节能的设置特别注意, 考虑全部关闭
- Android端WOL软件推荐. `Wake On LAN` 配置简单, 界面友好.
- 参考链接
  - [TeamViewer手册-LAN唤醒](https://www.teamviewer.com/zhCN/res/pdf/Teamviewer9-Manual-Wake-on-LAN-zhCN.pdf)
  - [WOL 网络唤醒远程开机设置方法教程 + 多款软件下载！(手机远程开启电脑)](http://www.iplaysoft.com/wol.html)

## WAN远程唤醒
- WAN远程唤醒的前提是配置好LAN唤醒.
- 需要设置路由器, 设置过程非常复杂, 而且免费的不稳定.
- 我买了向日葵开机棒, 但实际体验不好. 一是向日葵的服务器不太稳定, 而是远程操作意义不大, 纯玩性质.
- 所以, 建议普通用户不用折腾这块了. 真有异地工作, 资料同步的需求, 用公共云, github, BitBucket都很好.


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***



[hanewin]:https://www.hanewin.net/nfs-e.htm
[ffs]:http://www.freefilesync.org/