---
title: Python 字符串处理
date: 2016-11-24
categories: python
tags: [python, string]
---

# 进制转换 / 编码转换

- [hex](https://docs.python.org/2/library/functions.html#hex), 十进制->十六进制字符串
- [oct](https://docs.python.org/2/library/functions.html#oct), 十进制->八进制字符串
- [oct](https://docs.python.org/2/library/functions.html#oct), 十进制->八进制字符串
- [chr](https://docs.python.org/2/library/functions.html#chr), 十进制->ASCII码字符
- [unichr](https://docs.python.org/2/library/functions.html#unichr),  十进制->unicode编码
- [ord](https://docs.python.org/2/library/functions.html#ord),  ascii码/unicode编码->十进制
- [binascii](https://docs.python.org/2/library/binascii.html), 字符串<->字节流
- [struct](https://docs.python.org/2/library/struct.html), 字符串<->字节流
  - struct中的 [fmt](https://docs.python.org/2/library/struct.html#format-characters) 详解


- [str.decode / str.encode](https://docs.python.org/2/library/stdtypes.html#string-methods), 基于unicode的编码转换
- [Standard Encodings](https://docs.python.org/2/library/codecs.html#standard-encodings), python支持的编码表
  - 常用的有 `hex`, `utf-8`, `unicode_escape`
- [python字符串编码及乱码解决方案](http://blog.csdn.net/pipisorry/article/details/44136297)
  - 解释了unicode与str在python2.7 和 python3下的区别. `str.decode`和`str.encode`的含义
  - python2.7, 默认str编码为ascii, 需要使用`s=u"人生苦短"`来表示unicode编码字符串(便于跨平台统一)
  - **终极原则： decode early, unicode everywhere, encode late**


- [更多的python内置函数](https://docs.python.org/2/library/functions.html)如下
  - int(x [,base ]), 将x转换为一个整数
  - long(x [,base ]), 将x转换为一个长整数
  - float(x), 将x转换到一个浮点数
  - complex(real [,imag ]), 创建一个复数
  - str(x) , 将对象 x 转换为字符串
  - repr(x), 将对象 x 转换为表达式字符串
  - eval(str), 用来计算在字符串中的有效Python表达式,并返回一个对象
  - tuple(s), 将序列 s 转换为一个元组
  - list(s), 将序列 s 转换为一个列表


## 十进制<->十六进制字符串
``` python
>>> hex(255)
'0xff'
>>> float.hex(1.0)
'0x1.0000000000000p+0'

# 可以有前缀 0b/0B(二进制), 0o/0O/0(八进制), or 0x/0X(十六进制),
>>> int('0xff', 16)
255
>>> int('ff', 16)
255
```

## 二进制字符串<->十六进制字符串
``` python
>>> bin(int('0xff', 16))
'0b11111111'

>>> hex(int('0b1010',2))
'0xa'
```

## 十进制<->unicode字符串<->utf8编码

``` python
>>> c = u'ñ'            # u表示使用unicode编码存储.
>>> c                   # 显示c在电脑中的值
u'\xf1'                 # 即 u'\u00f1', \u需要2byte!

>>> ord(c)
241

>>> unichr(241)
u'\xf1'

>>> u'\u00f1'.encode('utf-8')       # unicode->utf-8
'\xc3\xb1'
>>> '\xc3\xb1'.decode('utf-8')      # utf-8->unicode
u'\xf1'
>>> print u'\u00f1'                 # 打印显示
ñ
```

## 字节流<->整数

``` python
# 使用 struct
>>> import struct

# 字节流->整数
>>> struct.unpack('<hh', bytes(b'\x01\x00\x00\x00'))    # 转义为short型整数
(1, 0)
>>> struct.unpack('<L', bytes(b'\x01\x00\x00\x00'))     # 转义为long型整数
(1,)

# 整数->字节流
>>> struct.pack('<HH', 1,2)
'\x01\x00\x02\x00'
>>> struct.pack('<LL', 1,2)
'\x01\x00\x00\x00\x02\x00\x00\x00'
```

## 几个实用的例子

- 去掉字符串中的跳脱符, 生成标准的unicode字符串

``` python
>>> u'\\u4f60\\u4f60'.decode('unicode_escape')
u'\u4f60\u4f60'
```

- 解码16进制字符串：也可以直接 print 出来

``` python
>>> b='\xd1\xee\xba\xea\xc1\xc1\n'
>>> print unicode(b, 'gbk').encode('utf8') # 等同于 print b.decode('gbk').encode('utf8')
```

- bin <-> ascii

``` python
# 字符串->ASCII编码串
>>> '1234'.encode("hex")
'31323334'
# ASCII编码串->字符串
>>> '3031'.decode("hex")
'01'

# 使用 binascii
>>> import binascii
>>> binascii.hexlify("1234")    # 或者 binascii.b2a_hex("1234")
'31323334'
>>> binascii.unhexlify("3031")  # 或者 binascii.a2b_hex("3031")
'01'
```



# 字符串<->数值/列表/字典

## 字符串<->数值

- int(x [,base ]), 将x转换为一个整数
- long(x [,base ]), 将x转换为一个长整数
- float(x), 将x转换到一个浮点数
- **使用re正则表达式, 实用范例**

``` python
>>> import re
>>> str = "test: 12a345 to 325.-123.34"
>>> # this can get the number from str like "good456sdg78", return ['456', '78']
>>> print re.findall(r'\d+', str)
['12', '345', '325', '123', '34']
>>> # this can get the number seperate in str like "good12sd 45 78 ", return ['45', '78']
>>> print re.findall(r'\b\d+\b', str)
['325', '123', '34']
>>> # more complicated, can recognize and return [30, -10, 34.12, -12.34, 67.56E+3, -14.23e-2]
>>> print re.findall("[-+]?\d+[\.]?\d+[eE]?[-+]?\d*", str)
['12', '345', '325', '-123.34']
```

## 字符串->列表/字典 (去掉引号)

- eval(), 将str当成有效的表达式来求值并返回计算结果. 在确保str源安全的情况下可用.
  - [Eval really is dangerous](http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html)
  - [Python:eval的妙用和滥用](http://blog.csdn.net/zhanh1218/article/details/37562167)
- [ast.literal_eval()](https://docs.python.org/2/library/ast.html#ast-helpers), eval的替代品, 更安全

``` python
# 字符串->列表
>>> eval("[1,2,3]")
[1, 2, 3]

# 字符串->字典
>>> eval("{'one':1, 'two':2}")
{'two': 2, 'one': 1}
```

## 字符串<->列表

- str.join(), 列表->字符串
- str.split(), 字符串->列表

``` python
# 字符串->列表
>>> lst = list("hello")
>>> lst
['h', 'e', 'l', 'l', 'o']

# 列表->字符串
>>> ''.join(lst)
'hello'

# 字符串->列表 (指定分隔符, 如空格, 逗号)
>>> season = 'spring, summer, autumn, winter'
>>> season.split (',')
['spring', ' summer', ' autumn', ' winter']

# 列表->字符串
>>> lst = ["spring", "summer", "autumn", "winter"]
>>> ', '.join(lst)
'spring, summer, autumn, winter'

# 整数列表->字符串
>>> lst = [1, 2, 3]
>>> ''.join(str(e) for e in lst)
'123'

# 字符串->hex格式列表->hex格式字符串
>>> map(ord, "1234") # [0x31, 0x32, 0x33 0x34]
[49, 50, 51, 52]
>>> ''.join(["%02x" % i for i in map(ord, "1234")])
'31323334'
```

# 字符串操作

## 操作基础

``` python
# 去前后空格及特殊符号
s.strip().lstrip().rstrip(',')

# 查找字符
sStr1.index(sStr2)  # 返回所在位置, 不存在则报错
sStr2 in sStr1      # 返回 True or False

# 比较字符串
cmp(sStr1,sStr)

# 字符串长度
len(sStr1)

# 将字符串中的大小写转换
sStr1.upper().lower()

# 扩充到指定长度
str(01).zfill(5) # “00001”

# 翻转字符串
sStr1[::-1]

# 分割字符串
s.split(',')

# 字符串切片
str = ’0123456789′
print str[0:3]      # 截取第一位到第三位的字符
print str[:]        # 截取字符串的全部字符
print str[6:]       # 截取第七个字符到结尾
print str[:-3]      # 截取从头开始到倒数第三个字符之前
print str[2]        # 截取第三个字符
print str[-1]       # 截取倒数第一个字符
print str[::-1]     # 创造一个与原字符串顺序相反的字符串
print str[-3:-1]    # 截取倒数第三位与倒数第一位之前的字符
print str[-3:]      # 截取倒数第三位到结尾
```

## 查看手册及高阶使用


- [cookbook-第二章：字符串和文本](http://python3-cookbook.readthedocs.io/zh_CN/latest/chapters/p02_strings_and_text.html), 实用范例
  - [2.1 使用多个界定符分割字符串](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p01_split_string_on_multiple_delimiters.html), split(), re.split()
  - [2.2 字符串开头或结尾匹配](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p02_match_text_at_start_end.html), startswith(), endswith()
  - [2.3 用Shell通配符匹配字符串](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p03_match_strings_with_shell_wildcard.html), fnmatch(), fnmatchcase()
  - [2.4 字符串匹配和搜索](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p04_match_and_search_text.html), find(), findall(), match(), re.match()
  - [2.5 字符串搜索和替换](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p05_search_and_replace_text.html), replace(), re.sub()
  - [2.6 字符串忽略大小写的搜索替换](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p06_search_replace_case_insensitive.html), re.IGNORECASE
  - [2.7 最短匹配模式](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p07_specify_regexp_for_shortest_match.html), 解决成对符号的问题, 避免贪婪算法
  - [2.8 多行匹配模式](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p08_regexp_for_multiline_partterns.html), 解决回车换行的问题
  - [2.9 将Unicode文本标准化](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p09_normalize_unicode_text_to_regexp.html)
  - [2.10 在正则式中使用Unicode](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p10_work_with_unicode_in_regexp.html)
  - [2.11 删除字符串中不需要的字符](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p11_strip_unwanted_characters.html), strip(), replace(), re.sub()
  - [2.12 审查清理文本字符串](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p12_sanitizing_clean_up_text.html)
  - [2.13 字符串对齐](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p13_aligning_text_strings.html), ljust(), rjust(), center(), format()
  - [2.14 合并拼接字符串](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p14_combine_and_concatenate_strings.html), join()
  - [2.15 字符串中插入变量](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p15_interpolating_variables_in_strings.html), format()的高阶使用
  - [2.16 以指定列宽格式化字符串](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p16_reformat_text_to_fixed_number_columns.html), textwrap
  - [2.17 在字符串中处理html和xml](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p17_handle_html_xml_in_text.html)
  - ~~[2.18 字符串令牌解析](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p18_tokenizing_text.html), 语法的解析~~
  - ~~[2.19 实现一个简单的递归下降分析器](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p19_writing_recursive_descent_parser.html), 语法的解析~~
  - ~~[2.20 字节字符串上的字符串操作](http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p20_perform_text_operations_on_byte_string.html), bytearray~~


- [String Methods](https://docs.python.org/2/library/stdtypes.html#string-methods), string提供的方法/函数
  - [String Formatting Operations](https://docs.python.org/2/library/stdtypes.html#string-formatting-operations), 格式化显示, 建议使用format替代


- [string — Common string operations](https://docs.python.org/2/library/string.html), python官方手册之字符串操作
  - [String constants](https://docs.python.org/2/library/string.html#string-constants), 字符串常量, 如字母, 数字
  - [Format examples](https://docs.python.org/2/library/string.html#format-examples), 格式化显示
  - ~~[Template strings](https://docs.python.org/2/library/string.html#template-strings), 模板显示~~, 建议使用format代替.


## 使用正则表达式的一些例子

``` python
# 去掉所有的空格和tab
re.sub('[\s+]', '', str)

# 转换小写下划线格式变化为驼峰格式
re.sub('^\w|_\w', lambda x:x.group()[-1].upper(), 'blog_view') # 输出 'BlogView'。
```


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***