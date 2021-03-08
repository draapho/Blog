---
title: Vim常用快捷键
date: 2016-10-1
categories: linux
tags: [shortcut, vim]
description: 如题.
---


# Vim常用快捷键
## 进入输入模式

| 快捷键       | 助记            | 说明          |
| --------- | ------------- | ----------- |
| `i`       | insert        | 光标前插入文本     |
| `I`       | insert        | 行首插入文本      |
| `ea`      | end append    | 单词末插入文本     |
| `a`       | append        | 光标后插入文本     |
| `A`       | append        | 行尾插入文本      |
| `o`       | open new line | 向下插入新行      |
| `O`       | open new line | 向上插入新行      |
| `cw`      | change word   | 修改单词        |
| `cc`      | change        | 删除整行后修改     |
| `c^` `c$` | change        | 删除到行首/行尾后修改 |

## 光标移动

| 快捷键          | 助记      | 说明        |
| --------------- | ------- | --------- |
| `h` `j` `k` `l` |         | 左/下/上/右   |
| `^` `0` `$`     |         | 行首/首字母/行尾 |
| `w`             | word    | 下个字开头     |
| `e`             | end     | 本字结尾      |
| `b`             | before  | 上个字开头     |
| `fx`            | find+字符 | 移动到x字符处   |
| `5enter`        |         | 向下移5行    |
| `gg` `1G`       | go      | 回首行       |
| `G`             | go      | 到末行       |
| `5G`            | num+go  | 到第5行      |
| `ctrl+u`        | up      | 向上翻半页     |
| `ctrl+d`        | down    | 向下翻半页     |
| `{` `}`         |         | 块首/块尾     |
| `H`             | high    | 屏幕顶部      |
| `M`             | medium  | 屏幕中部      |
| `L`             | low     | 屏幕底部      |

## 文本编辑

| 快捷键       | 助记           | 说明          |
| ------------ | ------------ | ----------- |
| `r`          | repalce      | 替换单个字符      |
| `~`          |              | 改变字符大小写 |
| `x` `5x`     |              | 删除字符        |
| `dw` `5dw`   | delete word  | 删除单词        |
| `db` `5db`   | delete befor | 向前删除单词      |
| `dd` `5dd`   | delete       | 删除整行        |
| `d^` `d$`    | delete       | 删除到行首/行尾    |
| `d1G` `dG`   | delete       | 删除到第一行/最后一行 |
| `yw` `5yw`   | yank word    | 复制单词        |
| `yy` `5yy`   | yank         | 复制整行        |
| `y^` `y$`    | yank         | 复制到行首/行尾    |
| `>>` `<<`    |              | 单行缩进   |
| `p` `P`      | paste        | 黏贴(光标后/光标前) |
| `J`          | join         | 将下一行合并到当前行 |
| `u`          | undo         | 撤销更改/撤销输入   |
| `ctrl+r`     | redo         | 恢复          |
| `ctrl+r`     | redo         | 恢复          |
| `.`          |              | 重复编辑动作 |

## 视图模式

| 快捷键     | 助记          | 说明     |
| ------- | ----------- | ------ |
| `v`     | visual      | 进入视图模式 |
| `>` `<` |             | 代码缩进   |
| `d` `y` | delete yank | 剪切/复制  |
| `~`     |             | 改变大小写 |

## 查找与替换

| 快捷键                 | 助记            | 说明              |
| ------------------- | ------------- | --------------- |
| `/str`              |               | 查找str           |
| `n` `N`             | next          | 查找下一个/上一个       |
| `:s/old/new/g`      | start...go    | 所在行old替换为new    |
| `:n1,n2s/old/new/g` | start...go    | n1-n2行old替换为new |
| `:0,$/old/new/g`    | start...go    | 全文old替换为new     |
| `:%s/old/new/g`     | start...go    | 全文old替换为new     |
| `:n1,n2s/^/\/\//g`  | `^` 行首 `/` 转义 | 行首替换为//, 即注释掉   |

## 保存与退出

| 快捷键          | 助记             | 说明    |
| ------------ | -------------- | ----- |
| `esc`  |  | 返回命令模式 |
| `:wq` `:wq!` | write & quit   | 保存并退出 |
| `:q` `:q!`   | quit  `!` sudo | 退出    |

## Vim 助记图, 总有一款适合你
- [中文版 Vim Cheat Sheet](http://vim.rtorr.com/lang/zh_cn/) 网页版, 支持多语言

- [A Great Vim Cheat Sheet](http://vimsheet.com/) 网页版

- [Graphical vi-vim Cheat Sheet and Tutorial](http://www.viemu.com/a_vi_vim_graphical_cheat_sheet_tutorial.html)
  ![vi/vim graphical cheat sheet](http://www.viemu.com/vi-vim-cheat-sheet.gif)
- [Beautiful Vim Cheat-Sheet](http://vimcheatsheet.com/)
  ![Vim Cheat-Sheet Preview](https://cdn.shopify.com/s/files/1/0165/4168/files/preview.png)
- [VI (Linux Terminal) Help Sheet](https://www.gosquared.com/blog/vi-linux-terminal-help-sheet)
  ![VI Help Sheet](https://downloads.gosquared.com/help_sheets/10/VI-Help-Sheet-large.jpg)
- [給程式設計師的Vim入門圖解說明](http://blog.vgod.tw/2009/12/08/vim-cheat-sheet-for-programmers/)
  ![Vim入門圖解說明](http://blog.vgod.tw.s3.amazonaws.com/wp-content/uploads/2009/12/vim-cheat-sheet-diagram.png)
- [vim极简中文示意图](http://linux.vbird.org/linux_basic/0310vi.php)->`9.3.6 vim 常用指令示意图`
  ![vim极简中文示意图](https://draapho.github.io/images/1604/vimCheatSheet.jpg)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***