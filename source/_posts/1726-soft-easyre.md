---
title: 人人都看得懂的正则表达式教程
date: 2017-09-19
categories: software
tags: [software, regular]
description: 正则表达式规范简介.
---

***转载自 [人人都看得懂的正则表达式教程](https://mp.weixin.qq.com/s?__biz=MzI4MDEwNzAzNg==&mid=2649444384&idx=1&sn=b1650af947842bbafb229eaabef4447e&key=93e82051231712653225010bec76aa3cdd1bb9dfb4cb4676f695a6cba336d79a73a39a9ae825aae8c16f26c0d1e0c67f7d96c8e03161da2c68ed58cc68e7c5818fdc72647bae92df46a1b85a43e276cd&ascene=1&uin=MTUzODYxOTg2MQ%3D%3D&devicetype=Windows-QQBrowser&version=61030006&pass_ticket=X0yVRsvNQron8bDKwr7uv0tD%2FafEwhP8NalG1zmH0siQV8OIDKoyAcobBC8fze13)***

---------------------------


# 前言
- [正则表达式](https://draapho.github.io/2016/12/18/1628-soft-regular/)
- [人人都看得懂的正则表达式教程](https://draapho.github.io/2017/09/19/1726-soft-easyre/)
- [最全的常用正则表达式大全](https://draapho.github.io/2017/10/07/1727-soft-reexample/)

本文有助于快速上手正则表达式, 但语法非常不全, 因此写出的表达式不够简练.

编写验证规则最流行和最简单的方法就是正则表达式了，但唯一的一个问题是正则表达式的语法太隐晦了，让人蛋疼无比。
很多开发者为了在项目中应用复杂的验证，经常要使用一些小抄来记住正则式的复杂语法和各种常用命令。
在这篇文章中，我将试图让大家明白什么是正则表达式，以及如何更轻松地学习正则表达式。

# 3个重要的正则式命令
记住正则语法最好的办法就是记住这三样东西：BCD

- **B**racket, 括号
    - 方括号 `[需要匹配的字符]`
    - 花括号 `{指定匹配字符的数量}`
    - 圆括号 `(字符分组)`
- **C**aret, 插入符号
    - `^` 表示字符串开始
- **D**ollars, 美元符号
    - `$` 表示字符串结束

# 举例
- `[a-g]{3}`
    输入的字符在a-g之间并且长度为3
- `[a-g]{1,3}`
    输入的字符在a-g之间并且最大长度为3最小长度为1
- `^[0-9]{8}$`
    匹配像91230456, 01237648那样的固定8位数
- `^[0-9]{3,7}$`
    验证最小长度为3最大长度为7的数字，如：123, 1274667, 87654
- `^[a-z]{3}[0-9]{7}$`
    验证像LJI1020那样的发票编号，前3个是字母剩余为8位长度的数字
- `^www[.][a-z]{1,15}[.](com|org)$`
    验证简单的网址URL格式, 域名是长度在1-15的英文字母
- `^[a-zA-Z0-9]{1,10}@[a-zA-Z]{1,10}.(com|org)$`
    验证email格式
- `^(([0-9])|([0-1][0-9])|([0-2][0-5]))$`
    验证值在0-25的数字
- `^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])[- / .]([1-9]|0[1-9]|1[0-2])[- / .](1[9][0-9][0-9]|2[0][0-9][0-9])$`
    验证DD/MM/YYYY格式的日期
        - `([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])` DD允许数值为`1-9,01-09,10-19,20-29,30-31`
        - `[- / .]` 允许的日期分隔符
        - `([1-9]|0[1-9]|1[0-2])` MM月份的数值 `1-9,01-09,10-12`
        - `(1[9][0-9][0-9]|2[0][0-9][0-9])` YY年份的数值 `1900-2099`

# 快捷命令

实际命令 | 快捷命令
--------|-------------
`[0-9]` | `d`
`[a-z][0-9][_]` | `w`
0次或多次发生 | `*`
1次或多次发生 | `+`
0次或1次发生 | `?`


------------------------------

***转载自 [人人都看得懂的正则表达式教程](https://mp.weixin.qq.com/s?__biz=MzI4MDEwNzAzNg==&mid=2649444384&idx=1&sn=b1650af947842bbafb229eaabef4447e&key=93e82051231712653225010bec76aa3cdd1bb9dfb4cb4676f695a6cba336d79a73a39a9ae825aae8c16f26c0d1e0c67f7d96c8e03161da2c68ed58cc68e7c5818fdc72647bae92df46a1b85a43e276cd&ascene=1&uin=MTUzODYxOTg2MQ%3D%3D&devicetype=Windows-QQBrowser&version=61030006&pass_ticket=X0yVRsvNQron8bDKwr7uv0tD%2FafEwhP8NalG1zmH0siQV8OIDKoyAcobBC8fze13)***