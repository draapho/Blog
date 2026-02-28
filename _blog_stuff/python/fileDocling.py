import os
import torch
import re
import gc
import tempfile
import math
import subprocess
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc import ImageRefMode

# ================= 配置区域 =================
CHUNK_PAGES = 5         # PDF分页设置. 使用GPU的话, 必须根据显存大小, 选取5-10.
CHUNK_ADD_PAGE = True   # True / False, PDF增加分页页码, 便于确认原书位置.
GENERATE_MD_PIC = False # True / False, PDF生成MD图文版. 便于手动校验修改.
ENABLE_MATH_ML = False  # True / False, 是否开启数学公式识别. 建议保持关闭.
IMAGE_SCALE = 1.38      # 图片格式的默认扫描精度. 范围0.5-3.0
# ===========================================

def check_pdf_type(pdf_path):
    """函数 1: 判断 PDF 类型。返回 True 表示是文字版，False 表示是扫描件/图片版"""
    print(f"🕵️ 正在检测文档类型...")
    if pdf_path.suffix.lower() != ".pdf":
        return False
    try:
        reader = PdfReader(pdf_path)
        pages_to_check = min(5, len(reader.pages))
        for i in range(pages_to_check):
            page_text = reader.pages[i].extract_text()
            # 如果单页文字超过 50 个字符，基本可以判定为文字版
            if page_text and len(page_text.strip()) > 50:
                return True
    except Exception as e:
        print(f"⚠️ 检测类型时出错: {e}，默认按扫描件处理。")
    return False

def clean_pdf_title(stem):
    """清洗书名：移除特殊符号、书名号、括号内容及副标题"""
    # 1. 移除书名号和常见特殊符号
    name = re.sub(r'[《》<>|\\/*?:"\']', '', stem)
    # 2. 移除括号及其内部内容 (包括 [], (), 【】, （）)
    name = re.sub(r'[\(\[\（【].*?[\)\]\）】]', '', name)
    # 3. 移除破折号、空格、冒号后的副标题 (取第一部分)
    name = re.split(r'[-—\s:_]', name.strip())[0]
    return name.strip()

def pdf_auto_scale(pdf_path):
    """基于 PDF 页面面积自动计算平滑缩放比例"""
    try:
        reader = PdfReader(pdf_path)
        # 抽样前 10 页找最大面积，避开可能的封面或空白页
        max_area = 0
        check_limit = min(10, len(reader.pages))
        for i in range(check_limit):
            box = reader.pages[i].mediabox
            area = float(box.width) * float(box.height)
            if area > max_area:
                max_area = area

        if max_area == 0: return 2.0  # 兜底值

        # 标准 A4 面积约为 500,395 平方点
        a4_area = 595 * 841

        # 计算当前页面相对于 A4 的比例系数 (ratio)
        # ratio < 1 说明比 A4 小，ratio > 1 说明比 A4 大
        ratio = max_area / a4_area

        # 这是一个简单的线性反比逻辑：
        # scale = 1.38 / sqrt(ratio) 是一个比较平滑的曲线模型
        import math
        calc_scale = 1.38 / math.sqrt(ratio)

        # 限制上下限：最小值 0.5，最大值 3.0
        final_scale = max(0.5, min(3.0, calc_scale))

        # 取2位小数，避免出现 2.13452 这种冗余值
        final_scale = round(final_scale, 2)

        print(f"📊 PDF 面积比例: {ratio:.2f}x A4 | 自动匹配 Scale: {final_scale}")
        return final_scale

    except Exception as e:
        print(f"⚠️ 自动尺寸识别失败，使用默认值 1.38")
        return 1.38

def extract_epub_to_rag(epub_path, output_folder, file_stem):
    """纯 Python 提取 EPUB 文本 (支持超大文件)"""
    print(f"📖 正在高速提取 EPUB 纯文本...")
    output_path = output_folder / f"{file_stem}_rag.md"

    try:
        book = epub.read_epub(str(epub_path))
        with open(output_path, "w", encoding="utf-8") as f:
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # 获取该章节的内部 ID 或文件名，备用
                    item_id = item.get_id()

                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    # 1. 尝试寻找章节标题
                    # 逻辑：找第一个 h1 或 h2，如果没有，就找 title 标签
                    chapter_title = ""
                    h_tag = soup.find(['h1', 'h2', 'h3'])
                    if h_tag:
                        chapter_title = h_tag.get_text().strip()
                    elif soup.title:
                        chapter_title = soup.title.get_text().strip()

                    # 2. 清理标签
                    for hidden in soup(["script", "style", "meta"]):
                        hidden.decompose()

                    # 3. 提取文本
                    text = soup.get_text(separator='\n')
                    lines = [line.strip() for line in text.splitlines() if line.strip()]

                    if lines:
                        # 4. 写入章节页眉（可选）
                        # 如果找到了章节标题就用标题，否则用内部文件名
                        display_name = chapter_title if chapter_title else item_id
                        f.write(f"\n\n## 章节: {display_name}\n\n")
                        f.write("\n".join(lines) + "\n")

        print(f"✨ EPUB 提取完成: {output_path.name}")
    except Exception as e:
        print(f"❌ EPUB 处理失败: {e}")

def convert_text_pdf(target_pdf, output_folder, file_stem):
    """函数 2: 文字版 PDF 快速转换为MD文本"""
    print(f"🚀 检测到电子文字版，正在极速提取文本...")
    output_rag_md_path = output_folder / f"{file_stem}_rag.md"

    try:
        reader = PdfReader(target_pdf)
        with open(output_rag_md_path, "w", encoding="utf-8") as f:
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    f.write(text + "\n\n")
        print(f"✨ 文字提取完成！已生成: {output_rag_md_path.name}")
    except Exception as e:
        print(f"❌ 文本提取失败: {e}")

def convert_scanned_file(target_file, output_folder, file_stem):
    """函数 3: 扫描件 OCR 处理 (流式写入 + 图片嵌入)"""
    is_pdf = target_file.suffix.lower() == ".pdf"
    print(f"📸 启动 OCR 引擎处理 {'PDF' if is_pdf else '图片'}...")
    # 自动计算缩放比
    auto_scale = pdf_auto_scale(target_file) if is_pdf else IMAGE_SCALE

    # 配置 Docling
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.images_scale = auto_scale  # 调整图片抓取清晰度
    pipeline_options.generate_picture_images = True
    pipeline_options.do_formula_enrichment = (ENABLE_MATH_ML == True)

    # 硬件加速检测
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipeline_options.accelerator_options.device = device
    print(f"⚙️ 运行设备: {device.upper()}")

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    # 非pdf, 处理单张图片
    if not is_pdf:
        page_label = f"🖼️ {file_stem}"
        print(f"⚡ 正在处理单张图片...")
        output_rag_pic_path = output_folder / f"{file_stem}_rag.md"
        try:
            result = converter.convert(target_file)
            raw_md = result.document.export_to_markdown()
            # 1. 立即追加写入 RAG MD
            with open(output_rag_pic_path, "a", encoding="utf-8") as f:
                f.write(raw_md + "\n\n")
        except Exception as e:
            print(f"❌ 图片处理失败: {e}")
        return;

    reader = PdfReader(target_file)
    total_pages = len(reader.pages)
    global_img_count = 0

    clean_title = clean_pdf_title(file_stem) # 获取清洗后的书名

    if GENERATE_MD_PIC:
        image_folder = output_folder / "images"
        image_folder.mkdir(parents=True, exist_ok=True)

    # 路径定义
    output_rag_md_path = output_folder / f"{file_stem}_rag.md"
    output_pic_md_path = output_folder / f"{file_stem}.md"
    output_html_path = output_folder / f"{file_stem}.html"

    # 初始化 HTML 头部
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><style>")
        if not CHUNK_ADD_PAGE:
            f.write("body{max-width:900px; margin:0 auto; padding:20px;} img{max-width:100%; height:auto;}")
        else:
            f.write("body{max-width:900px; margin:0 auto; padding:20px; font-family:sans-serif; background:#f5f5f5;}")
            f.write(".page-label{background:#4A90E2; color:white; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:bold; display:inline-block; margin-bottom:10px;}")
            f.write(".chunk{background:white; padding:30px; margin-bottom:30px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1); position:relative;}")
            f.write("img{max-width:100%; height:auto; display:block; margin:20px 0; border:1px solid #ddd;}")
        f.write("</style></head><body>")

    # --- 开始流式处理循环 ---
    for start_page in range(0, total_pages, CHUNK_PAGES):
        end_page = min(start_page + CHUNK_PAGES, total_pages)
        print(f"⚡ 正在 OCR 批次: {start_page+1} - {end_page} 页...", end="\r")
        page_label = f"📄{clean_title}:{start_page+1}-{end_page} 页"

        writer = PdfWriter()
        for i in range(start_page, end_page):
            writer.add_page(reader.pages[i])

        timestamp = datetime.now().strftime("%H%M%S_%f")
        temp_chunk_path = os.path.join(tempfile.gettempdir(), f"chunk_{timestamp}.pdf")
        with open(temp_chunk_path, "wb") as f: writer.write(f)

        try:
            result = converter.convert(temp_chunk_path)
            raw_md = result.document.export_to_markdown()

            # 1. 立即追加写入 RAG MD
            with open(output_rag_md_path, "a", encoding="utf-8") as f:
                if CHUNK_ADD_PAGE:
                    # 使用引用格式注入，方便 RAG 模型识别上下文边界
                    f.write(f"\n\n> =={page_label}==\n\n")
                f.write(raw_md + "\n\n")

            # 2. 导出内嵌图片的 HTML 片段
            chunk_html = result.document.export_to_html(image_mode=ImageRefMode.EMBEDDED)
            with open(output_html_path, "a", encoding="utf-8") as f:
                if CHUNK_ADD_PAGE:
                    f.write(f"<div class='chunk'><div class='page-label'>{page_label}</div>")
                    f.write(chunk_html + "</div>")

            # 3. 处理图片并生成 _pic 版本的正则替换
            if GENERATE_MD_PIC:
                current_batch_images = []
                for element, _ in result.document.iterate_items():
                    if hasattr(element, "image") and element.image and element.image.pil_image:
                        global_img_count += 1
                        img_filename = f"img_{global_img_count}.png"
                        element.image.pil_image.save(image_folder / img_filename)
                        current_batch_images.append(f"images/{img_filename}")

                # 对 _pic 版进行正则替换
                pattern = r"<!--\s*image\s*-->"
                def replacer(match):
                    if current_batch_images:
                        return f"\n![image]({current_batch_images.pop(0)})\n"
                    return match.group(0)
                md_pic = re.sub(pattern, replacer, raw_md)
                with open(output_pic_md_path, "a", encoding="utf-8") as f:
                    if CHUNK_ADD_PAGE:
                        # 使用引用格式注入，方便 RAG 模型识别上下文边界
                        f.write(f"\n\n> =={page_label}==\n\n")
                    f.write(md_pic + "\n\n")

            del result, raw_md, chunk_html
        except Exception as e:
            print(f"\n⚠️ 批次 {start_page+1} 失败: {e}")
        finally:
            if os.path.exists(temp_chunk_path): os.remove(temp_chunk_path)
            gc.collect()
            if torch.cuda.is_available(): torch.cuda.empty_cache()

    # 关闭 HTML 标签
    with open(output_html_path, "a", encoding="utf-8") as f:
        f.write("</body></html>")

def main_flow():
    current_dir = Path(".")
    exts = [".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".epub"]

    all_files = [f for f in current_dir.iterdir() if f.suffix.lower() in exts]
    # all_files = list(current_dir.glob("*.pdf"))[:9]   # 仅支持pdf的写法

    if not all_files:
        print("❌ 未发现 PDF、 EPUB 或 图片文件。")
        return

    print("\n--- 🔍 全能文档 OCR 系统 ---")
    for i, file in enumerate(all_files[:9], 1): # 最多显示9个
        print(f"[{i}] {file.name}")

    choice = input(f"请选择文件 (1-{len(all_files)}): ")
    if not choice.strip() or not choice.isdigit(): return
    target_file = all_files[int(choice) - 1]

    file_stem = target_file.stem.strip()
    output_folder = current_dir / f"{file_stem}_OCR"
    output_folder.mkdir(parents=True, exist_ok=True)

    start_time = datetime.now()

    # 执行自动分流判断
    if target_file.suffix.lower() == ".epub":
        extract_epub_to_rag(target_file, output_folder, file_stem)
    elif check_pdf_type(target_file):
        convert_text_pdf(target_file, output_folder, file_stem)
    else:
        convert_scanned_file(target_file, output_folder, file_stem)

    duration = (datetime.now() - start_time).seconds
    print(f"⏱️ 总耗时: {duration} 秒")
    print(f"📂 结果目录: {output_folder.absolute()}")
    input("\n处理完成。按回车键退出...")

if __name__ == "__main__":
    main_flow()