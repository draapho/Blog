---
title: Windows 软件系列-提高效率
date: 2016-09-28
categories: windows
tags: [windows, AutoHotKey]
description: 如题.
---

# ~~[AutoHotKey][AutoHotKey]~~

## AHK 简介
- [AutoHotkey][AutoHotKey]是一个windows下的开源, 免费, 自动化软件工具.
- 我主要用于绑定快捷键, 便于快速打开应用和文件夹. 以此提高**工作效率**
- 常用符号含义
  > `#` 代表 Win 键
  > `!` 代表 Alt 键
  > `^` 代表 Ctrl 键
  > `+` 代表 shift 键
  > `::` 起分隔作用
  > `run` 非常常用 的 AHK 命令之一
  > `;`  注释后面一行内容
- 举个例子
  用 `Ctrl - Alt - Shift - Win - n` 打开记事本的脚本
  ``` ahk
  ^!+#n::run C:\Windows\notepad.exe
  ```

## AHK懒人用法: [ezAHK](https://github.com/draapho/ezAHK)
- 安装 [AutoHotKey](https://autohotkey.com/download/) V1.1.\* 版本
- 下载 [ezAHK](https://github.com/draapho/ezAHK) 放到任意位置
- 把文件或目录的**快捷方式放到link目录**里, 改成希望使用的**快捷键名称**即可.
  譬如, 希望把notepad绑定到 `win-n`这个快捷键, 只需要:
  1. 创建**notepad.exe的快捷方式**到**link目录**
  2. 重命名该快捷方式为 `win-n`
  3. 注意 `-` 的左右**没有空格**, **删除后缀** `.exe`
  4. 可以考虑使用 `win-r` 的方式替代, 毕竟快捷键数量有限, 命令行更灵活.
- ezAHK 还包括如下几个实用功能
  - `鼠标中键` 复制
  - `shift-鼠标中键` 剪切
  - `ctrl-shift-鼠标中键` 复制路径
  - `鼠标右键` 使用鼠标中键复制后, 首次黏贴
  - `ctrl-鼠标右键` 黏贴
  - `ctrl-~` 根据所在目录打开终端
  - `alt-win-鼠标中键` 复制颜色
  - `alt-win-↑ ↓ ← →` 单像素移动鼠标
  - `alt-win-d` 输入当前日期
- 添加到开机自启动: 创建`ezAHK.ahk`的快捷方式, 并放到如下 Windows 的 **StartUp目录**.
  Windows 10 的 StartUp 目录如下:
  `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`


## 资源和参考
- [实用 AutoHotkey 脚本推荐](https://autohotkey.com/boards/viewtopic.php?t=4296)
- [AHK 快餐店系列索引](https://autohotkey.com/boards/viewtopic.php?t=4267)
- [AutoHotkey_Script_Showcase](https://autohotkey.com/docs/scripts/#AutoHotkey_Script_Showcase)
- [Get paths of selected items in an explorer window](https://autohotkey.com/board/topic/60985-get-paths-of-selected-items-in-an-explorer-window/)
- AutoHotKey[官网](https://autohotkey.com/) 及 [中文帮助](http://ahkcn.sourceforge.net/docs/AutoHotkey.htm)
- [Win下最爱效率神器:AutoHotKey](http://www.jeffjade.com/2016/03/11/2016-03-11-autohotkey/)



# 快速搜索和定位

## [Everything][Everything]
- [Everything][Everything]是免费软件, 有**便携版**.
- [Everything][Everything]是**普通搜索工具**, 便于在搜索结果中慢慢查阅.

## ~~[Listary][Listary]~~
- [Listary][Listary]分为免费版和专业版.
- 相比于 [Everything][Everything], 索引方式相似,但操作体验完全不同.
- [Listary][Listary]是**随时随地的查找定位**, 目标明确时很方便.
- 强烈推荐都尝试一下后决定用哪个, 或和我一样同时使用.
- Listary 实用快捷键

| Listary             | 助记                 | 功能                |
| --------------- | ------------------ | --------------------- |
| `win-~`         |                    |  打开Listary            |
| `enter`         | enter              |  打开文件                 |
| `ctrl-enter`    | enter              |  打开路径             |
| `ctrl-c`        | copy        | 复制       |
| `ctrl-shift-c`  | copy        | 复制路径       |
| `ctrl+j` `ctrl+k` | vim j,k           | 下一个 / 上一个(需设置) |

## ~~使用 `win-r` 快速启动~~
- 基本原理是使用 `Run` 来直接运行配置在环境变量中的快捷方式 `.lnk`,
- 由于是执行命令行, 比快捷键方式有更好的扩展性和灵活性更好. 也可以在任何终端中直接调用!
- 运行环境的搭建可以参考 [Windows 软件系列-自定义环境变量](https://draapho.github.io/2016/10/09/1608-WinSoft-path/)
- 详细介绍可参考 [最绿色最高效，用win+r启动常用程序和文档](https://xbeta.info/win-run.htm#h-6)
- 为了更省事, 可以使用AHK设置为`win`键替代`win-r`键
- 要把win键也省了的话, 专业版 [Listary][Listary] 可以满足这个需求



# ~~[Ditto][ditto]~~

- [Ditto][ditto] 一款剪切板增强软件, 免费开源. 有绿色便携版(无法支持部分功能)
- 对复制黏贴功能多多支持总是好的, 使用频率太高了! 这个软件的功能非常实用.
  - 软件的核心在于 `ctrl-~` 调用出 Ditto 信息板
  - `shift-enter` 忽略格式黏贴纯文本
  - `新建剪辑`->`项目标题` `email`->`快速黏贴文本` `myemail@gmail.com`->设置为`禁止自动删除`, 也可以归类到组. 以后只需输入email, 就可以直接黏贴具体email地址了
  - 轻松管理复制历史, 可用作搜索资料, 然后批量黏贴
- 重新设置 `激活Ditto` 快捷键为 `ctrl-q`, 因为 `ctrl-~`默认用于打开终端
- 参考 [Ditto:首选的剪贴板增强软件](https://xbeta.info/ditto.htm)



# ~~[Chocolatey][Chocolatey]~~

**[Chocolatey][Chocolatey]可以作为软件安装的补充, 但不做推荐**

## Chocolatey 简介
-   [Chocolatey][Chocolatey]是windows下的软件管理工具. 软件源由社区成员提交和维护. 基础版免费.
-   基于命令行来查找和安装软件,方便快捷,~~耍酷~~.
-   安装包的类型:
    - 无后缀, 如 git
    - *.install, 如 git.install, 这个会出现在系统的 **卸载或更改程序** 界面里
    - *.commandline, 如 git.commandline. 不建议使用
    - *.portable, 如 putty.portable, zip包, 我的理解就是绿色便携软件
-   软件都是自动静默安装, 无法指定安装位置, 无法再安装时配置.
-   由于运行在管理员权限且不能保证软件绝对无毒, 所以有安全风险. [Chocolatey官网](https://chocolatey.org/about)有如下语句:
    > If you need better peace of mind, we offer [runtime malware protection](https://chocolatey.org/docs/features-virus-check) in [Chocolatey Pro](https://chocolatey.org/pricing) and [Chocolatey for Business](https://chocolatey.org/pricing)
-   搜索和下载指定版本的软件也没有想象中方便.
-   综合考虑后, [Chocolatey][Chocolatey]可以作为软件安装的补充(如制作安装脚本), 但不做推荐

## 常用指令
- windows [安装 Chocolatey](https://chocolatey.org/install). 使用管理员权限打开 cmd.exe, 输入:
  ``` shell
  @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
  ```
- 几个常用指令
  - `choco -?` 帮助指令, 获取choco指令的详细说明
  - `choco search` 搜索. 用 `-all` 可显示所有版本. 也可以查看[网页版](https://chocolatey.org/packages/)
  - `choco install` 安装. 用 '-version' 可指定版本
  - `choco upgrade` 升级
  - `choco uninstall` 删除
  - `choco list -localonly` 查看本地已安装的软件
- 以nodejs为例
  - `choco search nodejs` 加 `-all` 会显示所有版本!!!
  - 建议网页端搜索 [**软件源列表**](https://chocolatey.org/packages/)
  - `choco install nodejs -version 5.0.0`  安装nodejs 5.0.0这个版本, 默认使用安装 **.install**
  - `choco upgrade nodejs`  升级nodejs到最新版本
  - `choco uninstall nodejs`  删除nodejs
  - `choco list -localonly` 确认是否已删除

## 资料和参考
- Chocolatey 官方说明的 [安装方式](https://chocolatey.org/install)
- [Chocolatey 软件源列表](https://chocolatey.org/packages/)
- [更好的安装软件的方法](http://ninghao.net/blog/2071)
- [Windows下的包管理器Chocolatey](http://www.jianshu.com/p/831aa4a280e7)
- [Why Chocolatey is broken beyond any hope](https://medium.com/@keivan/why-chocolatey-is-broken-beyond-any-hope-d1a4e33b3d23#.jzmj9o5cd)


# ~~[Zeal][Zeal]~~

- [Zeal][Zeal]是一款在windows和Linux上, 功能类似于Mac上Dash的一款离线文档查看软件.
- 免费软件, 有绿色便携版, 支持的手册种类和Dash是一样的. 应该是为了跨平台, 基于Qt5开发, 反应有点慢.
- 下载安装完成后, `Tool`->`Docksets...`->窗口`Docsets`下->`Available`->选择语言->`Download`即可.
- **软件开发人员必备**. 还可以在atom直接调用查看API, 省去大量的文档搜索时间.

# 方案更新(2021年3月)
- 配置好以下两个软件就足够了.
    - [Quicker](https://getquicker.net/) 免费版, 完全使用鼠标的效率提升软件.
    - [utools](https://u.tools/) 免费版, 完全使用键盘的效率提升软件.
- 需要部分的第三方软件支持, 如 [Everything]


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***



[AutoHotKey]: https://autohotkey.com/
[Everything]: https://www.voidtools.com/
[Listary]: http://www.listary.com/
[Chocolatey]: https://chocolatey.org/
[ditto]: http://ditto-cp.sourceforge.net/
[Zeal]: https://zealdocs.org/
