---
title: Windows 软件系列-atom插件
date: 2016-10-12
categories: environment
tags: [windows, atom, mingw, c, python]
---

# [atom](https://atom.io/)简介
- 界面简洁, 基本上手可用, 无需复杂设置
- 开源免费, 而且多平台支持, 有丰富的插件库
- 和git的整合度很好! 直观明了好用
- 启动相对较慢, 但可接受.
- 懒人不想折腾, atom无明显短板, 就作为主力代码编辑器了
- 定位是 Notepad++ 为快速处理文件, atom 处理项目
- 此篇重点介绍 atom 插件的选择和安装, 以及配置快捷键. 基础介绍见[Windows 软件系列-文本编辑](https://draapho.github.io/2016/09/30/1603-WinSoft-editor/)


# atom 插件的安装方式
- `ctrl-,`->`Settings`->`Install`->选择要安装的插件
- 终端下使用命令行 `apm install`, 装完后需要重启atom.
  有些插件只能通过这个方式安装. 譬如要安装 `linter`, 命令行输入
  ```
  apm install linter
  ```


# atom 通用插件
- `Sublime-Style-Column-Selection` 使用 `alt-鼠标左键` 进入列选模式
- `atom-beautify` 自动格式化代码,
  - 需设置 `ctrl-b` 美化
- ~~`autocomplete-paths`~~ 辅助完成路径
- `block-comment-plus` 批量注释, 支持多种语言
  - 需设置 `ctrl-shift-/` 和 `ctrl-shift-\`
- `dash`  文档帮助, 配合 zeal (windows/linux) 或 dash(apple), 实现快速查询API
  - 需设置 `F1` 帮助
- ~~`disable-keybindings`~~ 快速禁用atom的部分快捷键
- `docblockr` 注释辅助, 快速添加函数的注释
  - 支持 `tab` 键直接在参数间跳转
  - `Align tags`->`deep`
  - `Auto add method tag`
  - ~~`Extend double slash`~~
- `highlight-selected` 自动高亮匹配的词,
- `hyperclick` 快速跳转到定义处, 仅限单文件, 但可由别的插件扩展
  - `Trigger keys for Windows` `ctrl-shift-click`. 用ctrl键和系统多选冲突
- `last-cursor-position` 浏览历史跳转
  - 需设置 `ctrl-shift-z` `ctrl-shift-y` 进行跳转
- `linter` 语法检查基础包
- `minimap` 文件地图
- `minimap-highlight-selected` 在文件地图中显示匹配的词
- `platformio-ide-terminal` 终端软件 
  - 支持 `ctrl-~` 快速打开, `ctrl-enter` 输入选中的文本
  - `Close Terminal on Exit`
  - `Shell Override`->`git-cmd.exe` 没有配置环境变量则需要使用绝对路径
  - `Shell Arguments`->`--no-cd --command=usr/bin/bash.exe -l -i`
  - `Working Directory`->`Project`
  - `Theme`->`homebrew` 黑底绿字
- ~~`Project Manager`~~ 加入项目的概念, 纯快捷键操作. 与`project-viewer`二选一即可.
- `project-viewer` 加入项目的概念,  带UI. 与`Project Manager`二选一即可.
  - `Status Bar Visibility`
  - `Autohide`
  - `Positon of the panel`->`Left`
  - ~~`Convert Old Data`~~
- `script` 一键执行, 支持多种代码, 不弹窗
  - 需设置 `F5` 执行
- `symbols-tree-view` 显示类/变量/函数列表
  - `Auto Hide`
  - `Auto Toggle`
- `tabs-to-spaces` tab空格互相转换
- ~~`vim-mode`~~ vim操作方式. 需要屏蔽按键 `ctrl-f`, 恢复为搜索按键
  ```
  'atom-text-editor.vim-mode:not(.insert-mode)':
    'ctrl-f': 'unset!'
  ```


# git 插件
- `git-time-machine` 查看单文件的git历史
  - 需设置 `f6` 查看比较
- ~~`git-plus`~~ git辅助, 我是通过 `platformio-ide-terminal` 打开终端敲git命令.
- merge-conflicts 查看git文件冲突
  - 需设置 `ctrl-f6` 查看冲突


# python 插件
- 配置 `atom-beautify` 之python语言
  - 安装 [python](https://www.python.org/) 
  - 安装 [autopep8](https://github.com/hhatto/autopep8), 调用 `pip install --upgrade autopep8`
  - 默认就是使用 `autopep8` 优化代码, 也推荐这个使用这个工具. `yapf`的优化结果无法满足`linter-flake8`的检查.
  - 测试. 打开一个 `.py` 文件, 右键选择 `Beautify editor contents` 看是否成功了.
- ~~`atom-python-run`~~ `F5`运行, 但是会弹cmd窗, 改用`script`
- `autocomplete-python` python辅助, 配合 `hyperclick` 跳转很方便
  - 设置快捷键 `f4` 跳转
  - `Show Descriptions`
  - `Autocomplete Function Parameters`->`all`
- `linter-flake8` 代码规范检查, 检查很严, 配合 autopep8 的自动格式化就很完美了.
  - 终端输入 `pip install flake8` python 安装 `flake8`
  - 终端输入 `apm install linter-flake8` atom 安装 `linter-flake8`
  - 插件配置 `Ignore Error`->`E501` 超过79列不要提示错误


# c/c++ 插件
- 配置 `atom-beautify` 之c/c++语言
  - 安装[uncrustify](http://uncrustify.sourceforge.net/), 可以自动美化多种语言的格式.
    - 下载[uncrustify-0.63.0-g44ce0f1-win32.zip](https://sourceforge.net/projects/uncrustify/files/uncrustify/uncrustify-0.63/)
    - 解压后, 将uncrustify目录加入环境变量, 已 `D:\uncrustify\` 为例
    - 终端内输入 `uncrustify -v`, 测试是否配置好 uncrustify
  - `atom-beautify` 插件的配置, 在c和c++下分别操作一次.
    - `Default Beautifier`->`Uncrustify` . ~~另一个选项 `clang-format` 需要安装clang, 里面带有指令`clang-format.exe`~~
    - `Config Path`->`D:\uncrustify\cfg\linux.cfg` 选择格式化模板
  - 测试, 打开一个 `.c` 文件, 右键选择 `Beautify editor contents` 看是否成功了.
- `atom-gtags`, 能比较好的实现跳转
  - 设置快捷键 `f4` 跳转
  - 右键项目根目录即可 `Build Gtags`
  - 放弃 ~~`atom-ctags`~~ 实测效果很差!
  - 比较: https://github.com/OpenGrok/OpenGrok/wiki/Comparison-with-Similar-Tools
- 基于gcc编译的配置
  - 下载 [MinGW](http://www.mingw.org/), 安装并设置好环境变量
    - 安装好后, 只是 `MinGW Installation Manager`, 实际上是个绿色软件. 打开后继续安装组件
    - `Basic Setup`->`mingw32-base` 和 `mingw32-gcc-g++`->左上 `Installation`->`Apply changes`->等待安装完成.
    - 这里只需要编译c和c++文件, 无需安装其它组件了.
    - 设置 `...\MinGW\bin` 文件夹到系统环境变量中
    - 复制一份 `mingw32-make.exe` 并重命名为 `make.exe`, 这样就能直接用 `make` 指令了
    - 测试. 终端中输入 `make -v` 和 `gcc -v`, 看是否可以识别到指令
  - ~~`gpp-compiler`~~ `f5`运行, 但会弹cmd窗, 决定使用内置终端
  - `linter-gcc` 基于gcc进行语法检查
    - `GCC Excutable Path`->`gcc` 或 `g++`, 没有配置环境变量的话, 使用绝对路径, 注意斜杠!
    - `GCC Include Paths`->`.../MinGW/include/*` 注意斜杠方向! 加入必要头文件.
    - 只在保存时, 才会进行语法检查
- ~~基于clang编译的配置~~
  - 彻底放弃这个系列, 不用vs, 基于mingw的配置失败.
  - 相关软件和参考如下
  - ~~`autocomplete-clang`~~ 自动完成
  - ~~`linter-clang`~~ 语法检查
  - [clang官网](http://llvm.org/). 官网进入的链接是找不到windows下编译好的版本的.
  - 下载特定版本的clang, 如 `LLVM-3.9.0`, 使用链接:<http://llvm.org/releases/3.9.0/>
  - 参考 [解决llvm/clang在windows下编译时找不到头文件和Lib的问题](http://m.blog.csdn.net/article/details?id=49902519)



# markdown插件
- atom已经支持markdown, 使用`ctrl-shift-m`即可预览. 如果要增强功能, 可以使用插件
- ~~`markdown-preview-enhanced`~~ markdown, 导出为pdf时, 制图显示有问题
  - `Break On Single Newline`
  - `Enable Typographer`
  - `Math Rendering Option`->`MathJax`
  - ~~`Enable Wiki Link Syntax`~~
  - ~~`Use GitHub.com syntax theme`~~
  - ~~`Print Background when generating pdf`~~ 否则pdf不显示制图
  - ~~`Use Github style when generating pdf`~~ 否则pdf不显示制图
  - ~~`Open preview pane automatically when opening a markdown file`~~
  - `Image Uploader`->`sm.ms` 建议这个. `imgur` 有时限
  - `Mermaid Theme`->`mermaid.forest.css`

  
  
# atom快捷键配置
- 使用 `ctrl-.` 查看按键冲突. 如果无效, 试试点到非编辑区(如目录树)试试.
- `ctrl-,`->`Settings`->`Keybindings`->`your keymap file`->打开`keymap.cson`
- 自定义快捷键方式可参考 [Basic Customization](http://flight-manual.atom.io/using-atom/sections/basic-customization/#_customizing_keybindings)
- 很明显, 要备份自己的快捷键设置, 只需要保存这份 `keymap.cson` 文件
- 最后禁用插件里不需要的快捷键, 或者使用 `disable-keybindings`.
  - `Keybindings` -> ~~`Enable`~~. 屏蔽以下插件:
  - `atom-beautify`, `atom-gtags`, `autocomplete-python`
  - `block-comment-plus`, `dash`, `git-time-machine`
  - `highlight-selected`, `hyperclick`, 
  - `script`, `symbols-tree-view`, `tabs-to-spaces`
- 我的 `keymap.cson` 配置

  ```
  # atom 大致原则是, 小窗口>大窗口, 然后才是客户配置>插件配置>系统配置
  # 因此优先级 'body' < 'atom-workspace' < 'atom-text-editor' < 'atom-text-editor:not([mini])'
  
  'atom-text-editor[data-grammar~=python]:not(.mini)':
    'f4': 'autocomplete-python:go-to-definition'
    'shift-f4': 'autocomplete-python:go-to-definition'
    'alt-shift-s': 'autocomplete-python:override-method'
  
  'atom-text-editor[data-grammar~=c]:not(.mini)':
    'f4': 'atom-gtags:get-definitions'
    'shift-f4': 'atom-gtags:get-references'
  
  '.platform-win32 atom-workspace atom-text-editor:not([mini])':
  # character                            
    'ctrl-b': 'atom-beautify:beautify-editor'
    'ctrl-d': 'core:delete'
    'ctrl-shift-d': 'editor:delete-line'
    'ctrl-j': 'core:move-down' 
    'ctrl-k': 'core:move-up'   
    'ctrl-l': 'core:move-right'
    'ctrl-h': 'core:move-left'
    'ctrl-shift-j': 'editor:move-line-down'
    'ctrl-shift-k': 'editor:move-line-up'
    'ctrl-shift-l': 'editor:move-to-end-of-word'
    'ctrl-shift-h': 'editor:move-to-beginning-of-word'
    'alt-shift-j': 'editor:join-lines'
    'ctrl-m': 'bookmarks:toggle-bookmark'  
    'ctrl-r': 'core:redo'
    'ctrl-u': 'core:undo'
    'ctrl-shift-v': 'editor:duplicate-lines'
    'ctrl-shift-W': 'tabs:close-other-tabs'
    'ctrl-shift-x': 'editor:select-line'
    'ctrl-shift-y': 'last-cursor-position:next'
    'ctrl-shift-z': 'last-cursor-position:previous'
  # special
    'ctrl-4': 'editor:move-to-end-of-screen-line'         # ctrl-$
    'ctrl-6': 'editor:move-to-first-character-of-line'    # ctrl-^
    'ctrl-$': 'editor:select-to-end-of-line'              # ctrl-shift-$
    'ctrl-^': 'editor:select-to-first-character-of-line'  # ctrl-shift-^
    'ctrl-?': 'block-comment-plus:toggle'                 # ctrl-shift-/
    'ctrl-|': 'block-comment-plus:toggle'                 # ctrl-shift-\
    'ctrl-]': 'bracket-matcher:select-inside-brackets'
    'ctrl-[': 'bracket-matcher:go-to-matching-bracket'
    'ctrl-.': 'tabs-to-spaces:untabify-all'
    'ctrl->': 'tabs-to-spaces:tabify'                     # ctrl-shift-.
  # alt
    'alt-0': 'editor:fold-all'
    'alt-)': 'editor:unfold-all'                          # alt-shift-0
    'alt-!': 'editor:unfold-all'                          # alt-shift-1
    'alt-1': 'editor:fold-at-indent-level-1'
    'alt-2': 'editor:fold-at-indent-level-2'
    'alt-3': 'editor:fold-at-indent-level-3'
    'alt-4': 'editor:fold-at-indent-level-4'
    'alt-5': 'editor:fold-at-indent-level-5'
    'alt-6': 'editor:fold-at-indent-level-6'
    'alt-7': 'editor:fold-at-indent-level-7'
    'alt-8': 'editor:fold-at-indent-level-8'
    'alt-9': 'editor:fold-at-indent-level-9'
  # f1-f6
    'f1': 'dash:shortcut'
    'ctrl-f2': 'bookmarks:view-all'
    'ctrl-shift-f2': 'bookmarks:clear-bookmarks'
    'ctrl-f3': 'find-and-replace:select-all'
    'f5': 'script:run'
    'f6': 'git-time-machine:toggle'
    'ctrl-f6': 'merge-conflicts:detect'
    'shift-f6': 'merge-conflicts:next-unresolved'
    'ctrl-shift-f6': 'merge-conflicts:previous-unresolved'
  
  'body':
    'ctrl-j': 'core:move-down'
    'ctrl-k': 'core:move-up'
    'ctrl-r': 'core:redo'
    'ctrl-u': 'core:undo'
    'ctrl-shift-S': 'window:save-all'
  # unset ctrl-k *
    'ctrl-k up': 'unset!'
    'ctrl-k down': 'unset!'
    'ctrl-k left': 'unset!'
    'ctrl-k right': 'unset!'
    'ctrl-k ctrl-w': 'unset!'
    'ctrl-k ctrl-alt-w': 'unset!'
    'ctrl-k ctrl-p': 'unset!'
    'ctrl-k ctrl-n': 'unset!'
    'ctrl-k ctrl-up': 'unset!'
    'ctrl-k ctrl-down': 'unset!'
    'ctrl-k ctrl-left': 'unset!'
    'ctrl-k ctrl-right': 'unset!'
  'atom-workspace atom-text-editor':
    'ctrl-k ctrl-u': 'unset!'
    'ctrl-k ctrl-l': 'unset!'
  'atom-workspace atom-text-editor:not([mini])':
    'ctrl-k ctrl-0': 'unset!'
    'ctrl-k ctrl-1': 'unset!'
    'ctrl-k ctrl-2': 'unset!'
    'ctrl-k ctrl-3': 'unset!'
    'ctrl-k ctrl-4': 'unset!'
    'ctrl-k ctrl-5': 'unset!'
    'ctrl-k ctrl-6': 'unset!'
    'ctrl-k ctrl-7': 'unset!'
    'ctrl-k ctrl-8': 'unset!'
    'ctrl-k ctrl-9': 'unset!'
  '.platform-win32, .platform-linux': 
    'ctrl-k ctrl-b': 'unset!'
  '.platform-win32 .tree-view, .platform-linux .tree-view':
    'ctrl-k right': 'unset!'
    'ctrl-k l': 'unset!'
    'ctrl-k left': 'unset!'
    'ctrl-k h': 'unset!'
    'ctrl-k up': 'unset!'
    'ctrl-k k': 'unset!'
    'ctrl-k down': 'unset!'
    'ctrl-k j': 'unset!'
  '.platform-win32 atom-text-editor, .platform-linux atom-text-editor':
    'ctrl-k ctrl-d': 'unset!'
    'ctrl-u': 'unset!'
  ```


  
# 参考和资料
- [Atom Flight Manual](http://flight-manual.atom.io/), atom手册
- [atom Packages](https://atom.io/packages), atom插件中心
- 我的 [Windows快捷键](https://draapho.github.io/2016/10/08/1607-Shortcut-win/)



----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
