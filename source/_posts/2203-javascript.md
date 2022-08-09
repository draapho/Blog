---
title: JavaScript 基础
date: 2022-08-02
categories: web
tags: [web, JavaScript]
description: 介绍学习 JavaScript 的语法
---

# 参考资料
- [JavaScript 和 HTML DOM 参考手册](https://www.runoob.com/jsref/jsref-tutorial.html)
- [JavaScript 学习指南](http://c.biancheng.net/js/)
- [JavaScript 教程](https://www.runoob.com/js/js-tutorial.html)

# JavaScript 的特点和运行环境
- JavaScript 的特点:
    - 解释型脚本语言
    - 弱类型. 可随时改变变量的类型
    - 面向对象 / 动态型 / 跨平台
    - 最早只能运行在浏览器中, 现在Node.js提供了独立的运行环境
- JavaScript 开发所依赖的组件:
    - 解释器. 作用是将JavaScript边编译边运行.
    - 标准库. 提供 JavaScript 的常用函数和功能
    - 本地模块. 如 Cookie, Ajax, HTML DOM
- Node.js 包含了上述所有组件, 因而JavaScript可以独立运行于Node.js中
    - 解释器: 使用的是V8引擎.
    - 常见的开源库
        - libuv: 基于事件驱动的异步I/O库. 还提供了进程管理, 线程池, 信号处理, 定时器等功能
        - nmp: 包管理器
        - http_parser: 轻量级HTTP解析器
        - zlib: 提供压缩解压功能
        - Open SSL: 提供加密机密功能
        - c-ares: 异步DNS查询和解析库
    - 最大的特点: 采用了基于事件的、单线程的异步 I/O 架构. 这种能力是依赖Libuv库而实现的.
- JS严格模式: use strict
    - 最直观是会通过**抛出错误**来消除一些原有**静默错误**
    - 使用方法: 脚本文件开头, 或函数内第一行, 写为 `"use strict";` 就在相关作用域内启用了严格模式
    - 当代码写在 `class` 和 `module` 中时，默认就是严格模式, 所以可以省略该行语句.
    - 推荐使用严格模式, 因而语法的介绍上, 会忽略掉一些普通模式才有的特点, 如隐式全局变量


``` html
<!-- 在 HTML 文档中嵌入 JavaScript 代码示例: -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>第一个JavaScript程序</title>
    <script type="text/javascript">
        // javascript 通过script标签嵌入到html中
        document.write("Welcome to");
    </script>
</head>
<body>
    <script>
        // type 可以省掉, javascript 已经成为script的默认类型
        document.write("<h1>https://draapho.github.io/</h1>");
    </script>
</body>
</html>
```

# JavaScript 基础语法

## 变量的声明
- `var` ,常用的变量声明关键字. 由于过于灵活, 也产生了相关问题.
    - 变量提升问题. 声明可以写在最后, 但作用域为整个文件或函数.
    - 允许重复声明相同名称的变量.
    - 作用域不够规范, 在函数中的var声明, 其作用域是函数体的全部.
- `let` ,更安全的变量声明关键字. 于ES6推出
    - 没有变量提升问题. 会直接报错.
    - let 声明的变量作用域更小更明确, 拥有块级作用域.
    - let 禁止在同一作用域内, 重复声明变量.
- `const` ,就是用来定义常量的.
- JS是弱类型变量. 可随时改变变量的类型. 变量类型由赋值决定.

## 基本数据类型
- 判断数据类型:
    - `typeof(x)` 或 `typeof x`, 仅可获得 `number`, `boolean`, `string`, `function`, `object`, `undefined`
    - `x instanceof Array`, 返回 boolean 值. 多用来判断变量是否为 `Array` 数组
    - `instanceof` 只能用来判断对象和函数, **不能用来判断字符串和数字(会直接返回 false)**.
    - 即 `var b = 'abc'; console.log(typeof b, b instanceof String);`, 返回string, false.
    - 即 `var b = new String("123"); console.log(typeof b, b instanceof String);`, 返回object, true.
- 基本数据类型
    - string, 字符串. 使用单引号或双引号.
        - 切片(位置)操作: `.slice()`, `.substr()`, `.substring()`, `.charAt()`, `.charCodeAt()`
        - 根据内容的操作: `.trim()`, `.split()`, `.match()`, `.replace()`, `.concat()`
        - 获取位置: `.indexOf()`, `.lastIndexOf()`, `.search()`
        - 获取长度: `.length`; 从编码生成字符串: `.fromCharCode()`
        - 生成HTML代码: `.anchor()`, `.big()`, `.blink()`, `.bold()`, `.fixed()`, `.fontcolor()`,
        - `fontsize()`, `.italics()`, `.link()`, `small()`, `.strike()`, `.sub()`, `.sup()`
    - number, 数值. 范围: -(2^53 - 1) 到 (2^53 -1), 以及:
        - `Infinity`: 用来表示正无穷大的数值，一般指大于 1.7976931348623157e+308 的数；
        - `-Infinity`: 用来表示负无穷大的数值，一般指小于 5e-324 的数；
        - `NaN`: 即非数值（Not a Number 的缩写）, 数据类型是 number
    - boolean: ture 和 false, 全部小写.
    - undefined: 用var声明变量时, 自动初始化为 `undefined`
    - symbol: 转为独一无二的值. 多用于对象的属性
        - 赋值方法 `symValue = Symbol(attr)`
- 引用数据类型:
    - object, 对象类型, `{}`, 用法和概念类似于python的字典 dict
        - Null: 类型上属于 object, 空指针.
        - Array, 类型上属于 object.
        - date, 类型也属于 object.
        - new关键字, 创建一个对象或函数的实例.
    - array, 数组类型, `[]`, 类型上属于 object. 用法和概念类似于python的列表 list.
        - 数组转字符串: `.toString()`, `.toLocaleString()`, `.join()`
        - 栈与队列: `.push()`, `.pop()`, `.shift()`, `unshift()`, `reverse()`
        - 拼接与拆分: `.concat()`, `.slice()`, `.splice()`, `.fill()`, `[...str]`
        - 位置查找: `.indexOf()`, `.lastIndexOf()`, `.find()`, `.findIndex()`
        - 条件判断: `.includes()`, `.every()`, `.some()`
        - 遍历迭代: `.filter()`, `.map()`, `.forEach()`, `.reduce()`
        - for遍历: `.entries()`, `.keys()`, `.values()`
        - object转为array, `.from()`; 排序 `.sort()`
    - function 函数类型.
        - 基本形式: `function fun_name(input=defaultValue) {...}` 不需要声明输入输出类型.
        - 变量形式: `var fun_name = function(input=defaultValue) {...};` 注意最后的分号.
        - 匿名函数: `var person = {name: 'draapho', display: function() {console.log(this.name);}}`
        - 箭头函数: `elements.map((element) => {return element.length;});`, `()`为输入参数, `{}`为函数体.
- JSON 格式
    - object 与 JSON 格式尽管看起来很相似, 但它们是不同的数据类型.
    - JSON中, 所有的属性名必须用双引号; JS的object属性名可以用单引号或双引号.
    - `JSON.parse()`, 解析json语句, 将json转换为object类型
    - `JSON.stringify()`, 将 JavaScript 值转换为 JSON 格式
- String 对象中的属性
    - `constructor`: 获取创建此对象的 String() 函数的引用
    - `length`: 获取字符串的长度
    - `prototype`: 通过该属性可以向对象中添加自定义属性和方法

``` javascript
// 使用 prototype 属性
String.prototype.name = null;   // 新增name属性到prototype中
str.name = "名称";              // 赋值
document.write(str.name);       // 输出：名称
```

## JS运算符
- 算术运算符
  - 和c语言非常相似. 区别在于: `/`是除法, 整除需要用函数`parseInt`来实现,  `>>>` 无符号右移位运算并赋值
  - 支持连续赋值, 但个人不建议养成这个习惯. 譬如 python 用连续赋值就完全是另外一种含义.
- 字符串运算符
    - `+` `+=` 字符串拼接. Number + String 类型, 会自动将Number转化为String然后拼接
- 数字和字符串混合运算时的隐式转换:
    - `加号 +` 数字转为字符串. (字符串有 `+` 运算)
    - `减号 -` 字符串转为数字, 转换失败则赋值为 `NaN`. (字符串没有 `-` 运算)
    - `乘, 除运算` 也会先将字符串转换为数字. (字符串没有乘除运算)
- 比较运算符
    - `==` 仅比较数值, 如 24 == '24' 为真.
    - `===` 比较数值和类型, 两者都相同才为真
    - `!=` 仅比较数值 `!==` 比较数值和类型.
- 数据类型的强制转换:
    - `parseInt()`
    - `parseFloat()`
    - `Number()`
    - `Boolean()`
    - `String()` , `num.toString()`
    - `num.toExponential()` , `num.toFixed()` , `num.toPrecision()`


## JS语句
- JS 输出语句汇总
    - `alert()` 或 `window.alert()` 只能输出文本内容, 弹窗显示一个提醒.
    - `confirm()` 带返回值的弹窗. 确定返回true, 取消返回false
    - `console.log()` 在浏览器控制台输出信息, 多用于调试. (Chrome 按F12 选Console)
    - `document.write()` 向所在的HTML文档写入文本.
- 条件判断, 循环语句. 和c, python类似
    - `for (variable in object) {}` 遍历对象
    - `for (variable of iterable) {}` 遍历数组, 字符串等.
- 跳转语句
    - `break;` 普通跳转.
    - `break label;`  跳转到label, 相当于 goto
- 异常处理
``` JavaScript
try {
    var rtn = tgrue;                     // 故意拼写错误为 ture 时, 就会抛出异常
    throw new Error("主动抛出的异常");  // 主动抛出异常
} catch(e) {
    // 错误处理
    rtn = false;
    console.log(, e)                    // 打印错误信息, 供调试使用
} finally {
    // 无论出错与否, 都会运行此部分
    console.log(rtn)                    // 打印最终结果
}
```


## JS闭包
当一个函数包含着一个内部函数, 且这两个函数彼此嵌套, 内部的函数就是闭包.
闭包的主要作用是为了防止对象被回收, 保证一直保存在内存中.

```javascript
// 一个闭包的实例.
function funOutside(i){         // i 在funOutside中
    function funInside(){
        console.log('数字：' + i);  // funInside 调用了funOutside中的i
    }
    return funInside;           // funOutside 调用了 funInside, 完成闭包
};

var fa = funOutside(110);       // 创建多个闭包函数
var fb = funOutside(111);
fa();                           // 输出：数字：110
fb();                           // 输出：数字：111

// 实际应用, 将闭包与匿名函数结合使用
var funAdd = (function(){
    var num = 0;            // num 在funAdd中
    return function(){      // funAdd引用了匿名funciton, 即renturn, 完成闭包
        num++;              // 匿名funciton引用了funAdd中的num
        return num;
    }
})();                       // 注意最后的 (), 让funAdd指向了内部的 "return function"
console.log(funAdd());      // 输出：1
console.log(funAdd());      // 输出：2
```


# JavaScript 常用对象说明
- [Math 对象](http://c.biancheng.net/view/9358.html)
- [RegExp 对象](http://c.biancheng.net/view/9359.html), 正则表达式的两种创建方法
    - `var patt = new RegExp(pattern, modifiers);`
    - `var patt = /pattern/modifiers;`
- [JS DOM 对象](http://c.biancheng.net/view/9360.html), 文档对象模型.
    - 当浏览器加载HTML网页时, 会自动将HTML信息组织成一个逻辑树结构供JS使用.
        - 该结构树的根节点就是document, 使用方法: `document.attr` 和 `document.fun()`
        - `xxx.innerHTML` 表示获取或设置xxx标签的内容 / 值
    - [Element 对象](http://c.biancheng.net/view/9361.html), 元素对象
        - 使用JS DOM对象可以获取HTML中的特定Element对象.
        - 这些元素对象有一系列的属性和方法.
    - [attributes 对象](http://c.biancheng.net/view/9362.html), 元素属性对象.
        - 主要属性: `.isId`, `.name`, `.value`, `.specified`, `.length`
        - 主要方法: `item()`, `.getNamedItem()`, `.removeNamedItem()`, `.setNamedItem()`
- [JS BOM 对象](http://c.biancheng.net/view/9363.html), Browser Object Model 的缩写, 浏览器对象模型.
    - window, 即显示HTML的浏览器界面. 里面都是一些GUI方面的属性和方法. 如窗口大小, 像素移动移动等等.
        - 一个HTML文档就会创建一个window对象. 这个window是一个全局对象.
        - 如果文档中包含`<frame>`或`<iframe>`, 则会为每个frame创建一个独立的window对象
        - BOM属性的调用 `window.xxx`; BOM方法可省去window, 直接用函数名, 如 `alert()`
    - [Navigator 对象](http://c.biancheng.net/view/9364.html), 获取浏览器信息
        - navigator 来自于`window.navigator`, 调用时经常省掉window, 直接使用 `navigator`
        - 可获取浏览器的名称, 版本, 操作系统, 是否启用了cookie, 是否支持java.
    - [Screen 对象](http://c.biancheng.net/view/9366.html), 获取屏幕信息, 如宽度高度, 分辨率, 色深等等.
    - [Location 对象](http://c.biancheng.net/view/9366.html), 获取HTML的URL信息
    - [History 对象](http://c.biancheng.net/view/9367.html), 获取浏览历史信息
- [JS 定时器](http://c.biancheng.net/view/9368.html
    - `setTimeout(fun, delay, arg1, arg2, ...)`, 延时指定毫秒后, 调用fun函数. 只会执行一次
    - `clearTimeout()`, 关闭setTimeout的定时器.
    - `setInterval(fun, delay, arg1, arg2, ...)`, 按照指定的毫秒周期, 重复调用fun函数. 不会自动停止.
    - `clearInterval()`, 关闭setInterval的定时器.




# JavaScript 交互示例
## js event 事件处理
- 主要分为四类.
    - 鼠标事件: `onclick`, `ondbclick`, `onmousedown`, `onmouseup`, ...
    - 键盘事件: `onkeypress`, `onkeydown`, `onkeyup`
    - 表单事件: `onblur`, `onchange`, `onfocus`, `onreset`, `onsubmit`
    - 窗口事件: `onload`, `onmove`, `onresize`, `onscroll`, `onstop`, ...
- 这是比较标准化的UI操作接口. 有两种绑定方式:

``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>JavaScript</title>
</head>
<body>
    <button type="button" onclick="clickBtn()">按钮</button>  <!-- HTML内 onclick 事件绑定函数 clickBtn -->
    <button type="button" id="idBtn">按钮</button>            <!-- 此处不绑定, 只是定义一个 idBtn -->
    <script>
        function clickBtn(){
            alert("onclick HTML绑定");
        }
        function sayHello() {
            alert('Hello World!');
        }
        document.getElementById("idBtn").onclick = sayHello;   // js 代码内 onclick 事件绑定函数 clickBtn
    </script>
</body>
</html>
```


- 事件捕获和事件冒泡
    - 如果给每个标签都定义事件, 触发目标节点时, 途径的各个父级节点都会被触发.
    - 从根节点一路触发到目标节点, 称之为`事件捕获`
    - 从目标节点一路触发到根节点, 称之为`事件冒泡`
    - 由于不是GUI设计和操作的本意, 这种特性并不友好.

![事件捕获和事件冒泡](https://draapho.github.io/images/2203/event.png)


- 阻止事件的方法
    - `event.stopPropagation();`, 阻止事件捕获和冒泡. 但无法阻止标签的默认行为.
    - `event.stopImmediatePropagation();`, 阻止同一节点上的其它事件
    - `event.preventDefault();`, 阻止默认操作
- [事件委托](http://c.biancheng.net/view/9380.html)
    - 子元素上的事件委托给父元素来监听. 父元素监听到冒泡事件后, 在找到这个子元素执行事件.
    - 多用于表格和列表的事件, 使用事件委托能减轻工作量, 提高页面性能.
    - 本质是一种观察者模式


## JS表单验证和动画效果示例

- [JS表单验证(附带示例)](http://c.biancheng.net/view/9370.html)
    - 表单验证通常由两个部分组成:
    - 必填字段验证: 确保必填的字段都被填写
    - 数据格式验证: 确保所填内容的类型和格式是正确, 有效的.
- [JS动画效果的实现(附带示例)](http://c.biancheng.net/view/9371.html)
    - JavaScript 主要通过代码修改 DOM 元素来实现动画的, 并且配合定时器来实现循环播放
    - 大多数显示器的刷新率为 60HZ, 为了实现更加平滑的动画效果, 使用定时器的最佳循环间隔约为 17ms


## JS 对cookie的操作
- Cookie 由若干个键/值对组成, 一个 Cookie 最大可以存储 4kb 的数据, 超过长度的 Cookie 将被忽略.
    - 形式为 `key1=value1;key2=value2;...`
- Cookie 数据中不能包含分号, 逗号或空格
- Cookie 没有所谓的修改, 更新, 删除. 唯一能做的就是对同名 Cookie再赋值
- 通过`document.cookie` 属性对 Cookie 赋值
- 使用内置的 `encodeURIComponent()` 函数对 cookie 数据进行编码
- 在读取 Cookie 时, 使用对应的 `decodeURIComponent()` 函数来解析


```javascript
/**
* 添加 Cookie 函数
* @param {[string]} name       [Cookie 的名称]
* @param {[string]} value      [Cookie 的值]
* @param {[number]} daysToLive [Cookie 的过期时间]
*/
function setCookie(name, value, daysToLive) {
    // 对 cookie 值进行编码以转义其中的分号, 逗号和空格
    var cookie = name + "=" + encodeURIComponent(value);

    if(typeof daysToLive === "number") {
        /* 设置 max-age 属性 */
        cookie += "; max-age=" + (daysToLive*24*60*60);
    }
    document.cookie = cookie;
}

function getCookie(name) {
    // 拆分 cookie 字符串
    var cookieArr = document.cookie.split(";");

    // 循环遍历数组元素
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");

        /* 删除 cookie 名称开头的空白并将其与给定字符串进行比较 */
        if(name == cookiePair[0].trim()) {
            // 解码cookie值并返回
            return decodeURIComponent(cookiePair[1]);
        }
    }
    // 如果未找到，则返回null
    return null;
}
```


## JS Ajax请求
- Ajax 全称“Asynchronous JavaScript and XML”, 异步从服务器请求数据并将数据更新到网页中, 避免重载整个网页.
- 主要流程如下:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>
    function loadXMLDoc()
    {
        // 1. 创建 XMLHttpRequest 对象
        var request = new XMLHttpRequest();
        // 2. 监听 readyState 的变化
        request.onreadystatechange = function()
        {
            if (request.readyState==4 && request.status==200)
            {
                // 5. 最后, 将来自服务器的响应插入当前页面
                document.getElementById("myDiv").innerHTML=request.responseText;
            }
        }
        // 3. 实例化请求对象, 调用网络数据库或文件, 此处略.
        request.open("GET","https://draapho.github.io/images/2203/ajax_test.txt");
        // 4. 将请求发送到服务器
        request.send();
    }
    </script>
</head>
<body>
    <div id="myDiv"><h2>使用 AJAX 修改该文本内容</h2></div>
    <button type="button" onclick="loadXMLDoc()">修改内容</button>
</body>
</html>
```

# 开源库及TypeScript
- 引用库的方法: `<script src=xxx></script>`, xxx为开源库URL地址
- 框架类:
    - 框架类库需要专门的搭建过程, 请参考相关库的说明文档
    - 运行环境: `Node.js`,
    - MVC框架: `vue.js`, `React.js`
- 基础操作类:
    - DOM 操作: `jQuery`, 语法与CSS非常相似
    - 日期: `Moment.js`, `Date.js`
- 数据相关:
    - 数据可视化: `Chart.js`
    - 数据处理: `D3.js`
    - 数据库: `TaffyDB`
- GUI炫酷:
    - 动画: `Anime.js`
- [`TypeScript`](https://www.typescriptlang.org/)
    - TypeScript 是添加了类型系统的 JavaScript, 适用于任何规模的项目.
    - TypeScript 是一门静态类型, 弱类型的语言.
    - TypeScript 是完全兼容 JavaScript. 可以编译为JavaScript运行.
    - TypeScript 拥有很多编译选项, 类型检查的严格程度由你决定
    - TypeScript 增强了编辑器(IDE)的功能, 提供了代码补全, 接口提示, 跳转到定义, 代码重构等能力.


# [`vue.js`](https://staging-cn.vuejs.org/)
- [Vue3 简介](https://staging-cn.vuejs.org/guide/introduction.html)
- [搭建环境](https://staging-cn.vuejs.org/guide/quick-start.html)
- [入门教程](https://staging-cn.vuejs.org/tutorial/#step-1)


# 参考资料
- [JavaScript 学习指南](http://c.biancheng.net/js/)
- [JavaScript 教程](https://www.runoob.com/js/js-tutorial.html)
- [JavaScript 和 HTML DOM 参考手册](https://www.runoob.com/jsref/jsref-tutorial.html)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
