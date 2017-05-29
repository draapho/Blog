---
title: Windows 软件系列-文本编辑
date: 2016-09-30
categories: windows
tags: [windows, Notepad++, atom, Typora, utf-8]
---


# [Notepad++][npp]

## Npp简介
- [Notepad++][npp]简称Npp, 是免费好用的记事本
- 轻便小巧, 打开速度快. 自带丰富功能且有插件, 如语法高亮
- 建议用他彻底替换windows自带的记事本
- 目前出到npp7, **不要装64位版本**, 很多插件都不支持
- 有绿色便携版, 但需要额外设置右键打开和文件关联功能

## Npp设置
### 首选项设置
- `Setting`->`Preferences` 打开首选项页面
- `General`->`Double click to close document`
- `Editing`->`Muli-Editing Setting`->`Enable (Ctrl...)`
- `Editing`->`Vertical Edge Setting`->`Show vertical edge`->`Line mode`->`Number of columns: 80`
- `File Association`->选择需要关联的文件后缀, 加入到`Registered extensions`
  关联其它后缀名, 只需在`customize`->填入后缀并加入, 如 `.config` `.gitignore`
  注意: **绿色便携版设置了文件关联也是没有效果的**, 用windows下右键`打开方式`设置吧
- `Tab Setting`->`[Default]`->`Tab size:4`->`Replace by space`
- `Tab Setting`->`makefile`->~~`Use default value`~~->~~`Replace by space`~~, 因为make只认TAB键
- `Auto-Completion`->`Auto-Completion`->`From 2 th character`
- `Auto-Completion`->`Auto-Insert`->`'`
- `Auto-Completion`->`Auto-Insert`->`html/xml close tag`
- ~~`Auto-Completion`->`Auto-Insert`->`Matched pair`~~ 加入 `*` 和 `(即`~`键), !!!重启后失效, 原因不明.

### 主题设置
- `Settings`->`Style Configurator`->`Select theme`->`Twilight`
- 对`Monokai `注释配色非常无语, 而且对python的配色也太不友好了, 只好放弃.

### 自定义语法高亮
- 以导入自定义的 markdown 语法高亮为例
- 可以去网上搜索[下载markdown语法高亮文件](https://github.com/draapho/Blog/tree/master/_blog_stuff/Notepad%2B%2B/markdown)
- `Language`->`Define your language ...`->`Import`->选择下载的`markdown_*.xml`文件即可
- 导入成功后, `Language`->`Define your language ...`下面就会有markdown语言了

### Npp插件
- 插件的安装 (**64位版本无法支持大多数插件**)
  1. `Plugins`->`Plugin Manager`->`Show Plugin Manager`->安装插件
  2. 将插件的`.dll`文件直接放到`plugins`目录下. (说明插件可以免安装)
- `compare` 文件比较功能.
  由于使用了深色主题, 需要使用深色作为背景
  `Plugins`->`compare`->`Option`->`Clolr setting`->点选颜色`More Colors` 调深即可
- `customize toolbar` 可自定义工具栏
- `File Switcher` 提供`ctrl+tab`在视图窗口切换标签的功能
- `Hex-Editor` 增加二进制编辑模式
- `Light Explorer` 增加资源管理器界面
- `Location Navigate` 浏览历史跳转
  取消 `Mark Changed Line`, 配色看不清楚!
- ~~`ViSimulator`~~ vim模式, `ctrl+shift+alt+v` 使能或禁止. 可以从[这里下载](https://web.archive.org/web/20150515145616/http://www.visimulator.com/download.html)
- `Zoom Disabler` 屏蔽ctrl+滚轮的缩放功能

## [Python Script][pys]插件
- [Python Script][pys]针对notepad++的python插件, 可以用来批量处理文件
- [下载最新版本1.0.8.0](https://sourceforge.net/projects/npppythonscript/files/Python%20Script%201.0.8.0/) `PythonScript_Full_1.0.8.0.zip` 即可
- 解压后将整个文件拷贝到notepad++的根目录下, 目录结构如下:
  ```
  Notepad++ (Notepad++ 根目录, 例如"C:\Program Files\npp")
   +
   |-- python26.dll
   +-- plugins
             |-- PythonScript.dll
             |-- PythonScript
             |   |-- lib
             |   |     |-- (*.py)
             |   |-- scripts
             |             |-- (machine-level scripts)
             |-- doc
             |     |-- PythonScript
             |             |-- PythonScript.chm
             |-- Config (也可能在 %APPDATA%\Notepad++\plugins\config\)
                           \-- PythonScript
                                           |-- scripts
                                                     |-- (用户脚本)
  ```

- 检测是否安装成功. 重启notepad++. 按如下步骤进行测试
  `Plugins->Python Script`->`Show Console`->显示`Python ... Ready.`

- [一个实用的脚本示例](https://github.com/draapho/Blog/tree/master/_blog_stuff/Notepad%2B%2B/Python%20Script), **注意**, 需要使用Notepad++ 7及以上版本, 否则执行结果和预期会有差别.
  ``` python
  import os;
  import sys;
  from Npp import *

  # 对所有打开的文件去除行尾空格并将空格替换为TAB
  def run_menu_command():
    # Edit->Blank Operations
    notepad.runMenuCommand("Blank Operations", "Trim Trailing Space")
    notepad.runMenuCommand("Blank Operations", "Space to TAB (All)")
    return

  # Find and operate files opened at notepad
  # There is something wrong run in NPP6.X
  def operate_file_in_notepad():
    file_list = notepad.getFiles()
    for file in file_list:
        fn = file[0]
        notepad.activateFile(fn)
        run_menu_command()

  operate_file_in_notepad()
  ```

## 绿色版注册右键
- 基本思路是直接修改注册表, 增加右键`Notepad++ Here`
- 写了批处理文件, 放到notepad++根目录, 管理员权限执行即可.
  [_RegisterKey_Admin.bat](https://github.com/draapho/Blog/blob/master/_blog_stuff/Notepad%2B%2B/_RegisterKey_Admin.bat) 注册右键, 需管理员权限执行.
  [_UnregisterKey_Admin.bat](https://github.com/draapho/Blog/blob/master/_blog_stuff/Notepad%2B%2B/_UnregisterKey_Admin.bat) 注销右键, 需管理员权限执行.
- 也可以手动创建文件 `注册右键.reg`, 内容如下.
  **上述批处理的思路**就是自动生成这个 `.reg` 文件然后导入注册表.
  **需要替换notepad++安装路径**. 然后管理员权限执行即可.
  ```
  Windows Registry Editor Version 5.00
  [HKEY_CLASSES_ROOT\*\Shell\NotePad++ Here]
  [HKEY_CLASSES_ROOT\*\Shell\NotePad++ Here\Command]
  @="\"D:\\Program Files\\npp\\notepad++.exe\" \"%1\""
  ```

## 快捷键设置
- 需按照[编辑器快捷键](https://draapho.github.io/2016/10/08/1607-Shortcut-win/)设置
- 设置好的[快捷键配置文件](https://github.com/draapho/Blog/tree/master/_blog_stuff/Notepad%2B%2B/shortcuts.xml), 直接替换原有的shortcuts.xml即可
- 说明一下`run`的设置, 可参考官方说明[Notepad++调用外部程序](http://docs.notepad-plus-plus.org/index.php/External_Programs)
  - `Zeal.lnk $(CURRENT_WORD)` 在Zeal中查询选中内容
  - `Typora.lnk "$(FULL_CURRENT_PATH)"` 在Typora中预览文件
  - `ConEmu.lnk -Dir "$(CURRENT_DIRECTORY)"` 使用当前路径打开ConEmu
  - 上述三个指令需要配置好全局变量, 或者使用绝对路径. 
  - 后缀名为lnk是因为我用了快捷方式放在同一个目录下, 简化设置全局变量的步骤
  - `http://www.google.com/search?q=$(CURRENT_WORD)` 选中的内容直接google搜索
- 环境变量的配置, 可以参考[Windows 软件系列-自定义环境变量](https://draapho.github.io/2016/10/09/1608-WinSoft-path/)
- notepad++的宏录制功能也非常有用, 譬如可以录制一个 `TAB to Space` + `Trim Trailing Space` + `Save` 保存并设置快捷键为 `ctrl-s`, 这样就可以保存前自动完成空格处理了.

## 资源和参考
[Notepad++官网][npp]
[Notepad++插件中心](http://docs.notepad-plus-plus.org/index.php/Plugin_Central)
[Notepad++调用外部程序](http://docs.notepad-plus-plus.org/index.php/External_Programs)
[轻量级文本编辑器，Notepad最佳替代品：Notepad++](http://www.crifan.com/files/doc/docbook/rec_soft_npp/release/html/rec_soft_npp.html)
[notepad++如何关联到右键菜单](http://jingyan.baidu.com/article/a24b33cd71f2d619ff002b60.html)


# [atom][atom]

## atom简介
- 界面简洁, 基本上手可用, 无需复杂设置
- 开源免费, 而且多平台支持, 有丰富的插件库
- 和git的整合度很好! 直观明了好用
- 启动相对较慢, 但可接受.
- 懒人不想折腾, atom无明显短板, 就作为主力代码编辑器了
- 定位是 Notepad++ 为快速处理文件, atom 处理项目

## 两个快捷键
- 为了避免打开atom后一头雾水, 需要记住两个快捷键
- `ctrl+shift+p`, 打开atom命令窗口, 可以输入指令如`setting`
- `ctrl+,` 打开设置页面

## atom设置
- `ctrl+,`进入设置界面 `Settings`
- `Editor` 界面下, 设置基本参数
  - `Show Ivisibles`
  - `Soft Tabs`
  - `Tab Length`->`4`
  - `Tab Type`->`auto`, 由于makefile必须为TAB, 否则可以设为 `soft` Tab键输入4个空格
- `System` 界面下, 增加系统右键
  - `Register as file handler`
  - `Show in file context menus`
  - `Show in folder context menus`
- `Themes` 界面下, 选个喜欢的主题. 默认是`One Dark`
- `Packages`->搜索`tree view`->`Core Packages`->`tree-view`->`Settings`
  - `Hide Ignored Names` 隐藏atom指定的文件
  - `Hide VCS Ignored Files` 隐藏`.gitignore`指定的文件

## atom插件
- 插件太多, 脱离需求讲插件是没有意义的. 新手的话, 先探索着玩玩吧.
- 记得仔细阅读插件的使用说明, 有些插件配置起来挺麻烦的. 但atom的插件管理已经很好了.
- 后续会根据自己的需求再写一篇atom的插件篇, 并详述如何配置.
- 下面推荐几个通用型的实用插件.
- `ctrl+,`进入设置界面 `Settings`
- `Install` 界面下, 搜索安装如下插件
   - `atom-beautify` 代码格式美化, 需要安装辅助软件
   - `git-time-machine` 查看比较文件的git历史
   - `highlight-selected` 高亮选择的词
   - `minimap` 文件小地图
   - `minimap-highlight-selected` 在minimap内高亮选择的词
   - `platformio-ide-terminal` 内嵌终端
   - `project-manager` 管理项目.
   - `project-viewer` 管理项目, 带UI
   - `Sublime-Style-Column-Selection` 列操作使用`alt+drag`
   - `tabs-to-spaces` 空格/TAB自动转换
   - `vim-mode` 提供vim模式.

## 自定义快捷键
- 以 `ctrl-f` 为例, 安装vim后, 变成翻页键, 但希望的是文件搜索和替换键.
- 可以禁止vim的`keybindings`, 但这里不适用, 因为还要用vim的其它快捷键.
- `ctrl+,`->进入设置界面 `Settings`->`Keybindings`->输入`ctrl-f`
- 找到`vim-mode:scroll-full-screen-down`->点左边的复制图标
- 点击`your keymap file`->打开`keymap.cson`->黏贴内容
  ```
  'atom-text-editor.vim-mode:not(.insert-mode)':
    'ctrl-f': 'vim-mode:scroll-full-screen-down'
  ```
- 要屏蔽 vim 的 `ctrl-f`, 修改为`unset!`即可. 内容如下:
  ```
  'atom-text-editor.vim-mode:not(.insert-mode)':
    'ctrl-f': 'unset!'
  ```
- 自定义详情可以参考官网的[Basic Customization](http://flight-manual.atom.io/using-atom/sections/basic-customization/#_customizing_keybindings)
- 需按照[编辑器快捷键](https://draapho.github.io/2016/10/08/1607-Shortcut-win/)设置
- 环境变量的配置, 可以参考[Windows 软件系列-自定义环境变量](https://draapho.github.io/2016/10/09/1608-WinSoft-path/)


# [Typora][typora]

## markdown简介
- ***强烈推荐 Markdown***, 基本可以放弃office word了!!!
- markdown在专注于写作内容的同时, 快速便捷的自动美化格式
- [查看Markdown语法和效果](https://draapho.github.io/about/markdownplus/)
- atom做编辑器也不错, 推荐插件 `markdown-preview-enhanced`. 但mermaid制图打印有问题.
- 而且什么都用atom, atom就太重了, 这里推荐 [Typora][typora].

## Typora简介
- [Typora][typora]是一款极简的markdown编辑器. 多平台可用
- 单窗口显示, 使用 `ctrl+/` 切换预览和写作模式. 而且预览模式下也可直接写作.
- 支持[LaTex数学公式](https://en.wikibooks.org/wiki/LaTeX/Mathematics), [mermaid制图](http://knsv.github.io/mermaid/),[Emoji图标](http://www.webpagefx.com/tools/emoji-cheat-sheet/)
- 借助[pandoc](http://pandoc.org/),可导出多种格式
- 缺点: 打开较慢, 不支持列操作, 不能用鼠标右键.
- 熟悉markdown格式后, 可以用notepad++写作, 用Typora查看效果和转换格式.

## Typora安装和设置
- 下载并安装[Typora windows 版本](http://www.typora.io/#windows)
- 下载并安装[pandoc-xxx-windows.msi](http://pandoc.org/installing.html)
- 打开`Typora`->`File`->`Preference`
- `Syntax Support` 使能如下选项
  - `Inline math` 数学公式
  - `Subscript` 下标
  - `Superscript` 上标
  - `Highlight` 高亮
  - `Diagrams` 制图
- `Syntax Preference`
  - `Heading Style` `atx(#)` 偏好使用`#`标记为标题
  - `Unodered List` `-` 偏好使用`-`标记为列表

## markdown语法参考
- [Markdown语法](https://draapho.github.io/about/markdownplus/)
- [mermaid制图](http://knsv.github.io/mermaid/)
- [LaTeX数学公式](https://en.wikibooks.org/wiki/LaTeX/Mathematics)
- [Emoji图标](http://www.webpagefx.com/tools/emoji-cheat-sheet/)



# [google drive][gd]

- 主要作为云使用, 不少手机APP支持[google drive][gd], 而且还有好用的网页端应用
- 在线markdown编辑器[stackedit](https://stackedit.io/)
- 在线制图软件[draw.io](https://www.draw.io)
- 手机端markdown编辑器[iA Writer](https://ia.net/writer)


# 默认新建utf-8文本文件

- 用notepad++建立一个样本文件, 命名为`UTF8.txt`, 设置为 `UTF-8` 编码(不带BOM), 放在 `C:\Windows\SHELLNEW` 下. 建议内容为空(内容会出现在新建文件中).
- `regedit`->打开 `注册表`->`HKEY_CLASSES_ROOT\.txt\ShellNew`->右侧新建 `字符串值`->名称 `FileName`-> 数据 `UTF8.txt`
- 此时, 新建的`文本文档`就是`UTF-8`编码的的文件. 事实上是复制了 `UTF8.txt` 这个样本文件.
- 参考 [Windows新建文件改为默认UTF8](http://alanhou.org/windows-default-encoding-utf8/)


----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***



[npp]: https://notepad-plus-plus.org/
[pys]: http://npppythonscript.sourceforge.net/index.shtml
[atom]: https://atom.io/
[typora]: http://www.typora.io/
[gd]: https://drive.google.com/
