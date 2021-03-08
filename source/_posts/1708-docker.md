---
title: Docker 初学笔记
date: 2017-02-23
categories: software
tags: [docker]
description: 如题.
---

# Docker 总览

## 几个重要概念

- Docker: 是一种容器技术, 可以提供虚拟服务. 物理上共享主机的硬件和网络资源.
  相比于虚拟机技术, 它轻巧, 快速, 便捷, 跨平台, 易于分配发布. 又同时拥有虚拟机的优点!
  由于以上特点, 目前docker的容器有蚕食传统软件的趋势: 提供服务时, 给的是docker镜像或容器而非传统的安装软件!
  譬如, 我学习docker的初衷就是: **一劳永逸的制作一个用于开发2440系列编译环境的pc linux系统**
  可以看出, 我需求就是提供编译服务. 传统的安装软件无法简单的实现, 但docker可以! (目前用的vm, 太重太麻烦)
- Union FS (分层存储): 本质是增量管理. 基于原有的运行系统, 执行某些命令后, 把新产生的文件作为增量新建一层文件.
  直观感受一下, 是这样的:
![docker-aufs](https://draapho.github.io/images/1708/docker-aufs.jpg)
- **images (镜像)**: docker 以镜像为基础. 镜像是只读的, 不包含任何动态数据, 内容不可更改!
  基于基础镜像, 可以在加入自己需要的app和服务后, 打包成自己的具有特殊功能的镜像.
- **container (容器)**: 容器就是镜像运行时的实体 (类似于类和实例的关系).
  容器必须基于镜像运行. 可以基于同一个镜像创建多个容器, 来实现不同的功能或服务.
  容器可以被创建, 启动, 停止, 删除, 暂停等等
  容器的本质就是进程, 运行时实现某种功能, 只是这个进程的上下文用的是虚拟化的镜像环境.
- **Docker Registry (仓库)**: 用于存储, 分发镜像的仓库.
  其中 [Docker Hub](https://hub.docker.com/) 就是官方的镜像仓储服务.
  其运行模式和 [github](https://github.com/) 一样, 公开资料免费, 私有资料收费
  当然, 也可以建立自己的私有 Docker Registry
- **Docker Volume**, Docker的数据服务.
  docker 体系要让自己表现更像应用程序, 就离不开对数据的存储和隔离.
  而docker容器是非持久化的, 可以随时创建和删除, 无法满足数据存储的基本要求.
  因此提供了Docker Volume. 包括 data volume 和 data volume container


## docker的技术架构

![docker-structure](https://draapho.github.io/images/1708/docker-structure.jpg)

- Docker Client / Docker Daemon: 用户和Docker的交互使用的是C/S模式.
  用户作为客户端使用 http 服务和 Docker Daemon 进行交互
- Engine 和 Job: Job本质就是进程. 基于容器, 运行任务.
  譬如, 对 Docker Registry 的操作就是作为一个job任务实现的.
- Docker Registry: 用于存储, 分发镜像的仓库
- Graph: Graph对已下载Docker镜像进行保管, 并对已下载容器镜像之间关系进行记录.
  Graph不但要存储本地具有版本信息的文件系统镜像,
  而且还要通过GraphDB记录所有文件系统镜像彼此之间的关系
- Driver: 驱动模块. Driver驱动主要作用是实现对Docker容器进行环境的定制
- Docker container: Docker容器是Docker架构中服务交付的最终体现形式
  Docker按照业务的需求, 依赖关系和配置文件打包相应的Docker容器


## 初步评估结论

- 感觉docker 的野心和潜力都很大. 如镜像管理, 跨平台, 容器应用化, 功能化, 服务化.
- 可以看出主要发展方向是网络和云方面的 (新的项目都是针对网络集群的).
- 基本已经可以跨平台使用(Docker machine).
- 我的初衷就是: **一劳永逸的制作一个用于开发2440系列编译环境的pc linux系统**
  就此而言, docker可用, 但初始配置并不轻松.
  因此暂不急于使用docker来配置这么一个主机编译环境.


# Docker 的安装

全程参考官网
[Get started with Docker](https://docs.docker.com/engine/getstarted/)

## Windows 10 64bit 直接安装

可直接下载安装 docker, 无需安装在虚拟机下面. 家中的win10是家庭版, 但也能正常安装运行docker.

使用默认设置就能运行, 说一下文件共享. 譬如勾选 `E` 盘共享后, shell 应该这样用:
``` bash
# docker下, 显示E盘全部内容
docker run -v e:/:/data alpine ls /data
# e:/       表示使能的windows e盘.
# :/data    docker容器下, 加载为 /data 目录
# alpine    一个小巧的linux内核, 基于此内核运行指令. 改为ubuntu效果也是一样的
# ls /data  在屏幕上列出 /data (就是e盘) 的内容

# 因此, 官网范例表示, 显示 c:/Users 下的内容
docker run -v c:/Users:/data alpine ls /data
```

## ToolBox 基于虚拟机的安装

参考[Install Docker Toolbox on Windows](https://docs.docker.com/toolbox/toolbox_install_windows/)
- 机器要求: 64bit 操作系统, 支持并使能IVT虚拟技术
- Windows Vista 及以上版本, 安装默认的 NDIS6 driver 即可.
- Windows 7 和 Windows XP, 安装时勾选 **NDIS5 driver**
- 里面也提到了卸载ToolBox时, 如何先删除虚拟机里的 dock-machine

使用虚拟机后的文件共享很简单, 在 `VirtualBox`->`Settings`->`Shared Folders` 直接修改好就行了.

使用 putty 登录docker虚拟机
- 不太喜欢 Docker Quickstart Terminal 提供的终端, 用起来不顺手(不能用鼠标, 不能复制黏贴)
  不过只有在这个终端里, 能直接使用 `docker-machine` 相关的指令
- 自己使用ConEmu统一了终端, 里面集成好putty. 因此需要使用ssh.
- 获取 boot2docker 的IP地址.
  运行 Docker Quickstart Terminal 成功后, 终端上可以找到这样一句话
  `docker is configured to use the default machine with IP 10.0.0.100`
  或者, 输入 `docker-machine ls`, 找到其IP地址. 譬如 `tcp://10.0.0.100:2376`
  或者, 直接登录boot2docker虚拟机, 输入指令 `ifconfig` 查看IP地址.`10.0.0.100`
- boot2docker的登录名默认就是 `docker`. 如果需要密码的话, 应该是 `tcuser`
- 运行过 Docker Quickstart Terminal 后, docker自动生成了ssh密钥.
  一般存储在 `C:\Users\my_name\.docker\machine\machines\default\ ` 或者 `%HOMEPATH%\.ssh`下面
  `id_rsa` 是私钥, `id_rsa.pub` 是公钥
- 打开 `puttygen.exe`->`Load an existing private key file`->`Load`->选择文件格式为 `All Files (*.*)`->选择`id_rsa`->弹出框 `OK`
  接着 `puttygen.exe` 主界面下->`Save private key`->保存为`id_rsa.ppk`
- 打开 `putty.exe`->左边`Connection`->`SSH`->`Auth`->右边`Private key file for authentication`->`Browse...`->选择`id_rsa.ppk`
  接着 `putty.exe`->左边`Session`->右边`Connection type:`点选`SSH`->`Host Name (or IP address)`填如`docker@10.0.0.100`->`Port`填入`22`
  最后 `Saved Sessions` 填入期望的名称如 `boot2docker`->`Save`->`Open`->连接成功!



# Docker 常用指令

可参考:
- [Docker命令指令详情-持续更新](http://www.dockerinfo.net/341.html)
- [Docker — 从入门到实践](https://yeasy.gitbooks.io/docker_practice/content/install/ubuntu.html)


## 镜像指令

``` bash
# 从 Docker Hub 获取 ubuntu 16.04 的镜像
docker pull ubuntu:16.04

# 列出所有镜像
docker images

# 运行 ubuntu
docker run -it --rm ubuntu:16.04 bash
# -it： -i, 交互式操作; -t, 显示终端
# --rm： 容器退出后随之将其删除 (不建议)

# 在容器里输入一些指令后, 查看容器的变化
docker diff ubuntu:16.04

# 用commit制作的进行成为黑箱镜像, 如果开源发布, 人们会有安全性的担忧(无法知道到底做了什么)
# 将当前容器制作为镜像 (会把容器内的变动新增一层文件)
docker commit --message "2440 compiler" container_ID_or_name ubuntu:2440
# --message: 可省, 记录本次修改的内容
# contain_ID_or_name: 使用 'docker ps -a' 可查看所有容器信息
# ubuntu:2440 目标镜像:标签

# 查看镜像历史记录
docker history ubuntu:2440

# 保存镜像 (本地文件)
docker save ubuntu:2440 | gzip > ubuntu-2440.tar.gz

# 加载镜像 (本地文件)
docker load -i ubuntu-2440.tar.gz
# 相比后面的 'docker import', 镜像存储文件保存完整记录, 体积要大.

# 删除镜像
docker rmi ubuntu:2440
# ubuntu:2440 目标镜像:标签. 这里也可以用镜像ID代替(短ID也行)

# 删除所有在 'mongo:3.2' 之前的镜像 (windows下不可用)
docker rmi $(docker images -q -f before=mongo:3.2)
```


## 容器指令

``` bash
# 输出 "hello world"
docker run ubuntu echo 'Hello world'

# 运行 ubuntu
docker run -it ubuntu:16.04 bash
# -it： -i, 交互式操作; -t, 显示终端

# 后台运行
docker run -d ubuntu sh -c "while true; do echo hello world; sleep 1; done"
# 会返回container的ID号
# -d: 后台运行, 不输出结果到主机界面上
# sh -c: 作为sh文件执行

# 获取容器的输出信息
docker logs container_ID_or_name

# 查看容器信息 (print server)
docker ps -a
# -a 表示显示所有容器状态(包括终止状态)

# 容器的终止,启动和重启
docker stop container_ID_or_name
docker start container_ID_or_name
docker restart container_ID_or_name

# 进入指定容器
docker attach container_ID_or_name
# attach 在多窗口时很不方便. 参考资料推荐的是nsenter (windows下不可用)

# 导出容器
docker export container_ID_or_name > ubuntu.tar
# 导入容器快照到本地镜像库
cat ubuntu.tar | docker import - test/ubuntu:v1.0
# 相比前面的 'docker load', 容器快照将丢弃历史记录. 另外, 可以重新指定标签.

# 删除容器
docker rm container_ID_or_name

# 删除所有容器 (windows下不可用)
docker rm $(docker ps -qa)

# 获取某个容器的PID信息 (windows下不可用)
docker inspect --format '{{ .State.Pid }}' container_ID_or_name

# 获取某个容器的 IP 地址 (windows下不可用)
docker inspect --format '{{ .NetworkSettings.IPAddress }}' container_ID_or_name

# 目前 Docker 并没有提供直接的对容器 IP 地址的管理支持
```

## 其它指令和功能

[Docker — 从入门到实践](https://yeasy.gitbooks.io/docker_practice/content/install/ubuntu.html)
- [使用 Dockerfile 定制镜像](https://yeasy.gitbooks.io/docker_practice/content/image/build.html)
- [Dockerfile 指令详解](https://yeasy.gitbooks.io/docker_practice/content/image/dockerfile/)
- [Docker Hub 基本操作及自动创建](https://yeasy.gitbooks.io/docker_practice/content/repository/dockerhub.html)
- [Docker Registry 构建私有仓库](https://yeasy.gitbooks.io/docker_practice/content/repository/local_repo.html)
- [Docker Volumn 数据卷的操作](https://yeasy.gitbooks.io/docker_practice/content/data_management/volume.html)
- [Docker Volumn Container 数据卷容器的操作](https://yeasy.gitbooks.io/docker_practice/content/data_management/container.html)
- [使用网络-外部访问容器](https://yeasy.gitbooks.io/docker_practice/content/network/port_mapping.html)
- [使用网络-容器互联](https://yeasy.gitbooks.io/docker_practice/content/network/linking.html)
- [高级网络配置](https://yeasy.gitbooks.io/docker_practice/content/advanced_network/)
- [高级网络配置-网络相关命令列表](https://yeasy.gitbooks.io/docker_practice/content/advanced_network/quick_guide.html)
- [常见问题总结](https://yeasy.gitbooks.io/docker_practice/content/appendix/faq/)



# 资料和参考

[Docker — 从入门到实践](https://yeasy.gitbooks.io/docker_practice/content/install/ubuntu.html)
[Docker技术架构详细分析 Docker模块分析](http://www.dockerinfo.net/2117.html)
[Microsoft Windows 安装docker](http://wiki.jikexueyuan.com/project/docker/installation/windows.html)
[Docker命令指令详情-持续更新](http://www.dockerinfo.net/341.html)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
