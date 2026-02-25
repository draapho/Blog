---
title: 本地AI配置教程
date: 2026-02-25
categories: software
tags: [software]
description: 本地AI配置教程, 及对AI的看法
---



- # 一. 需求

  准备安装可以离线的本地AI，主要用于灾备，存储知识，可以离线问答。
  次要目标是学习了解AI嵌入式本地化的实用性情况
  电脑1台式机配置是: 5070ti, AMD Ryzen 7 7800X3D, 32GB,1tb+2tb硬盘
  电脑2笔记本配置是: 无显卡, Intel Ultra7 255H, 64G,1tb+2tb硬盘

  要求：

  - 本地AI能回答常识性知识，如如何种菜等等， 
  - 可以给他已有的知识库学习， 譬如PDF版本的书籍和文件。 
  - 主要用于灾备，即断网情况下的自救知识。
  - 顺便学习一下本地AI的发展情况和工具集, 评估嵌入式AI的应用前景.

  


  # 二. 独立显卡, 安装 Ollama

  1. Ollama 支持的硬件
     - 完美支持 NVIDIA 独立显卡 (CUDA协议). 
     - 良好支持 AMD RX6000系列及以上的显卡 (ROCm协议).
     - 完美支持 苹果电脑(M1/M2/M3/M4)
     - 其它情况, Ollama 只能默认使用CPU的算力(体验极差, 无法流畅使用).
  2. **下载**：前往 [ollama.com](https://ollama.com/download) 下载 Windows 版并安装。
     - 安装后。打开终端（PowerShell），输入：`  ollama --version`  验证
  3. **下载模型**（基于 5070 Ti 16GB，2026年主流选型）：
     - **下载主模型**：`ollama pull qwen3:14b` (百科全书，种菜、自救首选)
     - **下载 Embedding 模型**：`ollama pull nomic-embed-text` (用于断网下量化文本内容)

  - **模型路径修改**：
    - Ollama 默认把模型存在 C 盘。
    - 在 Windows 环境变量中添加 `OLLAMA_MODELS`
      - `D:\My_Work\2015_20xx_FREE\202602_LocalAI\models`
    - 也需要在Setting UI中修改到同样的路径. 一个是cmd模式路径, 一个是UI模式路径.
  - https://ollama.com/library 可以进行模型查询
  - 常用指令
    - `ollama list`  列出下载的本地模型
    - `ollama pull <模型名称>`   下载模型到本地
    - `ollama rm <模型名称>`     移除本地模型
    - `ollama ps`     运行模型的情况及占用内存
    - `ollama stop <模型名称>`  停止指定的模型,释放内存
    - `ollama show <模型名称>`  显示模型的详细信息

  

  # 三. Intel AI PC, 安装 Intel AI Playground

  ## Intel Ultra 系列的三脑架构

  | **核心单元**             | **核心优势**                                     | **255H 的硬核参数**                     |
  | ------------------------ | ------------------------------------------------ | --------------------------------------- |
  | **CPU (中央处理器)**     | 处理突发、复杂的指令，调度全局。                 | 16核/16线程，主频高达 **5.1 GHz**。     |
  | **GPU (集成显卡)**       | **暴力输出**。处理大规模并行数据，速度极快。     | 8个Xe核心，AI 算力高达 **74 TOPS**。    |
  | **NPU (神经网络处理器)** | **极致节能**。专门应付需要长效、静默运行的任务。 | 2026 年新一代 NPU，算力约 **13 TOPS**。 |

  

  ## 修改基础配置

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
      - 勾选 `OpenVINO` 进行安装. 用于激活GPU和NPU
      - 勾选 `ComfyUI` 进行安装. 使其具备生成图片的能力
      - 勾选 ` Llama.cpp (GGUF)` 进行安装. 可运行开源模型

  - 设置界面：直接搜索 `图形设置`。

    - 确保 `Intel AI Playground` 处于 “高性能（High performance）” 模式.

    


  ## 设置和使用 Intel AI Playground

  - 安装完成后, App Settings 进行设置

    - 开启 `Speech To Text`, 后端选定硬件为 `NPU`
    - 内存足够大话, 开启 `Keep Models Loaded 保持模型加载`, 即AI模型常驻内存.

  - 下载指定模型

    - 几个模式下, 都有推荐的模型. 首次使用会提示下载.
      - 保持地址在安装目录下的 `resources\models\`
    - Chat 模式下, 点击右侧的`Chat Settings`, 
      - 前往 [HuggingFace - OpenVINO Models 专区](https://huggingface.co/Intel) 选择模型
      - 点击 `Add Model 添加Model` 填入模型名称, 配置参数.

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

      

  # 四. AnythingLLM

  ## AnythingLLM的介绍

  这是管理 PDF 知识库的地方。

  **AnythingLLM** 的核心价值在于将复杂的 **RAG（检索增强生成）** 技术变得像使用文件夹一样简单。

  以下是它的四大核心功能：

  - 构建“私人知识库” (RAG)

  - 模型的多端调度与管理

  - 会议与全局助理 (2026 新特性)

  配置里面**主模型（Qwen 3）**就是**大脑**，而**嵌入器（Embedder）**和**向量数据库**就是**超级索引库**。

  为了在断网灾备时能快速从几千页 PDF 里翻出答案，这三者必须分工明确：

  

  ## 安装和配置 AnythingLLM

  - 安装: 直接从 [useanything.com](https://useanything.com/download) 下载安装包。
  - 安装完成后, 打开 AnythingLLM 界面后，按照以下顺序配置：
    1. **LLM Setup (大语言模型)**：
       - **LLM Provider**: 选择 `Ollama` 或者 `Intel AI Playground`
       - **Model**: 选择 `qwen3:14b`  (请按实际需求选择)
       - **Ollama URL**: `http://127.0.0.1:11434`。
    2. **Embedder (嵌入器)**：
       - 如果安装了 ` Intel AI Playground` 
         - 保持默认值即可
         - 目前不支持 `nomic-embed-text`
       - 如果安装了`Ollama`
         - **Embedding Provider**: 选择 `Ollama` 
         - **Model**: 选择 `nomic-embed-text`。
    3. **Vector Database (数据库)**：
       - 选择 `LanceDB` (这是内置的，直接存在你硬盘里，无需额外安装)。

  

  ## 什么是嵌入器 (Embedder)？

  **它是 AI 的“翻译官”，负责把文字变成“坐标”。**

  - **作用**：人类的文字（如“如何过滤水”）对计算机来说太感性了。嵌入器会将这段话转化成一串长长的数字（向量），比如 `[0.12, -0.98, 0.55...]`。
  - 它能让意思相近的话，在数字空间里的“位置”也非常接近。比如“怎么找喝的水”和“野外水源净化”，虽然字面上没一个字相同，但在嵌入器眼里，它们的数字坐标挨得很近。
  - `nomic-embed-text`：是这个“翻译官”的名字。它是目前公认的**离线性能最强、速度最快**的小模型之一。

  

  ## 什么是向量数据库 (Vector Database)？

  **它是 AI 的“超级图书馆架”，负责存坐标。**

  - **作用**：当把一个 1GB 的 PDF 塞给 AnythingLLM 时，系统会先把 PDF 切成几万个小碎片，让 `nomic-embed-text` 把每个碎片都翻译成“数字坐标”，然后存进这个“向量数据库”里。
  - **查询过程**：当问题时，它不是在搜关键词（像 Ctrl+F 那样），而是在数据库里找“离你问题坐标最近”的那几个 PDF 碎片。
  - **在 AnythingLLM 里**：它通常内置了一个叫 **LanceDB** 或 **Chroma** 的数据库，不需要额外下载，它会自动管理。

  

  

  # 五. 如何选择正确的AI模型

  - 核心公式: **显存必须装下整个模型文件 + 上下文（Context）所需的空间。**
  - “全显存”是分水岭. AI 推理本质上是极其密集的数学运算。

    - **全显存模式（GPU Only）：** 数据在显存（VRAM）和 GPU 核心之间传输，带宽通常在 **500GB/s - 1000GB/s** 以上。
    - **混合模式（GPU + CPU/RAM）：** 当显存装不下，模型的一部分会被迫放在内存里。由于总瓶颈，内存带宽通常只有 **50GB/s - 100GB/s**。
    - **结果：** 整个系统的速度会被最慢的环节（内存）拖累。即便只溢出了 1GB 到内存，速度也会从 50 t/s 掉到 3-5 t/s。

  

  ## 第一部分：模型权重（固定支出）

  这是模型文件加载进显卡的大小。

  - **计算：** 如果是 **14B** 模型，使用 **Q4_K_M** 量化，大约占用 **9GB - 9.5GB**。
  - **余额：** 16GB - 9.5GB = **6.5GB**。这剩下的 6.5GB 就是剩余可用显卡内存。

  

  ## 第二部分：上下文长度缓存, Context Cache

  这决定了 AI 能记得多远的聊天记录。**Context Cache 是显存占用的大户。**

  - **估算公式（经验法则）：** 
    - 对于 7B 的模型，每 1K Token大约占用 100MB - 200MB 显存。
    - 对于 14B 的模型，每 1K Token大约占用 300MB - 400MB 显存。
    - 对于 32B 的模型，每 1K Token大约占用 600MB - 800MB 显存。
  - **最低4K上下文的情况下. 7B模型约0.7GB; 14B模型约1.5GB.**

  

  ## 第三部分：多模态图片预留缓冲

  对于支持多模态的AI大模型, 还需要预留出足够的图片缓冲.

  视觉模型处理图片时，会将图片编码为 “Token”。

  - **计算参考：** Qwen-VL 系列通常将一张图片编码为约 **1000 - 1500 个 Token**。
  - 处理图片瞬间的计算（Activation）和存储这些图片 Token，
    - 建议为“单次对话处理 1-2 张图”预留 **1.5GB - 2GB** 的显存。

  

  # 六. 喂入自救知识库 (RAG)

  1. 回到 AnythingLLM 主界面。点击搜索旁边的**”+“**号， 就是新建工作区。
  2. **创建工作区 (Workspace)**：起名为 `EmergencySurvival`。
  3. **上传 PDF**：点击新建工作区右侧的上传按钮，把收集的《赤脚医生手册》、《野外生存指南》、种植等灾备书籍(**必须是文字版**)拖进去。
  4. **搬运到 Workspace**：点击 **"Move to Workspace"**，然后点击 **"Save and Embed"**。
     - 此时显卡会疯狂工作一会，它正在把书里的文字变成 AI 能理解的数学向量。
  5. **开始提问**：
     - 在对话框切换到 **"Query"** 模式（仅从文档找答案）或 **"Chat"** 模式（文档+AI自带常识）。
     - 试着问：“如果断水了，如何用简单的材料制作净水装置？”

  

  # 七. 扫描版pdf的自动识别

  在尝试放入PDF文件时, 马上会遇到的问题就是: 大部分的PDF是图片扫描版本, 而不是文字版.
  因而需要自动批量化实现以下功能

  - PDF文件的加载和读取
  - 图片识别为文字, 保存.
  - 识别出文件中真正的图片, 保存.
  - 文字和图片, 尽量保持原有布局, 导出为新文件.

  经过比较判断, 直接使用图片识别大模型并不现实. 

  - 本地AI大多只能处理一二张图片的识别
  - 大多不支持PDF格式的导入, 或PDF文件过大.
  - 无法自动保留布局, 并导出为新文件.

  一样要编程实现, 选了IBM的Docling.

  - 需要安装python 3.10以上.

  

  ## 使用IBM的 Docling

  下载安装Docling

  ```powershell
  python -V 	# 需要python 3.10以上.
  python -m pip install docling		# 核心库
  python -m pip install docling[ocr]	# 文字识别引擎
  python -m pip install docling[render]	# 图片渲染引擎
  
  # !!!注意, 只有NV独立显卡, 才需要安装特殊版本的torch以便加速.!!!
  # 要先卸载已有的版本, 无法自动覆盖安装
  python -m pip uninstall torch torchvision -y
  # 安装CUDA工具, 让NVIDIA 5070Ti参与加速OCR.
  python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
  # !!!注意结束!!!
  
  # 检查torch版本
  python -c "import torch; print(torch.__version__)"
  # 默认是 +cpu 工作.NV显卡则显示 +cuXXX
  
  # 默认的 torch 版本, 使用CPU, 一般已经自动安装. 便于错误安装后的恢复.
  ### python -m pip install torch torchvision
  
  ```

  

  自动化提取图文脚本, 创建`read_pdf.py`文件

  ```python
  import os
  import torch
  import re  # 导入正则，用于精准替换占位符
  from pathlib import Path
  from docling.document_converter import DocumentConverter, PdfFormatOption
  from docling.datamodel.pipeline_options import PdfPipelineOptions
  from docling.datamodel.base_models import InputFormat
  
  # ================= 配置区域 =================
  # 如果想输出图片，请设置为 "1"；否则设为 "0"
  IMAGE_EXPORT_MODE = "1"
  # ===========================================
  
  def select_and_convert():
      current_dir = Path(".")
      pdf_files = list(current_dir.glob("*.pdf"))[:9]
  
      if not pdf_files:
          print("❌ 错误：未发现 PDF 文件。")
          input("\n按回车键退出..."); return
  
      print("\n--- 🔍 PDF AI 识别引擎 (Docling 2.x) ---")
      for i, file in enumerate(pdf_files, 1):
          print(f"[{i}] {file.name}")
      print("------------------------------------------")
  
      choice = input(f"请输入数字选择文件 (1-{len(pdf_files)}): ")
      if not choice.strip() or not choice.isdigit(): return
  
      target_pdf = pdf_files[int(choice) - 1]
  
      # 定义输出路径：文件夹 Result_文件名，内部文件 文件名.md
      output_folder = current_dir / f"Result_{target_pdf.stem}"
      output_md_path = output_folder / f"{target_pdf.stem}.md"
  
      # --- 1. 核心配置 ---
      pipeline_options = PdfPipelineOptions()
      pipeline_options.do_ocr = True
      pipeline_options.do_table_structure = True
  
      if IMAGE_EXPORT_MODE == "1":
          pipeline_options.generate_picture_images = True
          print("🖼️ 已开启图片提取模式...")
      else:
          pipeline_options.generate_picture_images = False
          print("📄 已开启普通文本模式...")
  
      # 显式检测 CUDA (会自动回退)
      if torch.cuda.is_available():
          pipeline_options.accelerator_options.device = "cuda"
      else:
          pipeline_options.accelerator_options.device = "cpu"
  
      converter = DocumentConverter(
          format_options={
              InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
          }
      )
  
      print(f"\n🚀 正在处理: {target_pdf.name}...")
  
      try:
          result = converter.convert(target_pdf)
          output_folder.mkdir(exist_ok=True)
  
          # 获取导出的原始 Markdown 文本（此时含有 占位符）
          md_content = result.document.export_to_markdown()
  
          # --- 2. 图片处理与位置替换逻辑 ---
          if IMAGE_EXPORT_MODE == "1":
              image_folder = output_folder / "images"
              image_folder.mkdir(exist_ok=True)
  
              # 按顺序提取文档中所有图片并存盘
              image_paths = []
              for element, _level in result.document.iterate_items():
                  if hasattr(element, "image") and element.image and element.image.pil_image:
                      # 转换 ID 格式，确保文件名合法
                      ref_id = getattr(element, 'self_ref', 'img').replace("/", "_").replace("#", "n")
                      img_name = f"image_{ref_id}.png"
  
                      # 物理保存图片到磁盘
                      element.image.pil_image.save(image_folder / img_name)
                      # 记录图片的相对路径供 MD 引用
                      image_paths.append(f"images/{img_name}")
  
              # 使用正则精准匹配并顺序替换占位符
              def replace_placeholder(match):
                  if image_paths:
                      return f"\n![image]({image_paths.pop(0)})\n"
                  return match.group(0)
  
              # 执行替换动作
              md_content = re.sub(r"<!--\s*image\s*-->", replace_placeholder, md_content)
              print(f"✅ 图片已成功存盘并插入对应位置。")
  
          # --- 3. 保存 Markdown 文件 ---
          # 不再输出 HTML，文件名与 PDF 同名
          with open(output_md_path, "w", encoding="utf-8") as f:
              f.write(md_content)
  
          print(f"\n✨ 转换成功！")
          print(f"📄 文件保存在: {output_md_path}")
  
      except Exception as e:
          print(f"\n❌ 出错: {e}")
          import traceback
          traceback.print_exc()
  
      input("\n按回车键返回菜单...")
  
  if __name__ == "__main__":
      select_and_convert()
  ```

  

  使用管理员权限, 运行该脚本

  ```bash
  # 方法一, 将pdf文件放到 `read_pdf.py` 所在文件夹
  # py文件右键, 点击 `以管理员身份运行` (见下面的脚本)
  # 或者打开管理员终端, 运行下述指令之一即可. 
  python read_pdf.py
  py read_pdf.py
  py -3.12 read_pdf.py
  
  # 方法二, 在pdf所在文件夹, 指定路径运行 read_pdf.py
  # 打开管理员终端, 运行下述指令之一即可. 
  python /...path/read_pdf.py
  py /...path/read_pdf.py
  py -3.12 /...path/read_pdf.py
  ```

  

  py文件右键添加管理员

  - 下述内容保存为文件 `文件py右键添加管理员打开.reg`
  - 如有必要, 保存一下windows注册表
  - 运行 `文件py右键添加管理员打开.reg`, 这样右键即可直接管理员运行选中的py文件.

  ```bash
  Windows Registry Editor Version 5.00
  
  [HKEY_CLASSES_ROOT\Python.File\shell\runas]
  @="以管理员身份运行"
  "Extended"=dword:00000001
  "Icon"="python.exe"
  "HasLUASHIELD"=""
  
  [HKEY_CLASSES_ROOT\Python.File\shell\runas\command]
  @="cmd.exe /k \"pushd \"%1\\..\" && python \"%1\" %*\""
  ```

  

  

  # 八. 整体操作流程

  - 预处理阶段（把扫描图变文本）
    - 将扫描版的PDF书籍放入 `read_pdf.py` 所在的文件夹. 
    - 运行 `read_pdf.py`脚本, 提取出md或html格式的书籍
  - 录入阶段（把文本变成LLM库）
    - **操作**：打开 **AnythingLLM**。
    - **动作**：进入 `Emergency_Survival` 工作区，把刚才保存的文本文件丢进去，点击 **"Save and Embed"**。
    - **结果**：这时“索引员” `nomic-embed-text` 会接手，把它存入本地向量数据库。

  - 提问阶段（正式使用）
    - **操作**：在 **AnythingLLM** 的聊天框里直接输入问题。
    - **后台状态**：Ollama 或 Intel AI Playground 必须在后台运行。
    - **关键点：选对模型**
      - 在 AnythingLLM 聊天窗口的顶部或设置里，确保 **Chat Model** 选的是 **`qwen3:14b`**。或其它高性能通用性大模型.

  

  # 九. 本地化AI模型比较(2026)

  | **大模型**               | **大小** | **逻辑推理** | **文本能力** | **多模视觉** | **核心定位**      | **主要特点**                         |
  | ------------------------ | -------- | ------------ | ------------ | ------------ | ----------------- | ------------------------------------ |
  | **Qwen3:14B**            | 9.3GB    | ⭐⭐⭐          | ⭐⭐⭐⭐         | 无           | 通用旗舰          | 中文语境理解与长文本处理最强。       |
  | **Qwen3:8B**             | 5.1GB    | ⭐⭐           | ⭐⭐⭐          | 无           | 轻量旗舰          | Qwen3:14B 的轻量化版。               |
  | **DeepSeek-R1:14B**      | 9.5GB    | ⭐⭐⭐⭐         | ⭐⭐           | 无           | 深度思考          | 逻辑推理天花板，自带“思考链”。       |
  | **DeepSeek-R1:8B**       | 5.3GB    | ⭐⭐⭐          | ⭐            | 无           | 轻量推理          | R1:14B 的轻量化版。                  |
  | **Gemma 3:12B**          | 8.2GB    | ⭐⭐           | ⭐⭐⭐          | ⭐⭐⭐          | 创意助手          | 文学创作、多轮对话自然，多模态。     |
  | **Qwen2.5-Coder:14B**    | 9.2GB    | ⭐⭐⭐          | ⭐⭐           | 无           | 编程专家          | 代码生成准确率和排错能力本地最强。   |
  | **Qwen2.5-Coder:7B**     | 4.7GB    | ⭐⭐           | ⭐            | 无           | 轻量编程          | Coder:14B 的轻量化版。               |
  | **Qwen3-VL:8B**          | 6.4GB    | ⭐            | ⭐⭐           | ⭐⭐⭐          | 图像解析          | 能够理解复杂图表并生成代码或描述。   |
  | **TranslateGemma:12B**   | 8.4GB    | ⭐⭐           | ⭐⭐⭐⭐⭐        | 无           | 翻译专用          | 翻译能力超过通用模型，带术语库支持。 |
  | **微小模型**             | 大小     |              |              |              | **端应用,嵌入式** | 成本和资源受限的情况                 |
  | **Qwen3-VL:2B**          | 1.8GB    | ⭐⭐           | ⭐⭐           | ⭐⭐⭐⭐         | 端侧视觉          | 视觉解析同级别顶尖                   |
  | **GLM-OCR:q8_0**         | 1.6GB    | ⭐            | ⭐            | ⭐⭐⭐⭐⭐        | 极致OCR           | 复杂图文的OCR高度还原。              |
  | **LFM2.5-Thinking:1.2B** | 0.8GB    | ⭐⭐⭐⭐⭐        | ⭐⭐           | 无           | 指令过滤          | 解析并拆解复杂的任务指令。           |

  

  

  # 十. 本地AI架构分层

  ## 1. 硬件层 (Hardware Layer)

  可以运行大模型的硬件有如下几种:

  | **硬件** | **缩写全称**   | **背后巨头**        | 特点                                                   |
  | -------- | -------------- | ------------------- | ------------------------------------------------------ |
  | **CPU**  | 中央处理器     | Intel / AMD         | 什么都可以做. 擅长逻辑调度, 串行计算. 不适合密集计算。 |
  | **GPU**  | 图形处理器     | NVIDIA / AMD        | 虽然每个只会简单算术，但一起算题速度极快。高功耗.      |
  | **NPU**  | 神经网络处理器 | Intel / 苹果 / 华为 | 专为AI设计. 低功耗AI专用机算器。                       |
  | **TPU**  | 张量处理器     | Google              | 专门处理极大规模的计算。买不到，只能云端租用。         |

  

  不同硬件芯片的指令集和加速协议:

  | **加速协议/框架** | **所属/适配** | **核心特点**                                                 |
  | ----------------- | ------------- | ------------------------------------------------------------ |
  | **CUDA**          | NVIDIA        | 生态最成熟，拥有物理层级最高的并行计算效率与底层算力优化能力。 |
  | **ROCm**          | AMD           | 对应 CUDA 的开源方案。                                       |
  | **Metal / AMX**   | Apple         | 苹果统一内存架构的核心。通过集成在 SoC 中的异步矩阵扩展（AMX）实现极高性能的推理。 |
  | **OpenVINO**      | Intel         | 跨硬件加速器。能将模型自动映射到 CPU、GPU（集显）和 NPU 上，是 Intel AI PC 的核心。 |
  | **DirectML**      | Microsoft     | 微软推出的跨硬件 API。只要支持 DirectX 12 的显卡都能跑，适配性最广但极致性能略逊。 |

  

  

  ## 2. 模型层(Model Layer) 

  即本地大模型, 纯二进制文件. 包含了训练后, AI的整个参数集和知识库.

  必要的知识点:

  - [Hugging Face](https://huggingface.co/).  AI 界的 GitHub. 用于存储、分享模型和数据集的标准云端仓库。
  - GGUF 文件格式：本地化部署的标准文件格式，通过“量化”技术让大模型能塞进家用显存里。

  

  当前模型的局限性. 资源和算力总是有限的, 单个AI是有自己的特点, 局限和专长的.

  因而需要了解主流AI模型的特长, 才能较好的选择正确的AI大模型.

  - 主流闭源云端模型（2026）
    - **Gemini 2.0 Ultra**：原生多模态，擅长处理视频流与复杂音频指令。
    - **GPT-5 / Claude 4**：逻辑推理与复杂指令，用于处理超长文本或极高难度逻辑。
  - 主流开源模型（2026）

    - **Qwen 3 (通义千问)**：中文语境下的绝对王者. 其云端产品性能已经与闭源模型对齐
      - 2025年起, Qwen有成为开源模型霸主的趋势.
      - 2026 年, 其提供的开源本地版, 逻辑能力已全面对齐 GPT-4.
    - **Llama 3.3 / 4 (Meta)**：过去几年, AI开源社区的生态位中心。
    - **DeepSeek V3**：性价比与架构创新的代表，在数学、编程等垂直领域表现突出。
    - **Mistral NeMo**：针对端侧优化，在极小参数量下保持了极高的上下文窗口处理能力。

  

  

  ## 3. 推理引擎层(Inference Engine)

  负责将静态的模型文件加载到硬件上，并提供与外界沟通的接口。

  - **Ollama**：全能驱动引擎。它极大的简化了复杂的部署流程, 并具有广泛的适配性。
  - **Intel AI Playground**：专为 Core Ultra 处理器设计，通过 OpenVINO 框架榨干 NPU 和集显的每一分性能。

  其它引擎层软件, 供参考学习.

  - **vLLM**：高并发首选。主要用于服务器端或本地多用户环境。
  - **LM Studio**：更像是调试工具, 适合企业和开发者进行模型性能对比与提示词测试。
  - **Text-Generation-WebUI **：高度自定义首选。适合发烧友。

  

  ## 4. 代理层(Agent Layer)

  这一层不再是关注如何让单个AI跑起来, 关注的重点是如何整合资源(多AI, 其它功能, 权限)来提供某种服务.

  - **AnythingLLM**：本地知识库管理专家。
    - 内置全套 RAG 链路（嵌入、切片、检索）。
    - 将 RAG流程标准化. 极大简化了知识库的构建过程.
    - 提供了非常实用的应用层功能, 诸如会议记录和摘要, 电脑交互收集信息, 知识库检索. 
  - **Claude Code / OpenClaw / OpenCode**：操作级 Agent。主要用于辅助编程.
  - **Dify / LangFlow**：工作流编排。通过拖拽节点的方式，将 LLM、搜索插件、数据库操作连成复杂的自动化流水线。

  

  ## 5. 应用层 (Application Layer)

  AI 的“隐形化与终端化”. 标志着 AI 从炙手可热的前沿工具演变为悄无声息的背景服务。

  - 集成层提供的功能, 进一步成为基础服务和API,
  - 应用层的开发者, 无需考虑大模型的选型适配. 选择对应集成服务即可.
  - 应用层纯粹的聚焦于用户需求及实现.
  - 最终用户按照自然习惯使用应用. 几乎没有学习曲线.

  

  ## 6. 矛盾和冲突

  AI的能力高度依赖知识库. 但是AI一旦通过知识库学会某种技能后, 整体趋势就是整个行业对人力的需求快速萎缩.
  这场变革正在不同领域以不均等的速度发生。

  目前, 很清晰的, 只要知识信息便于收集和获取的, AI的表现都比较出众.

  - 编程领域, 完全能替代新手编程员. 
    - 缺少的是大局观, 架构设计, 底层交互调试等高度依赖个人经验积累的, 抽象级别更高, 更离散的知识库.
  - 商用创意多媒体, 如平面设计, CG 建模, 动画中间帧, 甚至商业摄影
    - 由于互联网上有海量的标注图像和视频流，AI 已经能实现从分镜到成片的端到端输出。
    - 低端美工和初级剪辑师已基本被集成层工具取代。
  - 文字助理, 大众文学. 由于经典文献、网络文学、新闻稿件已高度数字化. AI 的遣词造句能力远超普通人类。
    - 法律文职助理
    - 售后服务
  - 交易员. 目标清晰, 历史走势可公开获取. 还没有人性固有的缺点.

  而专业领域, 由于缺乏数字化公开资料, 会形成"数字孤岛", AI的替换速度就要缓慢的多. 但渗透只是时间问题.

  - 硬件电路设计. 主要障碍是AI的大规模图片识别能力有限, 无法从公开的原理图中总结普适性经验. 
    - 电路板layout 走线设计以及硬件调试, 更是深藏资深硬件工程师的经验和离线文档中. 
    - AI可以从辅助设计原理图和走线开始. 电路调试相当长时间内, 依旧需要人类参与.
  - 精密机械结构. 涉及复杂的物理材料特性、模具精度与装配公差.
    - AI 仍需大量高质量的闭环实验数据支撑。
  - 医疗临床诊断. 临床经验很难量化为标准数据. 甚至会被描述成一种"临床直觉"
    - 影像诊断是例外, 目前已经成为了辅助判断病例的得力助手.
  - 法律与高端智库. 法律的博弈并不全在公开的法律条文.
    - 而是隐藏在案件背后的利益博弈, 人情世故与法庭辩论的即时反应. 
    - 往往要针对每个案件, 深入研究分析其背后的相关利益者. AI 难以触及.

  最后. 核心不是人和AI的矛盾, 而是人和人的矛盾. 即: 资源的分配问题.

  - 当前的主要分配形式为: 按劳取酬和资本得利. 普通大众基本是按劳取酬.
  - 去焦虑被AI淘汰是没有用的, 这只是时间问题. 
    - 不要相信什么AI只是新技术, 会产生新的工作. AI对整个生产模式是颠覆性的, 破坏性的. 
    - 即凡是被AI占领的工作, 人类再也没有可能分一杯羹.  是生产主体从"碳基" 向"硅基"的永久迁移.
    - 而且, 这种占领范围是全方位的, 鲜有死角, 只有快慢之分.
    - **犹如猛虎在后, 现在引导的焦虑感, 是让你觉得只要跑赢周围的人就行了. 但这只猛虎永不停歇!!!**
  - 目前, AI带来的技术红利, 主要流向了资产持有者. 即资本得利. 这是不可持续的.
    - 现有的制度崩溃是无法避免的, 要么损上益下逐步改良, 要么乱而后治.
  - 因而, 后AI时代, 需要解决的是人类的制度问题! 

  

  打破一个旧世界很难, 更难的是破而后立, 我们需要共同思考: 

  - **我们, 真正追求的是怎样的人生?** 
  - **人的价值和尊严, 应该建立在怎样的制度之上?**





----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
