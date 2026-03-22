---
title: Intel的本地AI玩法
date: 2026-03-03
categories: AI
tags: [crisis, AI]
description: 探索Intel的本地AI玩法
---

[TOC]

# 总览

- [知识革命](https://draapho.github.io/2023/04/11/2301-revolution-of-knowledge/)
- [拆解追溯 GPT-3.5 各项能力的起源](https://draapho.github.io/2023/05/03/2303-chatgpt/)
- [基于Ollama的本地AI配置教程](https://draapho.github.io/2026/02/25/2607-LocalAI/)
- [Intel的本地AI玩法](https://draapho.github.io/2026/03/03/2609-IntelAI/)



# 需求

~~另有一台笔记本配置是: 无独立显卡, Intel Ultra7 255H, 64G,1tb+2tb硬盘~~
~~也想一并探索安装一下本地AI.~~

~~然后发现, 要Ollama 去支持Intel的集成显卡, 配置较为复杂. 最后还是决定直接安装Intel AI Playground, 可以灵活的选择CPU, GPU, NPU. 故决定能简单应用即可. 毕竟不是本地AI主力机.~~

不推荐安装 `Intel AI Playground`
参考 [基于Ollama的本地AI配置教程](https://draapho.github.io/2026/02/25/2607-LocalAI/), 推荐安装使用 [llama.cpp Portable Zip](https://github.com/intel/ipex-llm/blob/main/docs/mddocs/Quickstart/llamacpp_portable_zip_gpu_quickstart.zh-CN.md)



## Intel Ultra 系列的三脑架构

| **核心单元**             | **核心优势**                                     | **255H 的硬核参数**                     |
| ------------------------ | ------------------------------------------------ | --------------------------------------- |
| **CPU (中央处理器)**     | 处理突发、复杂的指令，调度全局。                 | 16核/16线程，主频高达 **5.1 GHz**。     |
| **GPU (集成显卡)**       | **暴力输出**。处理大规模并行数据，速度极快。     | 8个Xe核心，AI 算力高达 **74 TOPS**。    |
| **NPU (神经网络处理器)** | **极致节能**。专门应付需要长效、静默运行的任务。 | 2026 年新一代 NPU，算力约 **13 TOPS**。 |




# 安装驱动和Intel AI Playground 

- 安装或更新 **Intel Graphics Driver** 显卡驱动
  - 下载地址 [Intel® Arc™ & Iris® Xe Graphics - Windows*](https://www.intel.com/content/www/us/en/download/785597/intel-arc-graphics-windows.html)
  - 注意选择 "Clean Install（全新安装）"
- 安装或更新 **Intel NPU Driver** 驱动
  - 下载地址 [Intel NPU Driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html)
  - 注意选择 "Clean Install（全新安装）"
- 安装或更新 **Intel AI Playground** 软件
  - 下载地址: [Intel AI-Playground GitHub Releases](https://github.com/intel/AI-Playground/releases)
  - 两个驱动安装好后, 需要重启. 然后管理员安装 Intel AI Playground
  - 首次打开后, 自动进入后端设置界面:
    - 勾选 `OpenVINO` 进行安装. 为Intel专用大模型格式, 可使用Intel GPU和NPU.
    - 勾选 `ComfyUI` 进行安装. 使其具备生成图片的能力
    - 勾选 ` Llama.cpp (GGUF)` 进行安装. 可运行GGUF通用格式的大模型
- 设置界面：直接搜索 `图形设置`。
  - 确保 `Intel AI Playground` 处于 “高性能（High performance）” 模式.




# 设置 Intel AI Playground

- 安装完成后, App Settings 进行设置
  - 开启 `Speech To Text`, 后端选定硬件为 `NPU`
  - 内存足够大话, 开启 `Keep Models Loaded 保持模型加载`, 即AI模型常驻内存.
- 下载指定模型
  - 几个模式下, 都有推荐的模型. 首次使用会提示下载.
    - 保持地址在安装目录下的 `resources\models\`
  - Chat 模式下, 点击右侧的`Chat Settings`,
    - 前往 [HuggingFace - OpenVINO Models 专区](https://huggingface.co/Intel) 选择模型
    - 点击 `Add Model 添加Model` 填入模型名称, 配置参数.
      - `OpenVINO/Qwen3-14B-int4-ov`
    - 通用的 `GGUF` 格式也是支持的, 但性能释放上不如专用的 `OpenVINO` 格式
    - `-cw` 表示为`npu`优化过的大模型
    - `-ov` 表示是`OpenVino` 格式, 即intel CPU专用格式.
- 注意: **AnythingLLM 目前没有支持 Intel AI Playground**
  - 无法让AnythingLLM 通过 Intel AI Playground 去调用核显GPU和NPU.
  - 有间接的方法, 可通过Ollama间接实现, 过程复杂. 没有去测试.
- 注意: WSL的内存占用
  - 由于自己的电脑分配给了WSL大量的内存. 如果运行过WSL, 需要确保Windows下的可用内存
  - `wsl --shutdown` 确保关闭wsl
  - `C:\Users\<你的用户名>\` 创建或修改 `.wslconfig` 文件, 让其自动归还内存
    ```ini
    [wsl2]
    memory=32GB
    # ......
    # 以上, 为原有的设置
    # 新增, 闲置时自动归还内存给Windows
    autoMemoryReclaim=gradual
    ```



# 使用 Intel AI Playground

Intel AI Playground 的使用分为两大类.
- 一个是文本为主的对话, 即 `Chat` 类别, 实用性较高.
  - 默认有几个推荐的模型供选择(首次使用会自动提示下载).
  - 推荐 `Backend` 使用 `OpenVINO`, 即Intel专用大模型格式, 性能更好.
  - `Backend` 选择 `llamaCPP-GGUF` 的话, 可以加载使用通用的GGUF格式.
  - 设备选择, GPU最优(性能最好, 能耗最高), NPU次之(性能一般, 能耗低), CPU最差(性能差, 能耗高).
  - 如下设置好后:
  	- 日常多用 `Basic Chat` 或者 `Chat with RAG` 模式
  	- 需要推理就用 `Advanced Chat` 模式
  	- 需要图文分析用 `Vision` 模式
- 另一个是基于`ComfyUI` 的图片视频生成玩法. 主要分成三大类
  - 图片生成 `Image Gen`
  - 图片修改 `Image Edit`
  - 视频生成 `Video`



## Chat Setting

进入`Chat Setting` 后, 也已经划分了好几种应用场景. `Backend` 统一使用`OpenVINO`
- Basic Chat. 基础对话
  - 推荐使用:  `OpenVINO/Qwen3-14B-int4-ov`
  - 需要通过 `添加 Model` 手动添加.
- NPU Chat. 固定使用NPU单元运行, 能耗低, 性能不如GPU.
  - 选择列表中的 `OpenVINO/Phi-3.5-mini-instruct-int4-cw-ov`
  - `-cw` 表示为`npu`优化过的大模型
  - 开始第一次对话时, 会提示下载大模型. 后续才可以离线使用. 后同.
- Chat with RAG. 基于知识库的对话
  - 推荐使用: `OpenVINO/Qwen3-14B-int4-ov`
  - 使用 `Add Documents` 添加外部知识库.
  - `Embeddings` 就是 `Embedder`, 文本嵌入器. 选择默认模型`bge-base-en-vl.5-fp16-ov`即可.
  - 注意: 需要上传一个文件, 进行一次对话, 才会下载默认的`Embedding`模型. 后续才可以离线使用.
- Vision. 多模态对话, 即支持图片分析的大模型.
  - 选择列表中的 `OpenVINO/Qwen2.5-VL-7B-Instruct-int4-ov`
  - `-VL` 表示多模态, 即支持输入图文.
- Agentic. 智能代理执行对话, 即自动尝试执行目标.
  - 选择列表中的 `OpenVINO/Qwen2.5-VL-7B-Instruct-int4-ov`
  - `-Instruct` 表示听从指令的模型. Agentic 需要这类模型才能调用外部工具.
- Reasoning. 推理分析
  - 选择列表中的 `OpenVINO/DeepSeek-R1-Distill-Qwen-7B-int4-ov`
- Advanced Chat. 高级自定义
  - 推荐使用: `OpenVINO/DeepSeek-R1-Distill-Qwen-14B-int4-ov`
- Intel OpenVINO AI 对话模型推荐(2026)

| **大模型**                                    | **大小** | **推荐应用**     | **主要特点**                             |
| --------------------------------------------- | -------- | ---------------- | ---------------------------------------- |
| OpenVINO/Phi-3.5-mini-instruct-int4-cw-ov     | ~2.0GB   | NPU Chat         | 默认可选. 功耗低, 响应快, 适用广.        |
| OpenVINO/DeepSeek-R1-Distill-Qwen-7B-int4-ov  | ~4.5GB   | Reasoning        | 默认可选. 逻辑推理. 大小性能的平衡.      |
| OpenVINO/Qwen2.5-VL-7B-Instruct-int4-ov       | ~5.2GB   | Vision / Agentic | 默认可选. 多模态模型, 支持看图.          |
| OpenVINO/Qwen3-14B-int4-ov                    | ~9.7GB   | GPU日常使用      | 手动添加. 中文语境理解与长文本处理最强。 |
| OpenVINO/DeepSeek-R1-Distill-Qwen-14B-int4-ov | ~8.5GB   | GPU深度思考      | 手动添加. 逻辑推理天花板，自带“思考链”。 |



## Image / Video Setting

Intel AI Playground 已经按照常用的应用需求配置好了所需的大模型和默认参数.
- 譬如. 换脸, 黑白变彩色, 图片指定修改等等.
- 选择好应用需求, 首次使用会提示下载缺失的大模型, 然后等待出效果即可.
- 此部分尝鲜为主, 尤其是视频生成. 如果硬盘空间不够, 不建议下载.



## 删除下载的大模型

目前软件界面没有提供大模型删除功能, 只能进入按照目录, 手动删除模型.
- `...\AI Playground\resources\models`
  - `ComfyUI` 存放图片和视频大模型的路径. 
    - 如果确认某个模型不需要了, 可以按需删除里面的文件夹.
  - `LLM` 对话类大模型的路径
    - `embedding`  文本嵌入器模型, 给 `Chat with RAG` 用的.
      - 下面依旧细分了 `ggufLLM` 和 `openvino` 两种文件格式.
    - `ggufLLM` 通用的GGUF格式大模型. 没下载过, 应该是空的.
    - `openvino` Intel专用格式大模型. 保持了下载好的模型.
      - 文件夹命名对应了大模型名称, 按需删除整个文件夹即可.
  - `STT` 语音转文本模型




----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
