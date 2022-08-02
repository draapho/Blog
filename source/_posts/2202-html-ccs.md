---
title: HTML和CSS基础
date: 2022-08-01
categories: 网页开发
tags: [网页开发, HTML, CSS]
description: 介绍学习HTML和CSS基础
---

# HTML 参考资料
- [HTML 教程](http://c.biancheng.net/html/)
- [HTML 参考手册](https://www.runoob.com/tags/html-reference.html)

# HTML 范例
```html
<!DOCTYPE html>
<html lang="en">
<!-- 这是注释 -->
<head>
    <meta charset="utf-8">		<!-- 当前文档采用UTF-8编码 -->
    <title>HTML网页布局</title>
    <h1 style="color:blue;text-align:center;">This is a heading</h1>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
    <div class="container">
        <div class="wrapper clearfix">
            <nav>
                <ul>
                    <li><a href="http://c.biancheng.net/">首页</a></li>
                    <li><a href="http://c.biancheng.net/html/">HTML教程</a></li>
                    <li><a href="http://c.biancheng.net/css3/">CSS教程</a></li>
                    <li><a href="http://c.biancheng.net/js/">JS教程</a></li>
                </ul>
            </nav>
            <section>
                <h2>网站简介</h2>
                <p>introduce yourself. welcome to <b>NOWHERE</b></p>
            </section>
        </div>
        <footer>
            <p>draapho.github.io</p>
        </footer>
    </div>
</body>
</html>
```

# CSS 参考资料
- [CSS 教程](http://c.biancheng.net/css3/)
- [CSS 参考手册](https://www.runoob.com/cssref/css-reference.html)

# CSS 范例
```css
/* 范例, 这条是注释 */
h1 {                    /* h1 是选择器 */
    color: blue;        /* color 是属性, blue是值 */
    text-align: center; /* text-align 是属性, center */
}
```

# CSS 选择器简要说明
- CSS 选择器用于快速选定HTML页面中的元素, 然后对这些元素进行设置/渲染.
- 选择器分类:
    - 通用选择器: `* {}` ,匹配HTML的所有元素
    - 标签选择器: `h1 {}` ,对应html标签. 后面可以紧跟其它类型的选择器, 譬如 `h1.info {}`
    - 分组选择器 `,` ,减少重复样式的定义. 如 `h1,h2,h3 {}`
    - ID选择器: `#idName {}` ,对应 html id
    - 类选择器: `.className {}` ,对应 html class
    - 多类选择器: `.name1.name2 {}` ,即选中多个 html class, 无需空格.
    - 后代选择器: `h1 a {}`, 标签中间留一个空格即可, 对应 html 嵌套关系
    - 子选择器: `>` ,标签必须是直接后代, 只有一层嵌套关系
    - 相邻兄弟选择器: `+` ,标签必须是相邻的兄弟关系, 即老二和老三, 但不能是老大和老三
    - 通用兄弟选择器: `~` ,标签必须是兄弟关系
    - 属性选择器: `[]` ,匹配特定属性的元素. 譬如 `input[lang|=en]`
    - [伪类选择器](http://c.biancheng.net/css3/pseudo-class.html): `:` ,匹配元素的特殊状态. 譬如 `li:first-child {}`



----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
