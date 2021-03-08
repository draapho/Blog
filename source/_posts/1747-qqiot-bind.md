---
title: QQ物联绑定分析
date: 2017-12-20
categories: qqiot
tags: [embedded linux, qqiot]
description: 如题.
---


# 总览
- [嵌入式linux学习目录](https://draapho.github.io/2017/11/23/1734-linux-content/)
- [嵌入式linux环境搭建-QQ物联](https://draapho.github.io/2017/12/18/1746-qqiot-env/)
- [QQ物联开发步骤简介](https://draapho.github.io/2017/12/22/1748-qqiot-procedure/)
- [QQ物联绑定分析](https://draapho.github.io/2017/12/20/1747-qqiot-bind/)
- [QQ物联演示项目](https://draapho.github.io/2017/12/23/1749-qqiot-demo/)

本文使用 linux-3.4.2 内核, 使用jz2440开发板.


# demo_bind.c 的分析与测试

## 分析

打开demo_bind.c, 说明很详细, 主要流程如下
- 调用 `tx_init_device` 初始化设备信息. 可理解为将设备在QQ服务器上注册一下
- 打开QQ, 保证和设备连在同一个路由器上且能上网.
- 然后就可以在QQ我的设备中, 点击搜索新设备.
- 扫描设备并绑定成功后, 即触发设备的登录逻辑. 调用指定的回调函数.

``` c
bool initDevice() {                 // bind的核心函数, 初始化设备
    // 先读取三个重要文件
    // license, 认证文件. 文件名 ./licence.sign.file.txt
    // guid, 即SN设备序列号. 文件名 ./GUID_file.txt
    // svrPubkey变量中, 公钥. 文件名 ./1000000004.pem

    // 设置设备的基本信息
    tx_device_info info = {0};
    info.os_platform            = "Linux";              // os平台

    info.device_name            = "demo1";              // 设备名称
    info.device_serial_number   = guid;                 // 设备SN
    info.device_license         = license;              // 由SN生成的LICENSE
    info.product_version        = 1;
    info.network_type           = network_type_wifi;    // 入网方式
    info.product_id             = 1000000004;           // PID, QQ分配
    info.server_pub_key         = svrPubkey;            // 公钥

    // 设置回调函数
    tx_device_notify notify      = {0};
    notify.on_login_complete     = on_login_complete;   // 登录完成
    notify.on_online_status      = on_online_status;    // 状态改变
    notify.on_binder_list_change = NULL;

    // 设置目录和文件大小
    tx_init_path init_path = {0};
    ......

    // 核心语句, 向QQ服务器注册此设备.
    int ret = tx_init_device(&info, &notify, &init_path);
}
```

## 修改

示例里面的 `readBufferFromFile` 已经对license和SN进行文件化管理了.
为了以后的批量生产, 这里将必要的配置信息再打包一层, 统一放入一个配置文件.

``` bash
# Ubuntu端

# 建立一个分支, 用来修改和测试bind
sudo cp -rf Tencent_iot_SDK/ bind_test/

# 解压获得的QQ物联相关文件, 包括 licence, sn和公钥
sudo tar xzf 1700003137001488.tar.gz

# 改名后放到测试目录
sudo mv 1700003137001488/ conf/
sudo mv conf/ bind_test/

# 改下权限
sudo chmod -R 777 bind_test/
```

然后打开 `./bind_test/demo_bind.c` 文件, 仿照readBufferFromFile进行修改

``` c
// 新增如下内容
#include <stdlib.h>
#include <unistd.h>

struct conf_info {
    int  pid;
    char name[128];
    char pubkey_file[128];
    char guid_file[128];
    char license_file[128];
};
struct conf_info configInfo = {0, {0}, {0}, {0}, {0}};

bool readConfigFromFile(void) {
    char buf[128]={0};
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    bool ret = true;
    char *pconf[] = {configInfo.pubkey_file, configInfo.guid_file,  configInfo.license_file};
    // 尝试打开目录下的配置文件
    FILE * file = fopen("./conf/config", "rb");
    if (!file) {
        printf("open ./conf/config failed...\n");
        return false;
    }
    // 读取第一行的数据, PID信息
    read = getline(&line, &len, file);
    if (read > sizeof(buf)) {
        ret = false;
        printf("read PID failed...\n");
    } else {
        strncpy(buf,line,read-1);
        buf[read]='\0';
        configInfo.pid = atoi(buf);
        printf("PID=%d\n",configInfo.pid);
    }
    // 读取第二行的数据, Name信息
    read = getline(&line, &len, file);
    if (read > sizeof(buf)) {
        ret = false;
        printf("read Name failed...\n");
    } else {
        strncpy(buf,line,read-1);
        buf[read]='\0';
        sprintf(configInfo.name, buf);
        // printf("Name=%s\n",configInfo.name);
    }
    // 读取剩下的行, 都是文件数据
    int i;
    for (i=0; i<sizeof(pconf)/sizeof(char *); i++) {
        read = getline(&line, &len, file);
        if (read > sizeof(buf)) {
            ret = false;
            printf("read line%d failed...\n", i+2);
            break;
        } else {
            strncpy(buf,line,read-1);
            buf[read]='\0';
            if (access(buf, R_OK)) {
                ret = false;
                printf("fail to read %s\n",buf);
                break;
            } else {
                sprintf(pconf[i], buf);
                // printf("line%d: %s\n", i+2, pconf[i]);
            }
        }
    }
    if (ret) {                                  // 调试检查
        printf("NAME=%s\n",configInfo.name);
        printf("PEM =%s\n",configInfo.pubkey_file);
        printf("GUID=%s\n",configInfo.guid_file);
        printf("LICENSE=%s\n",configInfo.license_file);
    }
    if (line) free(line);
    fclose(file);
    return ret;
}

// 修改如下内容, -为原内容, +为修改后的内容
bool initDevice() {
+   if(readConfigFromFile() == false){
+       return false;
+   }

    // 读取 license
    unsigned char license[256] = {0};
    int nLicenseSize = 0;
-   if (!readBufferFromFile("./licence.sign.file.txt", license, sizeof(license), &nLicenseSize)) {
+   if (!readBufferFromFile(configInfo.license_file, license, sizeof(license), &nLicenseSize)) {

-   if(!readBufferFromFile("./GUID_file.txt", guid, sizeof(guid), &nGUIDSize)) {
+   if (!readBufferFromFile(configInfo.guid_file, guid, sizeof(guid), &nGUIDSize)) {

-   if (!readBufferFromFile("./1000000004.pem", svrPubkey, sizeof(svrPubkey), &nPubkeySize))
+   if (!readBufferFromFile(configInfo.pubkey_file, svrPubkey, sizeof(svrPubkey), &nPubkeySize))

-   info.device_name            = "demo1";
+   info.device_name            = configInfo.name;
    info.device_serial_number   = guid;
    info.device_license         = license;
    info.product_version        = 1;
    info.network_type           = network_type_wifi;
-   info.product_id             = 1000000004;
+   info.product_id             = configInfo.pid;
    info.server_pub_key         = svrPubkey;
}
```

然后, 需要修改makefile文件, 用的交叉编译. (注意空格改为TAB)

``` makefile
# 改为交叉编译!
CROSS_COMPILE = arm-linux-
CC  = $(CROSS_COMPILE)gcc

all:app1
    @echo build complete

clean:
    -rm SDKDemo_bind

app1:demo_bind.c
    $(CC) demo_bind.c -o SDKDemo_bind -O0 -g3 -I"./include" -L"./lib" -ltxdevicesdk -lpthread -ldl -lstdc++
```


最后, 设置conf文件.

```
1700003137
jz2440_bind_demo
./conf/1700003137.pem
./conf/GUID_file[1700003137001488].txt
./conf/licence.sign.file[1700003137001488].txt
```


## 测试


``` bash
# ubuntu端
# pwd = share/.../bind_test         # 共享文件夹下的bind_test目录
$ make                              # 编译


# jz2440端
# pwd = mnt/share/.../bind_test     # 共享文件夹下的bind_test目录
$ cp ./lib/libtxdevicesdk.so /lib   # 拷贝动态库到开发板本地lib
$ ls -l /lib/libtxdevicesdk.so      # 检查一下

$ mkdir /qqiot
$ cp SDKDemo_bind /qqiot            # 拷贝执行文件
$ cp -rf conf/ /qqiot               # 拷贝配置文件
$ cd /qqiot                         # 切换目录
$ ls                                # 查看结果

$ ./SDKDemo_bind                    # 运行范例
# 会打印很多信息. 查看是否有如下类似信息
WLAN connection with tencent iot server ... is setting up
xpnet_gethostbyname: Begin gethostbyname device msf.3g.qq.com
```

**注意**:
必须正确设置开发板的网络. 我已设置开发板为dhcp, 因此没有遇到网络方面的问题.
如果使用的是静态IP, 记得设置一下网关等信息.
可以用 `route` 指令查看网络路由表

然后, 打开手机端QQ, 保证手机和开发板在同一局域网下.
联系人->设备->发现新设备->绑定设备...就能看到jz2440_demo设备的界面了.

# 参考资料

- [QQ物联资料库](http://iot.open.qq.com/wiki/index.html)