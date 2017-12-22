---
title: QQ物联演示项目
date: 2017-12-23
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


# 编译和安装驱动

先编译安装一下LED, 测试一下LCD功能

## LED驱动

``` bash
# ubuntu主机端

unzip led_driver.zip
cd led_driver/
ll /work/system/linux-3.4.2/            # 确定内核目录存在, 编译要用到
make                                    # 编译LED驱动
arm-linux-gcc jz2440_led_app.c -o jz2440_led_app    # 编译测试文件


# jz2440开发板
#pwd = .../share/.../led_driver/        # 共享文件进入ubuntu下的驱动目录
cp jz2440_led_drv.ko /lib/modules/3.4.2/
insmod jz2440_led_drv.ko
./jz2440_led_app
# 可以看到打印信息, 并且开发板的LED灯亮灭.
rmmod jz2440_led_drv.ko                 # 卸载设备模块
```

## LCD测试

``` bash
# ubuntu主机端

unzip lcd_gui_simple.zip
cd lcd_gui_simple/
make                                    # 编译LED测试源码


# jz2440开发板
#pwd = .../share/.../lcd_gui_simple/    # 共享文件进入ubuntu下的驱动目录
ls /dev/fb0                             # 确认已存在设备fb0
./lcd_gui_simple                        # 测试屏幕
```

# 演示项目

## 编译和测试

必须将应用程序需要用到的文件都准备好, 这样才能正常原型.
有如下重点:
- 密钥文件放到 `/etc/qq_iot/demo_bind/`
- QQ SDK动态库放到 `/lib/`
- 应用文件和资源文件放在一起, 譬如 `/qqiot/`
- 准备好开发板必要驱动, 这里是led驱动. 其它驱动已经打包进内核.
- 确保网络正确, 能ping通外网.

``` bash
# ubuntu主机端
unzip net_bind_detector.zip
cd net_bind_detector/
# 确认一下./lib/libtxdevicesdk.so的版本. 保证所有代码用的同一个库
make clean
make                                    # 生成 net_bind_detector


# jz2440开发板
#pwd=.../share/.../密钥文件目录/
mkdir -p /etc/qq_iot/demo_bind/
tar xzf 1700003137001488.tar.gz         # 解压密钥文件
mv 1700003137001488/* /etc/qq_iot/demo_bind/
rm -r 1700003137001488
ls /etc/qq_iot/demo_bind/               # 确认一下

#pwd=.../share/.../net_bind_detector/   # 共享文件进入ubuntu下的驱动目录
cp net_bind_detector /qqiot/            # 拷贝到开发板flash中
cp lib/libtxdevicesdk.so /lib/          # 拷贝QQ SKD库
cp -rfd res/ /qqiot/                    # 拷贝测试用资源, d表示忽略软连接
ls /qqiot
ls /qqiot/res                           # 确认拷贝结果


# 开始测试
cd /qqiot/
insmod /lib/modules/3.4.2/jz2440_led_drv.ko     # 加载led模块
./net_bind_detector
# 开始演示, 在QQ界面上操作, 开发板屏幕或LED就会有响应
# 然后测试QQ物联设备给手机QQ发送消息 (需要QQ服务器端正确配置)
sendtextmsg                             # 测试文本的发送
sendpic                                 # 测试图片文件的发送
sendaudio                               # 测试音频文件的发送
sendvideo                               # 测试视频文件的发送
```

如果要实现开机自启动, 把相关命令放在 `/etc/init.d/rcS` 结尾处即可.
注意, 此程序用到了相对路径. 如果直接用 `/qqiot/net_bind_detector`, 加载相对路径文件时就会失败!



# 查看源码

这里就不分析了, 仅列出其文件结构

目录| 说明
-----|-----
led                 | led的应用程序(很简单)
framebuffer         | framebuffer底层实现
gui                 | 自制gui
lib                 | 腾讯QQ物联SDK的库文件存放位置
include             | 头文件
... qq_dev_sdk      | 腾讯QQ物联SDK的头文件存放位置
initDevice          | 设备初始化
DataPoint           | 实现 `tx_init_data_point` `tx_ack_data_point` `tx_report_data_point`
fileTransfer        | 实现 `tx_init_file_transfer`
msg                 | 实现 `tx_send_text_msg` `tx_send_structuring_msg`
res                 | 存放图片文件, 音频文件, 视频文件
