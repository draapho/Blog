---
title: Windows 软件系列-新装系统
date: 2020-05-02
categories: windows
tags: [windows]
description: 新PC装机过程.
---


# 系统优化



- 硬件检查: [卡硬工具箱](http://www.kbtool.cn/)  (***绿色软件***)
    - 综合检测
    - 显示器工具
- 系统分区: [分区助手](https://www.disktool.cn/) (***绿色软件***)
    - 设置->搜索Bitlocker->关闭`Bitlocker`
    - 软件盘C, SOFT, 120G-250G
    - 数据盘D, DATA
- 中文以及解决中文乱码
    - 设置->语言/Language->中文
    - 设置->区域->国家或地区->中国
    - 设置->区域->区域格式->中文.
    - 设置->区域->其他日期,时间和区域设置->弹出传统的控制面板界面
    - 更改日期,时间或数字格式->管理标签->更改系统区域设置...->选中国
- 性能优化
    - 蓝牙鼠标
        - 右键开始菜单->设备管理器->蓝牙->无线Bluetooth->右键属性->电源选项->禁止节电!
    - 设置->电脑信息->关于页面
        - 重命名这台电脑->更改电脑名字.
        - 系统信息->远程设置->关闭所有的远程选项.
        - 系统信息->高级系统设置->设置性能, 设置启动和故障恢复.
    - 设置->活动->活动历史记录
        - 关闭活动历史记录, 关闭显示账户活动
        - 隐私相关的设置, 全部过一遍
    - 设置->数据使用量->后台数据->开启 限制后台执行的操作
    - 桌面右键->个性化->开始 优化一便. 任务栏 优化一便
- 更改默认路径
    - 设置->存储->更改新内容的保存位置
        - 应用, 文档, 离线地图, 不修改
        - 音乐, 照片, 视频, 电影, 保存到D盘
    - 我的电脑->桌面等7个文件->分别右键属性->位置
        - 3D对象,文档->不修改
        - 视频,图片,音乐,下载,桌面->移动到D盘
        - 路径格式举例: `D:\用户名\桌面`
- 快速访问:
    - 保留最常用的: 下载, 云盘, 用户内容, 生活, 学习, 工作, 家庭, 备份等等
- 共享 Downloads 文件夹
    - 设置->启用或关闭 windows 功能->勾选 `SMB 1.0/CIFS...`. 顺手开启NFS服务
    - 设置->高级共享设置->启用网络发现, 启用文件和打印机共享. 建议启用密码保护
    - 右键 Downloads 文件夹->属性->共享->共享...->添加`Everyone`->权限改为读取写入.
    - 用无线网络时, 设置->查看网络连接->右键网络适配器->勾选 Microsoft 网络的文件和打印机共享
- 杀毒软件 ESET
    - 用国内注册码的话, 区域要改为中国.
    - 依旧不行的话, 用穿梭或快帆翻墙到国内, 变为国内的IP地址.



# 效率软件



- quicklook (***Microsoft Store***)
- Keypass. (***绿色软件***) 密码管理软件
- BANDIZIP6.27 (后续版本有广告). 解压软件
    - 7zip 备选
- quicker. 鼠标工具. 使用鼠标的常用操作.
    - 快捷键 `鼠标中键` 和 `鼠标画圈`
    - 免费版只支持2台电脑. 可用多账号. 账号间用本地存储同步应用数据
    - quicker->...->工具->应用数据文件夹. `data` `states` 内容
- uTool. 键盘工具. 使用关键词的常用和低频操作.
    - 设置
        - 快捷键 `alt+space`. 支持拼音首字母搜索.
        - 插件分离, 插件固定: `Ctrl+D` 改为 `Alt+V`.
        - 关闭 自动黏贴. 恢复输入框: 1分钟
        - 启用 搜索本地应用程序
        - 自定义快捷方式目录 `.\Green\setting\uTools\shortcuts`
            - 常用目录和软件助记快捷方式
    - PDF转换器
    - 网页快开. 设置网页关键字, 以图搜图, 聚合搜索
    - 我的上网IP
    - 批量重命名
    - Code计算器. 计算器功能
    - 程序员手册
    - 正则编辑器
    - 编码小助手. 时间转换, UUID, 编码
    - JSON编辑器
    - 二维码小助手
    - 颜色助手. 取色, 选色.
    - 剪切板. 剪切板历史
    - 聚合翻译
    - 本地搜索. 安装 everything
    - 沙拉查词. 翻译. 导入设置
- ~~Listary 快速搜索: 配置文件 `Preferences.json`~~
    - 取消 所有关键字
    - 精简 动作
    - 快捷键, 下一项目: `Ctrl+J`
    - 快捷键, 前一项目: `Ctrl+K`
- 微软输入法
    - 设置->高级键盘设置->反选 使用桌面语言栏(如果可用)



# 文本办公



- [MicroSoft Office 365](https://www.office.com/)
    - OneDrive 设置:
        - 修改路径: 退出软件, 移动OneDrive文件夹到D盘, 重新启动即可重设路径.
        - 可使能 `让我使用OneDrive获取我在此电脑上的任何文件`, 只能下载单个文件
        - 备份任意文件 (默认只有Desktop, Documents, Pictures):
            - 管理员权限打开cmd: `mklink /d "C:\Users\[Username]\OneDrive\Test" "E:\Test"`
            - 第一个路径为目标路径, 必须是OneDrive本地文件夹. 第二个路径为需要同步的文件夹.
    - Excel 插件:
        - 方方格子.
    - PowerPoint 插件:
        - ~~iSlide.  (需要登录, 模板等需要收费)~~
    - OneNote 插件
        - ~~[NoteHighlight2016](https://github.com/elvirbrk/NoteHighlight2016/releases)~~, 代码高亮. 不支持OneNote2010.
- Dynalist. 备忘+笔记, 全平台云存储. 支持Markdown. 需要图床才能加载图片.
    - 类似的软件: WorkFlow, 幕布
- typora. markdown文本编辑器
- notepad++ (***绿色软件***)
    - 点击bat文件注册右键即可. 已完成[配置](https://draapho.github.io/2016/09/30/1603-WinSoft-editor/).
- Amazon kindle. 读书软件
- iReader (***Microsoft Store***). txt读书软件
- PDF Reader-Xodo (***Microsoft Store***)
- SumatraPDF (***绿色软件***). 小巧, 快速, 绿色, 但功能有限.
- GoldenDict (***绿色软件***). 离线翻译软件.
- 冰点文库下载器 (***绿色软件***). 免积分下载百度文库、道客巴巴、豆丁网上的资料



# 多媒体



- Audacity (***绿色软件***). 音频编辑
- QQ音乐 (***Microsoft Store*** 设置为中国区才有)
- Snipaste (***Microsoft Store / 绿色软件***). 截图
    - 用绿色版的话, 需要添加环境变量.
    - 也可直接从 Microsoft Store 下载.
- ShareX (***Microsoft Store***) 滚动捕捉, 屏幕录制, OCR.
- Lightroom CC
- Photoshop CC
- HONEYVIEW. 图片查看器
- PotPlayer. 视频播放器. 设置里关闭自动更新!
- UWP爱奇艺  (***Microsoft Store***)



# 社交网络

- Chrome. 网页浏览器
    - 插件可以自动同步, 但需要分别设置!
    - `chrome://extensions/` 进行安全性设置
        - 检查权限, 避免高风险应用, 它会要求访问计算机上所有的数据.
        - 点击时. 低频使用的插件建议此选项, 增加安全性.
        - 在特定网站上. 针对特定网站的高频插件, 建议选用此选项.
        - 在所有网站上. 高频通用性插件, 选此选项. 此为Chrome默认选项.
    - Clip to OneNote. 点击时启用
    - ~~EagleGet Free Download. 点击时启用~~
    - Tampermonkey, 油猴. 脚本方式实现多种功能.
        - 尽量用Chrome插件代替脚本. 平时只打开常用的脚本. 低频使用的脚本保持关闭状态.
        - 脚本网站: [greasy fork](https://greasyfork.org/zh-CN)、[openuserJS](https://openuserjs.org/)
        - 设置->通用->配置模式->初学者
        - 设置->同步脚本->启用TESLA->浏览器同步.
        - 这样即可跟随Chrome同步脚本, 但脚本配置不会自动同步!
    - SuperCopy 超级复制. 使能某些顽固网页的复制黏贴. 点击时启用.
    - IE tab. 转为IE内核. 点击时启用
    - Infinity new tab pro. 自建导航网页, 管理插件. 点击时启用
    - Graphitabs. 多标签整理为思维导图模式
    - octotree. github扩展. 启用隐身模式
    - Imagus 图片预览, 设置为ctrl使能. 启用隐身模式
    - AdGuard 广告拦截器, 启用隐身模式
- eagleget. 下载软件.
- Motrix. 下载软件
- 微信PC版. 可用于备份手机微信内容
- QQ. 按需安装
- 穿梭或快帆, 翻墙到国内. 收费建议用穿梭.



# 系统软件


- eset. 杀毒软件
    - 此为收费软件. 可选用如下两个免费方案之一代替
    - windows defender + Avira
    - windows defender + Malwarebytes
- Sandboxie 沙盘工具
- FreeFileSync. 文件备份
- CCleaner (***绿色软件***) 文件清理
- rufus (***绿色软件***) 制作启动盘
- UltraISO (***绿色软件***) ISO映像文件
- 卡硬工具箱 (***绿色软件***), 包含很多小工具如 Dism++
- 分区助手 (***绿色软件***)
- 轻松备份



# 开发工具



- ConEmu (***绿色软件***)
    - 已完成[配置](https://draapho.github.io/2016/10/10/1609-WinSoft-terminal/), 相关目录需要加入 `环境变量...`
    - 潜在的替代软件 Windows Terminal (***Microsoft Store***).
- git
    - p4vinst64, 只需安装 p4merge.
    - 配置git见: [Git 初始设置及常用命令](https://draapho.github.io/2016/10/24/1614-CheatSheet-git/)
- Node.js
    - 配置blog见: [Windows下使用github和hexo建独立博客](https://draapho.github.io/2016/09/24/1601-InitBlog/)
- ~~Ubuntu (***Microsoft Store***)~~
    - 若安装失败 管理员运行 Powershell `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux`
    - 不确定稳定性和全功能.



# 系统清理:



- 卡硬工具箱->其他工具->DISM++ ->依次优化
- CCleaner->清理文件, 清理启动项
- RightMenuMgr->清理右键菜单
- 管理员运行cmd->执行 `sfc /scannow`.  系统文件检查和修复
- 右键C盘->属性->磁盘清理->清理系统文件. 可安全释放系统盘空间.
- 轻松备份->备份C盘



----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
