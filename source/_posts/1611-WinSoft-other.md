---
title: Windows 软件系列-开发软件
date: 2016-10-16
categories: windows
tags: [windows, eclipse, TrueSTUIDO, mingw]
description: 无干货, 自己常用开发软件的设置提醒.
---

# [eclipse](https://eclipse.org/downloads/)
- [eclipse](https://eclipse.org/downloads/) 就不做介绍了.
- 设置主题
  - `Window`->`Preferences`->`General`->`Appearance`->`Color Theme`->`Sublime Text 2`
- 设置编辑界面
  - `Window`->`Preferences`-> `General`->`Editors`->`Text Editors`->
    - `Insert spaces for tabs`
    - `Show print margin`
    - `Show whitespace characters`->`configure visibility`->~~`Carriage Return`~~ ~~`Line Feed`~~
  - `Window`->`Preferences`-> `General`->`Editors`->`Text Editors`->`Quick Diff`
    - `Enable Quick Diff`
    - `Use this reference source:`->`A Git Revision`
    - 需要装好git
- 设置路径
  - `Window`->`Preferences`->`Team`->`Git`->`Default repository folder:`->`${project_loc}`
  - `Window`->`Preferences`->`Terminal`->`Local Terminal`->`Initial Working Directory`->`${project_loc}`
  - 注意, 上述两项需要有git项目并编译后, 才可以成功设置
- 设置快捷键
  - `Window`->`Preferences`->`General`->`Keys` 可设置快捷键
  - 快捷键设置要求见 [Windows快捷键](https://draapho.github.io/2016/10/08/1607-CheatSheet-win/)
  - 配置文件名为 `org.eclipse.ui.workbench.prefs`, 路径如下, $workspace$ 表示 eclipse 的工作路径.
  - `$workspace$\.metadata\.plugins\org.eclipse.core.runtime\.settings`下
  - TrueSTUIDO版的快捷键见TureSTUDIO


# ~~[TrueSTUIDO](http://atollic.com/truestudio/)~~, 已改为 [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html#get-software)
- [TrueSTUIDO](http://atollic.com/truestudio/)是一款免费的ARM IDE, 基于eclipse. 免费版有5s广告.
- 快捷键配置文件
  - 我的配置文件 [org.eclipse.ui.workbench.prefs](https://github.com/draapho/Blog/tree/master/_blog_stuff/TrueSTUIDIO/org.eclipse.ui.workbench.prefs)
  - 下载后直接覆盖放入 `$workspace$/.metadata/.plugins/org.eclipse.core.runtime/.settings/`
- [TrueSTUIDO Download and Reset (no debug)](https://www.youtube.com/watch?v=R2hfq4S_-B0)
  - `Run`->`Debug Configurations...`->`Embedded C/C++...`下的文件->`Startup Scripts`
  - delete all context after `load` and input `quit`
  - `Window`->`Perspective`->`Customize Pespective...`->`Launch`->选择 `Debug` 和 `Run`
- 生成指定格式
  - 项目右键 `Properties`->`C/C++ Build`->`Settings`->`Tool Settings`->`Other`->`Output format`->`Convert build output`->`Intel Hex` or `Binary`


# RealView MDK
- RVMDK 设置成utf8格式. `Edit`->`Configuration`->`Editor`->`Encoding`->`UTF8`


# Source Insight
- 添加完文件后, 需要同步. `Project`->`Synchronize Files...`
- 添加文件类型. `Options`->`Document Options`->`Document Type`, 在file filter内增加文件类型即可


# 使用mingw编译C语言
- 主要用于写一些小程序用来验证或测试. 与linux开发习惯一致, 而且免费轻巧快捷.
- 下载 [MinGW](http://www.mingw.org/), 安装并设置好环境变量.
  - 安装好后, 只是 MinGW Installation Manager, 实际上是个绿色软件. 打开后继续安装组件
  - `Basic Setup`->`mingw32-base` 和 `mingw32-gcc-g++`->左上 `Installation`->`Apply changes`->等待安装完成.
  - 这里只需要编译c和c++文件, 无需安装其它组件了.
  - 设置 `...\MinGW\bin` 文件夹到系统环境变量中
  - 复制一份 `mingw32-make.exe` 并重命名为 `make.exe`, 这样就能直接用 make 指令了
  - 测试. 终端中输入 `make -v` 和 `gcc -v`, 看是否可以识别到指令

- 建立一个工作目录, 建立2个文件即可. 一个 `.c`, 另一个 `makefile` 即可
  - 创建并命名为 `main.c`
``` c
#include "stdio.h"

int main() {
    printf("\r\nhello: %s\r\n", "DRA&PHO");
}
```
  - 创建并命名为 `makefile`
``` makefile
test:main.o
    gcc -o hello main.o

main.o:main.c
    gcc -c main.c
```



- 打开终端, 切换到这个工作目录
  - 输入 `make` 即可编译, 会生成 `main.o` `hello.exe` 两个文件
  - 输入 `./hello.exe` 执行, 终端就会输出 `hello: DRA&PHO`
- 资料和参考
  - [windows下使用makefile编译C语言](http://blog.csdn.net/zhanghan3/article/details/1334308)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***

