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
        - 注意, C盘根目录下创建`Program`目录, 可以命名为`Programs`
    - 数据盘D, DATA
- 中文以及解决中文乱码
    - 设置->语言/Language->中文
    - 设置->区域->国家或地区->中国
    - 设置->区域->区域格式->中文.
    - 设置->区域->其他日期,时间和区域设置->弹出传统的控制面板界面
    - 更改日期,时间或数字格式->管理标签->更改系统区域设置...->选中国
    - 如果要保留英文系统, 但支持中文字符显示, 只需要下述步骤:
        - 设置里搜索`Region Settings`并进入->`Additional data, time & regional settings`->`Change date, time or number formats`
        - 弹出框后, 选择`Adminstrative`标签->`Change System locale`->选为中文, UTF-8 不要打勾
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
        - 视频,图片,音乐->移动到D盘
        - 路径格式举例: `D:\用户名\音乐`
- 快速访问:
    - 保留最常用的: 下载, 云盘, 用户内容, 生活, 学习, 工作, 家庭, 备份等等
- ~~共享 Downloads 文件夹~~, NAS服务器 替代
    - 设置->启用或关闭 windows 功能->勾选 `SMB 1.0/CIFS...`. 顺手开启NFS服务
    - 设置->高级共享设置->启用网络发现, 启用文件和打印机共享. 建议启用密码保护
    - 右键 Downloads 文件夹->属性->共享->共享...->添加`Everyone`->权限改为读取写入.
    - 用无线网络时, 设置->查看网络连接->右键网络适配器->勾选 Microsoft 网络的文件和打印机共享
- ~~杀毒软件 ESET~~, Bitdefender 替代
    - 用国内注册码的话, 区域要改为中国.
    - 依旧不行的话, 用穿梭或快帆翻墙到国内, 变为国内的IP地址.



# 效率软件



- quicklook (***Microsoft Store***)
- Keepass. (***绿色软件***) 密码管理软件
- BANDIZIP6.27 (后续版本有广告). 解压软件
    - 7zip 备选
- ~~uTool. 键盘工具. 使用关键词的常用和低频操作.~~
    - 插件会强制升级, 用起来不方便
    - 需要的功能, quicker可以实现.
- 微软输入法
    - 设置->高级键盘设置->反选 使用桌面语言栏(如果可用)
    - 启用`中文输入英文标点`, `模糊拼音`, 候选词改为5, 开启`自学习`和`云服务`
    - 关闭`人名输入`
- quicker. 鼠标工具. 使用鼠标的常用操作.
    - 弹出面板->鼠标方式->`鼠标中键`
    - 功能快捷键->停止运行中的动作->`Alt + Esc`
    - 功能快捷键->打开搜索框->`Alt + Space`
    - 免费版只支持2台电脑. 账号间可以用本地存储同步应用数据
        - quicker->...->工具->应用数据文件夹. `data` `states` 内容
        - 也可以使用网络添加动作或本地导入动作.
    - 自用的动作库:
        - [11. 我的电脑](https://getquicker.net/Sharedaction?code=2a98fd68-6628-4ca5-8edb-08d639a457d1)
        - [12. 设置](https://getquicker.net/Sharedaction?code=7adf975c-0fa7-4a03-8ed4-08d639a457d1)
        - [13. 回收站](https://getquicker.net/Sharedaction?code=e162e460-1cab-483c-ee97-08d9ffe2991a)
        - [21. ChatGPT](https://getquicker.net/Sharedaction?code=78c204ab-174e-45c2-aa6d-08db66a6be43)
        - [22. Dynalist](https://getquicker.net/Sharedaction?code=2c7c56e0-2dfa-4bc7-38c1-08db65bc27d9)
        - [23. Notepad++](https://getquicker.net/Sharedaction?code=c6978455-0fc2-4b8b-aa6e-08db66a6be43)
        - [24. 沙拉翻译](https://getquicker.net/Sharedaction?code=b0d1a134-8284-4a44-d1be-08d746da5869)
            - 需要沙拉查词的浏览器插件, 并做好相关配置. 参考使用说明.
            - 首次运行后, 会弹出设置界面. 或按ctrl键运行沙拉查词动作库, 可进行配置
            - 配置`在独立窗口中搜索剪贴板内容`快捷键: `%L`, 即 Alt+Shift+l
            - 翻译模式: 划词翻译.
        - [31. 复制路径](https://getquicker.net/Sharedaction?code=fd36be81-ac53-4ba3-b1c7-08d8a7a50e21)
        - [32. EVER智识](https://getquicker.net/Sharedaction?code=4f8b0df2-d031-4309-173c-08d7079ea819)
        - [33. Everything](https://getquicker.net/Sharedaction?code=fd99c3f8-630a-4583-aa55-08db66a6be43)
            - 配置快捷键 `Alt+f`
        - [34. 安装目录](https://getquicker.net/Sharedaction?code=5a1fb8df-4540-4da0-4fb4-08d6ba918de2)
        - [41. 复制](https://getquicker.net/Sharedaction?code=de41c12a-ba97-4e5b-8ec1-08d639a457d1)
        - [42. 纯文本粘贴](https://getquicker.net/Sharedaction?code=f35761f9-6e2b-4b30-f992-08d6963ca36f)
        - [43. 剪贴板](https://getquicker.net/Sharedaction?code=9ec53d43-5539-4571-6886-08d8c752bfcb)
        - [44. 计算器](https://getquicker.net/Sharedaction?code=ae51f6c0-6a08-4ac6-39f2-08d6dd213093)
        - [51. Snipaste](https://getquicker.net/Sharedaction?code=729a411e-b89b-4e5a-aa6f-08db66a6be43)
        - [52. 截图OCR](https://getquicker.net/Sharedaction?code=ba82e11a-f845-4ca3-44ee-08d690b5076c)
        - [53. 图片拼接](https://getquicker.net/Sharedaction?code=40cf6cd5-eccd-4f12-6766-08d7d248d373)
        - [54. 画图](https://getquicker.net/Sharedaction?code=225c71b9-f5d0-48ec-8edf-08d639a457d1)
        - [61. 显示桌面](https://getquicker.net/Sharedaction?code=3830c01e-b3b9-42c8-65ff-08d904baa62c)
        - [62. 置顶](https://getquicker.net/Sharedaction?code=277b6f2c-fd93-4ff2-d53d-08d6d8f7a71c)
        - [63. 关闭窗口](https://getquicker.net/Sharedaction?code=4e83d856-b866-4019-8ec7-08d639a457d1)
        - [64. 装模作样](https://getquicker.net/Sharedaction?code=3b6c01cc-e061-4eac-b162-08d6de53af4f)
            - 配置快捷键 `Alt+Z`
        - [72. EVER批图](https://getquicker.net/Sharedaction?code=dd54f738-eda1-4a28-5cb2-08d8bb6e7688)
        - [73. EVER重命名](https://getquicker.net/Sharedaction?code=19fe14e5-ff6d-46fb-efcb-08d72c3bd710)
        - [74. 输入纠正](https://getquicker.net/Sharedaction?code=d3f2c98f-a37f-4c67-aa72-08db66a6be43)
            - 配置快捷键 `Alt+回车`
    - 搜索功能设置
        - 文件(指定位置和文件类型)->索引目录->`D:\Green\shortcuts`->指定扩展名的文件->`.lnk`
        - 将常用的软件和目录的快捷方式放入这个文件夹中, 并可以重命名用来助记.
        - 其它配置如截图:
![search](https://draapho.github.io/images/2004/search.png)


# 文本办公

- [MicroSoft Office 365](https://www.office.com/)
    - OneDrive 设置:
        - 修改路径: 退出软件, 移动OneDrive文件夹到D盘, 重新启动即可重设路径.
        - 可使能 `让我使用OneDrive获取我在此电脑上的任何文件`, 只能下载单个文件
        - 备份任意文件 (默认只有Desktop, Documents, Pictures):
            - 管理员权限打开cmd: `mklink /d "C:\Users\[Username]\OneDrive\Test" "E:\Test"`
            - 第一个路径为目标路径, 必须是OneDrive本地文件夹. 第二个路径为需要同步的文件夹.
- Dynalist. 备忘+笔记, 全平台云存储. 支持Markdown. 需要图床才能加载图片.
    - 类似的软件: WorkFlow, 幕布
- typora. markdown文本编辑器
- notepad++ (***绿色软件***)
    - 点击bat文件注册右键即可. 已完成[配置](https://draapho.github.io/2016/09/30/1603-WinSoft-editor/).
- Amazon kindle. 读书软件
- 越飞读书 Fly Reader (***Microsoft Store***). 读书软件, 多格式支持
- pdf Viewer plus (***Microsoft Store***), 轻巧的PDF阅读器
- PDF Reader-Xodo (***Microsoft Store***), PDF阅读和编辑, 以及格式转换
- SumatraPDF (***绿色软件***). 小巧, 快速, 绿色, 但功能有限.
- GoldenDict (***绿色软件***). 离线翻译软件.
- ~~冰点文库下载器 (***绿色软件***). 免积分下载百度文库、道客巴巴、豆丁网上的资料~~



# 多媒体



- Audacity (***绿色软件***). 音频编辑
- QQ音乐 (***Microsoft Store*** 设置为中国区才有)
- Snipaste (***绿色软件***). 截图
- ~~ShareX (***Microsoft Store***) 滚动捕捉, 屏幕录制, OCR.~~
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
    - ~~Clip to OneNote. 点击时启用~~, 登录经常发生问题.
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
- ~~穿梭或快帆, 翻墙到国内. 收费建议用穿梭.~~
    - 可以用手机APP版的穿梭, 配合 Every Proxy 代理. 给电脑联网使用.



# 系统软件


- ~~eset. 杀毒软件~~
    - 此为收费软件. 可选用如下的免费方案之一代替
    - Bitdefender
    - windows defender + Avira
    - windows defender + Malwarebytes
- ~~Sandboxie 沙盘工具~~
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
