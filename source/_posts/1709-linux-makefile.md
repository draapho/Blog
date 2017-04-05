---
title: 快速读懂 makefile
date: 2017-04-04
categories: linux
tags: [embedded, linux, makefile]
---

***转载自 [怎么看懂和编写makefile](http://lucky521.github.io/blog/design/2015/10/01/makefile.html)***

----------

# Makefile最基本的组成

``` makefile
target: dependencies
[TAB] command

目标: 依赖1 依赖2
[TAB] 命令
```
- `target` 可以是object文件，也可以是可执行文件，也可以是target关键字。
   可以一次写多个文件作为同一批次的target。
- `dependencies` 有的是源文件，有的是链接文件，如果没有的话可以不写；
   想要编target必须先准备好dependencies。
- `clean` 是一个特殊的target，一般要做的是rm清理工作；
- `make`命令在执行的时候会检查目标文件是否存在, 并比较target文件和dependencies文件的修改日期，
  如果存在更新的dependencies文件，那么对应的command就会执行，否则的话就不执行，还使用已存在target文件。
- `command` 必须要以`TAB`来对齐， 一般会是gcc/g++的编译命令；
- 细化到模块一般会有若干个分支target，形成层级的target依赖关系。


举个例子:
``` makefile
# 编译和链接一起做了, 看不到中间的.o目标文件
hello: hello.c a.c
    gcc -o hello hello.c a.c


# 对于大型系统, 更推荐的是编译和链接分开, 如下:
hello: hello.o a.o                  # 可执行文件hello 依赖于 hello.o 和 a.o
    gcc -o hello hello.o a.o        # 执行链接

hello.o: hello.c                    # 目标文件依赖于hello.c
    gcc -o hello.o -c hello.c       # 编译出目标文件

a.o : a.c                           # 另一个目标文件
    gcc -o a.o -c a.c               # -o: object 目标文件, -c: compile 编译
```

# 隐形规则和变量

为了使得makefile的内容尽量少一些废话，GNU为makefile加入了一些约定的规则。
- 如果`target`文件的名称是`aa.o`，那么make会主动的把同名的源代码文件（如`aa.c`,`aa.cpp`）加入到依赖中去。
- `target` 和 `dependencies` 处: 用 `%` 通配任意的非空字符串
- `command` 处: `$@`目标文件, `$<`依赖1, `$^`所有的依赖文件, `$?`比目标文件新的依赖. 这三个叫自动变量.
- 变量在定义或被赋值时不加$()，在使用其值时要加 `$()`
- 常用`$(CC)`来代替具体的编译器，比如 `CC=g++`
- 常用`$(CFLAGS)`来代替C语言编译选项，比如 `CFLAGS=-c -Wall`
  还会指定头文件include路径，比如 `CFLAGS+=-I/usr/include`
- 常用`$(LDFLAGS)`来指定库文件lib路径，比如 `LDFLAGS+=-L/usr/lib`
- 常用`$(LDLIBS)`来指定要链接的库名称，比如 `LDLIBS+=-llibname`


修改上面的例子:
``` makefile
# 先使用通配符 % 及自动变量
hello: hello.o a.o
    gcc -o $@ $^                    # $@ 表示hello, $^ 表示两个.o文件

%.o : %.c                           # 对应了hello.o 和 a.o 两条语句!
    gcc -o $@ -c $<                 # $@ 表示 .o 文件, $< 表示第一个依赖, 即 .c 文件

# 然后使用更多的变量 $()
hello: hello.o a.o
    $(CC) -o $@ $^                  # CC=gcc, 因此 $(CC)表示gcc

%.o : %.c                           # 使用更多的编译参数变量
    $(CC) -o $@ -c $(CFLAGS) $(CPPFLAGS) $<
```

# 伪目标
`.PHONY` 经常被用来作为伪目标。 它的使用目的是这样的：
因为当类似clean这样的target关键字作为target并且没有依赖文件时，
假如目录下有一个文件也叫clean时，make clean命令则会以为我想编clean这个目标文件，
恰好clean文件又不会比依赖文件更旧，所以下面的command就不会被执行。

现在我们用.PHONY作为target，clean作为依赖。
这就是告诉make，clean它是一个target，而不是一个普通的文件。


加入 clean 的例子:
``` makefile
hello: hello.o a.o                          # 执行文件hello, 依赖于.o文件
    $(CC) -o $@ $^                          # 进行链接

%.o : %.c                                   # 目标文件.o 依赖于同名的.c文件
    $(CC) -o $@ -c $(CFLAGS) $(CPPFLAGS) $< # 编译出目标文件

.PHONY: clean
clean:                                      # 目标指令, 可调用 make clean 来执行了!
    rm -rf *.o                              # 删除所有的.o文件
```

# 文件引用和条件判断

- 如果makefile中引入其他makefile， 使用 `include` 即可
- 条件语句的基本结构一般由 `ifeq` `else` `endif` 三个关键字组成


``` makefile
include another.mk                          # 调用 another.mk
include foo *.mk $(bar)                     # 更复杂的调用


libs_for_gcc = -lgnu                        # 变量赋值
normal_libs =

ifeq ($(CC),gcc)                            # 条件判断 $(CC) 是否为gcc
    libs=$(libs_for_gcc)                    # 变量赋值
else
    libs=$(normal_libs)
endif

foo: $(objects)                             # 目标: 依赖
ifeq ($(CC),gcc)
    $(CC) -o foo $(objects) $(libs_for_gcc) # 执行的命令
else
    $(CC) -o foo $(objects) $(normal_libs)
endif
```



----------

***转载自 [怎么看懂和编写makefile](http://lucky521.github.io/blog/design/2015/10/01/makefile.html)***

