---
title: python的第一个小程序, 蓝牙及串口终端
date: 2016-11-16
categories: python
tags: [python, pyqt, pyinstaller, BLE]
---


# 环境与资源
- windows 开发环境
- python 2.7
- pywin32, windows support
- pyserial, serial port, com
- pygatt, ble
- pyinstaller, generate exe file
- qt 4.8 (pyqt 4.11), GUI
- Bluegiga 的 [BLED112 Bluetooth Smart Dongle](http://www.silabs.com/products/wireless/bluetooth/bluetooth-smart-modules/Pages/bled112-bluetooth-smart-dongle.aspx)


# 安装
- 略过 python 的安装++
- 实际做项目的话, 建议使用2.7版本, 32位(这样生成的exe文件是32位的, 能兼容所有机器)
- 安装 pywin32: `pip install pypiwin32`
- 安装 pyserial: `pip install pyserial`
- 安装 pygatt: `pip install pygatt`, 事实上, pygatt依赖于pyserial. 因此直接装pygatt也可以
- 安装 pyinstaller: `pip install pyinstaller`
- 下载并安装 [PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7.exe](https://riverbankcomputing.com/software/pyqt/download)
  - 注意匹配python版本和32位/64位window
  - pyqt5 仅支持 python3 以上版本. 我用 python2.7 是因为需要使用其它的库, 如 [LabJack](https://labjack.com/)
  - `Qt Designer` 用于设计UI, 文件格式为`.ui`. 它一般位于 `C:\Python27\Lib\site-packages\PyQt4\designer.exe`. 最终取决于Python安装路径
  - `pyuic4.bat` 用于将 `.ui` 文件转换为 `.py` 文件. 它一般位于 `C:\Python27\Lib\site-packages\PyQt4\`
  - 把 `pyuic4.bat` 的路径放入系统环境变量, 这样后续就能方便使用这个指令了
- windows平台需要借助 [BLED112 Bluetooth Smart Dongle](http://www.silabs.com/products/wireless/bluetooth/bluetooth-smart-modules/Pages/bled112-bluetooth-smart-dongle.aspx) 这么一个设备才能实现BLE通讯

# UI设计
- 可以参考我的另一篇文章 [PyQt 的交互操作](https://draapho.github.io/2016/10/20/1612-python-pyqtui/)

## PyQt 入门
- 为什么选择PyQt? (注意, 如果商用, PyQt是需要授权使用的)
- [PyGTK, PyQT, Tkinter and wxPython comparison](http://ojs.pythonpapers.org/index.php/tpp/article/view/61/57)
- PyQt使用入门:
- [PyQt Tutorial](https://www.tutorialspoint.com/pyqt/index.htm), 新手上路, 建议看到 `Using Qt Designer` 即可
- [Introduction to GUI development using Qt](http://www.training.prace-ri.eu/uploads/tx_pracetmo/QtGuiIntro.pdf), 整体理解Qt设计思路
- [PyQt4教程](http://www.qaulau.com/books/PyQt4_Tutorial/), 中文版, 分类很细, 便于查阅范例

## 使用 Qt Designer 设计GUI并生成 gui.py
- 使用 `Qt Designer` 设计 GUI 框架, 并保存`gui.ui`到项目路径, 如 `D:\ble terminal`
- 打开cmd终端, 并切换到 `D:\ble terminal`
- `pyuic4.bat -x -o gui.py gui.ui` 生成`gui.py`文件,
  - `-x` 表示可执行, 即包含`if __name__ == "__main__"`这部分代码
  - `-o` 表示目标文件名
  - 也可以使用命令行 `pyuic4.bat demo.ui > demo.py`, 效果等同于 `pyuic4.bat -o gui.py gui.ui`
- 创建 `gui_action.py` 文件, 用于书写交互操作部分的代码, 基本格式如下
``` python
# coding=utf-8
import sys
import gui
from PyQt4.QtGui import QApplication, QMainWindow


class GuiAction(QMainWindow, gui.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui_action = GuiAction()
    gui_action.show()
    sys.exit(app.exec_())
```

# UI线程通讯
- 可以参考我的另一篇文章 [PyQt 的交互操作](https://draapho.github.io/2016/10/20/1612-python-pyqtui/)
- PyQt的信号和槽, 是一种通讯机制, 可以用于QObject之间的信息交互. 可以参考:
  - [Introduction to GUI development using Qt](http://www.training.prace-ri.eu/uploads/tx_pracetmo/QtGuiIntro.pdf)
  - [PyQt4 信号和槽详解](https://www.linuxzen.com/pyqt4-xin-hao-he-cao-xiang-jie.html)
- 参考 [PyQt: Threading Basics Tutorial](https://nikolak.com/pyqt-threading-tutorial/)
- 关于 QThread 高阶应用和注意事项, 可参考 [Qt之QThread（深入理解）](http://blog.csdn.net/u011012932/article/details/52186626)
- 本程序使用的线程通讯框架如下:

``` python
class GuiAction(QMainWindow, gui.Ui_MainWindow):

    def __init__(self):
        ...
        # queue_ble 用于传递数据给ble线程 (这样用不好, 可能有风险)
        self.queue_ble = Queue.Queue()
        # thread_ble 为 ble 处理线程
        self.thread_ble = ThreadBleServer(self.queue_ble)

    def cmd_send(self):
        cmd = self.lineEdit.text()
        # 通过 queue_ble 传递数据给ble线程
        self.queue_ble.put(cmd)

    def ble_start(self):
        # 简单理解, 就是将 self.ble_handle 设置为 thread_ble 信号触发后的处理函数
        # 使用 PyQt_PyObject 作为参数类型具有更好的通用性, 可以传递任何数据.
        self.connect(self.thread_ble, SIGNAL(
            "ble_handle(PyQt_PyObject, PyQt_PyObject)"), self.ble_handle)
        # 启动 ble 处理线程
        self.thread_ble.start()

    def ble_stop(self):
        # 用于终止 thread_ble 线程
        self.thread_ble.stop_ble()
        self.disconnect(self.thread_ble, SIGNAL(
            "ble_handle(PyQt_PyObject, PyQt_PyObject)"), self.ble_handle)


class ThreadBleServer(QThread):

    def __init__(self, queue):
        QThread.__init__(self)
        self.stop = False
        self.queue = queue

    def stop_ble(self):
        self.stop = True

    def run(self):
        while not self.stop:
            # 这是一个循环任务, 每100ms执行一次
            time.sleep(0.1)
            ...
            # 非阻塞查询queue队列
            command = str(self.queue.get(False))
            do something after get command ...
            ...
            # 发送信号给主线程
            self.emit(SIGNAL("ble_handle(PyQt_PyObject, PyQt_PyObject)"), "ble_rx_timeout", "")
            ...
```

- 上述代码有一个未知风险, 在 QThread 中用了属于 python threading 的 Queque. 更稳妥的方法应该使用 PyQt 的信号和槽解决这个问题, 即
  `self.connect(self.cmd_send, SIGNAL("send_cmd(PyQt_PyObject)"), self.thread_ble)`
- 关于 QThread 和 Threading, 简单而言, 如果需要和PyQt打交道, 那就用 QThread, 否则就用 python 自带的 Threading
- [全部源码](https://github.com/draapho/ble-terminal) 在 github, 注意, 作为一个练习用程序, 上述错误我没有修改! 目前为止, 没看到不良影响.


# 生成exe文件
- 可以创建一个 `ble-terminal.bat` 文件, 点击即可运行. 但终究是显的不够专业, 没法给老板和客户交代. 内容如下:

``` shell
@echo off

start pythonw gui_action.py
exit
```

- windows下, 使用起来最简单的就是 `PyInstaller` 了. 基本一条指令, 然后需要的关联库全自动解决
- 其它方案有 `Py2Exe`, 需要自己配置dll之类的. `Py2App` 给Mac电脑用的. `cx_Freeze` 优点是跨平台, 看了下需要先做配置文件.
- 用一条指令即可生成 `.exe` 文件
  `pyinstaller.exe --windowed gui_action.py`
- 另外还可以指定图标, 设置版本信息(需要写好`version.txt`), 将所有内容绑到单文件. 指令为:
  `pyinstaller.exe --onefile --windowed --icon=app.ico --version-file=version.txt gui_action.py`
- 详情可参考 [Creating an Executable from a Python Script](https://mborgerson.com/creating-an-executable-from-a-python-script)



----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***
