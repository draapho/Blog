---
title: PyQt 的交互操作
date: 2016-10-20
categories: python
tags: [python, pyqt]
description: 如题.
---


# environment
- Windows
- [python 2.7](https://www.python.org/downloads/)
- [PyQt 4.11.4](https://riverbankcomputing.com/software/pyqt/download)


# useful guide / startup
- [Introduction to GUI development using Qt](http://www.training.prace-ri.eu/uploads/tx_pracetmo/QtGuiIntro.pdf), 简单明了的介绍了qt gui的基本特性
- [PyQt Tutorial](https://www.tutorialspoint.com/pyqt/), learn PyQt step by step.
- [PyQt: Threading Basics Tutorial](https://nikolak.com/pyqt-threading-tutorial/), 防止UI阻塞, 使用线程


# Generate basic UI file

- use `Qt Designer` to create basic UI
  - `New`->`Widget`->drag `PushButton` to `Form` Window
  - Save it, for example `demo.ui`
- make sure `pyuic4.bat` is in the System PATH
  - input `pyuic4.bat -h` in shell, check the response.
- change `.ui` to `.py` file
  - run `pyuic4.bat -x -o demo.py demo.ui` in the working folder.
  - `-o` means output, set the output filename.
  - `-x` will generate `if __name__ == '__main__':` then can run directly
  - `pyuic4.bat demo.ui > demo.py` is also OK.
- ~~the sample of `demo.py`, generated automatically by pyuic4.bat~~

``` python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 40, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "PushButton", None))

# using -x will generate the following code
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
```


- ~~run & check the　UI~~
  - run `python demo.py` in the working folder.
  - OR run directly in editor like atom.


# click then do sth

- create a new py file, for example `show.py`. input code like:

``` python
import sys
import demo  # generated from xxx.ui
from PyQt4 import QtGui


class MyForm(QtGui.QWidget, demo.Ui_Form):

    def __init__(self):
        super(self.__class__, self).__init__()  # QtGui.QWidget.__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(
            self.handleButton)  # here is important line

    def handleButton(self):
        print ("hello, https://draapho.github.io/")
        # size = self.geometry()
        # self.resize(size.width() + 2, size.height() + 2)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec_())
```

- look at `self.ui.pushButton.clicked.connect(self.handleButton)`
  it links clicked event with handleButton function.
- if you want to resize the window after clicked the button. change `handleButton` to

``` python
    def handleButton(self):
        # print ("hello, https://draapho.github.io/")
        size = self.geometry()
        self.resize(size.width() + 2, size.height() + 2)
```

# click then do heavy work

- ~~bad code, UI totally dead~~
``` python
from PyQt4 import QtGui
import sys
import demo
import time


class MyForm(QtGui.QWidget, demo.Ui_Form):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.startCount)

    def startCount(self):
        self.pushButton.clicked.disconnect()
        self.pushButton.clicked.connect(self.stopCount)
        i = 0
        while i < 15:
            i += 1
            self.pushButton.setText(str(i))
            print i
            time.sleep(1)

    def stopCount(self):
        self.pushButton.clicked.disconnect()
        self.pushButton.clicked.connect(self.startCount)
        self.pushButton.setText("PushButton")

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = MyForm()
    form.show()
    app.exec_()
```

- use thread, can do everything in UI
``` python
from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL
import sys
import demo


class getCountThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.count = 0

    def __del__(self):
        self.wait()

    def run(self):
        while self.count < 15:
            self.count += 1
            self.emit(SIGNAL('showCount(int)'), self.count)
            print self.count
            self.sleep(1)


class MyForm(QtGui.QWidget, demo.Ui_Form):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.startCount)

    def startCount(self):
        self.pushButton.clicked.disconnect()
        self.get_thread = getCountThread()
        self.connect(self.get_thread, SIGNAL("showCount(int)"), self.showCount)
        self.connect(self.get_thread, SIGNAL("finished()"), self.done)
        self.get_thread.start()
        # must be under the self.get_thread.start()
        self.pushButton.clicked.connect(self.get_thread.terminate)

    def showCount(self, count):
        self.pushButton.setText(str(count))

    def done(self):
        self.pushButton.clicked.disconnect()
        self.pushButton.setText("PushButton")
        self.pushButton.clicked.connect(self.startCount)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = MyForm()
    form.show()
    app.exec_()
```


- explanation
  - `getCountThread` 子线程类, 执行繁重任务
  - `MyForm`->`startCount` 点击按键后执行, 设置好信号, 启动子线程
  - `self.connect(self.get_thread, SIGNAL("showCount(int)"), self.showCount)`
    准备接收来自线程的信号, 并在 `showCount` 更新UI
  - `self.connect(self.get_thread, SIGNAL("finished()"), self.done)`
    准备接收来自线程的结束信号, 然后在 `done` 下更新标记和UI
  - `self.get_thread.start()`
    启动子线程
  - `self.pushButton.clicked.connect(self.get_thread.terminate)`
    将按键的功能设置为终止子线程, 必须放在 `self.get_thread.start()` 下面



----------

***原创于 [DRA&PHO](https://draapho.github.io/)***


