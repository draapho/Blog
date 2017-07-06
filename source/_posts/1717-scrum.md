---
title: 敏捷开发 Scrum 学习
date: 2017-05-31
categories: software
tags: [scrum]
---

# 学习资源推荐

- [Scrum Training Series](http://scrumtrainingseries.com/), 通俗易懂的视频教程
- [Scrum Reference Card](http://www.scrumreferencecard.com/), Scrum 参考卡
- [The Scrum Master Checklist](http://scrummasterchecklist.org/), Scrum Master 职能清单
- [The Scrum Guide™](http://www.scrumguides.org/download.html), Scrum 指导手册下载 (多国语言)
- 测试. 建议测试完后, 再看一下 [Scrum Training Series](http://scrumtrainingseries.com/) 视频
    - [Scrum Assessment](https://www.proprofs.com/quiz-school/story.php?title=mte3mjcynamkcf)
    - [Scrum (Programming) Quiz](https://www.proprofs.com/quiz-school/story.php?title=quizscrum)
    - [Certified Scrum Master Test](https://www.proprofs.com/quiz-school/story.php?title=certified-scrum-master-test)
    - [Scrum Training Series, Part 1: Introduction To Scrum](https://www.proprofs.com/quiz-school/story.php?title=NjAyMjg5#)
    - [Scrum 30题](https://www.proprofs.com/quiz-school/story.php?title=NzA4NjI0OO75)


# Scrum 核心点概要

![Sprint](https://draapho.github.io/images/1717/Sprint.JPG)


## 敏捷开发宣言
- **Individuals and interactions** over processes and tools
- **Working software** over comprehensive documentation
- **Customer collaboration** over contract negotiation
- **Responding to change** over following a plan

## Scrum Team Roles

- **Product Owner**, 产品负责人
  1. 核心工作是确定产品需求, 确定产品是否可接受/可发布. 并确保研发团队专注于该产品的开发(挡住干系人对研发团队可能的干扰)
  2. 管理和维护 `PBI`, 并设定优先级.
  3. 确保 `PBI` 对整个团队清晰可见, 高度透明, 并清楚的知道最高优先项.
  4. 需要与第三方(利益相关者/老板/客户)确定需求, 接纳或拒绝新需求.
  5. 第三方只能和产品负责人讨论产品进度/好坏之类的问题, 甚至发牢骚. 不得直接干预研发团队!
  6. 一般地, 此职位可由项目经理担任. 需要特别注意公司老板不得越过项目经理去分配任务!
  7. 产品负责人只需要粗颗粒的拆分一下需求, 更细粒度的拆分由研发团队一起完成.
  8. **Focused more on the what than on how**. 侧重于要产品实现什么, 而不是怎么实现的问题.
  9. 仅对产品负责, 并不是研发团队的管理人员! Scrum 要求研发团队自我管理.
- **Development Team**, 研发团队
  1. 产品的技术实现团队, 由4-9人组成较为合适. 譬如 UI设计师x1, 行业专家x1, 软件开发x2, 测试x1.
  2. 跨职能, 职责包括需求分析和拆解, 设计, 编码, 测试以及部署.
  3. 团队成员自我组织和管理, 高度协作. 相互平等, 没有领导者!
  4. 整个团队最好在一起工作, 可以大大提高效率.
  5. 在 `Sprint Planning Meeting` 上, 把 `PBI` 拆解为 `Sprint Tasks` 放在 `Sprint Backlog` 一栏.
  6. 以 `Sprint` 为周期, 都要尽可能的完成一个可演示/可发布的产品版本.
- **Scrum Master**, Scrum大师 (被误解最多的一个职位)
  1. Scrum的起步很困难, 因此有了Scrum大师来帮助整个团队理解Scrum的理论, 实践方式, 以及内在精神. 排除实践过程中可能走得弯路.
  3. Scrum大师没有任何决策权, 也不是一个管理岗位. 主要作用就是帮助团队学习使用Scrum框架, 消除误解, 排除干扰和障碍.
  2. 这个角色的初衷, 类似于婴儿学步阶段需要有个引导者, 这样可以学的快, 少摔跤. 但没有这个角色, 并不是说就学不会走路了.
  3. 实际项目中, 很少有团队会去请一个Scrum大师... 因此这个职位可以被分解为两部分: 理解Scrum, 严格执行Scrum的实践要求.
  4. Scrum的理论和精神已经摆在那里, 因此可以团队成员一起学习讨论, 在实践中进行案例分析, 自学之.
  5. 严格执行Scrum的实践, 主要包括: 建立一个舒适的会议环境, 安排和控制会议时间, 确保会议内容仅与项目相关. 建议找一个项目之外的人来做.


## The Sprint
- `Sprint` 是Scrum的核心, 时间跨度为2周到一个月.
- `Sprint` 由 `Sprint Planning`, `Daily Scrums`, 开发工作, `Sprint Review`, `Sprint Retrospective` 组成
- 一个 Sprint 周期内, 可以看成是一个完整的瀑布模式:
  - 不能改变设定的目标
  - 必须有测试, 不能降低检测标准
  - 目标实现的范围可以和 `Product Owner` 重新讨论和确定
  - 最终实现一个可用的, 完全测试过的, 可潜在发布的软件版本.
- 仅`Product Owner` 有权取消一个 `Sprint`. 很少出现这种情况, 写在这里只是为了明确职责.
- `Done`的定义
  - Scrum团队的每个人都清除的知道 `Done` 意味着什么.
  - `Done` 可以是大家共同理解的惯例, 标准或指南
  - `Done` 也可以由 `Development Team` 在 `Sprint Planning Meeting` 上确定.

## Scrum Meetings

![meeting_flow](https://draapho.github.io/images/1717/meeting_flow.JPG)

![meeting_schedule](https://draapho.github.io/images/1717/meeting_schedule.JPG)

- **Backlog Refinement Meeting** PBI修整会议
  1. 所有Scrum人员参与, 可以在每个Sprint执行过程中拿出点时间(如2小时)进行一次, 为下一次的 `Sprint Planning` 做准备
  2. 主要任务是将部分高优先级的粗颗粒`PBI`分解为细颗粒 `PBI`, 并确定对`Product Owner`而言何为 `Done`
  3. 细化程度为 [**INVEST**: Independent, Negotiable, Valuable, Estimable, Small, Testable 或 **SMART**: Specific, Measurable, Achievable, Relevant, Time-boxed](http://xp123.com/articles/invest-in-good-stories-and-smart-tasks/), 以及 **3W**: Who, What, Why
- **Sprint Planning Meeting** 计划会议
  1. 所有Scrum人员参与. 时间控制在4-8小时左右.
  2. `Sprint Planning` 需要确定在一个`Sprint`周期内, 做什么以及怎么做.
  3. `Product Owner` 维护 `PBI` 的优先级. 每次总是讨论最高优先级的 `PBI`
  4. `Product Owner` 不应对 `Development Team` 施加进度压力. 产品开发复杂度远大于外行的想象, 直接干预容易在后期造成技术负债.
  5. `Development Team` 确定何为 `Done`. 需要特别注意还要考虑代码的向后兼容性, 必要时甚至重构.
  6. `Development Team` 进一步拆分 `PBI` 为 `Sprint Task`, 并认领这些任务.
  7. `Development Team` 需要相互协作和评估, 设定在一个 `Sprint` 周期内可完成的目标.
     初期, 开发人员容易接受过多的任务, 而不是过少的任务. 这会导致一个 `Sprint` 内无法完成承诺的任务!
     注意, 这里不单是指编码工作, 还包含了设计, 代码重构, 完整的测试, 以及潜在的发布, 是一整个瀑布开发的模式.
- **Daily Scrum Meeting** 日会
  1. 每天同一时间, 同一地点, `Development Team` 花费15分钟相互报告情况.
  2. 内容为: 昨天做了什么, 今天要做什么, 是否遇到障碍. 这样可确保任务透明, 成员自律而高效.
  3. 站着开会, 以保持会议简短. 如果有额外需要关注的话题, 在该会议结束后, 相关人员参与即可.
  4. `Product Owner` 可以选择参与. 但团队的领导或主管不要参与!
  5. 日会讨论时, 可能会讨论出其他不相干的话题(sidebar), 则可以日会后仅相关人员参与. 不要占用日会时间.
- **Sprint Review Meeting** 评审会议
  1. 一个`Sprint`周期到达后, 就需要开评审会议, 以确定成果. `Development Team` 展示一个可潜在交付的软件版本.
  2. 所有Scrum人员, 以及干系人都可以参加, `Development Team` 进行现场演示以获得干系人的反馈 (不是写文案做报告).
  3. `Product Owner` 逐条检查在 `Sprint Backlog` 里的 `PBI`, 宣布哪些`Done`, 哪些没有完成(即将完成也是没完成!). 
  4. `Product Owner` 将没完成的 `PBI` 放回 `Product Backlog`, 重新设定优先级
  5. `Product Owner` 配合干系人, 将他们新的意见转换为需求, 放入 `Product Backlog`, 设定优先级
- **Sprint Retrospective Meeting** 回顾会议
  1. 所有Scrum人员参与, 可以放在`Sprint Review Meeting` 之后, 花费1-3小时.
  2. 回顾上一个 Sprint 执行过程中的经验得失 (譬如交流是否顺畅, 开发工具的使用, 学习心得) . 是否有改进余地.
  3. `Scrum Master` 需要引导与会人真实的表达了自己的想法, 达到解决障碍和问题, 改进流程的目的. 
  4. 回顾会议不是为了评估谁好谁坏, 决定日后如何分配奖金. 追求的是共同进步, 一起完成项目, 追求团队的成功.
  5. 这一部分, 我理解的不是很好.


## Scrum Artifacts
- **Product Backlog**
  1. 一个展示区, 用于展示项目所期望的功能, 可以随时增减. 说明要做什么(开发目标)
  2. 所有干系人可见, 所有干系人(包括团队)均可添加条目
  3. `Product Owner` 持续地按优先级在 `Product Backlog` 区域排列 `PBI`
  4. 顶部为细颗粒`PBI`, 底部为粗颗粒`PBI`.
- **Product Backlog Item**, 简称`PBI`
  1. 由 `Backlog Refinement Meeting` 分解条目, 安排优先级.
  2. `PBI` 通常写成 `User Story`, 工作规模控制在 2-3个人工作2-3天可完成.
- **Sprint Backlog**
  1. 在 `Sprint Planning Meeting` 上, `Development Team` 和 `Product Owner` 协商承诺的`PBI`组成
  2. 整个Scrum人员可见. 在Sprint执行期间, 承诺范围和任务目标不可改变.
  3. 在Sprint执⾏行期间, 团队将发现兑现既定范围承诺还需要的附加任务, 则放到 `Sprint Backlog` 中.
  4. 放在这里的 `PBI` 需要定义好 `Done`. 注意考虑复用性和向后兼容性, 以防止潜在的技术债务.
- **Sprint Task** (optional)
  1. 对如何完成一条PBI的若干简单描述. 该任务必须细化到一天以内即可完成
  2. 在Sprint执行期间, 每个人都可主动认领任务
  3. 由整个团队拥有, 需要协作.
  4. 这是一个可选项, 而非必须项. 过度使用并不利于提高效率.
- **Increment**
  1. `Increment` 是一个 Sprint 完成的所有产品待办列表项的总和
  2. 完成一个 Sprint 时, 新的 `Increment` 必须是 `Done` 的, 并可用和潜在可发布.

## 若干种Sprint的展示板

![Sprint_backlog_1](https://draapho.github.io/images/1717/Sprint_backlog_1.JPG)

![Sprint_backlog_2](https://draapho.github.io/images/1717/Sprint_backlog_2.JPG)

![Sprint_backlog_3](https://draapho.github.io/images/1717/Sprint_backlog_3.JPG)

![Sprint_backlog_4](https://draapho.github.io/images/1717/Sprint_backlog_4.JPG)


  
  
----------

***原创于 [DRA&PHO](https://draapho.github.io/) E-mail: draapho@gmail.com***