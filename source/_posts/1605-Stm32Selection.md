---
title: stm32选型及资料搜索指南
date: 2016-10-1
categories: embedded
tags: [stm32]
---

# stm32选型及手册搜索
  - 进入搜索网页[STM选型](http://www.st.com/content/st_com/en/products/microcontrollers.html)
  - 在搜索框输入指定型号, 点击进入具体型号的页面. 如[STM32F103RC](http://www.st.com/content/st_com/en/products/microcontrollers/stm32-32-bit-arm-cortex-mcus/stm32f1-series/stm32f103/stm32f103rc.html)
  - [DS5792](http://www.st.com/content/ccc/resource/technical/document/datasheet/59/f6/fa/84/20/4e/4c/59/CD00191185.pdf/files/CD00191185.pdf/jcr:content/translations/en.CD00191185.pdf) -  **DataSheet, 数据手册. 电气参数详解, 软硬件必备**
  - [RM0008](http://www.st.com/content/ccc/resource/technical/document/reference_manual/59/b9/ba/7f/11/af/43/d5/CD00171190.pdf/files/CD00171190.pdf/jcr:content/translations/en.CD00171190.pdf) - **Reference Manuals, 参考手册. 寄存器详解. 软件开发必备**
  - [AN1709](http://www.st.com/content/ccc/resource/technical/document/application_note/a2/9c/07/d9/2a/b2/47/dc/CD00004479.pdf/files/CD00004479.pdf/jcr:content/translations/en.CD00004479.pdf) - **Application Notes, 应用指南. 需要仔细看这类文档**. 是针对具体问题的指南, 如这一篇是EMC设计指南
  - [PM0075](http://www.st.com/content/ccc/resource/technical/document/programming_manual/10/98/e8/d4/2b/51/4b/f5/CD00283419.pdf/files/CD00283419.pdf/jcr:content/translations/en.CD00283419.pdf) - Programming Manuals, 烧录手册. 介绍擦写flash相关的流程和寄存器
  - [ES0340](http://www.st.com/content/ccc/resource/technical/document/errata_sheet/f5/50/c9/46/56/db/4a/f6/CD00197763.pdf/files/CD00197763.pdf/jcr:content/translations/en.CD00197763.pdf) - Errata Sheets, 勘误表. 遇到非常奇怪的问题时, 可以先来看看勘误表, 是否源文件就是错的!
  - [TN1163](http://www.st.com/content/ccc/resource/technical/document/technical_note/92/30/3c/a1/4c/bb/43/6f/DM00103228.pdf/files/DM00103228.pdf/jcr:content/translations/en.DM00103228.pdf) - Technical Notes & Articles, 技术指南, 存储焊接, 开发工具配置之类的解答. **生产必备**
  - [UM1561](http://www.st.com/content/ccc/resource/technical/document/user_manual/f9/4a/8d/e6/b8/20/4a/46/DM00062592.pdf/files/DM00062592.pdf/jcr:content/translations/en.DM00062592.pdf) - User Manuals, 对官方开发板或开发工具的用户说明书

# 其它设计资料的搜索
  - 根据型号并不能找出期望的文档. 譬如需要一份电源设计参考.
  - 进去搜索网页[STM选型](http://www.st.com/content/st_com/en/products/microcontrollers.html)
  - 在搜索框输入关键词`hardware power`, 在搜索结果页面, 选择`Resouces`标签
  - 这里第一条就是 [AN4218: Hardware design guideline power supply and voltage measurement](http://www.st.com/content/ccc/resource/technical/document/application_note/87/b8/0f/5e/ab/d0/4f/2d/DM00071779.pdf/files/DM00071779.pdf/jcr:content/translations/en.DM00071779.pdf)


----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***