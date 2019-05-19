---
title: Python 错误及解决方法
date: 2019-05-19
categories: python
tags: [python, debug]
---

# UnicodeEncodeError: 'charmap' codec can't encode characters
- 此问题多发生在windows的区域和开发中用到在字符不匹配. 譬如英文区域的windows要编解码中文字符.
- 原因及解决方法参考 [代码页即地狱](https://blog.csdn.net/haiross/article/details/36189103)

简单来说, 就是windows底层编码的问题. 要解决这个问题, 只能从windows系统着手.

![Region](https://draapho.github.io/images/1904/Region.png)

----------

***原创于 [DRA&PHO](https://draapho.github.io/)***