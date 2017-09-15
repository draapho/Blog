---
title: linux文件与目录相关指令
date: 2016-12-16
categories: linux
tags: [linux, command]
---

# linux 文件基础

## 特殊符号代表的目录:

| 特殊符号       | 目录                     |
| ---------- | ---------------------- |
| `.`        | 代表此层目录                 |
| `..`       | 代表上一层目录                |
| `~`        | 代表**目前使用者**所在的家目录      |
| `~account` | 代表**account**这个使用者的家目录 |
| `~+`       | 当前的工作目录, 等同于`pwd`      |
| `~-`       | 上次的工作目录                |

## 文件类型

| bit9 | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| -    | r    | w    | x    | r    | -    | x    | -    | -    | -    |


| bit  | 字母    | 说明                         |
| ---- | ----- | -------------------------- |
| 9    |       | 文件类型                       |
|      | `d`   | 目录(dir)                    |
|      | `-`   | 文件                         |
|      | `l`   | 链接文件(link)                 |
|      | `b`   | 块设备文件(block)               |
|      | `c`   | 字符设备文件(character)          |
|      | `s`   | 网络接口文件(sockets)            |
|      | `p`   | 管道文件(FIFO, pipe)           |
| 876  | `rwx` | 拥有人的权限, r为可读, w为可写, x为可执行  |
| 543  | `r-x` | 同群组的权限, r为可读, -为不可写, x为可执行 |
| 210  | `---` | 其它群组权限, 不可读, 不可写, 不可执行     |


# 文件与目录常用指令

| 指令                                       | 说明                                   |
| ---------------------------------------- | ------------------------------------ |
| `cd`                                     | **Change Directory**, 变换目录           |
| `pwd`                                    | **Print Working Directory**, 显示目前的目录 |
| ...... **`pwd -P`**                      | 显示真实路径, 而非link路径                     |
| `mkdir dir`                              | Make Directory, 建立一个新的目录             |
| ...... **`mkdir -p dir1/dir2`**          | 递归建立所有目录                             |
| ...... **`mkdir -m 711 dir`**            | 建立目录时,设定权限                           |
| `rmdir dir`                              | **Remove Directory**, 删除一个空的目录       |
|                                          |                                      |
| `ls`                                     | **List Files**, 显示文件与目录              |
| ...... **`ls -h`**                       | 以KB,GB显示容量.                          |
| ...... **`ls -R`**                       | Recursive, 递归显示子目录信息                 |
| ...... **`ls -t`**                       | 以时间排序                                |
| ...... **`ls -S`**                       | 以容量大小排序                              |
| ...... **`ll`**                          | `ls –al`, List All, 显示所有文件及信息        |
| `cp src dst`                             | copy                                 |
| ...... **`cp -a src dst`**               | 即`cp -pdr`, 递归复制目录.不会改变属性和权限         |
| ...... **`cp -f src dst`**               | Force, 强制复制,不询问使用者                   |
| ...... **`cp -u src dst`**               | 若 src比dst新,才进行复制工作,多用于备份             |
| ...... **`cp src1 src2 src3 dir`**       | 将多个原文件拷贝到指定目录                        |
| `mv src dst`                             | **move**, 移动目录和文件                    |
| `rm file_dir`                            | **remove**, 移除文件                     |
| ...... **`rm -fr dir`**                  | 强制递归删除dir下的所有文件和目录                   |
| `ln -s src dst`                          | **Symbolic Link**, 创建一个符号链接          |
| ...... **`ln file hardLink`**            | 实际链接, 仅支持同区块下的文件,不占用inode            |
| ...... **`ln -s dir symbolicLink`**      | 符号链接, 同快捷方式,为一个文件,占用inode            |
| `basename /dir/dir/file`                 | 结果为`file`, 路径中取得文件名称                 |
| `dirname /dir/dir/file`                  | 结果为`/dir/dir`, 路径中取得目录名称             |
|                                          |                                      |
| `cat file`                               | **Concatenate** (连续), 连续显示文件内容       |
| ...... **`cat -n file`**                 | 在前面加上行号                              |
| ...... **`cat -A`**                      | 即 `cat -vET`, 可显示一些特殊符号              |
| `more` `less` `head` `tail`              | 都用于显示文件内容, `less`功能最强大               |
| `od -t x1 file`                          | 按1byte 十六进制显示文件.若x2则为2byte.          |
| `touch file`                             | 建立一个空文件, 修改文件时间(mtime和atime)         |
| `file file`                              | 读取文件类型                               |
|                                          |                                      |
| `umask`                                  | 读取和设置当前默认权限, 数字是被取消的默认权限             |
| ...... **`umask 022`**                   | 新建文档权限为 777-022 = 755权限              |
| `chgrp -R group file_dir`                | 递归改变file_dir文件/目录的群组(group必须存在)      |
| `chown owner file_dir`                   | 改变文件或目录的所有者(owner必须存在)               |
| ...... **`chown -R owner:group dir`**    | 递归改变dir的所有者和组群                       |
| ...... **`chmod -R 755 file_dir`**       | 递归改名文件或目录的权限 (7=0b111=rwx)           |
|                                          |                                      |
| `which -a cmd`                           | 搜索执行文件完整路径                           |
| `whereis file`                           | 快速搜索文件(用数据库),实测下来没啥用                 |
| `find dir -name file`                    | 搜索文件(整个硬盘),很强大的一个指令                  |
| ...... **`-name`**                       | 表示按文件名搜索. 类似的参数有很多.有需要在查.            |
| `grep pattern files`                     | 在files中寻找 pattern项,支持正则表达式           |
| ...... **`grep -r “hello” ./*`**         | 在当前文件夹下的所有文件下搜索 “hello”              |
| ...... **`grep -n “Test” *`**            | 在当前文件夹下搜索 “hello”, 并显示行号           |
| ...... **`grep -i “Bye” *`**             | 在当前文件夹下忽略大小写搜索 ”Bye”                 |
| ...... **`grep -w “Test” aa bb`**        | 在aa, bb文件内,只匹配整个单词搜索 “Test”          |
| ...... **`grep -nd skip 100ask24x0 *`**  | 仅在当前目录查找, 不显示子目录信息 |
| `find ./ -name "*" l(竖杠) xargs grep --color "key"` | 在当前文件夹下查找包含 "key" 内容的文件       |
|                                          |                                      |
| `tar -cvf file.tar /dir`                 | 将/dir打包为file.tar,没有压缩                |
| `tar -zcvf file.tar.gz /dir`             | 将/dir打包为file.tar.gz,用gzip压缩          |
| `tar -jcvf file.tar.bz2 /dir`            | 将/dir打包为file.tar.gz2,用bzip2压缩        |
| `tar -xvf file.tar`                      | 还原file.tar到当前目录                      |
| `tar -zxvf file.tar.gz`                  | 解压file.tar.gz到当前目录                   |
| `tar -jxvf file.tar.bz2`                 | 解压file.tar.bz2到当前目录                  |
| `tar -N ‘2005/06/01’ -zcvffile.tar.gz /dir` | 将/dir下比2005/06/01新的文件备份              |
| `cpio`                                   | 文件/设备的输入输出, 多配合find进行备份              |

- **`find ./ -name "*" | xargs grep --color "key"`** 在当前文件夹下查找包含 "key" 内容的文件
- **`find / -print | cpio -covB > /dev/st0`** , 将系统数据全部写入磁带机



----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***