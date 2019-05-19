---
title: Python 调试及测试
date: 2016-12-13
categories: python
tags: [python, debug]
---

# 调试
常用的方法有:
- print, 仅作临时测试, 而且还要删除.
- assert, 同print, 无明显优势.
- logging, 推荐使用. 可选级别, 可选输出方式, 适用于各种情况的调试.
- pdb 以及 基于pdb的图形化工具.
- python的IDE, 如PyCharm(推荐), eclipse+PyDev


## logging

### 简单使用
``` python
# -*- coding:utf-8 -*-
import logging

if __name__ == "__main__":
    '''默认日志输出为终端, 设置日志等级, DEBUG=LEVEL10, 优先级最低'''
    logging.basicConfig(level=logging.DEBUG)
    '''更多设置'''
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(asctime)s %(filename)-s[%(lineno)d] %(levelname)-8s: %(message)s')

    logging.debug('DEBUG message')
    logging.info('INFO message')
    logging.warn('WARN message')
    logging.error('ERROR message')
    logging.critical('CRITICAL message')
```

### 自定义显示格式

日志输出到 `logger.log`
``` python
# -*- coding:utf-8 -*-
import logging

if __name__ == "__main__":
    '''设置显示格式, 日志输出到文件'''
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)-s[%(lineno)d] %(levelname)-8s: %(message)s',
                        filename='logger.log',
                        filemode='w') # default is 'a'=append, 'w'=overwrite

    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')
```


日志输出到 `logger.log` 以及终端
``` python
# -*- coding:utf-8 -*-
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[%(lineno)d] %(levelname)-8s: %(message)s',
                        filename='logger.log',
                        filemode='w') # default is 'a'=append, 'w'=overwrite

    '''
    定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
    '''
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')
```

### 使用文件配置

``` python
#logging.conf

###############################################
[loggers]
keys=root

[logger_root]
level=DEBUG
handlers=hand01,hand02

###############################################
[handlers]
keys=hand01,hand02,hand03

# 写入终端
[handler_hand01]
class=StreamHandler
level=DEBUG
formatter=form01
args=(sys.stderr,)

# 写入文件, 'w'覆写, 'a'追加
[handler_hand02]
class=FileHandler
level=INFO
formatter=form01
args=('logging.log', 'w')

# 最多备份5个日志文件，每个日志文件最大10M
[handler_hand03]
class=handlers.RotatingFileHandler
level=INFO
formatter=form01
args=('logging.log', 'a', 10*1024*1024, 5)

###############################################
[formatters]
keys=form01

[formatter_form01]
format=%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-8s: %(message)s
```

``` python
import logging

if __name__ == "__main__":
    from logging.config import fileConfig
    fileConfig("logging.conf")

    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')
```

### 更多应用参考手册

- [15.6. logging — Logging facility for Python](https://docs.python.org/3.1/library/logging.html)
  - 15.6.11. Sending and receiving logging events across a network
  - 15.6.20.2. Configuration file format
  - 15.6.20.3. Configuration server example
  - 15.6.21. More examples


## pdb

进入调试模式 `python -m pdb example.py`
``` shell
$ python -m pdb example.py
(Pdb)
```

pdb 常用命令
```
# 断点
(Pdb) b 10          # 断点设置在当前文件的第10行
(Pdb) tbreak 10     # temp  break, 临时断点, 执行后会自动删除
(Pdb) b my.py:20    # 断点设置到 my.py第20行
(Pdb) b             # break, 查看断点编号
(Pdb) cl 2          # clear, 删除第2个断点
(Pdb) disable 2     # 禁用第2个断点
(Pdb) enable 2      # 使能第2个断点
(Pdb) ignore 2 10   # 略过第2个断点10次, 循环调试特别有用!
(Pdb) condition 2 (i>10)    # 条件为真时,使能断点

# 运行
(Pdb) n             # next, 单步运行
(Pdb) s             # step, 进入方法
(Pdb) r             # return, 返回上级方法
(Pdb) c             # continue, 跳到下个断点

# 查看
(Pdb) p param       # print, 查看当前 变量值
(Pdb) l             # list, 查看运行到某处代码
(Pdb) a             # args, 查看全部栈内变量
(Pdb) w             # where, 堆栈信息

# 其它
(Pdb) h             # help, 帮助
(Pdb) q             # quit, 退出调试
```

使用alias设置别名, 可大大提高调试速度!
**将下述文件存储为 `.pdbrc`, 然后放在系统目录 `~` 或 项目目录下, pdb会自动加载.**
``` python
# name it as ".pdbrc", then put into ~ or project folder

# Print a dictionary, sorted. %1 is the dict, %2 is the prefix for the names.
alias p_ for k in sorted(%1.keys()): print "%s%-15s= %-80.80s" % ("%2",k,repr(%1[k]))

# Print the instance variables of a thing.
alias pi p_ %1.__dict__ %1.

# Print the instance variables of self.
alias ps pi self

# Print the locals.
alias pl p_ locals() local:

# Next and list, and step and list.
alias nl n;;l
alias sl s;;l

# go to line
alias gl tbreak %*;;c %*;;l

# go to next
alias g1 n;;l
alias g2 n;;n;;l
alias g3 n;;n;;n;;l
alias g4 n;;n;;n;;n;;l
alias g5 n;;n;;n;;n;;n;;l
alias g6 n;;n;;n;;n;;n;;n;;nl
alias g7 n;;n;;n;;n;;n;;n;;n;;l
alias g8 n;;n;;n;;n;;n;;n;;n;;n;;l
alias g9 n;;n;;n;;n;;n;;n;;n;;n;;n;;l

# Short cuts for walking up and down the stack
alias uu u;;u
alias uuu u;;u;;u
alias uuuu u;;u;;u;;u
alias uuuuu u;;u;;u;;u;;u
alias dd d;;d
alias ddd d;;d;;d
alias dddd d;;d;;d;;d
alias ddddd d;;d;;d;;d;;d
```


## 查看函数调用

使用如下的装饰器, 即可观察该函数被调用的情况
``` python
def findcaller(func):
    def wrapper(*args, **kwargs):
        import sys
        f = sys._getframe()
        filename = f.f_back.f_code.co_filename
        lineno = f.f_back.f_lineno
        print '######################################'
        print '{}, args: {}, {}'.format(func, args, kwargs)
        print 'called by {}, line {}'.format(filename, lineno)
        print '######################################'
        func(*args, **kwargs)
    return wrapper
```

``` python
# example

@findcaller
def hello(name='world'):
    print "hello", name

if __name__ == "__main__":
    hello('DRA&PHO')
```


# 测试

## doctest
简单的函数测试个人比较喜欢使用doctest, 因为一举两得, 即可以做测试案例, 又是极好的代码注释和范例
输出和预期一致时, 没有任何提醒. 输出和预期不一致时, 就会弹出错误.

``` python
def hello(name='world'):
    """
    >>> hello()
    hello world
    >>> hello('DRA&PHO')
    hello, DRA&PHO
    """
    print "hello", name

if __name__ == '__main__':
    import doctest
    doctest.testmod()
```

## 其它

- [unittest](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/00140137128705556022982cfd844b38d050add8565dcb9000), 更专业的一种测试方法, 可批量执行
- [Python指南-测试你的代码](http://pythonguidecn.readthedocs.io/zh/latest/writing/tests.html)
  - 单元测试(unittest)
  - 文档测试(doctest)
  - 测试工具: py.test, nose, tox, Unittest2, mock



# 参考资料
- [python 的日志logging模块学习](http://blog.csdn.net/yatere/article/details/6655445)
- [python logging模块使用教程](http://www.jianshu.com/p/feb86c06c4f4)
- [15.6. logging — Logging facility for Python](https://docs.python.org/3.1/library/logging.html)
- [Debugging in Python](https://pythonconquerstheuniverse.wordpress.com/category/python-debugger/)
- [Interactive Debugging in Python](http://www.onlamp.com/pub/a/python/2005/09/01/debugger.html)

- [廖雪峰的官方网站-单元测试](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/00140137128705556022982cfd844b38d050add8565dcb9000)
- [Python 指南-测试你的代码](http://pythonguidecn.readthedocs.io/zh/latest/writing/tests.html)

- [python笔记_查看函数调用栈的一个小技巧](http://www.jianshu.com/p/ae5bc6093337)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***