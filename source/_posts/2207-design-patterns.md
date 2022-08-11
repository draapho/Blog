---
title: 设计模式概要
date: 2022-08-11
categories: software
tags: [interview, software, OOP]
description: 23种设计模式的简单总结
---

# 总览
- [逻辑|这样表达，事半功倍](https://draapho.github.io/2017/05/04/1714-expression/)
- [面试之常规问题](https://draapho.github.io/2018/01/10/1805-interview-general/)
- [面试之嵌入式C语言](https://draapho.github.io/2018/05/07/1816-interview-c/)
- [C语言知识巩固](https://draapho.github.io/2017/05/17/1715-c/)
- [面试之嵌入式Linux](https://draapho.github.io/2018/05/08/1817-interview-linux/)
- [面试之面向对象](https://draapho.github.io/2022/08/10/2206-interview-oop/)
- [设计模式概要](https://draapho.github.io/2022/08/11/2207-design-patterns/)


# OOPs 的设计原则
- 单一职责原则, SRP原则 (Single responsibility principle)
    - 高内聚, 低耦合. 自己能做的, 就不麻烦别人.
    - 每个类应该只有一个职责. 对外只能提供一种功能. 而引起类变化的原因应该只有一个.
- 开闭原则, ocp原则 (open closed principle)
    - 一个对象对扩展开放, 对修改关闭
    - 对类的改动应该通过增加代码实现, 而不是修改现有的代码.
- 里氏替换原则, LSP原则 (Liskov Substitution principle)
    - 在任何父类出现的地方都可以用它的子类来替代
    - 即: 同一个继承体系中的对象, 应该有共同的行为特征
- 依赖注入原则, DI原则 (Dependency Injection)
    - 要依赖于抽象, 不要依赖于具体的实现
    - 要求我们在编程的时候针对抽象类或者接口编程, 而不是针对具体的实现编程
- 接口分离原则, ISP原则 (Interface Segregation Principle)
    - 不应该强迫程序依赖他们不需要的方法. 
    - 即: 一个接口应该只提供一种对外的功能. 不应该把所有的操作都封装到一个接口中
- 迪米特原则 (Law of Demeter)
    - 最少知识原则. 一个类对于其他类知道的越少越好.
    - 类比: 只和朋友通信, 不和陌生人说话
    - 降低个个对象间的耦合, 提高系统的可维护性.
- 总结: **高内聚, 低耦合, 可复用**


# 设计模式简介
- 创建型模式 Creational Pattern
    - 对类的实例化过程进行了抽象, 能够将软件模块中对象的创建和对象的使用分离.
    - 5种: **工厂模式、抽象工厂模式、单例模式、建造者模式**、原型模式
    - 记忆口诀: 创工原单建抽 (创公园, 但见愁)
- 结构型模式 Structural Pattern
    - 关注于对象的组成以及对象之间的依赖关系, 描述如何将类或者对象结合在一起形成更大的结构.
    - 就像搭积木, 可以通过简单积木的组合形成复杂的, 功能更为强大的结构.
    - 7种: **适配器模式、装饰者模式、代理模式**、外观模式、**桥接模式**、组合模式、享元模式
    - 记忆口诀: 结享外组适代装桥 (姐想外租, 世代装桥)
- 行为型模式 Behavioral Pattern
    - 关注于对象的行为问题, 是对在不同的对象之间划分责任和算法的抽象化
    - 不仅仅关注类和对象的结构, 而且重点关注它们之间的相互作用.
    - 11种: **策略模式、模板方法模式、观察者模式、迭代器模式、责任链模式**、命令模式、备忘录模式、**状态模式**、访问者模式、中介者模式、解释器模式
    - 记忆口诀: 行状责中模访解备观策命迭 (形状折中模仿, 戒备观测鸣笛)



|        | Creational 创建型         | Structural 结构型       | Behavioral 行为型              |
|--------|---------------------------|-------------------------|------------------------------|
| Class  | Factory Method 工厂方法   | Adapter (class) 适配器  | ~~Interpreter 解释器~~         |
| Class  |                           |                         | Template Method 模板方法       |
| Object | Abstract Factory 抽象工厂 | Adapter (object) 适配器 | Chain of Responsibility 责任链 |
| Object | Builder 建造者            | Bridge 桥接             | ~~Command 命令~~               |
| Object | ~~Prototype 原型~~        | ~~Composite 组合~~      | Iterator 迭代器                |
| Object | Singleton 单例            | Decorator 装饰器        | ~~Mediator 中介者~~            |
| Object |                           | ~~Facade 外观~~         | ~~Memento 备忘录~~             |
| Object |                           | ~~Flyweight 享元/共享~~ | Observer 观察者                |
| Object |                           | Proxy 代理              | State 状态                     |
| Object |                           |                         | Strategy 策略                  |
| Object |                           |                         | ~~Visitor 访问者~~             |


# UML类图

| 类型           | 图标                 | 含义                                                  |
|----------------|----------------------|-----------------------------------------------------|
| 泛化（继承）     | A ◁————— B           | B **继承(is)** A, 即B是A的子类.                       |
| 实现           | A ◁- - - - - - - -B  | B **实现(realizes)** A 接口                           |
| 依赖           | A - - - - - - - - >B | B 作为 A 某个方法的参数. 两者强关联.                  |
|                |                      | A **依赖/需要** B, 不然无法完成特定的事情.            |
| 关联           | A ——————>B           | B 作为 A 的某种属性存在, 两者弱 **关联**              |
|                |                      | 如 人(A) 住 房子(B). 但人和房子是没什么共性的独立事物 |
| 聚合           | A ♢—————>B           | 语义上 B 可作为 A 的一部分, 但 B 可以独立存在         |
|                |                      | A **has** B 的关系. 如房子(A), 桌子(B)                |
| 组合           | A ♦—————>B           | 语义上 B 是 A 的一部分, 但 B 无法独立存在.            |
|                |                      | A **owns** B 的关系, 如人(A), 大脑(B)                 |
| 对应关系的数量 | A m..n B             | B最多和m个数量的A有关系, A最多和n个数量的B有关系      |

![uml_example](https://draapho.github.io/images/2207/uml.png)


# 参考资料
- [Design Patterns](https://cs.lmu.edu/~ray/notes/designpatterns/), 简单的归纳总结.
- [What’s a Software Design Pattern? (+7 Most Popular Patterns)](https://www.netsolutions.com/insights/software-design-pattern/), 介绍了7种最常用的设计模式. 并介绍了软件架构(MVC, MVP, MVVM)
- [Design Patterns](https://www.oodesign.com/), 详细地介绍了所有23种设计模式.
- [快速记忆23种设计模式](https://zhuanlan.zhihu.com/p/128145128)
- [设计模式简介 - 菜鸟教程](https://www.runoob.com/design-pattern/design-pattern-intro.html)
- [图文详解 23 种设计模式](http://dockone.io/article/2434385)
- [UML图标含义与图例](https://blog.csdn.net/huaishu/article/details/108343852)
- [设计模式前篇之：UML类图必会知识点](https://www.jianshu.com/p/fcb642ff3be5)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
