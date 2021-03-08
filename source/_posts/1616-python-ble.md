---
title: 使用python实现BLE通讯
date: 2016-11-15
categories: python
tags: [python, pygatt, BLE]
description: 如题.
---

# 环境与资源
- windows 开发环境
- python 2.7
- [pygatt](https://github.com/peplin/pygatt)
- Bluegiga 的 [BLED112 Bluetooth Smart Dongle](http://www.silabs.com/products/wireless/bluetooth/bluetooth-smart-modules/Pages/bled112-bluetooth-smart-dongle.aspx)

# 闲扯
- 背景, 需要在windows上做一款基于BLE通讯的软件. 第一反应, 痛苦.
- 使用的是 Bluegiga 的BLE方案, 协议栈芯片内置, 串口通讯即可, 并寻得 [bglib](https://github.com/jrowberg/bglib) 这么一个python库, 还有范例!
- 不幸的是, 自己功力不够, 基于此函数库开发出的BLE通讯, 非常不稳定... 没有痛下决心自己写, 于是继续尝试寻找资源.
- 觅得 [pygatt](https://github.com/peplin/pygatt) 方案, 三平台全支持! windows 和 mac 下正是基于bglib实现的!
- [pygatt](https://github.com/peplin/pygatt) 是python的第三方库, 说明文档比较少, 测试了一下非常好用!

# 测试代码
- DEVICE_ADDRESS, 默认的需要connect的BLE地址
- 基于 Bluegiga 的 `cable_replacement` 范例, 其 characteristic uuid 为 `e7add780-b042-4876-aae1-112855353cc1`

``` python
import pygatt
import logging
import binascii
import time


# Many devices, e.g. Fitbit, use random addressing - this is required to connect.
ADDRESS_TYPE = pygatt.BLEAddressType.random
DEVICE_ADDRESS = "00:07:80:BF:6A:73"


def indication_callback(handle, value):
    print "indication, handle %d: %s " % (handle, value)


def pytest(address=DEVICE_ADDRESS, type=pygatt.BLEAddressType.public):
    try:
        adapter = pygatt.BGAPIBackend()
        adapter.start()

        print "===== adapter.scan() ====="
        devices = adapter.scan()
        for dev in devices:
            # print dev
            print "address: %s, name: %s " % (dev['address'], dev['name'])

        print "===== adapter.connect() ====="
        device = adapter.connect(address, address_type=type)
        print "address: " + str(device._address)
        print "handle : " + str(device._handle)
        print "rssi   : " + str(device.get_rssi())

        print "====== device.discover_characteristics() ====="
        for uuid in device.discover_characteristics().keys():
            try:
                print("Read UUID %s (handle %d): %s" %
                      (uuid, device.get_handle(uuid), binascii.hexlify(device.char_read(uuid))))
            except:
                print("Read UUID %s (handle %d): %s" %
                      (uuid, device.get_handle(uuid), "!deny!"))

        print "====== device.char_read() / device.char_read_handle() ====="
        print "2a00: " + device.char_read("00002a00-0000-1000-8000-00805f9b34fb")
        print "2a00: " + device.char_read_handle(3)

        print "====== device.subscribe() ====="
        device.subscribe("e7add780-b042-4876-aae1-112855353cc1",
                         callback=indication_callback, indication=True)
        # device.receive_notification(8, "test")

        print "====== device.char_write_handle() ====="
        in_buf = map(ord, "hello world, hello BLE!!!")
        # send via uuid & handle, maximum is 20 bytes
        device.char_write("e7add780-b042-4876-aae1-112855353cc1", in_buf[:20])
        device.char_write_handle(0x08, in_buf[20:])

        while (True):
            time.sleep(0.1)
    finally:
        adapter.stop()


if __name__ == "__main__":
    # logging.basicConfig()
    # logging.getLogger('pygatt').setLevel(logging.DEBUG)
    pytest()
```

# BleDevice 类
- 为了方便使用, 自己基于 pygatt 再打包一层
- 遗憾的是没有disconnect的通知. 可以参考 [Disconnect event not shown](https://github.com/peplin/pygatt/issues/72)

``` python
import pygatt
import logging


class BleDevice(pygatt.BGAPIBackend):

    def __init__(self):
        self.device = None
        self.adapter = pygatt.BGAPIBackend()
        self.adapter.start()

    def stop(self):
        self.adapter.stop()

    def scan(self, timeout=5):
        self.devices = self.adapter.scan(timeout)
        return self.devices

    def connect_name(self, name, devices=None):
        if devices is None:
            devices = self.devices
        for dev in self.devices:
            if name == dev['name']:
                return self.connect(dev['address'])
        return None

    def connect(self, address):
        self.device = self.adapter.connect(address)
        return self.device

    def discover_characteristics(self, device=None):
        if device is None:
            device = self.device
        characteristics = []
        for uuid in device.discover_characteristics().keys():
            try:
                device.char_read(uuid)
                characteristics.append(
                    {'uuid': uuid, 'handle': device.get_handle(uuid), 'readable': True})
            except Exception as e:
                if "unable to read" in str(e).lower():
                    characteristics.append(
                        {'uuid': uuid, 'handle': device.get_handle(uuid), 'readable': False})
                else:
                    raise e
        return characteristics

    def set_indication(self, uuid, device=None, callback=None, indication=True):
        if device is None:
            device = self.device
        device.subscribe(uuid, callback, indication)

    def read_characteristics(self, uuid, device=None):
        if device is None:
            device = self.device
        return device.char_read(uuid)

    def read_characteristics_handle(self, handle, device=None):
        if device is None:
            device = self.device
        return device.char_read_handle(handle)

    def write_characteristics(self, str, uuid, device=None):
        if device is None:
            device = self.device
        data = map(ord, str)
        for i in range(0, len(data), 20):
            device.char_write(uuid, data[i:i + 20])

    def write_characteristics_handle(self, str, handle, device=None):
        if device is None:
            device = self.device
        data = map(ord, str)
        for i in range(0, len(data), 20):
            device.char_write_handle(handle, data[i:i + 20])


if __name__ == "__main__":
    # logging.basicConfig()
    # logging.getLogger('pygatt').setLevel(logging.DEBUG)
    ble = BleDevice()
    print ble.scan()
    device = ble.connect_name("Bluegiga CR Demo")
    print device._address
    chars = ble.discover_characteristics(device)
    print chars
    # print chars[0]['uuid']
    print ble.read_characteristics(chars[1]['uuid'])
    ble.write_characteristics("hello world", chars[0]['uuid'])
```


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***