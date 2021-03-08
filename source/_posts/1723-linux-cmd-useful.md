---
title: 最实用的 Linux 命令行使用技巧
date: 2017-09-07
categories: linux
tags: [linux, command]
description: 如题.
---

***转载自 [最实用的 Linux 命令行使用技巧](https://www.oschina.net/translate/most-useful-linux-command-line-tricks#comments)***
***英文原文 [Most Useful Linux Command Line Tricks](https://dzone.com/articles/most-useful-linux-command-line-tricks)***

----------


# 将输出内容以表格的形式显示出来

可以使用 `cmd | column -t` 指令, 譬如:

``` bash
mount | column –t                   # 默认空格进行制表
cat /etc/passwd | column -t -s:     # 指定冒号进行制表
```


# 重复执行一个命令，直到它运行成功

如果在 Google 上搜索这个功能，你会发现很多人都问到了如何重复执行命令，直到这个命令成功返回并且运行正常。 Google上的建议里就包括 ping 服务器，直到它变得空闲为止，还有就是检查是否有向特定的目录上传了具有特定扩展名的文件，还有就是检查特定的URL是否已经存在，诸如此类的办法。

其实你还可以使用 while true 的循环来实现来实现这个功能：
``` bash
$ while true    # 检测文件是否存在, 直到创建成功
> do
> cat test > /dev/null 2>&1 && break
> done

$ while true    # ping google, 直到成功
> do
> ping -c 1 google.com > /dev/null 2>&1 && break
> done
```
在上面这个示例中，`>/dev/null 2>＆1` 会让程序的输出重定向到 `/dev/ null`。 标准错误和标准输出都会被包含进去。
这是我认为最酷的Linux命令行技巧之一。



# 对进程进行排序

``` bash
ps aux | sort -rnk 4        # 内存资源的使用量排序
ps aux | sort -nk 3         # 按CPU资源的使用量排序
```


# 定时的监视性命令输出

使用 watch 命令，你就可以查看到任何命令的任何输出。例如，你可以查看可用空间以及它的使用量增长情况。
通过利用 watch 命令来操作会变化的数据，你可以尽情想象自己能拿这个来做些什么哦。 譬如

``` bash
watch df -h                 # 实时查看磁盘空间情况
```


# 在会话关掉以后继续运行程序

可以用 nohup 命令做到 - 该指令表示不做挂断操作：
``` bash
nohup wget site.com/file.zip
nohup ping -c 10 google.com
# 会在同一个目录下生成一个名称为 nohup.out 的文件，其中包含了正在运行的程序的输出内容
```


# 自动对任何命令回答 Yes 或者 No

``` bash
yes | apt-get update
no | apt-get update
```


# 创建具有指定大小的文件

``` bash
dd if=/dev/zero of=out.txt bs=1M count=10
# 创建出一个 10 MB 的文件，填充零作为内容
```


# 以根目录用户来运行最后一个命令

有时，你会忘记在需要 root 权限的命令之前敲入 sudo。 这时候你没必要去重写命令;
只要输入 `sudo !!` 就行了！

``` bash
cat /etc/shadow
!!                  # 重复执行最后一条指令 cat /etc/shadow
sudo !!             # 等同于最后一条指令前面加上sudo
```


# 对命令行会话进行记录

如果想要把自己在 shell 屏幕上敲的内容记录下来，可以使用 `script` 命令
将所有敲写的内容保存到一个名为 `typescript` 的文件中去。
等你敲入 `exit` 命令以后，所有命令就都会被写入该文件，以便你事后再回过头去查看。

``` bash
script
# Script started, file is typescript
ll                  # normal cmd, will be　saved to typescript
exit                # exit script
# Script done, file is typescript

cat typescript      # show what you do
```


# 用标签符号替换空格符

可以使用 tr 命令替换任何字符，这个用起来非常方便：
``` bash
cat typescript | tr ' ' '\t' > out      # 空格替换为制表符, 保存为out文件
cat myfile | tr a-z A-Z> output         # 大小写转换
```


# 强大的 Xargs 命令

xargs 命令是最重要的 Linux 命令行技巧之一。你可以使用这个命令将命令的输出作为参数传递给另一个命令。例如，搜索 png 文件然后对其进行压缩或者其它操作：
`find. -name *.png -type f -print | xargs tar -cvzf images.tar.gz`

又或者你的文件中有一个 URL 的列表，而你想要做的是以不同的方式下载或者处理这些 URL，可以这样做：
`cat urls.txt | xargs wget`

请你要记得，**第一个命令的输出会在 xargs 命令结尾处传递**。
那如果命令需要中间过程的输出，该怎么办呢？这个简单！
只需要使用 `xargs -i` 并结合 `{}` 就行了。如下所示，替换在第一个命令的输出应该去的地方的参数：
`ls /etc/*.conf | xargs -i cp {} /home/out`


# 其它指令

``` bash
cd -                        # 回到你操作过的上一个目录去
getconf LONG_BIT            # 检查机器架构的位数 32/64
```


----------

***转载自 [最实用的 Linux 命令行使用技巧](https://www.oschina.net/translate/most-useful-linux-command-line-tricks#comments)***
***英文原文 [Most Useful Linux Command Line Tricks](https://dzone.com/articles/most-useful-linux-command-line-tricks)***