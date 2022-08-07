---
title: Visual Studio Code 环境配置
date: 2022-08-03
categories: 网页开发
tags: [网页开发, 环境配置, JavaScript, PHP]
description: 将 Visual Studio Code 配置为网页开发IDE
---

# IDE 的选择
- 不太好的Atom使用经验
    - 之前有过 atom 的使用和配置经验.
    - 结论是看上去啥都能支持, 结果啥都支持不好.
    - 各种插件的升级维护本身就会消耗很多精力, 而且越用越慢.
    - 之后, 自己就全面转向一站式的专用IDE. 如 pycharm.
- 还是选了 Visual Studio Code
    - 网页开发入门初学, 没有大项目需求, 用着顺手就行.
    - 主要原因还是免费. WebStorm 和 PHPStorm 都是收费软件.
    - 仅仅作为编辑器使用, 也非常舒服, 且自带git版本管理.
- 需求确定
    - 将 VS Code 定位为网页开发和远程开发主力IDE. 并兼容运行单文件其它语言.
    - 支持 markdown 的编辑和打印
    - 支持远程开发, 如 putty 连接远程服务器
    - 支持运行调试: JavaScript, PHP, Vue
    - 支持直接运行 c/c++, java, python 等单文件, 直接看结果.
    - 尽量用默认配置, 并尽可能少的使用插件.
- 清空旧有版本
    - 卸载vscode
    - 删除 `C:\Users\xxx\.vscode` 文件夹
    - 删除 `C:\Users\xxx\AppData\Roaming\code` 文件夹
    - 即可准备全新安装.

# VS Code 及其扩展的安装

## VS Code 的安装
- [官网下载](https://code.visualstudio.com/) 安装, 没什么好说的.
- 打开后, 选一个喜欢的主题, 我会选暗色主题.
    - 右下的账号按钮, 建议开启同步功能.
    - 右下的设置按钮, 建议添加好常用的工作目录作为信任文件夹.
    - 右侧活动栏, 对项目按需显隐和排序.
- 解决 VS Code 在此系统上**禁止运行脚本的报错**
    - 管理员身份运行 window.powershell
    - 执行：`get-ExecutionPolicy`，显示 Restrict，表示状态是禁止的；
    - 执行：`set-ExecutionPolicy`；
    - 提示输入参数，输入：`RemoteSigned`；
    - 提示进行选择，输入：`Y`；
    - 检查：执行`get-ExecutionPolicy`,显示 RemoteSigned。


## VS Code 扩展(插件)的选择
- 快捷键
    - `Eclipse Keymap`, 自己统一使用eclipse模式快捷键
    - `Ctrl+Shift+P`, 打开命令面板
- MarkDown:
    - `Markdown PDF`
    - `Markdown Preview Enhanced`
    - `Markdown Table Prettifier`
- git:
    - `gitLens`
    - `Git History`
    - `gitignore`
        - 命令面板输入 `add gitignore`
- XML和CSV文件:
    - `XML Tools`
    - `Rainbow CSV`
    - `Auto Close Tag`
    - `Auto Rename Tag`, 偷懒装此扩展(VSCode可配置)
- PHP 语言:
    - `PHP Debug`
    - `PHP Intelephense`
- Node.js, 按需选择
    - `ESLint`
    - `Search node_modules`, 扩展设置中可指定搜索路径
    - `JavaScript (ES6) Snippets`
    - `NPM IntelliSense`
    - `Path IntelliSense`
    - `open in browser`
    - `Auto Import`
    - `File Peek`, 快速跳转到工程内文件.
    - `CSS Peek`
    - `Sass`
- Vue.js, 按需选择
    - Node.js 的扩展
    - `Vue Language Features (Volar)`
    - `Vue 3 Snippets`
    - `Vite`, VS Code for Vite
    - 配置请参考: [Vue.js 官方安装文档](https://v3.cn.vuejs.org/guide/installation.html)
- uniapp, 按需选择
    - Node.js 的扩展
    - `uni-helper`
    - `uni-create-view`
    - 自己多测试吧, 相关扩展都不太成熟.
    - uniapp项目建议用 [HBuilderX](https://www.dcloud.io/hbuilderx.html) 编译调试.
- 远程开发
    - `Remote - SSH`
        - 本地需要ssh客户端支持, 譬如安装git.
        - 命令格式: `ssh name@ip_address`, 然后登录输入密码.
    - `Remote - SSH: Editing Configuration Files`
    - `Remote - WSL`, 在windows下提供近似的Linux的环境.
    - ~~`Remote - Containers`~~
- 其它语言, 按需选择:
    - `C/C++`, 
        - 打开 `Settings` 或者 `Extension Settings`
        - 搜索 `@ext:ms-vscode.cpptools C_Cpp.clang_format_fallbackStyle:`
        - 将值改为: `{BasedOnStyle: Google, IndentWidth: 4, ColumnLimit: 0}`
    - `REST Client`
        - 仅识别`.http`和`.rest`文件, 点击`Send Request`
- 辅助工具
    - `Todo Tree`
        - 勾选 `Highlights:Use Colour Scheme`
        - `General:Tags` 大写改为小写
    - `Code Runner`
        - 打开 `Settings` 或者 `Extension Settings`
        - 搜索 `@ext:formulahendry.code-runner Code-runner: Run In Terminal`
        - 勾选 `Whether to run code in Integrated Terminal.`
        - 需要配置各语言的运行环境
    - ~~IntelliCode~~

# VS Code 的配置

## VS Code 扩展(插件)的配置
- PHP 运行环境:
    - PHP官网解压安装 [VS16 x64 Thread Safe](https://windows.php.net/download/) PHP, 然后配置好环境变量.
    - 如果要全套本地开发环境, 官网推荐安装包: [XAMPP建站集成软件包](https://www.apachefriends.org/index.html).
    - 终端输入 `php --version` 测试. 返回版本号即配置完成
    - 就能顺利使用 `Code Runner` 运行php文件了
- JavaScript 运行环境: `Node.js`
    - [Node.js 官网下载](https://nodejs.org/zh-cn/download/) 并安装
    - 终端输入 `node --version` 和 `npm --version` 测试, 返回版本号即配置完成
    - 就能顺利使用 `Code Runner` 运行js文件了
- TypeScript 运行环境:
    - 先搭建好 JavaScript 的运行环境
    - 终端运行 `npm install -g typescript`
    - 终端运行 `npm install -g ts-node`
    - 终端输入 `ts-node --version` 测试, 返回版本号即配置完成
    - 就能顺利使用 `Code Runner` 运行ts文件了
- python 运行环境:
    - [Python 官网](https://www.python.org/downloads/) 下载安装, 然后配置好环境变量.
    - 终端输入 `python --version` 测试, 返回版本号即配置完成
    - 就能顺利使用 `Code Runner` 运行py文件了
- C/C++ 运行环境:
    - 下载安装 [MinGW for Windows](https://sourceforge.net/projects/mingw/), 然后配置好环境变量
    - 终端输入 `gcc --version` 测试, 返回版本号即配置完成
    - 就能顺利使用 `Code Runner` 运行c/c++文件了
- `REST Client`, 保存为`.http`或`.rest`.
    - 点击 Send Request 即可. 或右键选择.
    - 支持转换为curl命令和代码, 支持变量.
    - 更多配置移步: [详细说明和文档](https://github.com/Huachao/vscode-restclient)
    - 简单的参考文件模板如下:
``` json
https://draapho.github.io/

###
GET https://draapho.github.io/

###
POST https://reqbin.com/echo/post/json HTTP/1.1
content-type: application/json; charset=utf-8

{
    "Id": 78912,
    "Customer": "Jason Sweet"
}
```

## 远程开发配置的参考资料
- 官方资料: [VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)
- `Remote - SSH`
    - [5 Steps: Setup VS Code for Remote Development via SSH from Windows to Linux system](https://towardsdatascience.com/5-steps-setup-vs-code-for-remote-development-via-ssh-from-windows-to-linux-b9bae9e8f904)
    - [Visual Studio Code远程开发初体验——Remote-SSH环境搭建](https://www.vsc.cc/article/100000.html)
    - [VS Code Remote SSH配置](http://www.getone.run/2022/02/06/VS-Code-Remote-SSH%E9%85%8D%E7%BD%AE/)
    - [ssh配置vscode实现一台电脑连接多台服务器进行开发](https://blog.csdn.net/qq_18145605/article/details/122106109)
- `Remote - WSL`
    - [Get started using Visual Studio Code with Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode)
    - [在WSL安装并配置VSCode](https://reeeeeeeeeein.github.io/2020/02/28/%E5%9C%A8WSL%E5%AE%89%E8%A3%85%E5%B9%B6%E9%85%8D%E7%BD%AEVSCode/)
    - [Win10+WSL+VS Code搭建Ubuntu开发环境](https://zhuanlan.zhihu.com/p/57882542)
    - [优雅地使用VSCode与WSL在Windows 10下开发](https://www.luogu.com.cn/blog/Quank-The-OI-er/VSCode-On-Windows-10)
- ~~`Remote - Containers`~~ 暂时没有这个需求, 直接放弃.
    - [VSCode Remote-Containers 配置记录](https://abxy.fun/post/vscode-remote-container/)
    - [VSCode之容器开发环境搭建 (Remote-Containers)](https://juejin.cn/post/7109154039434067982)

## 根据使用环境切换配置文件
- 需求: 根据不同的语言/工作目录方便地切换配置文件, 实现尽可能少的加载扩展便于快速启动, 减少可能的冲突.
- 写此文时, 安装版本 1.70.0. 官方尚在开发此功能. 相信很快就会发布到稳定版.
- 请参考官方资料: [Updates: Settings Profiles](https://code.visualstudio.com/updates/v1_69#_settings-profiles)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
