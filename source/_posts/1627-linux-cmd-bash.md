---
title: Bash Shell及环境变量
date: 2016-12-17
categories: linux
tags: [linux, shell]
---


# 入门教程
推荐 [C语言中文网-Shell教程](http://c.biancheng.net/cpp/shell/)
- [第一个shell脚本](http://c.biancheng.net/cpp/view/6998.html)
- [shell变量](http://c.biancheng.net/cpp/view/6999.html)
- [shell特殊变量](http://c.biancheng.net/cpp/view/2739.html)
- [shell替换](http://c.biancheng.net/cpp/view/2737.html)
- [shell运算符](http://c.biancheng.net/cpp/view/2736.html)
- [shell注释](http://c.biancheng.net/cpp/view/7000.html)
- [shell字符串](http://c.biancheng.net/cpp/view/7001.html)
- [shell数组](http://c.biancheng.net/cpp/view/7002.html)
- [shell echo命令](http://c.biancheng.net/cpp/view/7003.html)
- [shell printf命令](http://c.biancheng.net/cpp/view/1499.html)
- [shell if else语句](http://c.biancheng.net/cpp/view/7005.html)
- [shell case esac语句](http://c.biancheng.net/cpp/view/7006.html)
- [shell for循环](http://c.biancheng.net/cpp/view/7007.html)
- [shell while循环](http://c.biancheng.net/cpp/view/7008.html)
- [shell until循环](http://c.biancheng.net/cpp/view/7009.html)
- [shell跳出循环](http://c.biancheng.net/cpp/view/7010.html)
- [shell函数](http://c.biancheng.net/cpp/view/7011.html)
- [shell函数参数](http://c.biancheng.net/cpp/view/2491.html)
- [shell输入输出重定向](http://c.biancheng.net/cpp/view/2738.html)
- [shell文件包含](http://c.biancheng.net/cpp/view/2740.html)


# Bash Shell基础操作

| 指令                                       | 说明                                      |
| ---------------------------------------- | --------------------------------------- |
| `[Tab]`                                  | 指令或文件名自动补齐                              |
| `[Tab][Tab]`                             | 连按两下[Tab], 列出所有可补齐的指令或档案                |
| `[ctrl]-c`                               | 中断指令                                    |
| `[ctrl]-d`                               | EOF,表示输入结束                              |
| `[↑]` `[↓]`                              | 浏览历史指令                                  |
|                                          |                                         |
| `stty`                                   | 查看和设置终端按键参数                             |
| ...... **`stty -a`**                     | 查看终端所有的按键参数                             |
| `history`                                | 查询历史指令, 建议将其设置别名`alias h=’history’`     |
| `!`                                      | 执行历史指令, 后接数字或字母                         |
| ...... **`!!`**                          | 执行上一个指令                                 |
| ...... **`!al`**                         | 执行以al为开头的最后一个指令                         |
| ...... **`!12`**                         | 执行第12条历史指令(先用history查看历史指令号)            |
| `alias cmd=’command’`                    | 设置指令别名, command为指令字符串                   |
| ...... **`alias h=history`**             | 设置指令history的别名为h.不用引号,单双引号皆可            |
| `unalias cmd`                            | 取消指令别名                                  |
| `type -a command`                        | 查询指令类型(file外部指令; alias别名指令;builtin内建指令) |
| `command --help`                         | 获取command内置的帮助信息,较为简短                   |
| `man command`                            | 获取command的帮助文件. `j` `k`上下移动, `q`退出       |
| `sh file`                                | 创建一个子shell, 执行file内的指令                  |
| `source file`                            | 在当前shell内,执行file内的指令                    |
| `. file`                                 | 等同于source file                          |
|                                          |                                         |
| `su -l user`                             | 切换用户, -l表示环境变量一起变                       |
| ...... **`su`**                          | 切换为管理员账户                                |
| `sudo command`                           | 赋予用户临时的管理员权限 (`/etc/sudoers`决定是否支持)     |
| `exit`                                   | 退出当前用户的终端环境                             |
| `shutdown -h now`                        | 立刻关机                                    |
| `sync; sync; shutdown -r now`            | 立刻重启, 重启前需要存储一下数据                       |
|                                          |                                         |
| `date`                                   | 时间                                      |
| `cal`                                    | 日期                                      |
| `bc`                                     | 计算器, 输入quit退出                           |
| `apt-get`                                | ubuntu deb包软件管理                         |
| ...... **`sudo apt-get install packagename`** | 安装指定软件包                                 |
| ...... **`sudo apt-get autoremovepackagename`** | 删除指定软件包 (包括配置文件)                        |


# 变量与环境变量

- 系统变量一般大写, 如MAIL
- 用户变量一般小写, 如myhome
- 普通变量(也称shell变量)作用范围: 当前的shell
- 环境变量(也称用户变量)作用范围: 当前的shell及其子shell
- 环境变量开机设置文档
  - `~/.bashrc`, `~/.profile`, `/etc/profile`, `/etc/bash.bashrc`,等等
  - 首先读取 `/etc/profile`, 最后读取 `~/.bashrc`
  - 个人设定建议放在`~/.bashrc`内,并做如下修改:
  - 修改`HISTSIZE=50`  (减少记录的历史指令,安全)
  - 加入`alias h='history'`


| 指令                                       | 说明                                       |
| ---------------------------------------- | ---------------------------------------- |
| `myhome=/home/my/`                       | 无空格字符串,注意等号左右不要有空格                       |
| `myhome=’/home/my/’`                     | 单引号内可包含任意字符串, 无特殊含义                      |
| `myname=”my name is”`                    | 双引号内某些字符有特殊作用, 如 $                       |
| `read variable`                          | 键盘输入变量, 回车表示结束输入                         |
| ...... **`read -p “Input name:” -t 30 myname`** | 提示输入变量给myname, 30秒输入时间                   |
| `echo $myhome`                           | 变量名前加上$, 即可读取该变量的值                       |
| `echo “$myhome”`                         | “$变量名”,无歧义. 注意不能单引号                      |
| `echo ${myhome}`                         | ${变量名},无歧义                               |
| `unset myhome`                           | 删除变量                                     |
|                                          |                                          |
| `let val=10*10`                          | 加上let后, val值为100,而非10*10. 用的比declare多!   |
| `readonly VAL=’read only’`               | 将VAL为只读变量,不可更改和unset (等同 declare -r)     |
| `declare -ai array`                      | 将array声明为整数数组 (不加参数a,效果一样)               |
| `array[1]=10*10`                         | 数组的赋值, array定义为整数,因此array[1]值为100        |
| `echo ${array[1]}`                       | 使用”$array[1]”没用.若无{}, 会认为是”$array”[1]    |
| `unset array`                            | 将array数组变量删除                             |
|                                          |                                          |
| `PATH=/home:$PATH`                       | 新增”/home:”在PATH变量最前面                     |
| `PATH=”$PATH””:/home”`                   | 前后都加”双引号”,无歧义. 建议这样书写                    |
| `PATH=${PATH}’:/home’`                   | 变量名用{大括号}指明,无歧义. 新增变量也可用’单引号’            |
|                                          |                                          |
| `echo $?`                                | ?为特殊变量,为上一指令传回的值. 0成功, !0失败              |
| `echo $$`                                | 获取并显示当前shell的 PID (process ID)           |
|                                          |                                          |
| `#` `##` `%` `%%` `/` `//`               | 变量的截取和替换. 以`myhome=/home/test/test.sh`为例 |
| ...... **`echo ${myhome#/*/}`**          | `test/test.sh`,从头比较, 单次删除,故~~`/home/`~~  |
| ...... **`echo ${myhome##/*/}`**         | `test.sh`, 从头比较, 全部删除,获得文件名              |
| ...... **`echo ${myhome%/*}`**           | `/home/test`,从尾比较, 单次删除,获得路径             |
| ...... **`echo ${myhome%%/*}`**          | 从尾比较, 全部删除,故全部被删掉                        |
| ...... **`echo ${myhome/test/TEST}`**    | `/home/TEST/test.h`, 从头比较, 单次替换          |
| ...... **`echo ${myhome//test/TEST}`**   | `/home/TEST/TEST.h`,从头比较, 全部替换           |
| `-` `:-` `+` `:+` `=` `:=` `?` `:?`      | 变量的比较和判断. 常用于判断和确保变量有效                   |
| ...... **`var=${str-expr}`**             | var为目标变量, str为已有变量, expr为变量值             |
| ...... **`myname=${myname:-root}`**      | 若myname不存在或为空,则myname=root               |
|                                          |                                          |
| `env`                                    | enviroment, 显示当前环境变量,用的最多!               |
| `set`                                    | 显示所有变量(环境变量,普通变量)                        |
| `export`                                 | 显示已成为当前环境变量的普通变量                         |
| ...... **`export variable`**             | 将variable设为环境变量, 等同 `declare -x variable` |
| `locale`                                 | 查看当前语言的环境变量                              |
| ...... **`locale -a`**                   | 查看系统支持的语言                                |


# Bash Shell特殊符号

| 符号                                       | 说明                                       |
| ---------------------------------------- | ---------------------------------------- |
| `*`                                      | 万用字符, 表示0或多个字符                           |
| `?`                                      | 万用字符, 表示一个字符                             |
| `!`                                      | 逻辑非, 通常在`[中括号]`内使用                       |
| `\`                                      | 转义字符, 需要转义的字符 `"` `'` `$` `\` ` ` \`  |
| ...... **`\n`**                          | 换行                                       |
| ...... **`\r`**                          | 回车                                       |
| ...... **`\t`**                          | 水平制表符                                    |
| ...... **`\v`**                          | 垂直制表符                                    |
| ...... **`\b`**                          | 后退                                       |
| ...... **`\a`**                          | 蜂鸣                                       |
| ...... **`\077`**                        | 八进制字符                                    |
| ...... **`\xff`**                        | 十六进制                                     |
| `#`                                      | 批注                                       |
|                                          |                                          |
| `$variable`                              | 变量名                                      |
| `${variable}`                            | 大括号. 中间为命令区块组合,限定变量名范围                   |
| ...... **`echo ${array[1]}`**            | 显示`array[1]` 变量值, array为数组,需用`{大括号}`包含变量名 |
| `[a-f], [35], [!a-z]`                    | 中括号. 中间为字符组合, `[仅代表一个字符]`                |
| ...... **`ls -d ~/*[0-9]*`**             | 列出用户home目录下所有包含数字的文件和目录                  |
| `$(command)`                             | 小括号. 中间为子shell,此命令等同于\`command\`         |
|                                          |                                          |
| `'$string'`                              | 单引号, 特殊符号无效,变量不置换, 显示为$string            |
| `"$variable"`                            | 双引号, 特殊符号有用,变量置换                         |
| \`command\`                              | \`(键盘1左边的字符),需要优先执行的指令                  |
| ...... **cd /usr/src/linux-headers-\`uname -r\`** | 进入当前linux的内核源码目录                         |
|                                          |                                          |
| cmd1 l cmd2 和 cm1 ll cmd2               | hexo解析问题, 无法再表格中正确显示`丨`, **故放到表格的最后**        |
| `cut` `grep` `split`                     | 截取分割, 通常配合 `pipe`使用                      |
| `sort` `wc` `uniq`                       | 排序命令, 通常配合 `pipe`使用                      |
| `tr` `col` `join` `paste` `expand`       | 字符转换, 通常配合 `pipe`使用                      |
| `cmd1;cmd2; cmd3`                        | 可以一行写多个指令                                |
| `cmd1 && cmd2`                           | cmd1执行正确($?为0),则继续执行cmd2, 否则不执行          |
|                                          |                                          |
| `>` `2>` `>>` `2>>`                      | 输出到文件 (>写入, >>累加, 2错误信息)                 |
| ...... **`ll > list.txt`**               | 将当前目录下的文件详细信息存储到list.txt文件中              |
| ...... **`ls / >> list.txt`**            | 将根目录下的文件信息追加到list.txt文件中                 |
| ...... **`find /home -name test > ok 2> error`** | 将正确信息写到ok中,错误的写到error中                   |
| ...... **`find /home -name test > list 2>&1`** | 将所有信息都写到list中 (&1是数字一)                   |
| ...... **`find /home -name test > /dev/null 2> err`** | `/dev/null`相当于黑洞.只将错误写到err中              |
| `<` `<<`                                 | 输入信息(<从文件获取, <<结束的输入字符)                  |
| ...... **`cat > catfile`**               | 从键盘获取文本并写到catfile中 (键盘按[ctrl]+d结束输入)     |
| ...... **`cat > catfile << end`**        | 从键盘获取文本并写到catfile中(键盘输入end结束输入)          |
| ...... **`cat > catfile < input`**       | 导入input文件信息再写到catfile中                   |


- `cmd1 | cmd2`  `pipe`管线命令,将cmd1的处理结果传给cmd2继续处理
- 譬如 `ll | more`  将ll获得的数据传给more进一步处理
- `cmd1 || cmd2`  cmd1执行错误($?为!0),则继续执行cmd2, 否则不执行
- 譬如 `ls /tmp/test && echo "exist" || echo "nofile"` 如果`/tmp/test`存在显示`exist`,否则`nofile`


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***