---
title: Windows快捷键
date: 2016-10-8
categories: windows
tags: [cheat sheet, windows, notepad++, atom, eclipse, Listary]
---

# 专用快捷键

| atom             | 备注             | 说明                  |
| ---------------- | -------------- | ------------------- |
| `ctrl-shift-p`   | palette        | 调出命令板               |
| `ctrl-alt-i`     | information    | 调用控制台               |
| `ctrl-,`         |                | 打开设置面板              |
| `ctrl-.`         | 非编辑区有效   | 调试快捷键               |
| +`ctrl-f6`       | merge-conflicts | 显示有冲突的文件        |
| +`shift-f6`      | merge-conflicts | 显示下一个冲突        |
| +`ctrl-shift-f6` | merge-conflicts | 显示上一个冲突        |
| **eclipse**      | **备注**       | **说明**              |
| `ctrl-o`         |                | 显示函数列表              |
| `ctrl-shift-o`   |                | 自动处理 include/import |
| `alt-shift-s`    | source         | 显示代码常用操作            |
| `alt-/`          |                | 代码提示                |
| + `ctrl \`       | ~~`ctrl-tab`~~ | 切换`.c``.h`文件        |
| + `alt-\`        | `alt-shift-a`  | 列选模式                |
| + `ctrl-f3`      | `ctrl-1`       | 快速修复                |
| + `alt-shift-f`  | `ctrl-shift-t` | 查找类                 |



# 编辑器快捷键


| 文件操作                    | 助记       | 说明            | 来源                 |
| ----------------------- | -------- | ------------- | ------------------ |
| `ctrl-n`                | new      | 创建文件          | windows            |
| `ctrl-o`                | open     | 打开文件          | windows            |
| `ctrl-s`                | save     | 保存            | windows            |
| `ctrl-shift-s`          | save     | 保存所有          | notepad++          |
| `ctrl-w`                | windows  | 关闭当前页         | windows            |
| `ctrl-shift-w`          | windows  | 关闭其它页面        | custom             |
| `ctrl-shift-t`          | tags     | 恢复关闭的文件       | notepad++          |
| `ctrl-tab`              | tab      | 下一个标签         | notepad++          |
| `ctrl-shift-tab`        | tab      | 上一个标签         | notepad++          |
| `f1`                    |          | help          | windows            |
| `ctrl-f1`               |          | google搜索选定内容  | custom             |
| **文件编辑**                | **助记**   | **说明**        | **来源**             |
| `ctrl-a`                | all      | 全部选中          | windows            |
| `ctrl-c`                | copy     | 复制            | windows            |
| `ctrl-shift-c`          | copy     | 复制文档路径        | atom               |
| `ctrl-d`                | delete   | 删除            | custom             |
| `ctrl-shift-d`          | delete   | 删除当前行         | custom             |
| `ctrl-` `h` `j` `k` `l` | vim      | 上下左右          | custom             |
| `ctrl-shift-h` `ctrl-←` | vim h    | 左移到词首         | custom / sublime   |
| `ctrl-shift-l` `ctrl-→` | vim l    | 右移到词尾         | custom / sublime   |
| `ctrl-shift-j` `ctrl-↓` | vim j    | 向下移行          | custom / sublime   |
| `ctrl-shift-k` `ctrl-↑` | vim k    | 向上移行          | custom / sublime   |
| `alt-shift-j`           | vim J    | 合并行           | custom             |
| ~~`ctrl-t`~~            | 禁用掉      | 避免`ctrl-y`失效  | custom             |
| `ctrl-v`                | velcro   | 黏贴            | windows            |
| `ctrl-shift-v`          | ctrl-v   | 复制当前行         | custom             |
| `ctrl-x`                |          | 剪切            | windows            |
| `ctrl-shift-x`          | ctrl-x   | 剪切当前行         | notepad++          |
| `ctrl-y` `ctrl-r`       | redo     | 恢复更改          | windows / vim      |
| `ctrl-z` `ctrl-u`       | undo     | 撤销更改          | windows / vim      |
| `ctrl-shift-y`          |          | 下一个浏览记录    | custom     |
| `ctrl-shift-z`          |          | 上一个浏览记录    | custom      |
| `alt-鼠标` `alt-\`        |          | 列选模式          | notepad++ / custom |
| `ctrl-enter`            | enter    | 下面新增一行        | sublime            |
| `ctrl-shift-enter`      | enter    | 上面新增一行        | sublime            |
| `tab` `shift-tab`       |          | 插入缩进/删除缩进     | notepad++          |
| `ctrl-^`                | vim      | 移到行首          | custom             |
| `ctrl-shift-^`          | vim      | 选到行首          | custom             |
| `ctrl-$`                | vim      | 移到行尾          | custom             |
| `ctrl-shift-$`          | vim      | 选到行尾          | custom             |
| **查找与替换**               | **助记**   | **说明**        | **来源**             |
| `ctrl-f`                | find     | 查找            | windows            |
| `ctrl-shift-f`          | find     | 多文件查找         | sublime            |
| `f3` `shift-f3`         |          | 查找下一个 / 查找上一个 | windows            |
| `ctrl-f3`               |          | 选中所有匹配的关键字    | custom             |
| `ctrl-m`                | mark     | 打标记           | custom             |
| `f2` `shift-f2`         | tag      | 下一个标记/上一个标记   | notepad++          |
| `ctrl-f2`               | tag      | 显示所有标签        | custom             |
| `ctrl-shift-f2`         | tag      | 清空所有标签        | custom             |
| `ctrl-.`                | ..       | TAB转为空格       | custom             |
| `ctrl-shift-.`          | >>       | 空格转为TAB       | custom             |
| **代码专用**                | **助记**   | **说明**        | **来源**             |
| `ctrl-b`                | beautify | 格式化代码         | custom             |
| `ctrl-shift-m`          | markdown | markdown预览    | atom               |
| `alt-0` `alt-shift-0`   | 0-9      | 折叠代码/展开代码     | notepad++          |
| `ctrl-[` `ctrl-]`       |          | 移动/全选对应括号     | custom             |
| `ctrl-鼠标` `shift-鼠标`    |          | 跳转            | eclipse / custom   |
| `f4` `shift-f4`         |          | 跳转 / 跳回       | custom             |
| `f5`                    | run      | 运行            | notepad++          |
| `f6`                    |          | 比较文件          | custom             |
| `ctrl-/`                | `//`     | 单行注释翻转        | eclipse            |
| `ctrl-shift-/`          | `/*`     | 多行注释          | eclipse            |
| `ctrl-shift-\`          | `/*`     | 取消多行注释        | eclipse            |
| `ctrl-~`                |          | 打开终端          | sublime            |


# Win系统快捷键

| Listary           | 助记                 | 功能                    |
| ----------------- | ------------------ | --------------------- |
| `win-~`           |                    | 打开Listary             |
| `enter`           | enter              | 打开文件                  |
| `ctrl-enter`      | enter              | 打开路径                  |
| `ctrl-c`          | copy               | 复制                    |
| `ctrl-shift-c`    | copy               | 复制路径                  |
| `ctrl+j` `ctrl+k` | vim j,k            | 下一个 / 上一个(需设置)        |
| **Ditto**         | **助记**             | **文件夹/应用**            |
| `ctrl-1`          | list               | 打开ditto面板             |
| `enter`           | enter              | 黏贴                    |
| `shift-enter`     | enter              | 纯文本黏贴                 |
| **AHK**           | **助记**             | **功能**                |
| `鼠标中键`            |                    | 复制                    |
| `shift-鼠标中键`      |                    | 剪切                    |
| `ctrl-shift-鼠标中键` |                    | 复制当前路径                |
| `鼠标右键`            |                    | 首次黏贴                  |
| `ctrl-鼠标右键`       |                    | 黏贴                    |
| `ctrl-~`          |                    | 打开终端 (关联路径)           |
| `alt-win-鼠标中键`    |                    | 复制屏幕颜色                |
| `alt-win-←↑↓→`    |                    | 单像素移动鼠标               |
| `alt-win-d`       | date               | 输入当前日期                |
| **AHK快捷方式**       | **助记**             | **文件夹/应用**            |
| `alt-a` `win-a`   | all / audio        | 我的电脑 / 音频处理软件         |
| `alt-b` `win-b`   | backup             | backup / FreeFileSync |
| `alt-c` `win-c`   | c盘 / caculate      | c盘 / 计算器              |
| `alt-d` `win-d`   | download           | download / 迅雷         |
| `alt-e` `win-e`   | e盘 / editor        | e盘 / 编辑器              |
| `alt-f` `win-f`   | f盘 / find          | f盘 / everything       |
| `alt-g` `win-g`   | green / google     | 绿色软件 / 浏览器            |
| `win-h`           | help               | zeal 文档帮助             |
| `win-i`           | ie                 | IE核浏览器                |
| `win-j`           | 记账                 | MoneyHome             |
| `alt-l` `win-l`   | life / look        | life / 视频搜索           |
| `alt-m` `win-m`   | music              | music / mcool         |
| `win-n`           | notepad            | notepad++             |
| `alt-p` `win-p`   | picture            | picture / Paint.Net   |
| `alt-s` `win-s`   | study / ScreenShot | study / 截屏            |
| `alt-v` `win-v`   | video              | video / PotPlayer     |
| `alt-w` `win-w`   | work / word        | work / word           |
| `win-x`           | 虚拟机                | Hyper-V               |
| `alt-y` `win-y`   | 移动硬盘 / 翻译          | y盘 / 有道词典             |
| `win-z`           | 证券                 | 证券                    |



# 大致原则

- `ctrl` 基本操作
- `shift` 反向操作/块操作
- `alt` 处理文件-AHK使用
- `win` 打开应用-AHK使用
- `alt-win` 特殊应用-AHK使用


----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***
