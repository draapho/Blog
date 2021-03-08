---
title: Windows 软件系列-终端
date: 2016-10-10
categories: windows
tags: [windows, ConEmu, mingw, putty, cygwin]
description: 使用ConEmu打造自己的windows终端.
---


# [ConEmu][ce] 简介
- [ConEmu][ce] 即 Console Emulate, 一款终端模拟器, 完全免费, 可以通过他加载多种终端如 cmd, shell, bash, putty 而且便于管理!
- 简而言之, 凡是喜欢用命令行方式的, windows就请使用这款软件, 分分钟变身geek或者hacker的感觉...
- 右键文件夹打开ConEmu就自动进入此文件夹, `ConEmu Inside` 甚至能嵌入到文件夹中.
- 顺便说一句, cmder就是他的马甲, 核心还是ConEmu.

## 我的ConEmu
- 我希望的ConEmu, 就是想输命令行, 打开ConEmu就行!
- 本文的配置可以在ConEmu中执行:
  - `cmd` `shell` windows自带终端
  - `git` windows下安装好git即可, 包含了`git-bash`
  - `mingw` windows下用gnu工具链编译c, c++
  - `putty` ssh链接远程linux, 串口链接嵌入式linux
  - `cygwin` windows下模拟linux运行环境 (目前尚未使用, 在用传统的虚拟机)
  - 其它指令如: `hexo` 博客使用, `choco` 安装软件使用, `apm` atom下载插件使用.
- 快速在指定文件夹下打开ConEmu, 可在 `Listary` 关联快捷键 `ctrl-~`
- 快速在Notepad++下打开ConEmu, 关联快捷键 `ctrl-~`

## 自制ConEmu绿色版
- 下载 [ConEmu便携版](https://conemu.github.io/)
  - 解压后放在理想的文件夹中. 下面以 `D:\Green\ConEmu` 路径为例.
- 下载 [clink便携版](https://mridgers.github.io/clink/), 用于增强终端操作, 如复制拷贝快捷键等
  - 解压后, 所有文件放入 `D:\Green\ConEmu\ConEmu\clink`, 这里面原来就有个 `Readme.txt`, 说的非常清楚了
- 下载 [git便携版](https://git-scm.com/download/win), 版本管理软件
  - 解压后命名为 `Git` 放到 `D:\Green\ConEmu\plugins`,
- 下载并使用默认设置安装 [mingw](http://www.mingw.org/), 用于在win下使用gnu工具编译
  - 只是装了 `MinGW Installation Manager` (实际上是个绿色软件). 打开后继续安装组件
  - `Basic Setup`->`mingw32-base`和`mingw32-gcc-g++`->左上`Installation`->`Apply changes`->等待安装完成.
  - 我只需要编译c和c++文件, `msys`也已经由git软件实现了, 因此无需安装其它组件了.
  - 然后把整个 `MinGW` 文件夹放到 `D:\Green\ConEmu\plugins`
  - 复制一份 `mingw32-make.exe` 并重命名为 `make.exe`, 这样就能直接用 `make` 指令了
- 下载 [putty.zip](http://www.putty.org/), ssh远程连接软件及串口软件
  - 解压后命名为 `putty` 放到 `D:\Green\ConEmu\plugins`
- 然后需要将上述软件加入环境变量, 这个可以在ConEmu设置中完成!!!
  - 打开ConEmu, `Setting`->`Startup`->`Environment`->`set PATH=%ConEmuBaseDir%\Scripts;%PATH%` 下面加上如下语句
  ```
  # git PATH
  set PATH=%ConEmuDir%\plugins\Git;%PATH%
  set PATH=%ConEmuDir%\plugins\Git\cmd;%PATH%
  # mingw PATH
  set PATH=%ConEmuDir%\plugins\MinGW\bin;%PATH%
  # putty PATH%
  set PATH=%ConEmuDir%\plugins\putty;%PATH%
  ```
  - 这样, ConEmu在启动时, 会自动加入上述软件到PATH中
  - 如果使用 **更通用的做法**, 把上述环境变量删除或注释掉.
- 自制ConEmu绿色版就初步完成, 下面只需要配置了.

## 更通用的做法
- 用上述方法有三个缺点
  - git便携版不支持ssh或GPG免密远程同步, 每次都要求输入用户名和密码, 非常麻烦.
  - 如果不用ConEmu, 那么其它终端, 如atom下的终端就无法使用上述软件.
  - 发现putty会新打开一个窗口, 而不是嵌入到ConEmu中.
- 下载 [git安装版](https://git-scm.com/download/win), 使用默认配置安装即可.
  - 为了便于使用, 建议把git的根目录也加入环境变量, 这样就能直接调用 `git-cmd.exe`
- 设置 `D:\Green\ConEmu\plugins\MinGW\bin` 文件夹到系统环境变量中
- 设置 `D:\Green\ConEmu\plugins\putty` 文件夹到系统环境变量中
- 还可以考虑下载安装 [cygwin](https://www.cygwin.com/) 并加入ConEmu中, 这是一款Windows下的Linux模拟器. 注意安装和卸载都比较麻烦.
## ConEmu的设置
- 所有设置都会存放在 `conEmu.xml` 里, 所以设置的备份很简单
- 首次打开会有设置向导 `fast configuration`, 用于生成 `conEmu.xml`
- 可以在设置好环境变量, 安装好git后, 删除`conEmu.xml`重新运行, 这样ConEmu会自动检测加入`Git bash` 和 `putty`, 省心不少. clink放在指定路径后, 其功能也会自动启用.
- 配置过程如下, 需要图文版可参考 [工具02：cmd的替代品ConEmu+Clink](https://higoge.github.io/2015/07/22/tools02/), 配置上略有区别, 进入 `Settings` 后
  - `Main`->`Appearance`->`Generic`->`Single instance mode (...)`
  - `Main`->`Confirm`->`CLose confirmations`->~~`When running process was detected`~~
  - `Startup`->`Specified named task`->`Bash:: Git bash` 更改打开时默认使用的终端类型
  - `Startup`->`Environment` 启动时, 会加载这里的环境变量. 配置好系统环境变量的话, 可以全部删除
  - 注册鼠标右键 `ConEmu Here` 和 `ConEmu Inside`, 并设置为使用 `Git bash` 启动
    - `Integration`->`ConEmu Here`->`Command:`改为`{Git Bash} -cur_console:n`->`Register`
    - `Integration`->`ConEmu Inside`->`Command:`改为`{Git Bash} -cur_console:n`->`Register`
  - `Integration`->`Default term`->`Force ConEmu as default terminal for console applications`
  - 添加 `tasks`. 选择 `Startup`->`Tasks`, 根据现有例子依样画葫芦即可.
    - `Bash::Git bash`: `git-cmd.lnk --no-cd --command=usr/bin/bash.exe -l -i` 也可以点击`File path...`使用绝对路径替代快捷方式.
    - `Bash::Git bash(Admin)`: `*git-cmd.exe --no-cd --command=usr/bin/bash.exe -l -i` 最前面加个`*`就是管理员权限了.
    - `Putty::default`: `putty.exe` 同样, 可能需要使用绝对路径, 点击`File path...`选择即可
    - `Putty::Ubuntu`: `putty.exe -new_console -load "ubuntu"` 需要putty设置好名为`ubuntu`的session
    - `Cygwin`: `set HOME=d:\cygwin\home\XXX & "d:\cygwin\bin\mintty.exe" -i /Cygwin.ico -` 这条指令没有测试过.


# [Putty][putty]
- [Putty][putty] 可用于ssh连接远程主机, 也支持串口. 使用简单, 完全免费
- putty的配置, 一个配置就是一个`Session`. 可以参考[Putty 工具 保存配置的 小技巧](http://blog.csdn.net/tianlesoftware/article/details/5831605)
- putty免密登录, 没有尝试, 可以参考如下两篇文章.
  - [PuTTY的自动登录设置](https://segmentfault.com/a/1190000000639516)
  - [windows 上用程序putty使用 ssh自动登录linux](http://blog.csdn.net/hxg130435477/article/details/9960187)

## 设置Default
- `Window`->`Lines of scrollback`-`20000`  回看更多历史屏幕信息
- `Window`->`Apperance`->`Vertical line`, `Cursor blinks` 游标闪烁
- `Window`->`Colours`->`Default Backgroud`->`R0 G43 B54` 使用ConEmu背景色
- `Connection`->`Serial`->`Flow control`->`None` 默认串口不用流控制
- `Session`->`Saved Sessions`->输入 `Default Settings`->`Save` 默认值设置完成

## 设置ssh
- `Session`->`Conncection type`选`SSH`->`Host Name (or IP address)`->`10.0.0.99` 或者  `username@10.0.0.99` 来指定登录名
- `Session`->`Saved Session` `Ubuntu`->`Save` 设置好配置名称, 保存即可.
- 如果需要免密登录, 明文的很简单, 调用 `putty.exe -load "session_name" -l "username" -pw "password"` 即可
- 如果需要密码加密, 稍微麻烦点. 参考 [windows 上用程序putty使用 ssh自动登录linux](http://blog.csdn.net/hxg130435477/article/details/9960187). 我不需要这个功能, 略过不表.

## 设置serial
- `Session`->`Conncection type`选`Serial`->`Serial line` `COM4`->`Speed` `9600` 即串口4, 波特率9600
- `Connection`->`Serial`->`Flow control` `None` 这里可以设置其它串口参数, 不支持自动回显.
- `Session`->`Saved Session` `COM4-9600`->`Save` 设置好配置名称, 保存即可.

## 配置的导入和导出
- putty直接把配置存放在注册表中. 所以思路就是导入导出注册表
- cmd下->`regedit`->打开注册表
- 找到 `HKEY_CURRENT_USER\Software\SimonTatham`
- 在 `SimonTatham` 这个节点上点击右键, 选择导出, 保存为`config.reg`. 这里不单单是putty的配置
- 恢复时, 管理员权限执行 `config.reg` 即可

## putty的调用
- 基本用法 `putty.exe -load "session_name"`
- 自动登录 `putty.exe -load "session_name" -l "username" -pw "password"`
- 更多调用方式可查看 `PUTTY.CHM 3.8.x` 包含于下载的`putty.zip`中

## 对比[TeraTerm](https://ttssh2.osdn.jp/index.html.en)
- TeraTerm相比于putty设置显得更复杂, 至少串口的功能比putty的要多一点
- TeraTerm有自己的脚本语句, 可以实现比较复杂的自动化功能
- TeraTerm在ConEmu字体显示有问题.
- putty完全满足需求, 配置简单, 完美兼容ConEmu, 因此没有考虑TeraTerm


# [Cygwin](https://www.cygwin.com/)
- 是windows下的unix仿真环境, 可以用来做交叉编译, 因此可替代虚拟机安装linux.
- 安装, 可以参考 [cygwin介绍、安装及其使用](http://velep.com/archives/747.html)
- 交叉编译, 可以参考
  - [Cygwin 安装  基本使用 交叉编译vivi kernel](http://mazhijing.blog.51cto.com/215535/39539/)
  - [在cygwin中安装gcc编译器](http://www.360doc.com/content/12/0929/14/5013584_238783155.shtml)
- 卸载, 因为权限问题, Cygwin卸载很麻烦. 可以参考两篇文章, 已经是最简单的方法了
  - [window 下完全卸载Cygwin最简单方法](http://blog.csdn.net/yelangjueqi/article/details/45199209), 就是在运行一次 `setup.exe` 来卸载
  - [Win7 完全删除cygwin（本人已删除成功）](http://blog.163.com/zhuandi_h/blog/static/180270288201282204521376/)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***


[ce]: https://conemu.github.io/
[putty]: http://www.putty.org/
