---
title: QQ物联开发步骤简介
date: 2017-12-22
categories: qqiot
tags: [embedded linux, qqiot]
---


# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [嵌入式linux环境搭建-QQ物联](https://draapho.github.io/2017/12/18/1746-qqiot-env/)
- [QQ物联开发步骤简介](https://draapho.github.io/2017/12/22/1748-qqiot-procedure/)
- [QQ物联绑定分析](https://draapho.github.io/2017/12/20/1747-qqiot-bind/)
- [QQ物联演示项目](https://draapho.github.io/2017/12/23/1749-qqiot-demo/)

本文使用 linux-3.4.2 内核, 使用jz2440开发板.


# 基础概念

## 硬件设备概念
- SN (serial number), 序列号
    - 由产品开发商提供, 但QQ规定了格式要求
    - 需要保证唯一性. 即同一种类的单品都有其唯一的SN
    - 格式: 16个字符长度. 由字母, 数字, 下划线, 连词符, 冒号组成.
    - 譬如 `ABC-0032-1234567`
    - 历史原因, 源码里面的名称是 `guid`
- LICENSE, 数字签名
    - license 是对sn的数字签名, 所以与sn是一一对应的关系
    - license由腾讯提供的工具来实现, 输入sn即可
    - 其目的就是保护设备信息, 避免设备被山寨.
- PID(product identify), 产品ID.
    - 即产品类别ID, 类似于超市商品的二维码, 表明产品类别
    - 有了PID和SN后, QQ就可以唯一确定一台智能设备
    - QQ物联的设备二维码就是由PID和SN这两个信息组成的
    - QQ会提供PID值
- DIN(device identify number), 设备ID
    - 可以认为就是此设备的QQ号码, 64位长度.
    - DIN 由 PID + SN + LICENSE 产生.
    - QQ会保证DIN的唯一性
- SDK, 开发套件
    - 分为设备SDK和应用SDK
    - 设备SDK, 就是给智能硬件使用的开发套件. 以后学习的重点是在这里.
    - 应用SDK, 如果要开发独立APP, 就需要此SDK. 提供QQ开放接口. 此处略过不表.

## QQ云端概念
- datapoint, 数据点
    - 理解为QQ指定的一套数据格式规范即可.
- PropertyID, 属性ID
    - 每个datapoint都有自己的id, 用于表明此数值的属性.
    - 譬如property_id (200001), 表示摄像头分辨率.
    - 简单的理解, datapoint传输整个键值对. PropertyID是key.

## 轻APP前端

QQ物联轻APP是手机QQ里“我的设备”控制器内嵌的HTML5页面（模板），分为通用/公共模板和开发商自定义模板

- 通用/公共模板
    - 公共模板的样式不可自定义, 但可以自行配置功能控件.
    - 可节省软件端的研发和维护成本, 缩短产品研发周期.
- 自定义模板
    - 使用Html5, 根据QQ物联提供的设计规范和接口实现定制化用户界面 (内嵌在QQ里)
    - 自定义模板需要开发者将页面发布到自有的服务器, 然后将url地址提交到平台.
- deviceAPI
    - QQ物联提供的给自定义模板调用的JS接口.
    - 注意, 目前其对视屏功能仅部分支持.

## 手机APP
手机端概念只有在需要自己开发app, 调用应用SDK时, 才会用到!

- AppID
    - 标识APP, 此App使用QQ登录组件. 即调用了QQ的应用SDK
- OpenID
    - 等同于用户QQ号码的身份. 长度128bit
    - OpenID 由 appid + qq号码 产生
- TinyID (Tiny OpenID)
    - QQ内部由于兼容问题, 对OpenID的一个缩略, 使用64bit长度

## 配网方式(wifi下)
不少硬件设备是没有屏幕的, 如何接入wifi就成为一个大问题. QQ物联提供如下几种方式

- WiFi Router： 设备自行解决入网问题，适用于有屏幕的智能设备
- SmartLink： 博通合作方案, 其wifi芯片支持Monitor模式(可实现数据包注入), 内置了AES-CCM加密库
- SmartLinkEx: 额外采用声波通讯技术协同配网, 提高极端环境下的配网成功率. 适合有麦克风的设备
- QQLink： SmartLink的弱加密版本, 安全性没有SmartLink方案高.
- QQLinkEx： 额外采用声波通讯技术协同配网. 适合有麦克风的设备


# 开发步骤

1. 建立企业开发账号.
    - [Step1. 申请开发者账号](http://iot.open.qq.com/wiki/index.html#!FUNC/Register_On_WebSite.md), 申请一个公司用QQ
    - [Step2. 申请加入白名单](http://iot.open.qq.com/wiki/index.html#!FUNC/Register_On_WebSite.md), 需等待审核结果.
    - [Step3. 进入配置平台](http://iot.open.qq.com/wiki/index.html#!FUNC/Register_On_WebSite.md), 成功后, 就有开发配置平台了.
2. 创建新设备.
    - 在配置平台里面, 可以创建新设备.
    - 慎重选择设备类型, 不同的设备类型提供不同的后台功能!
    - 测试环境不要点击 `提交上线`, 最多有100台设备任意调试.
    - 如果提交上线, 设备就会被锁定, 等待QQ审核结果. 此过程无法开发调试!
    - 开发和测试完成后, 再去 `提交上线`, 等待审核结果.
    - 已审核通过的产品如果还要更改配置页面, 则需要再次通过腾讯审核.
3. 配置设备后台
    - 新建设备之设备类型: 决定QQ物联设备大致需要的功能(控制/音视频).
    - 设备信息之公钥上传: 用工具生成`public.pem`, 然后上传. 用于认证GUID/SN号.
    - 设备信息之联网方式: 如果设备有界面可以自行入网, 可以选择自行入网. 如果没有输入界面, 则需要选wifi配网方式.
    - 功能配置之公有功能: 设定手机QQ和QQ物联设备的收发内容
    - 功能配置之特殊功能: 用来定义手机QQ与QQ物联设备两者之间特殊消息的数据格式
        - 显示类型：只能是QQ物联设备向手机QQ发送用于显示的的数据
        - 控制类型：QQ物联设备与手机QQ可以互传控制消息的数据
        - 设置好后, 会获得一个ID值! 数据传输格式是腾讯的 datapoint
        - **功能描述**:  自定义数据的组织格式. 参考 [自定义指令](http://iot.open.qq.com/wiki/index.html#!FUNC/DataPoint_Custom_CMD.md) 里的说明
    - 控制器设置: 配置手机QQ的控制UI界面
        - 自动生成控制器, 就是使用QQ提供的通用模板. 模板里的元素可以自定义
        - 自定义控制器, 就是自定义模板. 需要HTML5开发并放到自己的服务器端
4. 创建设备序列号和密钥
    - 整个过程有两组公钥私钥配对.
    - 服务器生成的公钥私钥, 开发者需下载公钥`170000xxxx.pem`. 此配对用于加密数据, 保证通讯安全.
    - 开发者生成的公钥私钥, 开发者需上传公钥`public.pem`. 保证私钥安全性. 此配对用于认证设备SN没有被盗用.
    - 设备SN的认证方法是, 开发者用私钥加密SN生成license, 将SN和license传给QQ服务器, QQ服务器会用上传的公钥去检查SN合法性.
    - license最好也保存好. 因为如果别人获取license和SN后, 可以仿冒特定的设备.
    - `公钥&证书工具`, 在设备信息的公钥上传里提供了下载.
5. QQ物联设备端功能开发
    - [控制指令](http://iot.open.qq.com/wiki/#!FUNC/DataPoint_Common_CMD.md)
    - [自定义指令](http://iot.open.qq.com/wiki/#!FUNC/DataPoint_Custom_CMD.md)
    - [状态同步](http://iot.open.qq.com/wiki/#!FUNC/DataPoint_Sync_Status.md)
6. 开发者测试
7. 交给QQ物联官方审核
8. 发布产品


# 收发消息的过程

## QQ物联设备接收消息

datapoint的主要函数:
- `tx_init_data_point`: 初始化
- `tx_report_data_point`: 上报
- `tx_ack_data_point`: 回应

QQ物联设备端, 对消息处理的主要过程如下:
- `tx_init_data_point` 进行初始化后, 并定义回调函数 `on_receive_datapoint`
- 手机QQ发送datapoint消息给QQ物联设备
- QQ物联设备接收到后, 使用回调函数处理消息
- 处理方式是通过datapoint的ID来分辨消息类型(特殊功能里设置)


## QQ物联设备发送消息
- QQ设备发送消息给QQ服务器
    - `tx_send_text_msg` 发送文本
    - `tx_send_structuring_msg` 发送图文和音视频
- QQ服务器更具配置情况(触发器-动作-模板), 只转发满足条件的消息给手机QQ
- 触发器页面: 设置过滤条件并制定动作
    - 该消息由哪个QQ物联设备发送来的
    - 该消息的ID号
    - 触发后要执行的动作
- 动作页面: 动作制定模板(文本/图片/语音/视频)
- QQ服务器根据模板构造发送给手机QQ的消息


# 参考资料

- [QQ物联资料库](http://iot.open.qq.com/wiki/index.html)