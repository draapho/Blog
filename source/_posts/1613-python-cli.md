---
title: python调用命令行
date: 2016-10-21
categories: python
tags: [python, cli]
---

# python调用CLI
- CLI = Command Line Interface, 即命令行
- 方法有很多, 通用性和安全性最好的就是`subprocess.Popen`这个方法. 见文档
  - [Subprocess management](https://docs.python.org/2.7/library/subprocess.html#popen-constructor)
  - ~~[os.popen](https://docs.python.org/2.7/library/os.html#os.popen)~~
  - ~~[Utilities for running commands](https://docs.python.org/2/library/commands.html)~~
- example:

``` python
import logging
from subprocess import Popen, PIPE


# CLI: Command Line Interface
def runCLI():
    # __cmd_link = self.cur_dir + "\\stlink_cli\\ST-LINK_CLI.exe -c SWD SWJCLK=5 UR"
    __cmd_link = "dir"

    # 多用 shell=True. shell=False只能运行bat文件或直接在终端中执行. 此例中显示的内容也会有区别
    _pp = Popen(__cmd_link, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = _pp.communicate()

    logging.debug("cmd > " + __cmd_link)
    logging.debug("out > " + out.rstrip())
    logging.debug("err > " + err.rstrip())
    return _pp.returncode


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(runCLI())

```

----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***


