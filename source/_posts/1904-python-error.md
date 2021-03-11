---
title: Python 错误及解决方法
date: 2019-05-19
categories: python
tags: [python, debug]
description: Python 疑难错误归纳.
---

# UnicodeEncodeError: 'charmap' codec can't encode characters
- 此问题多发生在windows的区域和开发中用到在字符不匹配. 譬如英文区域的windows要编解码中文字符.
- 原因及解决方法参考 [代码页即地狱](https://blog.csdn.net/haiross/article/details/36189103)

简单来说, 就是windows底层编码的问题. 要解决这个问题, 只能从windows系统着手.

![Region](https://draapho.github.io/images/1904/Region.png)


# `from PyQt5 import QtCore` `from PyQt5.QtGui import *` errors `No module named 'PyQt5'`
- python3 和 pyqt5 兼容性问题. 最新版本的 pyqt5 和 python3.6, python3.7 不兼容.
- 现象为: `import PyQt5` 调用正常. `from PyQt5 import QtCore` 提示错误, 无法找到模块 `PyQt5`
- 解决方法: 试了很多版本组合. 最后成功的是 `Python 3.8.8` 32位 和 `PyQt5 5.15.2`.
    - 先软件安装 `Python 3.8.8`
    - 直接 `pip install pyqt5-tools` 自动安装的最新版本.


# Python 2 下 `pip install pyinstaller` 无法安装, 编译失败.
- 很复杂的兼容性问题. 需要降低 pip 版本以及 pyinstaller 版本
- 首先, 降低pip版本到18.1: `pip install pip==18.1`
- 然后, 指定pyinstaller版本为3.4: `pip install pyinstaller==3.4`
- 检查是否安装成功. `pyinstaller -v`



----------

***原创于 [DRA&PHO](https://draapho.github.io/)***