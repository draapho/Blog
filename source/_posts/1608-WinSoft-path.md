---
title: Windows 软件系列-自定义环境变量
date: 2016-10-9
categories: windows
tags: [windows, path]
---


# 自定义环境变量
- 测试过几个例子, 简单的调用没问题, 但带参调用就会有各种无法预料的问题.
- `ConEmu.lnk` 后面不支持带参数, `git-cmd.lnk` 支持带参, 但有奇怪现象.
- `Typora.lnk` `zeal.lnk` 没有问题.
- 使用此方法可以配合 `win-r` 快速打开文件夹, 软件等功能! 我没有使用, 因为有更好的替代方案.
- !!!注意!!!, 带参调用 `.lnk` 不完全等同于 `.exe`, 还是没有linux的链接来的便捷

## 前言
- 做软件开发是绕不过环境变量 `PATH` 的设置的, 经常到后来 `PATH` 就变得非常长, 难以管理维护.
- 借助linux链接的概念, 实验了一下windows的快捷方式是否也可以用命令行执行, 发现是可行的!
- 譬如创建 `ConEmu.exe` 的快捷方式 `ConEmu.lnk` (.lnk不会显示). 此时, 在cmd内执行 `ConEmu.lnk` 等同于执行 `ConEmu.exe`
- 这样, 就有办法简化自定义 `PATH` 的数量了, 只需添加一个用户路径到 `PATH` 中, 如`D:\Green\userpath\bin`, 然后把用户软件的 `.exe` 和 `.lnk` 放到这个目录下面就可以了.

## 设置
- 譬如, 配置 `D:\Green\cli\bin` 到环境变量中.
- `我的电脑`->右键`属性` 或者 `控制面板`->`系统和安全`->`系统`->`高级系统设置`
- 弹出 `系统属性` 页面->`高级` 标签->最下面 `环境变量...`->`系统变量`->`Path`->加入自定义路径如 `D:\Green\cli\bin`, windows7的话需要分隔符`;`
- `D:\Green\cli\bin` 只是个例子, 可以自己规定任意一个文件夹, 便于记忆即可.

## 添加软件
- MinGW, windows下提供 gnu 工具链, 像linux下一样使用 make 编译即可
  把 `.\MinGW\bin` 下的所有文件复制一份到 `D:\Green\cli\bin` 即可
- Pandoc, 格式转换软件. 众多markdown编辑器需要此软件来转换格式
  把 `pandoc.exe` 和 `pandoc-citeproc.exe` 复制一份到 `D:\Green\cli\bin` 即可
- putty, ssh和串口终端软件, 多用于远程连接
  ~~putty所有文件复制一份到 `D:\Green\cli\bin`~~, 放个 `putty.exe` 即可
- uncrustify, 编程语言格式化软件. 可格式化 c, c++, d, java 等众多语言
  把 `uncrustify.exe` 复制到 `D:\Green\cli\bin` 即可
- 下述软件创建快捷方式, 然后放到 `D:\Green\cli\bin` 即可
- ~~`ConEmu.lnk`~~ 模拟终端软件, 可整合多种终端如cmd, shell, bash, putty
- ~~`Cygwin.lnk`~~ 模拟linux环境, 可以部分充当windows下的linux虚拟机使用
- ~~`git-cmd.lnk`~~ 启动git, 供ConEmu调用
- `Typora.lnk` 一款markdown编辑器
- `zeal.lnk` 软件API离线查询工具, windows下的dash

## 便捷性
- 上述软件主要是辅助作用, 我会在常用软件中调用上述软件. 如notepad++, atom, ConEmu中
- 以 notepad++ 调用 `zeal.lnk` 为例.
- `notepad++`->`Run`->`Run...`->输入 `zeal.lnk $(CURRENT_WORD)`->`Save...`->`Name:``help`, 快捷键`F1`->`OK`
- 配置好以后, 写代码遇到需要查询的地方, 只要选中关键词, 按 `F1` 就会自动调用 zeal 了
- 以后环境变了, 只需要重新创建一下 `zeal.lnk` 然后放到 `D:\Green\userpath\bin` 即可.


----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***
