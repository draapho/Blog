---
title: 使用OMV搭建家庭NAS
date: 2021-3-31
categories: windows
tags: [NAS, OMV]
description: 基于淘汰了的NUC5i5, 搭建家庭NAS
---

# 前言
5年前写过一篇 [Windows 软件系列-基于NFS的家庭网](https://draapho.github.io/2016/10/03/1606-WinSoft-cloud/), 就有了搭建一个较为理想的NAS的愿望. 正好利用起淘汰下来的NUC5i5, 尝试自建.
优先级由高到低, 需求如下:
- 24小时开机. 因而必须低功耗, 静音.
- 支持共享文件, 支持Windows网络映射.
- 手机端资料单向备份, 电脑端资料单向同步. 不需要版本控制.
- NAS系统盘备份功能. 若NAS系统意外崩溃, 可迅速恢复.
- NAS数据盘能在熟悉的windows系统下, 自己进行恢复.
- 下面的功能, 精力有限, 尽量避坑. 实现起来太困难就直接放弃.
- 内网可以直接看电影.
- 自动下载大文件.
- 外网可访问.


# 方案选择
- 硬件没得纠结, NUC5i5优缺点都很明显.
    - BIOS关闭所有不需要的外设, 降低风扇频率, 跑linux系统妥妥的超低功耗.
    - 缺点是支持的盘位有限. 能用的就是一块SSD, 一块SATA硬盘. 剩下的就只有USB3.0的接口了.
- 对于数据安全问题, 其实除了备份冗余, 同样重要的是数据恢复和异地存储.
    - 只关注备份冗余程度, 而不关注恢复价格和恢复难度, 那是没有意义的.
    - 真正的数据安全, 还要防止物理地点上被一锅端的可能性. 如盗窃, 火灾. 因而最核心的资料必须有异地存储.
- 故而, NUC5i5的缺点与我而言也不算大缺点.
    - 规划上够用, SSD放备份手机数据, SATA盘备份电脑数据, USB硬盘放影视资料.
    - 为了异地存储, 我还会定期使用移动硬盘对核心资料进行单向备份, 然后将移动硬盘放在办公地点.
    - 用RAID或者非常见的磁盘格式, 就意味着很难在自己熟悉的环境下进行数据恢复. (只接受FAT/NTFS/EXT系列的格式)
        - **windows下识别ext4的方法: 安装[ext2fsd-0.69.exe](https://sourceforge.net/projects/ext2fsd/files/Ext2fsd/0.69/)后, ext4硬盘会直接识别**
    - 单向备份本身就是一种RAID1模式, 再加上异地存储的移动硬盘, 对于普通家庭来说, 冗余度已经足够高了.
- 为了配置省心, 免费和硬件低功耗, 选择了[OMV](https://www.openmediavault.org/)


# 环境搭建
- 第一步, [安装OMV](https://openmediavault.readthedocs.io/en/5.x/installation/index.html). 过程略, 可参考[OMV安装：系统安装设置及一些功能的开启](https://post.smzdm.com/p/av7z2564/). 注意点如下:
    - 我使用的是U盘安装, 然后安装到U盘里. 因而需要不同容量的U盘, 便于区分.
    - 容量小的U盘用来烧录OMV安装文件. 容量大的U盘作为OMV系统盘, 容量至少是`8G+RAM`, 建议直接上32G或64G, 再大也没必要.
    - BIOS最好打开`legacy`启动模式. OMV5也支持`UEFI`, 只是系统盘会多一个UEFI区.
    - 将待安装的系统U盘, 用DiskGenius格式化为MBR磁盘. 否则装到一半容易报错, 内容如下:
        - `Partition(s) 1 on /dev/sda have been written, but we have been unable to inform the kernel of the change, probably because it they are in use. As a result, the old part it ion(s) will remain in use. You should reboot now before making further changes ERROR`
    - 如果出错了, 删除EFI分区需要用到`diskpart`内的`clean`指令. 可参考[DOS命令diskpart格式化磁盘](https://blog.csdn.net/u013005025/article/details/52947632). **务必再三确认, 谨慎操作!!!**
    - 键盘选择 `keymap` 建议选 `British English`, 不选 `American English`. 我遇到了标点符号乱码的情况.
    - `Root password` 要填写并记好.
    - 安装完毕, 提示`Finsih the installation`, **不要拔出安装用的U盘. 否则可能进不了OMV系统.** 进过一次系统后, 可以安全拔出安装U盘.
- 第二步, 配置OMV, 过程略, 继续参考 [OMV安装：系统安装设置及一些功能的开启](https://post.smzdm.com/p/av7z2564/). 注意点如下:
    - 配置 `网络->接口`时, DNS必须填, 一般填自己的网关地址即可.
    - `更新管理` 里面有很多是用不到的软件包, 不建议无脑全部安装. 如果驱动没问题, 不更新也可以.
    - `插件`部分, 我安装了 `backup`, `flashmemory`, `resetperms`, `omvextrasorg`
    - 一路安装到`Docker`和`portainer`即可. `cockpit`安装后运行失败, 也不知道开发者何时解决这个常见问题, 不装了.
- 第三步, 挂载文件系统, smb共享. 基本配置可参考 [OpenMediaVault(OMV)共享文件夹/SMB设置](https://www.jianshu.com/p/67b3587bb597). 注意点如下:
    - `存储器`->`S.M.A.R.T`. 我没有激活SMART监测. 但是配置了测试计划, 每年进行一次短暂自检.
    - 设置`共享文件夹`时, 先了解一下权限的相关知识, omv这一块做的很复杂.
        - [OpenMediaVault 共享权限注意事项](https://www.flysfeq.site/index.php/archives/60/)
        - [OMV使用篇三：文件共享](https://post.smzdm.com/p/a4wmvovk/)
        - `resetperms`插件就是用来恢复默认权限的.
    - 设置 `SMB/CIFS`共享文件时, 可以启用`权限继承`
- 第四步, 其它配置
    - `通告`, 配置一下SMTP, 这样OMV会及时发送email, 通告系统运行情况
    - 插件 `backup` 要配置, 我用的 `fsarchiver`方式, 定期自动备份到指定目录. 可参考 [NAS系统备份与恢复以OMV为案例的几种方法](https://opts-22.github.io/2020/10/17/omvbackup/)
    - 用的U盘当系统盘, 因而需要插件 `flashmemory`, 按照该插件`Notes(optional)`里的步骤, 用ssh, root权限依次修改执行.
    - omv挂载硬盘的名称又臭又长. 可以重命名磁盘名称, 并在`~`目录下建立软连接
        - 重命名ext格式磁盘名称: `e2label /dev/sdXX "ssd-disk"`. 其他格式的指令自查.
        - 建立软连接: 譬如 `ln -s /srv/dev-disk-by-XXXXXXX/ ~/ssd-disk`
    - 如果U盘容量不够, 可以考虑修改`docker`存储地址. 参考 [如何修改 Docker 默认存储位置](https://www.youtube.com/watch?v=stTK4YBKSw4)

# Docker之路
- 镜像的安装
    - [Docker Hub](https://hub.docker.com/)基本上都能搜到.
    - 安装方式有命令行模式和docker compose. 推荐后者, 只需要一个yml文件.
    - 命令行模式, 直接ssh即可. 也可以选择`Containers`进行配置. 参考 [Omv的Docker之路](https://sspai.com/post/59364)
    - docker compose. 更推荐. 参考 [OMV5利用图形化Docker工具Portainer部署jellyfin](http://loonlog.com/2020/7/2/openmediavault5-omv5-docker-portainer-jellyfin/)
- 镜像的选择. 我这边按需选择, 尽量少折腾.(依然被折腾的够呛)
    - 先看看别人的选择.
        - [NAS也能用上【统一认证】](https://post.smzdm.com/p/a8307lel/)
        - [谈谈如何使用docker，搭建一台“群晖”](https://post.smzdm.com/p/alpompze/)
        - [unraid折腾笔记 篇七：必装Docker推荐](https://post.smzdm.com/p/ax02p2d9/)
        - [NAS 上的 Docker](https://zhuanlan.zhihu.com/p/143264028)
    - 简单评估和实验后的选择:
        - [heimdall](https://hub.docker.com/r/linuxserver/heimdall), 相当于收藏夹功能. 有用且方便. 不用记一大堆的端口号了.
        - ~~[openLDAP](https://hub.docker.com/r/osixia/openldap), 统一认证功能. 试了一下, 配置繁琐, 而且不是所有的应用都支持LDAP功能, 放弃使用.~~
        - [jellyfin](https://hub.docker.com/r/jellyfin/jellyfin), 影音播放
        - [aria2-pro](https://github.com/P3TERX/Aria2-Pro-Docker), 下载工具
        - [syncthing](https://hub.docker.com/r/linuxserver/syncthing), 同步备份软件. 放弃了收费的 Resilio_sync
        - [filebrowser](https://hub.docker.com/r/filebrowser/filebrowser), 文件管理
        - [wetty](https://github.com/butlerx/wetty)  网页版ssh
    - 外网访问:
        - 方案总结, 见 [内网穿透、远程控制、端口映射，N种方法汇总](https://www.simongong.net/neiwangchuantouyuanchengkongzhiduankouyingshenzhongfangfahuizong/)
        - 不愿意折腾, 一度是放弃的. 我用的是 [Ubiquiti AmpliFi](https://amplifi.com/) 路由器, 支持手机端的远程访问, 但不支持电脑.
        - 找到了 [zerotier](https://www.zerotier.com/), 免费, 似乎简单易配置, 决定尝试一下.


## `heimdall` 收藏夹
- [heimdall](https://hub.docker.com/r/linuxserver/heimdall), 使用docker-compose安装即可
- PUID和GUID的值, 指令 `id user_name`
- TZ配置项, 参考[List of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
- ports, 为了避免冲突, 使用高位端口, 如 `8880:80`, 用8880映射80端口.
- OMV的docker-compose, 选择`portainer.io`->`local`->`Stacks`->`Add stack`即可.


## `jellyfin` 影音播放
- [jellyfin](https://hub.docker.com/r/linuxserver/jellyfin), 使用docker-compose安装即可. 官网地址为 [Welcome to the Jellyfin Documentation](https://jellyfin.org/docs/)
- OMV需要先共享音视频文件夹.
- 然后在`docker-compose`的`volumes`一栏下, 映射好相关文件夹.
- 输入`jellyfin`的地址`192.168.xx.xx:8096`, 设置`Users`, 添加`Libraries`即可.


## `filebrowsers` 文件管理
- [filebrowsers](https://github.com/filebrowser/filebrowser), 使用如下docker-compose安装即可.
```
version: "2.1"
services:
  filebrowser:
    image: filebrowser/filebrowser
    container_name: filebrowser
    volumes:
      - /srv:/srv
      #- ./config.json:/config.json     # 要自己指定配置文件的话, 必须先存在文件.
      #- ./database.db:/database.db
    ports:
      - 8888:80
    restart: unless-stopped
```


## wetty 网页版ssh
- [wetty](https://github.com/butlerx/wetty), 使用如下命令安装即可.
- docker指令安装 `docker run --restart always -p 3000:3000 wettyoss/wetty --ssh-host=192.168.xx.xx`
- 网址登录 `192.168.xx.xx:3000/wetty`
- android端输入法, 推荐 `Hacker's Keyboard`


## aria2pro 下载工具
- [aria2pro](https://p3terx.com/archives/docker-aria2-pro.html), 使用如下docker-compose安装即可.
- 初次登录会显示认证失败, 需要在AriaNg设置->RPC(192.168.XX.XX)里面输入`RPC_SECRET`里设置的密码.
- 可参考 [打开Aria2状态页面提示认证失败的解决办法](https://yiwangmeng.com/aria2-status-page-to-prompt-the-solution-of)
```
version: "3.8"

services:

  aria2-pro:
    container_name: aria2-pro
    image: p3terx/aria2-pro
    environment:
      - PUID=1000
      - PGID=1000
      - UMASK_SET=022
      - RPC_SECRET=1234abcd     # 设置一个密码, 用来连接Aria2
      - RPC_PORT=6800
      - LISTEN_PORT=6888
      - DISK_CACHE=64M
      - IPV6_MODE=false
      - UPDATE_TRACKERS=true
      - CUSTOM_TRACKER_URL=
      - TZ=Australia/Melbourne
    volumes:
      - /path/to/docker_data/aria2/config:/config
      - /path/to/download_file:/downloads
# If you use host network mode, then no port mapping is required.
# This is the easiest way to use IPv6 networks.
    network_mode: host
#    network_mode: bridge
#    ports:
#      - 6800:6800
#      - 6888:6888
#      - 6888:6888/udp
    restart: unless-stopped
# Since Aria2 will continue to generate logs, limit the log size to 1M to prevent your hard disk from running out of space.
    logging:
      driver: json-file
      options:
        max-size: 1m

# AriaNg is just a static web page, usually you only need to deploy on a single host.
  ariang:
    container_name: ariang
    image: p3terx/ariang
#    command: --port 6880 --ipv6
    network_mode: host
#    network_mode: bridge
#    ports:
#      - 6880:6880
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: 1m
```


## syncthing 同步工具
- [syncthing](https://syncthing.net/), 好用的全平台同步工具.
    - 自己的需求很简单, 只需要内网同步.
    - 手机和NAS, `Pictures`, `DCIM`, `Download`文件夹双向同步
    - 电脑和NAS, 单向同步. NAS作为备份端即可.
    - 不需要版本控制.
- Windows端名称为`SyncTrayzor`, Android端就是`syncthing`
- OMV端安装到Docker中, 使用如下docker-compose安装即可. 参考 [linuxserver/syncthing](https://hub.docker.com/r/linuxserver/syncthing)
```
version: "2.1"
services:
  syncthing:
    image: ghcr.io/linuxserver/syncthing
    container_name: syncthing
    hostname: syncthing #optional
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Australia/Melbourne
    volumes:
      - /path/to/docker_data/syncthing/config:/config  # syncthing的默认路径
      - /path/to/data:/data                 # 电脑数据单向备份
      - /path/to/smartphone:/smartphone     # 手机数据双向备份
    ports:
      - 8384:8384               # GUI界面端口
      - 22000:22000             # 数据同步端口
      - 21027:21027/udp         # 设备监听端口
    restart: unless-stopped
```
- 应用
    - 先匹配设备, 再从备份源一端共享目录, 这样最方便.
    - 关联文件夹使用的是 `文件夹ID`, 默认会给出随机字符, 且创建共享文件夹后不可修改, 建议自己提前设置成有意义的名字.
- 配置
    - 所有电脑都在同一个局域网下的话, 系统`设置`->`连接`->反选`全球发现`, 反选`启用 NAT 遍历`, 反选`开启中继`
    - OMV端的文件夹权限需要改成777, 可以在OMV共享文件夹设置里, `Reset Permissions` -> `每个人:读/写.`
    - `文件夹选项`. `高级`. 如果是和Windows/Android同步, 勾选 `忽略文件夹权限`
    - `文件夹选项`. 忽略模式. 忽略Linux隐藏文件, Windows回收站, 系统文件等.
```
.*
!.gitignore
*RECYCLE*\
*Recycle*\
*\desktop.ini
*\thumbs.db
```
- 参考资料
    - [(二十三)小众但好用: Syncthing 把手机变成同步网盘](https://zhuanlan.zhihu.com/p/121544814)
    - [Syncthing – 数据同步新选择，手把手教你做自己的网盘](https://www.appinn.com/syncthing/)
    - [论多设备同步文件，它说第二，没人敢说第一：Syncthing 使用笔记](https://ld246.com/article/1597823746488)
    - 权限问题的讨论, 里面用了ACL模式. [Syncthing / permissions — Create a share with existing folder](https://forum.yunohost.org/t/syncthing-permissions-create-a-share-with-existing-folder/8265)


## zerotier 外网访问
- zerotier 建议直接在NAS主机运行, 不要用docker.
- 图文教程, 参考[ZeroTier 的安装与使用](https://blog.csdn.net/RadiantJeral/article/details/104150070).
- 安装指南参考[zerotier官网](https://www.zerotier.com/download/#downloadLinux)
    - 先zerotier官网创建一个账号, `Create A Network`, 获取`Network ID`
    - 安装curl `sudo apt install curl`
    - 安装zerotier `curl -s https://install.zerotier.com | sudo bash`
        - 安装成功, 最后会显示 `Success! You are ZeroTier address [ 7cXXXXXX6f ]`
    - `zerotier-cli join 35xxxxxxxxxxxx22` 将设备通过`Network ID`加入到zerotier网络.
    - `zerotier-cli set 35xxxxxxxxxxxx22 allowManaged=1`
    - `zerotier-cli info` 检查连接状态. 返回值 `200 info 7cXXXXXX6f 1.6.4 ONLINE`
    - 在另外一台设备上, 如windows或手机端. 安装zerotier, 加入网络. 网页端使能加入的网络.
    - 两个设备相互ping zerotier给出的ip地址.
    - 然后再测试外网的情况. 如果外网情况也能相互ping通, 继续设置.
    - 在zerotier官网管理界面 `Managed Routes`, 添加转发规则 `家庭局域网IP/24 via NAS在zero-tier端的IP`,
        - 譬如 `192.168.1.0/24 via 10.147.17.111`.
        - 其中的`192.168.1.0`是家庭局域网地址段,
        - 其中的`10.147.17.111`是zero-tier分配给NAS的地址.
    - NAS端打开IP转发 `sudo sysctl -w net.ipv4.ip_forward=1`
    - 测试: 外网电脑登录OMV控制界面.
    - 安装完成.
- 我这边, 一共试了三到四次, 总是失败. 最后发现是路由器的问题.
    - `Amplifi`需要关闭`硬件NAT`功能, 有线连接的设备才能正常使用第三方VPN.
    - 参考资料 [UNABLE TO CONNECT TO MY WORK VPN](https://community.amplifi.com/topic/3916/unable-to-connect-to-my-work-vpn)
    - 把折腾过程也记录一下, 仅供参考.


## ~~zerotier 折腾记~~
- 凭着记忆记录下折腾过程. 没有遇到问题的话, 不需要看.
- 现象: NAS端显示连接zerotier成功, 有ip地址, 返回200, 显示ONLINE. 但内外网都ping不通.
- 一通查资料和修改, 突然ping通了内网. 大概的折腾过程如下:
    - `apt-get install net-tools` 安装 netstat.  `netstat -ntulp | grep 9993` 查看9993端口使用情况.
    - `ip link` 查看网卡状态. zerotier的网卡名字为 zt开头的一串数字字母组合.
    - [Make MTU configurable](https://github.com/zerotier/ZeroTierOne/issues/74)
        - 默认的mtu=2800, 应该有问题. 我设置成了`ip link set ztxxxxxxxx mtu 1500`
    - [Failing to assign IP to network interface](https://github.com/zerotier/ZeroTierOne/issues/809)
        - `modprobe tun` 确定tun可用
        - `nano /lib/systemd/system/zerotier-one.service` 加入`-U`
        - 删除`zerotier-one`的user和group:
            - `id zerotier-one` 查看用户信息 `nano /etc/group` 查看组信息
            - `userdel zerotier-one`  删除用户
            - `groupdel group` 删除用户组
        - 后面还提到了添加 `/etc/systemd/network/50-zerotier.conf`文件
            - `Name=zt* Unmanaged=yes`
- 这样可以ping内网, 但还是ping不通外网. 继续瞎折腾
    - 参考资料.
        - [设置ZeroTier网络](https://chrisatech.wordpress.com/2020/02/09/setting-up-a-zerotier-network/)
        - [Getting Started with Software-Defined Networking and Creating a VPN with ZeroTier One](https://www.digitalocean.com/community/tutorials/getting-started-software-defined-networking-creating-vpn-zerotier-one)
        - [Zerotier 异地组网问题](https://www.v2ex.com/t/681731)
        - `zerotier-cli listnetworks` 查看状态
        - `zerotier-cli info` 查看是否在线
        - `systemctl restart zerotier-one` 重启服务. 另stop则停止, start则开始.
    - 最后放弃. 想着自己的路由器是AmpliFi, 可以很方便的实现手机外网访问.
- 彻底卸载 Zerotier-one 的方法
    - 参考 [搭建Zerotier内网穿透网络及彻底删除zerotier方法](https://www.taodudu.cc/news/show-1734416.html)
    - `sudo dpkg -P zerotier-one`
    - `sudo rm -rf /var/lib/zerotier-one/`
- 最后一次尝试前, 查了一下路由器端的资料, 关了硬件NAT, 重新安装配置, 一切顺利...


# Clonezilla 系统盘备份
- 防止系统盘损害, 无法启动. 直接替换克隆下的系统U盘即可.
- 克隆系统U盘方法如下:
    - NAS-OMV主页->`磁盘`->**确定系统盘的序列号, 记录下来**
    - 插入目标U盘->方法同上, 记录下序列号.
    - NAS-OMV主页->`OMV-extras`->`内核`->`再生龙 Clonezilla`->安装
    - 然后点击下面的`从再生龙 Clonezilla 启动一次`.
    - 重启 NAS-OMV, 等待进入Clonezilla系统.
    - 使用ssh, 登录到Clonezilla界面. 用户名`user`, 密码`live`
    - 输入指令 `sudo clonezilla`, 启动该软件.
    - 选择第二项, 设备到设备. `device-device work directly from ...`
    - 选初学者模式 `beginner ...`
    - 选磁盘到磁盘 `disk to local disk`
    - 然后选择母盘, **注意序列号, 千万别选错!!!**
    - 然后选目标盘, **注意序列号, 千万别选错!!!**
    - 选第一项 `sfsck` 跳过文件系统检查
    - 然后选完成后的动作. 选第一项即可 `-pa choose`
    - 一路 `y` 就开始克隆了.
    - 拔掉母盘, 输入 `reboot`, 测试是否克隆成功.
- 参考资料[Clonezilla 克隆系统盘 OMV 无限续命大法 再生龙 | 一台电脑的 NAS 之旅](https://www.bilibili.com/s/video/BV1S7411h7PH)
