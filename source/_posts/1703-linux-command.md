---
title: Unix/Linux 命令参考
date: 2017-01-19
categories: linux
tags: [embedded, linux, cheat sheet]
description: 如题.
---


***转载自 [Unix/Linux 命令速查表](https://linuxtoy.org/pages/download.html)***

----------

# 搜索指令 `find` `grep`
``` bash
find -name april*                   # 当前目录下查找以april开始的文件
find -iname april*                  # 忽略大小写
find /home -size +512k              # 查大于512k的文件
find /home -size -512k              # 查小于512k的文件
find /home -links +2                # 查硬连接数大于2的文件或目录
find /home -perm 0700               # 查权限为700的文件或目录

find -name tom.txt -user kim        # 查找名称为tom.txt且用户为kim的文件
find -name ap* -or -name may*       # 查找以ap或may开头的文件
find -name wa* -not -type l         # 查找名为wa开头且类型不为符号链接的文件
find -name wa* ! -type l            # 查找名为wa开头且类型不为符号链接的文件
# 对于 -type, 有 b=block, d=dictory, c=character, p=pipe, l=link, f=file

find / -iname "MyCProgram.c" -exec md5sum {} \; # 对所有找到的文件进行MD5验证
find / -name filename -ok rm -rf {} \;          # 确认删除找到的文件
find . -mtime +3 | xargs rm -rf                 # 删除3天以前的文件
find . -size +3000k -exec ls -ld {} \;          # 查找大于3M的文件
find . -size -3000k | xargs echo "" >./file.log # 查找小于3M的文件并写入file.log
find . -type f | xargs grep "hostname"          # 在普通文件中搜索hostname这个词
```

``` bash
ls -l | grep '^a'                   # 只显示以a开头的文件名。
grep 'test' d*                      # 显示所有以d开头的文件中包含test的行。
grep 'test' aa bb cc                # 显示在aa，bb，cc文件中匹配test的行。
grep -i pattern files               # 不区分大小写地搜索。默认情况区分大小写
grep -l pattern files               # 只列出匹配的文件名，
grep -L pattern files               # 列出不匹配的文件名，
grep -w pattern files               # 只匹配整个单词(如匹配‘magic’，而不是‘magical’)
grep -C number pattern files        # 匹配的上下文分别显示[number]行，
grep pattern1 | pattern2 files      # 显示匹配 pattern1 或 pattern2 的行，
grep pattern1 files | grep pattern2 # 显示既匹配 pattern1 又匹配 pattern2的行
```

# 常用命令表
文件命令 | 指令说明
------|----------
`ls`|列出目录
`ls -al` | 使用格式化列出隐藏文件
`cd dir` | 更改目录到 dir
`cd` | 更改到 home 目录
`pwd` | 显示当前目录
`mkdir dir` | 创建目录 dir
`rm file` | 删除 file
`rm -r dir` | 删除目录 dir
`rm -f file` | 强制删除 file
`rm -rf dir` | 强制删除整个目录 dir (小心使用)
`cp file1 file2` | 将 file1 复制到 file2
`cp -r dir1 dir2` | 将 dir1 复制到 dir2; 如果 dir2 不存在则创建它
`mv file1 file2` | 将 file1 重命名或移动到 file2;
`ln -s file link` | 创建 file 的符号连接 link
`touch file` | 创建 file
`cat > file` | 将标准输入添加到 file
`more file` | 查看 file 的内容
`head file` | 查看 file 的前 10 行
`tail file` | 查看 file 的后 10 行
`tail -f file` | 从后 10 行开始查看 file 的内容
**进程管理**|**指令说明**
`ps` | 显示当前的活动进程
`top` | 显示所有正在运行的进程
`kill pid` | 杀掉进程 id pid
`killall proc` | 杀掉所有名为 proc 的进程 (小心使用)
`bg` | 列出已停止或后台的作业
`fg` | 将最近的作业带到前台
`fg n` | 将作业 n 带到前台
**文件权限**|**指令说明**
`chmod rwxrwxrwx file` | 更改 file 的权限
`chmod 777` | 为所有用户添加 rwx 权限
`chmod 755` | 为所有者添加 rwx 权限, 为组和其他用户添加 rx 权限
**SSH**|**指令说明**
`ssh user@host` | 以 user 用户身份连接到 host
`ssh -p port user@host` | 在端口 port 以 user 用户身份连接到 host
`ssh-copy-id user@host` | 将密钥添加到 host 以实现无密码登录
**系统信息**|**指令说明**
`date` | 显示当前日期和时间
`cal` | 显示当月的日历
`uptime` | 显示系统从开机到现在所运行的时间
`w` | 显示登录的用户
`whoami` | 查看你的当前用户名
`finger user` | 显示 user 的相关信息
`uname -a` | 显示内核信息
`cat /proc/cpuinfo` | 查看 cpu 信息
`cat /proc/meminfo` | 查看内存信息
`man command` | 显示 command 的说明手册
`df` | 显示磁盘占用情况
`du` | 显示目录空间占用情况
`free` | 显示内存及交换区占用情况
**压缩**|**指令说明**
`tar cf file.tar files` | 创建包含 files 的 tar 文件 file.tar
`tar xf file.tar` | 从 file.tar 提取文件
`tar czf file.tar.gz files` | 使用 Gzip 压缩创建 tar 文件
`tar xzf file.tar.gz` | 使用 Gzip 提取 tar 文件
`tar cjf file.tar.bz2` | 使用 Bzip2 压缩创建 tar 文件
`tar xjf file.tar.bz2` | 使用 Bzip2 提取 tar 文件
`gzip file` | 压缩 file 并重命名为 file.gz
`gzip -d file.gz` | 将 file.gz 解压缩为 file
**网络**|**指令说明**
`ping host` | ping host 并输出结果
`whois domain` | 获取 domain 的 whois 信息
`dig domain` | 获取 domain 的 DNS 信息
`dig -x host` | 逆向查询 host
`wget file` | 下载 file
`wget -c file` | 断点续传
**安装**|**指令说明**
`./configure` `make` `make install` | 从源码安装
`dpkg -i pkg.deb` | 安装包 (Debian)
`rpm -Uvh pkg.rpm` | 安装包 (RPM)
`yum install package` | 安装包 (CentOS)
`sudo apt-get install package` | 安装包 (Ubuntu)
**快捷键**|**指令说明**
`Ctrl+C` | 停止当前命令
`Ctrl+Z` | 停止当前命令，并使用 fg 恢复
`Ctrl+D` | 注销当前会话，与 exit 相似
`Ctrl+W` | 删除当前行中的字
`Ctrl+U` | 删除整行
`!!` | 重复上次的命令
`exit` | 注销当前会话


----------

***转载自 [Unix/Linux 命令速查表](https://linuxtoy.org/pages/download.html)***