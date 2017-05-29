---
title: 嵌入式linux环境搭建2-CentOS7
date: 2017-02-19
categories: embedded linux
tags: [embedded linux, environment]
---


# 环境及结论

- 大环境的搭建思路可参考[嵌入式linux环境搭建](https://draapho.github.io/2017/02/16/1705-linux-env/)
  - gateway ip `10.0.0.138`
  - PC windows: win10 64bit, ip `10.0.0.98`
  - PC linux(最终版本): ubuntu server 16.04 32 bit, ip `10.0.0.100`
  - Embedded Linux: jz2440v3 ip `10.0.0.111`
- 目的是尝试不同linux系统下的环境搭建
- 使用环境: CentOS7 64bit (安装在win10的虚拟机内)
- kernel make 失败
- 彻底死机一次
- 没法直接安装 u-boot-tools
- 彻底放弃! 转战Ubuntu
- 不知是 centos 做 2440 的交叉编译兼容性不好, 还是64bit linux的兼容性不好. 或者两者皆有!


# 安装必要的软件
静态ip, 安装向导时, 就设置了.

``` bash
yum install net-tools 	# to use ifconfig  or use ip addr
yum install bzip2		# bz2压缩格式
yum install patch
yum install gcc

# 64位系统要安装了32位程序, 安装如下软件
yum install glibc.i686
yum install libstdc++.so.6
```

# 安装nfs客户端

可以参考: [NFS server and client installation on CentOS 7](https://www.howtoforge.com/nfs-server-and-client-on-centos-7)

``` bash
# 安装nfs工具, 服务器和客户端都装这个
yum install nfs-utils

# 创建用于mount的节点
mkdir -p /mnt/nfs/study
mkdir -p /mnt/nfs/work

# 启动服务
systemctl enable rpcbind
systemctl enable nfs-server
systemctl enable nfs-lock       # No such file or directory, 但没影响
systemctl enable nfs-idmap      # No such file or directory
systemctl start rpcbind
systemctl start nfs-server
systemctl start nfs-lock
systemctl start nfs-idmap

# 手动mount
mount -t nfs 10.0.0.98:/study /mnt/nfs/study/
mount -t nfs 10.0.0.98:/work /mnt/nfs/work/

# 确认结果
df -kh

# 设置为开机自动加载
vi /etc/fstab
    # ===== 文件内容, 加入如下两句 =====
    10.0.0.98:/study   /mnt/nfs/study  nfs defaults 0 0
    10.0.0.98:/work    /mnt/nfs/work   nfs defaults 0 0
    # ===== 结束修改, 保存退出vim =====

// 建立软连接(快捷方式)
cd /home/user/
sudo ln -s /mnt/nfs/study study
sudo ln -s /mnt/nfs/work work
```


# 安装 mkyaffs2image

该工具用于制作文件系统镜像文件
文件系统烧录到开发板flash时需要使用镜像文件

``` bash
cp mkyaffs2image /bin/                         # 拷贝到bin
chmod +x /bin/mkyaffs2image                    # 增加可执行权限
mkyaffs2image                                       # 测试是否可用
```


# 安装及使用交叉编译工具gcc

## 安装 arm-linux-gcc-3.4.5

使用指定的 `arm-linux-gcc-3.4.5-glibc-2.3.6`. 不要用新版本, 有坑.

``` bash
# 安装 gcc
mv arm-linux-gcc-3.4.5-glibc-2.3.6.tar.bz2 /usr/local/arm/
cd /usr/local/arm/
tar -xjf arm-linux-gcc-3.4.5-glibc-2.3.6.tar.bz2

# 添加路径到环境变量
vi /etc/bashrc
    # ===== 文件内容, 末尾加入如下语句 =====
    if [ -d /usr/local/arm/gcc-3.4.5-glibc-2.3.6 ] ; then
        PATH=/usr/local/arm/gcc-3.4.5-glibc-2.3.6/bin:"${PATH}"
    fi
    # ===== 结束修改, 保存退出vim =====
    
# 测试安装结果
source /etc/bashrc							# 不重启更新PATH
echo $PATH									# 查看PATH
arm-linux-gcc -v							# 测试是否安装成功
```

## 遇到问题

在centos下, 内核 make clean 会报错: Makefile‘混和的隐含和普通规则’
我想还是因为 2440 内核文件使用的makefile太老了. 和centos兼容性不好.
按下述方法改了一点后, 最后make还是失败了. 因而放弃 centos 系统.

``` bash
# 修改根目录下的 Makefile
/ %/: prepare scripts FORCE
    $(Q)$(MAKE) KBUILD_MODULES=$(if $(CONFIG_MODULES),1) \
    $(build)=$(build-dir)
# 改成： ----->
/: prepare scripts FORCE
    $(Q)$(MAKE) KBUILD_MODULES=$(if $(CONFIG_MODULES),1) \
    $(build)=$(build-dir)
%/: prepare scripts FORCE
    $(Q)$(MAKE) KBUILD_MODULES=$(if $(CONFIG_MODULES),1) \
    $(build)=$(build-dir)

# 把：
config %config: scripts_basic outputmakefile FORCE
    $(Q)mkdir -p include/linux include/config
    $(Q)$(MAKE) $(build)=scripts/kconfig $@
# 改成： ----->
config: scripts_basic outputmakefile FORCE
    $(Q)mkdir -p include/linux include/config
    $(Q)$(MAKE) $(build)=scripts/kconfig $@
%config: scripts_basic outputmakefile FORCE
    $(Q)mkdir -p include/linux include/config
    $(Q)$(MAKE) $(build)=scripts/kconfig $@
```





----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***