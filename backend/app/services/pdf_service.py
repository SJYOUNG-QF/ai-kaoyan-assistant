"""
PDF 文件服务
处理 PDF 的读取、文本提取等纯数据操作
不包含任何 HTTP 逻辑，可被路由、脚本、测试等任意模块复用
"""

import os
from PyPDF2 import PdfReader
from app.config import UPLOAD_DIR


def extract_text(file_path: str) -> str:
    """读取一个 PDF 文件，逐页提取文本并拼接返回"""
    reader = PdfReader(file_path)
    all_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            all_text += page_text + "\n"
    return all_text


def save_file(filename: str, content: bytes) -> str:
    """将文件保存到上传目录，返回完整的保存路径"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path
