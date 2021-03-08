---
title: Git 初始设置及常用命令
date: 2016-10-24
categories: software
tags: [git, cheat sheet]
description: 如题.
---

# git示意图

  ![git](https://draapho.github.io/images/1614/git.jpg)



# 资料和参考

- [Visual Git Cheat Sheet](http://ndpsoftware.com/git-cheatsheet.html)
- [Pro Git book](https://git-scm.com/book/zh/v2)
- 廖雪峰的 [Git教程](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)
- 设置SSH, 参考 [GitHub Help - SSH](https://help.github.com/categories/ssh/)
- 设置GPG, 参考 [GitHub Help - GPG](https://help.github.com/categories/gpg/)


# 一些理解
- git的核心理解为指针即可, 包括 `workspace`, `index`, `commitHash`
  - `repository`是基于`commitHash`管理版本的.
  - `HEAD`, `HEAD^1`, `HEAD~3`, `branch`, `tags`都是`commitHash`的别名, 便于人们记忆和理解.
  - 可以基于 `git reset` 来检测是否完全理解git基于指针的设计思路.
  - `HEAD^1`基于父节点, `HEAD~1`基于层次. 单层结构下没有差别. 复杂多层结构建议直接用 `commitHash`

```
       A ---------------------  A =      = A^0
      / \
     B   C                      B = A^   = A^1     = A~1
    /|\  |                      C = A^2  = A^2
   / | \ |
  D  E   F -------------------  D = A^^  = A^1^1   = A~2
 / \    / \                     E = B^2  = A^^2
/   \  /   \                    F = B^3  = A^^3
G   H  I   J -----------------  G = A^^^ = A^1^1^1 = A~3
                                H = D^2  = B^^2    = A^^^2  = A~2^2
                                I = F^   = B^3^    = A^^3^
                                J = F^2  = B^3^2   = A^^3^2
```

- git的命令, 常见格式为 `git diff p1 p2 -- file`. 意为, 比较`p1`与`p2`两处指定file的区别
  - `p1` 缺省指向workspace, `p2` 缺省指向index.
  - `--` 接文件或目录, 名字无歧义时可以省去`--`. (如 git checkout name 就可能有歧义, branch OR file?)
  - `.` 表示所有的文件, 如 `git add .`
- 学会查看帮助, 加上 `-h` 即可. 如 `git checkout -h`
  - `[]` 表示可选项, `<>` 表示必填项



# 初始安装


- 新建git仓库
``` git
# Create local repository
# put ".gitignore" to project root direct.
git init                        # create local repository
git add README.md               # add somefiles
git commit -m "first commit"    # commit to local repository

# link with remote repository
git remote add origin url       # add remote repository, <url> like https://... OR ssh://...
git push -u origin master       # -u, 指定默认远程主机为 origin

# Clone existing repository
git clone url                   # <url> like https://... OR ssh://...

# more cmd about config
git config --list               # show config
git config -e                   # edit local config file
git config -e --global          # edit global config file
```


- 使用命令设置全局参数. (可跳过, 建议使用 `git config -e --global`)
``` git
# global setting
git config --global user.name "Your Name"
git config --global user.email "email@example.com"

# alise setting
git config --global alias.a 'add'
git config --global alias.aa 'add .'
git config --global alias.b 'branch'
git config --global alias.bb 'branch -a -v'
git config --global alias.co 'checkout'
git config --global alias.cm 'commit -m'
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config --global alias.ll "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit -10"
git config --global alias.st 'status'
git config --global alias.diffname 'diff --name-status'

# set diff color
git config --global color.diff.old "red normal bold"
git config --global color.diff.new "green normal bold"

# solve the warning, LF will be replaced by CRLF
git config --global core.autocrlf false
git config --global core.safecrlf false

# set difftool mergetool (need p4merge)
git config --global diff.tool p4merge
git config --global difftool.p4merge.cmd '"D:\Program\Perforce\p4merge.exe" "$LOCAL" "$REMOTE"'
git config --global difftool.prompt false
git config --global merge.tool p4merge
git config --global mergetool.p4merge.cmd '"D:\Program\Perforce\p4merge.exe" "$PWD/$BASE" "$PWD/$REMOTE" "$PWD/$LOCAL" "$PWD/$MERGED"'
git config --global mergetool.p4merge.trustExitCode false
git config --global mergetool.keepBackup false
```


- 使用 `git config -e --global` 打开全局配置文件, 设置全局参数.
- 安装 [p4merge](https://www.perforce.com/product/components/perforce-visual-merge-and-diff-tools), 用于支持 `difftool` 和 `mergetool`
- 安装位置以 `D:\Program\Perforce\p4merge.exe` 为例
```
[user]
    name = https://draapho.github.io/
    email = draapho@gmail.com
[alias]
    a = add
    aa = add .
    b = branch
    bb = branch -a -v
    co = checkout
    cm = commit -m
    lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    ll = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit -10
    st = status
    diffname = diff --name-status
[color "diff"]
    old = red normal bold
    new = green normal bold
[core]
    autocrlf = false
    safecrlf = false
[diff]
    tool = p4merge
[difftool "p4merge"]
    cmd = \"D:\\Program\\Perforce\\p4merge.exe\" \"$LOCAL\" \"$REMOTE\"
[difftool]
    prompt = false
[merge]
    tool = p4merge
[mergetool "p4merge"]
    cmd = \"D:\\Program\\Perforce\\p4merge.exe\" \"$PWD/$BASE\" \"$PWD/$REMOTE\" \"$PWD/$LOCAL\" \"$PWD/$MERGED\"
    trustExitCode = false
[mergetool]
    keepBackup = false
```



# 常用指令
``` git
# 查看信息
git st                          # git status            # 显示工作区变更的文件
git lg                          # git log 增强版        # 显示所有提交
git ll                          # git lg -10            # 显示过去10次提交
git shortlog -sn                                        # 显示所有提交过的用户
git show --name-only commit                             # 显示某次提交发生变化的文件

# stash                                                 # 少量且短时间的使用!
git stash                                               # workspace->stash(藏匿处)
git stash pop                                           # stash(不保存)->workspace

# 提交文件
git aa                          # git add .             # workspace->index
git a *.c *.h                   # <file | dir>          # 添加指定文件
git reset HEAD [file]           # discard file @index   # add的逆操作 HEAD->index
git cm "msg"                    # git commit -m "msg"   # index->repository
git commit --amend -m "message"                         # 修改/替换之前的提交

# 分支操作
git b name                      # git branch name       # 创建分支
git b name commit                                       # 基于指定 commit 创建分支
git b -d name                   # branch delete         # 删除分支
git b -dr origin/name           # delete remote         # 删除远程分支
git b -m new_name               # git branch --move     # 重命名分支
git bb                          # git branch -a         # 查看所有分支
git remote -v                                           # 查看远程分支
git co name                     # git checkout name     # 切换分支
git co -b name                  # checkout & branch     # 创建并切换分支

# 版本合并和回退
git merge branch                # 合并branch到当前分支
git mergetool                   # 已图形化工具处理文件冲突 (如 p4merge.exe)
git cherry-pick commit          # 合并commit到当前分支
git rebase -i HEAD~3            # 修改/压缩多个提交, 根据提示操作, 第一行不能是squash!
git revert commit               # 提交逆操作来实现版本恢复, 不影响任何历史记录!
git push                                                # 推送到默认的远程主机
git push -f                     # --force               # 忽略冲突, 强制推送
git pull                        # fetch & merge         # 合并远程分支到当前分支

# tag                           # 用于标记一个版本, 可以替代 commitHash
git tag                         # 查看版本
git tag v100                    # 创建版本
git tag -d v100                 # 删除版本
git push --tags                 # 推送tag

# 查看差异
git diff                        # workspace VS index (p1缺省指向workspace, p2缺省指向index)
git diff p1 p2                  # p1 VS p2, 可以是 HEAD~1, commitHash值, TAG, 分支名称
git diff p1 p2 -- *.c *.h       # -- 指定文件或目录, 可省
git diff --name-status p1 p2    # 获得变更的文件列表
git diff --stat p1 p2           # 统计变更的数据
git difftool p1 p2 -- file      # 使用图形化工具显示差异 (如 p4merge.exe)

# 撤销
git checkout p1 -- file         # p1->index->workspace  # p1缺省为index, --和file可省
git reset p1 -- file            # p1->HEAD->index,      # p1缺省为HEAD, --和file可省
git reset --soft p1             # p1->HEAD                      # p1缺省为HEAD, 不可带file参
git reset --hard p1             # p1->HEAD->index & workspace   # p1缺省为HEAD, 不可带file参

git checkout .                  # index->workspace      # 清除工作区的变更(!!!危险操作)
git checkout branch             # branch->index->workspace      # 切换分支
git reset --hard                # HEAD->index & workspace       # 恢复仓库到HEAD状态
git reset HEAD^ file            # HEAD^->HEAD->index            # 指定file, 进行版本回滚
git reset --soft HEAD~3         # HEAD~3->HEAD                  # 版本回滚
```


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***


