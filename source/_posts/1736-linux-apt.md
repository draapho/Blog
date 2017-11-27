---
title: linux软件的安装和管理
date: 2017-11-26
categories: linux
tags: [linux, apt]
---

# 背景

接触linux至今, 遇到的最大的坑就是软件的安装!
找不到包, 找不到指定版本的包, 包依赖关系出问题, 软件源要更新...
因此, 在这里集中整理一下上述问题的解决方式.


# apt 命令
最新 Ubuntu推荐使用 `apt` 指令. 其常用功能如下

| apt 命令             | 功能说明              | 对应的旧命令                      |
| ------------------ | ----------------- | --------------------------- |
| `apt list`         | 根据名称列出软件包         | `dpkg list`                 |
| `apt search`       | 搜索软件包描述           | `apt-cache search`          |
| `apt show`         | 显示软件包细节           | `apt-cache show`            |
| `apt install`      | 安装软件包             | `apt-get install`           |
| `apt remove`       | 移除软件包             | `apt-get remove`            |
| `apt update`       | 更新可用软件包列表         | `apt-get update`            |
| `apt upgrade`      | 升级指定的软件  | `apt-get upgrade`           |
| `apt full-upgrade` | 升级指定的软件并安装或删除其依赖的软件 | `apt-get dist-upgrade`      |
| `apt edit-sources` | 编辑软件源信息文件         | `vim /etc/apt/sources.list` |

# 软件源

就是存放Ubuntu可执行软件的网址. 分为官方软件源和PPA软件源
Ubuntu的软件源都记录在了 `/etc/apt/sources.list` 文件下面.

## Ubuntu 官方软件源

顾名思义, 就是官方提供的软件下载地址. 格式如下:
```
deb http://us.archive.ubuntu.com/ubuntu/ xenial main restricted
# deb-src http://us.archive.ubuntu.com/ubuntu/ xenial main restricted
```

由于众所周知的原因, 在国内经常是不能用的. 那么可以替换为如下网址, 是官方软件源的镜像.
更多可见 [国内开源镜像站点汇总](https://segmentfault.com/a/1190000000375848)
```
deb http://mirrors.zju.edu.cn/ubuntu/ xenial main restricted
# deb-src http://mirrors.zju.edu.cn/ubuntu/ xenial main restricted
```

## PPA软件源

PPA软件源, 即"Personal Package Archives", 个人软件包集.
Ubuntu开设了一个开发者平台, 允许开发者建立自己的软件仓库并上传.
因此, 用PPA不能保证安全性.

PPA的格式如下, 网址都是 `ppa.launchpad.net` 开头的

``` bash
deb http://ppa.launchpad.net/wireshark-dev/stable/ubuntu trusty main
# deb-src http://ppa.launchpad.net/wireshark-dev/stable/ubuntu trusty main
```

# `update` `upgrade` `dist-upgrade` 的区别

update 更新的是软件源信息. 因此一般习惯在install之前, 使用update更新一下.

``` bash
sudo apt edit-sources       # 更改软件源列表
sudo apt update             # 根据软件源列表下载新的版本信息和包信息
sudo apt install XXX        # 可以下载了. 如果还是有问题, 说明这个软件在源列表中不存在或者是网络问题.
```

upgrade 更新的是指定的软件到最新版本. 但不去考虑依赖关系.
dist-upgrade 会判断软件新版本的依赖关系, 如果依赖关系变了, 它能自动升级依赖的软件.
``` bash
sudo apt upgrade XXX        # 只升级指定的软件, 不考虑其依赖关系
sudo apt full-upgrade XXX   # 字面意思: 全面升级! 就是会去自动安装/删除依赖的软件.
```

# build-dep 自动建立编译环境

譬如要手工编译 apache2, 那么可以用 `apt-get build-dep` 来快速建立编译环境.

``` bash
sudo apt-get build-dep apache2
# 会列出一系列会被安装的软件, 并询问是否要安装.
# 先回答NO.

sudo apt-get build-dep apache2 | tee apache2.log 
# 为了便于日后查看关系包, 建议先做个记录:
```

# 查看依赖关系

```bash
apt-cache depends XXX
# 查看正向依赖, XXX依赖的软件

apt-cache rdepends XXX
# 查看反向依赖, 依赖XXX的软件
```


# 遇到错误

## 找不到资源
- 检查网络, 是否需要翻墙. 必要的话, 更改软件源列表.
- 检查网络, 是否安全性太高了. 有些公司网络容易产生这样的情况.
- `sudo apt update`, 更新软件源在试试.


## Java 安装失败
Java向下兼容, 建议直接安装java最新版
`sudo apt-get install openjdk-8-jdk`

更复杂的情况, 参考这篇stackoverflow吧
- [Ubuntu: OpenJDK 8 - Unable to locate package](https://stackoverflow.com/questions/32942023/ubuntu-openjdk-8-unable-to-locate-package)


## Could not get lock 

`E:Could not get lock /var/lib/apt/lists/lock - open (11: Resource temporarily unavailable)`
获取资源锁失败, 说明有另外一个apt-get在运行. 这种情况多发生在新装的Ubuntu中, 他会自动运行apt-get
解决方法:
``` bash
# 或者去查看进程
ps -e | grep apt
# 看是否有进程在执行
# 6362 ? 00:00:00 apt
# 6934 ? 00:00:00 apt-get
# 7368 ? 00:00:00 synaptic

# 有的话, 直接杀掉
sudo killall apt
sudo killall apt-get
sudo killall synaptic

# 还是不行的话, 直接移除锁
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/lock
```

## 软件版本问题

先试试指定版本号安装

``` bash
apt-get install package=version

# 譬如
apt-get install nautilus=2.2.4-1
```

如果更复杂的, 譬如依赖的软件需要指定版本, 直接参考stackoverflow吧
[How do I resolve unmet dependencies after adding a PPA?](https://askubuntu.com/questions/140246/how-do-i-resolve-unmet-dependencies-after-adding-a-ppa)


# 参考
- [apt与apt-get的区别](http://www.jianshu.com/p/3dad50f452b6)
- [详解Ubuntu软件源](http://www.jianshu.com/p/57a91bc0c594)
- [apt-get update ，upgarde 和dist-upgrade 的区别](http://blog.csdn.net/wangyezi19930928/article/details/54928201)
- [记一条好用的ubuntu命令: apt-get build-dep](http://blog.csdn.net/mifangdebaise/article/details/50553596)
- [sudo apt-get update更新源失败](http://blog.csdn.net/zwjsatan/article/details/8101712)


----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***