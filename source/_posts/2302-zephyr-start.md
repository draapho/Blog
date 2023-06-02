---
title: Zephyr Project 环境配置
date: 2023-04-25
categories: embedded
tags: [embedded, zephyr]
description: 如题.
---


# 概述

Zephyr Project 是一个可扩展的实时操作系统, 为资源受限的设备提供支持. 由 Linux 基金会托管.
因而该项目极具Linux特点: 性能强大, 学习曲线陡峭, 入门困难. 主要使用命令行格式, 基于类Unix系统测试比较充分, Window下容易遇到各种莫名的问题.
该项目刚出来的时候, 也关注过, 根据其指导手册, 在windows下就没有配置成功. 现在有空又试了一下, 算是在windows环境下, 成功搭建了运行环境, 并把范例跑了起来.



# 1. 安装 Chocolatey

首先，需要安装 Chocolatey 包管理器。请参阅 [Chocolatey 安装页面](https://chocolatey.org/install) 获取详细信息。

使用 PowerShell 以**管理员身份**运行以下命令：

```powershell
Set-ExecutionPolicy AllSigned
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

升级 Chocolatey：

```powershell
choco upgrade chocolatey
```


# 2. 安装依赖

以**管理员身份**打开命令提示符, 并运行以下命令，用以安装 cmake, ninja, gperf, python, git, dtc-msys2, wget, unzip 等依赖工具。如果已经安装过，请确保升级到最新版本。

```cmd
choco feature enable -n allowGlobalConfirmation
choco install cmake --installargs 'ADD_CMAKE_TO_PATH=System'
choco install ninja gperf python git dtc-msys2 wget unzip
```


# 3. 安装 West 工具

使用 Python 安装 West 工具。West 专门用于管理 Zephyr 项目，它可以下载并更新项目。

```cmd
pip3 install -U west
cd %HOMEPATH%
west init zephyrproject
cd zephyrproject
west update

west zephyr-export
pip3 install -r %HOMEPATH%\zephyrproject\zephyr\scripts\requirements.txt
```

# 4. 安装 Zephyr SDK

安装 Zephyr SDK 时，请从 [Zephyr SDK 的 GitHub 页面](https://github.com/zephyrproject-rtos/sdk-ng/releases) 下载最新版本，而不是官方文档中, 命令行里的版本 (官方文档更新不及时, 后面编译时会提示版本过低)。

例如，当前最新版本为 Zephyr SDK 0.16.0。下载 Windows 的 FULL 版本（[下载链接](https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.0/zephyr-sdk-0.16.0_windows-x86_64.7z)），然后将其手动解压到适当的目录。

在解压出的 `zephyr-sdk-0.16.0` 目录下，双击运行 `setup.cmd`。
这时候会提示 `Zephyr SDK setup requires '7z' to be installed and available in the PATH.` 就是要把7z的bin加入到环境变量PATH中.
一个简单的方法，可以将 7z.exe 和 7z.dll 复制到 `zephyr-sdk-0.16.0` 目录下，然后运行 `setup.cmd`。
注意: `setup.cmd`, 只需要执行一次, 不要多次执行.


# 5. 编译项目

要查看支持的开发板列表，请访问：[官方支持的开发板列表](https://docs.zephyrproject.org/3.1.0/boards/index.html#boards)。

我手头有 ST Nucleo L152RE 开发板. 就以此为例，运行以下命令：

```cmd
cd %HOMEPATH%\zephyrproject\zephyr
west build -p always -b nucleo_l152re samples/basic/blinky
REM -p always 是指编译前, 强制清理编译目录. auto 是自动识别

REM west build -p auto -b nucleo_l152re samples/basic/blinky
REM west build -p auto -b nucleo_f031k6 samples/basic/blinky
```

注意：
- 如果是从其他地方复制的 zephyrproject 文件夹，build 可能会出错。此时，删除 zephyr 目录下的 build 文件夹, 或者使用 `west build -p always ...`
- 如果在编译过程中出现错误，请仔细检查依赖工具的最低版本要求，然后按需解决问题。

编译结果: L152RE 用了 14K的 flash, 4K的 RAM...

|  Memory region    |  Used Size    |  Region Size    | %age Used     |
| ---- | ---- | ---- | ---- |
|  FLASH:    |   14200 B   | 512 KB     |  2.71%    |
|  RAM:     |  4224 B    |  80 KB    |    5.16%  |
|  IDT_LIST:      | 0 GB     |  2 KB    |  0.00%    |


换f031K开发板看下编译结果: 13K的flash, 2K的RAM

|  Memory region    |  Used Size    | Region Size     | %age Used     |
| ---- | ---- | ---- | ---- |
|  FLASH:     | 12770 B     |  32 KB     | 38.97%     |
|  RAM:     |  1784 B      |  4 KB     |  43.55%    |
| IDT_LIST:     |  0 GB     |  2 KB    |  0.00%    |

**简单的结论**: 对于某些成本敏感, 有超低成本需求的应用, Zephyr 依旧太耗资源了. 直观感觉, 适合使用 Zephyr 的项目, 和 RT-thread 的目标类似, 就是有联网需求的嵌入式应用, 能直接使用到里面成熟的模块或方案, 功能上保证了可靠性和稳定性, 加速项目的开发进度.


# 6. 烧录

使用以下命令进行烧录：

```cmd
west flash
```

这时, 会提示未安装 openocd 或未正确配置 openocd 的环境变量.
请访问 [OpenOCD 官网](https://openocd.org/pages/getting-openocd.html) 下载源代码，
windows安装版本在 [OpenOCD 的 GitHub 页面](https://github.com/openocd-org/openocd/releases/tag/v0.12.0) 可以下载到相应版本。
例如:  [Windows 版本的 OpenOCD](https://github.com/openocd-org/openocd/releases/download/v0.12.0/openocd-v0.12.0-i686-w64-mingw32.tar.gz)。
下载并解压后，将其 bin 目录添加到环境变量 PATH 中。

完成上述操作后，在新的命令提示符窗口中运行以下命令以测试：

```cmd
openocd
REM 如果返回 Open On-Chip Debugger ... 则 openocd 安装成功
```

然后，再次尝试烧录和调试：

```cmd
west flash
west debug
REM 进入 (gdb) 调试模式
```

如果仍然出现问题，请根据提示信息仔细检查硬件连接和系统配置。例如，首先检查烧录器，然后查看检测到的硬件电压等。具体操作因硬件而异，无法一一详述。



# 参考资料

- [Zephyr Getting Started Guide](https://docs.zephyrproject.org/3.1.0/develop/getting_started/index.html)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***