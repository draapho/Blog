
---
title: Python2和Python3共存时, pip的使用
date: 2017-11-13
categories: python
tags: [python, pip]
---

# pip的使用
pip 为python的包管理器. 最新的python2和python3都已经自带pip.

``` bash
# 显示帮助
pip
pip --help
pip install -h                      # 显示安装的帮助

# 安装包
pip install PackageName             # latest version
pip install PackageName==1.0.4      # specific version

# 包列表
pip list                            # 显示已安装的包   
pip list --outdated                 # 显示有更新的包

# 显示包的简介, 以及包的源码文件
pip show --files PackageName

# 更新包
pip install --U PackageName
pip install --upgrade PackageName
pip install --upgrade pip           # pip更新自己
python -m pip install --U pip       # -m 表示调用python模块, 这里就是要调用pip

# 卸载包
pip uninstall PackageName

# 遇到SSL问题, 下载失败时, 信任下载源即可
# [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:XXX)
pip list --outdated --trusted-host pypi.python.org 
pip install --trusted-host pypi.python.org PackageName

# 如果还是不行, 再试试下面这句. index-url 将源指定为http格式, 不用https了, 然后设置为信任.
pip install --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org PackageName
```

# linux下的双版本

``` bash
sudo python2 hello.py
sudo python3 hello.py
# 指定版本运行源码

sudo pip2 install PackageName
sudo pip3 install PackageName
# 直接使用pip+版本

sudo python2 -m pip install PackageName
sudo python3 -m pip install PackageName
# -m 表示调用python模块, 这里就是要调用pip
```

## 源码内指定版本

将需要指定的python版本放在源码的第一行.
支持如下方式:
``` python
#!/usr/bin/env
# 使用默认的系统环境

#!python2
#!python3
#!/usr/bin/env python2
#!/usr/bin/env python3
# 指定python版本

#!/usr/bin/python2
#!/usr/bin/python3
#!/usr/local/bin/python2.7
#!/usr/local/bin/python3.5
# 通过路径指定版本
```

举个python3的例子, 格式如下:
``` python
#! python3
# coding: utf-8

import logging
# ... 源码
```

# linux下的双版本

## windows官解

Windows下, 官方提供了 [Python launcher for Windows](https://www.python.org/dev/peps/pep-0397/) 的方法. 
在安装 python3 的时候 (版本>=3.3), 记得勾选 `py launcher` 选项.
这样, 就会python3就会生成一个py.exe命令. 可以指定调用python2或者python3.
安装了 `py laucher` 后, 也支持源码第一行指定版本
- `#! python2`
- `#! python3`

``` bash
py -2 hello.py
py -3 hello.py
# 指定版本运行源码

py -2 -m pip install PackageName
py -3 -m pip install PackageName
# -m 表示调用python模块, 这里就是要调用pip
```

## windows土法

但是, 官解真的没有土方法方便. 但不知道是否有潜在风险题
土法就是改名, 让windows下的用法和linux一样.
- 在python2的根目录, **复制**一份`python.exe`, 然后改名为 `python2.exe`. 
- 进入`Scripts`目录, **复制**一份`pip.exe`, 然后改名为 `pip2.exe`. 
- 同样python3根目录, **复制**一份`python.exe`, 然后改名为 `python3.exe`. 
- 进入`Scripts`目录, **复制**一份`pip.exe`, 然后改名为 `pip3.exe`. 
- 注意不是直接改名. 要保留原来的 `python.exe` 和 `pip.exe`
- 可以和linux下一样, 愉快的玩耍了. 如下:

``` bash
python2 hello.py
python3 hello.py
# 指定版本运行源码

pip2 install PackageName
pip3 install PackageName
# 直接使用pip+版本

sudo python2 -m pip install PackageName
sudo python3 -m pip install PackageName
# -m 表示调用python模块, 这里就是要调用pip
```


# 参考资料
- [Windows上Python2和3如何兼容？](https://python.freelycode.com/contribution/detail/139)
- [python2.X和python3.X在同一平台下的切换技巧](http://www.cnblogs.com/an9wer/p/5564284.html)
----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***