---
title: Windows下使用github和hexo建独立博客
date: 2016-09-24
categories: environment
tags: [windows, hexo]
---

# 我需要一个[博客](https://draapho.github.io)

三年前学linux的时候, 深感复杂,  然后也略微记录了些笔记放在电脑里. 但是真要用的时候, 依旧会google或baidu, 原因很简单: 电脑的笔记用起来不方便, 找文档慢不说, 找到后要么是没有格式的txt文档, 有些是花了力气排版好的word, 又觉得打开很慢. 于是觉得需要一个博客, 在CSDN开了博, 坚持不到10篇文章就放弃了, 原因很简单: 太麻烦了. 我的本意只是学习笔记加资料仓库, 但维护它的时间成本太高了. 一晃三年, 工作上进入一个新领域, 需要系统的学习嵌入式linux和python, 再度觉得需要建一个博客来管理和维护一些笔记和资料.

**工欲善其事, 必先利其器**. 所以, 我需要一个博客. 寻寻觅觅, 幸运寻得github.io和markdown写作这么一个方案.


# ~~折腾记, jekyII方案~~

不过依旧走了一点弯路, 因为github.io推荐的是jekyII环境, 如果对这个方案感兴趣, 点击[这里](https://help.github.com/articles/using-jekyll-as-a-static-site-generator-with-github-pages/)可以按照官方教程来操作. 人家第一句话就是[**jekyII并不原生支持Windows**](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/) , 但我岂是会轻易投降的人, 遇到问题就解决问题, 这不还有另外一句 [**Jekyll on Windows**](http://jekyllrb.com/docs/windows/#installation), 流程如下, 然后还要注意编码问题.
- 装[Ruby](http://rubyinstaller.org/downloads/) 或者 `choco install ruby -y`
- 装jekyII,   `gem install jekyll`
  最终, 我是安装失败了...具体卡在哪个错误提示也给忘了. 所幸的是搜到了对windows友好的hexo方案.


# Hexo方案

恩, 这里才是正文的开始! windows下安装hexo这个任务非常简单!
- 对[Git软件](https://git-scm.com/)和[GitHub网站](https://github.com/)不熟的话, 建议安装[GitHub Windows](https://desktop.github.com/), 安装后根据提示操作.
- 安装[Node.JS](https://nodejs.org/en/), 选推荐版本, 目前是v4.5.0 LTS (即 Long Term Support), 环境变量默认会设置好.
- 安装Hexo
  ``` shell
  npm install -g hexo-cli
  ```
- 创建并初始化博客文件夹,这里命名为***Blog***, 右键点"Git Bash Here", 或者打开cmd进入到***Blog***目录下
  ``` shell
  cd Blog           # 确保在Blog这文件夹下
  npm install hexo --save # 安装hexo
  hexo init         # 初始化Blog文件夹内容
  npm install       # 安装必要的依赖包
  # 下面是必要的插件包
  npm install hexo-deployer-git --save      # 使用github发布
  npm install hexo-deployer-rsync --save    # 不装, 使用 rysnc发布
  npm install hexo-deployer-openshift --save    # 不装, 使用OpenShift发布
  npm install hexo-generator-feed --save    # 不装, 生成atom.xml, 供RSS使用
  npm install hexo-generator-sitemap --save # 不装, 生成sitemap.xml, 用于提高搜索量
  npm install hexo-generator-search --save  # 用于本地搜索
  ```
- 本地查看效果, 输入`hexo s`成功后登录 `localhost:4000`查看效果
  这里, 我遇到了错误, 提示是 4000 端口已经被占用.
  最后发现是 foxitProtect.exe (福昕PDF保护进程)占用此端口, 先结束, 然后直接删除.
  ```shell
  netstat -aon | findstr "4000"     # 查找占用4000端口的PID, 譬如, 结果为1234
  tasklist | findstr "1234"         # 查找PID=1234的进程名称, 譬如, 结果为foxitProtect.exe
  taskkill /f /t /im foxitProtect.exe   # 强制杀死此进程
  ```
- 配置 hexo 的 `_config.yml`

  > \# Site
  > title: DRA&PHO                  # 博客名字
  > subtitle: thinking & logging    # 副标题
  > description: Embedded System, IoT, M2M  # 博客描述
  > author: draapho                 # 作者
  > language: en        # 语言, 中文为 zh-Hans, 需设置category_map和tag_map
  >
  > \# URL
  > url: https://YourGitHubName.github.io/  # 替换***YourGitHubName***
  > \# 譬如: https://draapho.github.io/ 我的GitHub注册名是***draapho***
  >
  > \# Directory
  > source_dir: source      # source文件夹, 用来写文章
  > public_dir: public      # public文件夹, 自动生成的静态页面都放在这里
  > tag_dir: tags           # 标签文件夹, 需要安装 hexo-generator-tag
  > archive_dir: archives   # 归档文件夹, 需安装 hexo-generator-archive
  > category_dir: categories    # 分类文件夹, 需安装 hexo-generator-category
  >
  > \# Extensions
  > theme: next         # 随了大流, 用了next主题
  >
  > \# Deployment
  > deploy:
  >   type: git         # 使用git部署, 需安装 hexo-deployer-git
  >   repository: https://github.com/YourGitHubName/YourGitHubName.github.io.git
  >   \# 我的注册名是***draapho***, 就写成: https://github.com/draapho/draapho.github.io.git
  >   branch: master
  >
  > \# search Settings, 默认没有这行内容, 自己添加即可
  > search:             # 本地搜索功能, 需安装 hexo-generator-search
  >    path: search.xml
  >    field: post

- 创建about,categories,tags文件夹及文件
  在`Blog\source`下, 新建文件夹about, 然后新建文件index.md, 用于生成关于页面

  > \---
  > title: about
  > date: 2016-09-08
  > comments: false
  > \---
  > 这一篇的内容是自我介绍

  在`Blog\source`下, 新建文件夹categories, 然后新建文件index.md, 用于生成分类页面

  > \---
  > title: categories
  > date: 2016-09-08
  > type: "categories"
  > comments: false
  > \---

  在`Blog\source`下, 新建文件夹tags, 然后新建文件index.md, 用于生成标签页面

  > \---
  > title: tags
  > date: 2016-09-08
  > type: "tags"
  > comments: false
  > \---


# github端的配置

- 如果之前没有使用过github, 第一次上传应该要求输入用户名和密码. 但如果每次部署都要这样, 就显得很麻烦. github端可以使用SSH 或 GPG keys来免去这个步骤. 建议使用GPG keys.
- 这里就不详细展开了, 具体步骤参考github, [生成一个GPG key](https://help.github.com/articles/generating-a-gpg-key/)


# ~~使用mermaid插件支持流程图等~~

- 安装
  ``` shell
  npm install hexo-tag-mermaid --save
  ```
- 添加mermaid依赖到主题模板
  进入themes/your_theme_folder/layout/partial目录，添加mermaid相关文件。
  head.jade 添加如下代码
  ``` jade
  link(rel="stylesheet", href=url_for("https://cdn.bootcss.com/mermaid/6.0.0/mermaid.min.css"))
  ```
  scripts.jade 添加如下代码
  ``` jade
  link(rel="stylesheet", script(src="//cdn.bootcss.com/mermaid/6.0.0/mermaid.min.js")
  ```
- 我暂时放弃了
  next用的swig, 不知道和jade文件是什么关系. 暂时不愿去研究.
  看了下此插件的格式, 和我常用的Typora使用的mermaid不一样.
  博客上用到流程图之类的机会不多, 偶尔需要使用图片即可.
  如有兴趣, 可参考 [Hexo流程图等插件安装教程](http://jcchow.com/2016/07/11/mermaid-sequence/)


# NexT主题

主题的选择我没有花太多时间, 测试了2-3个主题后, 最终还是随大流的用了NexT主题. 说实话, 设计感很好, 用的人很多, 略有审美疲劳. 好在博客目标明确, NexT能很好的覆盖我几个基本需求, 文档又写的很完善, 就不折腾了.

- 安装NexT, 见[官方文档](http://theme-next.iissnan.com/getting-started.html)
- menu_icons 图标配置, 名称用的是[Font Awesome](http://fontawesome.io/icons/)
- about 页面的链接是 https://YourGitHubName.github.io/about
  我的注册名是***draapho***, 就写成 <https://draapho.github.io/about>
- `\themes\next\_config.yml`文件内找到`use_motion:` 设置为`false`. 表示禁止动画效果, 立刻显示页面

# Hexo的日常使用

- 习惯于直接在 \Blog\source\_posts\ 下面直接新建文件 xxx.md
  然后打开文件, 添加并修改如下内容:
  > title: Windows下使用github和hexo建立自己的博客
  > date: 2016-09-08
  > categories: environment
  > tags: [blog, hexo, next]
- Hexo的常用指令
  ``` shell
  hexo clean    #更换hexo主题后, 建议先执行此条命令清空
  hexo g        # g=generate, 生成public静态文件
  hexo s        # s=server, 本地发布预览效果, 默认地址是 localhost:4000
  hexo d        # d=deploy, 自动部署
  hexo d -g     # 我最常用的指令, 意思是先generate再deploy.
  ```


# 参考

- [使用GitHub和Hexo搭建免费静态Blog](https://wsgzao.github.io/post/hexo-guide/)
- [Hexo搭建Github-Pages博客填坑教程](http://www.jianshu.com/p/35e197cb1273)
- [Hexo 文档](https://hexo.io/zh-cn/docs/index.html)
- [Next 主题](http://theme-next.iissnan.com/getting-started.html)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***