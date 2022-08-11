---
title: 面试之面向对象
date: 2022-08-10
categories: interview
tags: [interview, OOP]
description: 系统学一下OOP英文面试表述
---

# 总览
- [逻辑|这样表达，事半功倍](https://draapho.github.io/2017/05/04/1714-expression/)
- [面试之常规问题](https://draapho.github.io/2018/01/10/1805-interview-general/)
- [面试之嵌入式C语言](https://draapho.github.io/2018/05/07/1816-interview-c/)
- [C语言知识巩固](https://draapho.github.io/2017/05/17/1715-c/)
- [面试之嵌入式Linux](https://draapho.github.io/2018/05/08/1817-interview-linux/)
- [面试之面向对象](https://draapho.github.io/2022/08/10/2206-interview-oop/)
- [设计模式概要](https://draapho.github.io/2022/08/11/2207-design-patterns/)

# OOPs 的基本概念
- What is OOPs
    - OOPs refers to Object-Oriented Programming. 
    - **Class** is an abstract/virtual template/blueprint/idea to create instance of objects.
    - Class can contain **attributes** and **methods**(functions)
    - **Objects** are instances of classes created with specific data.
    - Class do NOT use any memory. When create objects needs memory.
- Why OOPs
    - For big projects, OOPs have lots of advatage than *Procedural Programming*
    - Thanks to **Class**, make complex things as *reproducible*(可重现的), *simple structures*.
    - Thanks to **Inheritance**, make code easier to *reuse* and *maintain*.
    - Thanks to **Encapsulation**, make code *secure* and easier to *understand* and *maintain*
    - Thanks to **Abstraction**, make code *simple* and *secure* and easier to *maintain*
    - Thanks to **Polymorphism**, make code, easier to *reuse* and *understand*
- Features or Principles
    - **Inheritance**(继承): *child classes* inherit data and behaviors from *parent class*
    - **Encapsulation**(封装): containing all information in an object, exposing only selected information
    - **Abstraction**(抽象): only exposing public methods for accessing an object
    - **Polymorphism**(多态性): many methods can do the same task

# 更多的细节
- types of Polymorphism(多态性)
    - **Compile Time Polymorphism**(编译时多态) / **Static Polymorphism**(静态多态): 
        - the type Polymorphism that happens at compile time
        - So the compiler decides which methods to be called
    - **Runtime Polymorphism**(运行时多态) / **Dynamic Polymorphism**(动态多态):
        - the type of Polymorphism that happens at the run time
        - use it when the compiler can NOT choose right methods by parameters.
- How C++ support Polymorphism
    - For Static Polymorphism: based on *templates*, *function overloading* and *default arguments*
    - For Dynamic Polymorphism: based on *virtual functions*
- Is it always necessary to create objects from class?
    - No, if class including *static* attributes or static methods, can use these attributes and methods directly.
- What is a **constructor** (构造函数)?
    - Constructors are special methods whose name is the same as the class name.
    - The purpose is *instantiate* the class and do some init jobs.
- various types of **constructors** in C++
    - *Default constructor*: constructor without any parameters.
    - *Parameterized constructor*: constructor's parameter with some arguments.
    - *Copy constructor*: constructor's parameter with onther object of the same class.
- What is a **destructor** (解构函数)?
    - destructors *free up the resources and memory* occupied by an object
    - Destructors are *automatically called* when an object is being destroyed.
- Different between **class** and **structure**(结构体)
    - class is saved in the heap memory
    - structure is saved in the stack memory
    - structure has NO data abstraction.
- any limitations of **Inheritance**?
    - needs more time to process.
    - the base class and the child class, are very *tightly coupled* (紧密耦合)
    - in some case,  Inheritance might be *complex for implementation*
- Types of **inheritance**
    - Single inheritance (单继承, 父类子类两代)
    - Multiple inheritances (多重继承, 1个子类多个父类)
    - Multi-level inheritance (多级继承, 三代)
    - Hierarchical inheritance (分层继承, 1个父类多个子类)
    - Hybrid inheritance (混合继承)
- Name in **inheritance**
    - child class, subclass, derived class
    - parent class, superclass, base class
    - **interface**: special type of class
        - only allowed methods declaration, No definition.
        - can NOT create objects for interface.
        - you need to implement interface and define methods for their implementation
- Overloading vs Overriding
    - **Overloading** is a compile-time polymorphism feature.
    - Example: Method overloading and Operator overloading
    - **Overriding** is a runtime polymorphism feature.
    - Example: Method overriding
- **abstract class**(抽象类) vs **interface**
    - 相同点: 都是特殊的类. 都不能实例化, 都包含抽象的方法.
    - special types of classes. contain only the methods declaration. can NOT be an object directly.
    - 主要区别: 实现接口时, 必须定义和实现所有方法. 继承抽象类时, 子类可以不定义其抽象方法.
    - when an interface is implemented, the subclass must define all its methods and provide its implementation.
    - when an abstract class is inherited, the subclass does not have to provide the definition of its abstract method
- What are **access specifiers**(访问说明符)
    - a special type of keywords, inlcude *private*, *public*, etc
    - to achieve **Encapsulation**
- What is Garbage Collection in OOPs world
    - Each object consumes memory when it created from class.
    - **Garbage collection** is a mechanism of handling the memory in the program.
    - Garbage collection will free up memory when objects are no longer needed


# 参考资料
- [40+ OOPs Interview Questions](https://www.interviewbit.com/oops-interview-questions/)
- [What is object-oriented programming? OOP explained in depth](https://www.educative.io/blog/object-oriented-programming)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
