---
title: Zephyr Project ��������
date: 2023-04-25
categories: embedded
tags: [embedded, zephyr]
description: ����.
---


# ����

Zephyr Project ��һ������չ��ʵʱ����ϵͳ, Ϊ��Դ���޵��豸�ṩ֧��. �� Linux ������й�.
�������Ŀ����Linux�ص�: ����ǿ��, ѧϰ���߶���, ��������. ��Ҫʹ�������и�ʽ, ������Unixϵͳ���ԱȽϳ��, Window��������������Ī��������.
����Ŀ�ճ�����ʱ��, Ҳ��ע��, ������ָ���ֲ�, ��windows�¾�û�����óɹ�. �����п�������һ��, ������windows������, �ɹ�������л���, ���ѷ�����������.



# 1. ��װ Chocolatey

���ȣ���Ҫ��װ Chocolatey ��������������� [Chocolatey ��װҳ��](https://chocolatey.org/install) ��ȡ��ϸ��Ϣ��

ʹ�� PowerShell ��**����Ա���**�����������

```powershell
Set-ExecutionPolicy AllSigned
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

���� Chocolatey��

```powershell
choco upgrade chocolatey
```


# 2. ��װ����

��**����Ա���**��������ʾ��, ����������������԰�װ cmake, ninja, gperf, python, git, dtc-msys2, wget, unzip ���������ߡ�����Ѿ���װ������ȷ�����������°汾��

```cmd
choco feature enable -n allowGlobalConfirmation
choco install cmake --installargs 'ADD_CMAKE_TO_PATH=System'
choco install ninja gperf python git dtc-msys2 wget unzip
```


# 3. ��װ West ����

ʹ�� Python ��װ West ���ߡ�West ר�����ڹ��� Zephyr ��Ŀ�����������ز�������Ŀ��

```cmd
pip3 install -U west
cd %HOMEPATH%
west init zephyrproject
cd zephyrproject
west update

west zephyr-export
pip3 install -r %HOMEPATH%\zephyrproject\zephyr\scripts\requirements.txt
```

# 4. ��װ Zephyr SDK

��װ Zephyr SDK ʱ����� [Zephyr SDK �� GitHub ҳ��](https://github.com/zephyrproject-rtos/sdk-ng/releases) �������°汾�������ǹٷ��ĵ���, ��������İ汾 (�ٷ��ĵ����²���ʱ, �������ʱ����ʾ�汾����)��

���磬��ǰ���°汾Ϊ Zephyr SDK 0.16.0������ Windows �� FULL �汾��[��������](https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.0/zephyr-sdk-0.16.0_windows-x86_64.7z)����Ȼ�����ֶ���ѹ���ʵ���Ŀ¼��

�ڽ�ѹ���� `zephyr-sdk-0.16.0` Ŀ¼�£�˫������ `setup.cmd`��
��ʱ�����ʾ `Zephyr SDK setup requires '7z' to be installed and available in the PATH.` ����Ҫ��7z��bin���뵽��������PATH��.
һ���򵥵ķ��������Խ� 7z.exe �� 7z.dll ���Ƶ� `zephyr-sdk-0.16.0` Ŀ¼�£�Ȼ������ `setup.cmd`��
ע��: `setup.cmd`, ֻ��Ҫִ��һ��, ��Ҫ���ִ��.


# 5. ������Ŀ

Ҫ�鿴֧�ֵĿ������б�����ʣ�[�ٷ�֧�ֵĿ������б�](https://docs.zephyrproject.org/3.1.0/boards/index.html#boards)��

����ͷ�� ST Nucleo L152RE ������. ���Դ�Ϊ���������������

```cmd
cd %HOMEPATH%\zephyrproject\zephyr
west build -p always -b nucleo_l152re samples/basic/blinky
REM -p always ��ָ����ǰ, ǿ���������Ŀ¼. auto ���Զ�ʶ��

REM west build -p auto -b nucleo_l152re samples/basic/blinky
REM west build -p auto -b nucleo_f031k6 samples/basic/blinky
```

ע�⣺
- ����Ǵ������ط����Ƶ� zephyrproject �ļ��У�build ���ܻ������ʱ��ɾ�� zephyr Ŀ¼�µ� build �ļ���, ����ʹ�� `west build -p always ...`
- ����ڱ�������г��ִ�������ϸ����������ߵ���Ͱ汾Ҫ��Ȼ���������⡣

������: L152RE ���� 14K�� flash, 4K�� RAM...

|  Memory region    |  Used Size    |  Region Size    | %age Used     |
| ---- | ---- | ---- | ---- |
|  FLASH:    |   14200 B   | 512 KB     |  2.71%    |
|  RAM:     |  4224 B    |  80 KB    |    5.16%  |
|  IDT_LIST:      | 0 GB     |  2 KB    |  0.00%    |


��f031K�����忴�±�����: 13K��flash, 2K��RAM

|  Memory region    |  Used Size    | Region Size     | %age Used     |
| ---- | ---- | ---- | ---- |
|  FLASH:     | 12770 B     |  32 KB     | 38.97%     |
|  RAM:     |  1784 B      |  4 KB     |  43.55%    |
| IDT_LIST:     |  0 GB     |  2 KB    |  0.00%    |

**�򵥵Ľ���**: ����ĳЩ�ɱ�����, �г��ͳɱ������Ӧ��, Zephyr ����̫����Դ��. ֱ�۸о�, �ʺ�ʹ�� Zephyr ����Ŀ, �� RT-thread ��Ŀ������, ���������������Ƕ��ʽӦ��, ��ֱ��ʹ�õ���������ģ��򷽰�, �����ϱ�֤�˿ɿ��Ժ��ȶ���, ������Ŀ�Ŀ�������.


# 6. ��¼

ʹ���������������¼��

```cmd
west flash
```

��ʱ, ����ʾδ��װ openocd ��δ��ȷ���� openocd �Ļ�������.
����� [OpenOCD ����](https://openocd.org/pages/getting-openocd.html) ����Դ���룬
windows��װ�汾�� [OpenOCD �� GitHub ҳ��](https://github.com/openocd-org/openocd/releases/tag/v0.12.0) �������ص���Ӧ�汾��
����:  [Windows �汾�� OpenOCD](https://github.com/openocd-org/openocd/releases/download/v0.12.0/openocd-v0.12.0-i686-w64-mingw32.tar.gz)��
���ز���ѹ�󣬽��� bin Ŀ¼��ӵ��������� PATH �С�

����������������µ�������ʾ���������������������Բ��ԣ�

```cmd
openocd
REM ������� Open On-Chip Debugger ... �� openocd ��װ�ɹ�
```

Ȼ���ٴγ�����¼�͵��ԣ�

```cmd
west flash
west debug   
REM ���� (gdb) ����ģʽ
```

�����Ȼ�������⣬�������ʾ��Ϣ��ϸ���Ӳ�����Ӻ�ϵͳ���á����磬���ȼ����¼����Ȼ��鿴��⵽��Ӳ����ѹ�ȡ����������Ӳ�����죬�޷�һһ������



# 7. � Zephyr ��IDE

�ο� [Coccinelle](https://docs.zephyrproject.org/3.2.0/develop/tools/coccinelle.html)
�ο� [Using with PlatformIO](https://docs.zephyrproject.org/3.2.0/develop/tools/platformio/index.html)
�ο� [ Zephyr Eclipse ���](https://github.com/zephyrproject-rtos/eclipse-plugin)
������������, �Ƿ����, �Ƿ�����ʹ��, ����.


# �ο�����

- [Zephyr Getting Started Guide](https://docs.zephyrproject.org/3.1.0/develop/getting_started/index.html)
- [ChatGPT - Zephyr Project �п��ӻ���IDE��](https://chat.openai.com/)


----------

***ԭ���� [DRA&PHO](https://draapho.github.io/)***