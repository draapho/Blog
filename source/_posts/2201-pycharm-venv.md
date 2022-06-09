---
title: PyCharm 设置虚拟开发环境
date: 2022-06-08
categories: python
tags: [python]
description: 设置python的虚拟开发环境, 项目资源独立化.
---


# 概述
介绍了python的虚拟开发环境的建立和配置.
用于独立各个项目的依赖库, 便于后续维护和更新, 并能最小化可执行文件的大小.


# PyCharm 新建工程

新建工程界面: PyCharm内, `File->New Project...`, 打开后如下图:
    - 下图红色1处为工程目录, 指定为 `XXX\code`
    - 下图红色2处为虚拟环境目录, 指定为 `XXX\venv`

![Create Project](https://draapho.github.io/images/2201/create.png)


这样, 会在项目的`XXX`根目录下, 自动生成 `code` 和 `venv` 两个文件夹.
再手动放入 `.gitignore`, 并新建一下 `exe` 文件夹.
目录结构为:
- `XXX`   项目根目录
    - `code`   python 代码
    - `exe`    可执行文件, 历史release版本
    - `venv`   该项目的虚拟环境
    - `.gitignore`  git版本管理使用, 建议加入 `exe/`, 去除exe文件夹的同步.



# ~~命令行建立venv环境~~

PyCharm新建工程可以直接建立python的虚拟工作环境, 因此**可以跳过此步骤.**
写在这里仅供不时之需.

- 在工程根目录`XXX`下, 打开终端
- `python -m venv .\venv` 在venv文件夹下, 创建虚拟环境.
    - 多版本python的话, 建议用指定路径, 如 `D:\Program\Python\Python38-32\python -m venv .\venv`
    - 若使用改了名的python指令, 会报错: `Error: [WinError 2] The system cannot find the file specified`
    - 如 `python2 -m venv .\venv` 或 `python3 -m venv .\venv` 则报上述错.
- 自动建立的venv\Scripts下 会有activate.bat, pip.exe, python.exe 几个常用指令
- 测试虚拟环境
    - `.\venv\Scripts\activate`  启用虚拟环境, 命令行之前会有(venv) 字样表示成功.
    - `python --version`   检查虚拟环境使用的python版本.
    - `pip list`  查看虚拟环境中的库.


# PyCharm 在指定的venv下安装库

- PyCharm内, `File->Settings`, 弹出Settings界面. 左边选择`Project:code->Python Interpreter`
- PyCharm内, 重命名虚拟环境.
    - 下图红色1处, 点击后, 选择`Show All...`, 会打开虚拟环境管理界面.
    - 下图红色3处, 先选中这次创建的虚拟环境, 默认名称就是 `Python 3.x (venv)`, 然后点击修改按钮.
    - 建议将 `Python 3.x (venv)` 改名为 `Python 3.x (XXX)`, XXX为工程名, 即根目录名.
    - 这样可以避免下次使用PyCharm建立虚拟环境时重名.
- 以pyinstaller为例, 添加库.
    - 下图红色2, 加号. 弹出库管理界面.
    - 下图红色4处, 输入关键字 `pyinstaller`, 然后选中需要安装的库
    - 下图红色5处, 勾选指定版本, 譬如 `4.7`
    - 下方点击 `Install Package`, 等待完成即可.
- 这样, 安装其它库类推, 需要特殊版本的依赖也很容易修改, 且不会影响其它项目.

![setting](https://draapho.github.io/images/2201/setting.png)

![change name](https://draapho.github.io/images/2201/change.png)

![add package](https://draapho.github.io/images/2201/add.png)


# 使用 pyinstaller 进行编译

- 在 `XXX\code` 文件下准备好编译时要用的 `xxx.ico` 和 `version.txt` 文件.
- 基于 `XXX\code` 文件夹, 打开终端.
- 启用python虚拟环境
    - `..\venv\Scripts\activate`
    - 成功后, 命令行目录的最前面会增加 (venv)字样
- 检查pyinstaller 版本
    - `..\venv\Scripts\python.exe ..\venv\Scripts\pyinstaller.exe -v`
    - 安装的是4.7,  所以返回值应该是4.7
- 执行编译
    - `..\venv\Scripts\python.exe ..\venv\Scripts\pyinstaller.exe --icon=xxx.ico --version-file=version.txt --name XXX main.py`
    - 如有需要, 可以加入 `--windowed` 和 `--onefile`. 前者表示有UI界面, 后者表示生成为单一的可执行文件.
- debug purpose, 查看详细的编译信息, 用于排查
    - `..\venv\Scripts\python.exe ..\venv\Scripts\pyinstaller.exe -d all --clean main.py`
- 参考资料:
    - [pyinstaller踩坑记，缺少依赖、打包错误或运行无效排查过程备忘](https://zhuanlan.zhihu.com/p/354609842)
    - [Pyinstaller 打包发布经验总结](https://blog.csdn.net/weixin_42052836/article/details/82315118)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***





