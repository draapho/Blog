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


# Win10 + Python + PyQt + PyCharm 开发环境搭建
此部分内容于2021年3月11日添加.

## 心得体会
- 用Python开发项目, 环境配置和维护是个坑...
- 此文简要说明环境搭建过程, 重点说明用于环境维护的python虚拟环境.
- 已知的兼容性问题:
    - Python2.7 无法正确安装 PyIntall. 解决方法如下:
        - 首先, 降低pip版本到18.1: `pip install pip==18.1`
        - 然后, 指定pyinstaller版本为3.4: `pip install pyinstaller==3.4`
        - 检查是否安装成功. `pyinstaller -v`
    - Python2.7 无法实用 `pip install pyqt4`. 解决方法:
        - 下载对应版本的 [PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-xxx](https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/), 运行安装即可.
    - Python3.6 和 Python3.7 与最新版 PyQt5 兼容性问题.
        - 出错形式: 类似于 `from PyQt5 import QtCore` `from PyQt5.QtGui import *` 报错 `No module named 'PyQt5'`
        - 解决方法: 我直接安装了 Python3.8.8, 然后 `pip install pyqt5-tools`, 就会自动下载最新版的pyqt5和关联文件.


## 环境搭建
- 开发环境: `Win10 + Python 3.8.8 + PyQt5 + PyCharm社区版`. 另有历史项目适用 `Python 2.7 + PyQt4 4.11.4`.
- 运行安装 [Python 3.8.8](https://www.python.org/downloads/windows/), 记得勾选加入PATH, 确保环境变量的正确配置.
- `pip install pyqt5-tools`, 会自动下载相关的包如pyqt5, sip.
    - 查了下, 当前版本是 `PyQt5 5.15.2`, 是能保证正常运行的.
    - 指定版本安装的话, 使用`pip install pyqt5-tools==5.15.2`
- `pip install xxx`, 安装其它常用包, 略过不表.
- 运行安装 [PyCharm社区版](https://www.jetbrains.com/pycharm/download/#section=windows), 略过不表
- 如下图, 将PyQt5的两个命令工具整合进PyCharm.
![external tools](https://draapho.github.io/images/1611/pycharm1.png)
- 配置 `designer.exe`, 用于设计 GUI.
    - Name: `Qt5 Designer`, 取个名字.
    - Group: `PyQt-cmd`. 用默认值 `External Tools` 也行. Group名称会出现在右键菜单里, 故单独分了个组.
    - Description: 爱填不填.
    - Program, 这是重点! 填入designer.exe的绝对路径. `xxx\Python38-32\Lib\site-packages\qt5_applications\Qt\bin\designer.exe`
    - Working directory: `$FileDir$`, 工作路径设置为文件所在为止
    - `OK` 保存配置. 点击第5步的加号, 继续增加配置.
- 配置 `pyuic`, 用于将 designer生成的`.ui` 文件转化为 python的`.py` 文件
    - 依样画葫芦, 填写 Name, Group, Description. 以下配置才是重点:
    - Program: 填入python.exe的绝对路径 `xxx\Python38-32\python.exe`, 其实直接填入 `python3.exe` 也可以, 因为已经加入环境变量了.
    - Arguments: `-m PyQt5.uic.pyuic $FileName$ -o $FileNameWithoutExtension$.py`
    - Working directory: `$FileDir$`, 工作路径设置为文件所在为止
    - `OK`保持. 整个配置的意思就是在`$FileDir$`目录下, 运行指令 `python -m PyQt5.uic.pyuic gui_file.ui -o gui.file.py`
- 一套简易的环境就搭好了, 但PyCharm这边还需要配置 `Python Interpreter`, 这是用来维护不同项目的Python虚拟环境用的.


## 虚拟环境搭建
- 如下图, 配置pycharm的`Python Interpreter`
![Python Interpreter](https://draapho.github.io/images/1611/pycharm2.png)
    - 首先选中某个项目, 然后点击`File`->`Settings...`->`Python Interpreter`-`Show All...`. 即图中的步骤1到4.
    - 然后在开发结束后选择新增虚拟环境(图中5), 弹出`Virtualenv Environment`的配置页面(图中6).
    - 图中7 `Location:` python虚拟环境的工作目录. 默认会在所选项目文件夹下新建一个`venv`文件夹. 表示这是此项目的虚拟Python工作环境.
        - 我个人的做法是, 在PyCharm的上级目录下, 建立针对不同python版本的通用性虚拟环境. 如图中12, 为已经配置好的 `python3.8-32-Comm` 和 `python2.7-32-Comm`, 为开发阶段使用.
        - 然后在开发结束后, 需要打包生成exe文件时, 或者只是想保存好这个开发环境时, 才会在项目文件夹下创建`venv`, 搭建好只针对该项目的虚拟环境, 并只安装必要的包.
    - 图中8 `Base Interpreter`, 选择本地安装好的一个python版本.
    - 图中9 `Inherit global site-packages`, 是否继承所选python里的包. 对于通用性环境, 建议勾选, 便于开发. 对于专用性环境, 建议不选, 给项目创建一个完全隔离的虚拟工作环境.
    - 图中10 `Make available to all projects`, 仅通用性环境建议勾选.
    - 最后, 点击`OK`, 配置完成. 新建的虚拟环境会出现在图中12的位置. 选择后继续`OK`, 就为这个项目指定了Python虚拟工作环境, 可以写代码运行了.
- 为完全隔离的专用虚拟环境, 安装Python包.
    - 方法1: 直接从Python系统目录下拷贝需要的包. 系统包路径类似于 `xxx\Python38-32\Lib\site-packages`, 直接拷贝到虚拟环境目录中, 类似于 `xxx_project\vevn\Lib\site-packages`
    - 方法2: 见图中绿色A处, 在`Setting`界面下, 选中专用虚拟环境, 点击这个`+`, 可以在弹出的界面里搜选需要的包, 然后 `Install Package` 即可.
    - 要包含所有的Python运行环境, 包括但不限于 `PyInstaller`, `setuptools` 等等.
- 不借助pycharm, python自身也可以搭建虚拟环境. 这里不介绍了. 只列出几条关键语句.
    - `pip3 install virtualenv` 安装工具. 建议指定python版本, 如pip2 或 pip3
    - `virtualenv venv` 建立了新环境名为venv，在项目文件夹中可以看到增加的文件
    - `xxx\venv\Scripts>activate` 进入venv\Scripts下运行, 激活此虚拟环境
    - `(venv) xxx\venv\Scripts>activate` 出现(venv), 说明激活成功. 继续敲命令行即可
- 如果加载venv中的python路径错误 (新电脑重新安装了)
    - 打开venv文件夹下的pyvenv.cfg文件, 修改home路径地址即可
    - 建议python统一安装地址到 "C:\Programs\Python\PythonXX-XX"


## PyInstaller
- 版本冲突问题.
    - python和pip可以通过使用 python2/python3, pip2/pip3来解决.
    - PyInstaller可以通过指定python调用. 如: `python3 -m PyInstaller -v`. 注意大小写!
- 也可以将PyInstaller加入到PyCharm的 `External Tools` 里. 由于参数组合多样, 我一般直接命令行.
- 建议在专用虚拟环境下打包. 也可以用参数 `-p` 指定路径. 如 `Pyinstaller -p xxx\venv\Lib\site-packages xxx.py`
- 其它参数: `-F/--onefile` 单文件.  `-w/--windowed` 窗口模式. `--clean` 清空编译文件.
- 如果打包失败, 加入 `-d all` 调试信息. 不要用`-w` 窗口模式. 慢慢调试吧.
    - 出错的原因多种多样, 软件开发好, 无法生成exe文件非常让人抓狂!


## 参考资料
- [超详细Windows + Python + PyQt5 + Pycharm 环境搭建](https://www.jianshu.com/p/1f002395a622)
- [Python界面开发:（一）环境搭建](https://cloud.tencent.com/developer/article/1568559)
- [pycharm配置本地python虚拟环境](https://blog.csdn.net/guying4875/article/details/80905472)
- [pyinstaller使用（内含虚拟环境使用）](https://zhuanlan.zhihu.com/p/35977093)
- [Pyinstaller虚拟环境下打包python文件](https://www.jianshu.com/p/2656fbc01c54)





----------

***原创于 [DRA&PHO](https://draapho.github.io/)***

