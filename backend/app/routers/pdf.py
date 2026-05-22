"""
PDF 上传路由
处理 PDF 文件的接收、验证——仅负责 HTTP 层
文件存储和文本提取逻辑已抽到 services/pdf_service.py
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_text, save_file
from app.services.rag_service import build_index_from_text

router = APIRouter(prefix="/api/pdf", tags=["pdf"])


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """接收一个 PDF 文件，校验后保存并提取文本"""

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="只允许上传 PDF 文件")

    file_bytes = await file.read()
    file_path = save_file(file.filename, file_bytes)

    # 提取 PDF 文本
    try:
        extracted_text = extract_text(file_path)
    except Exception as e:
        print(f"[警告] PDF 文本提取失败: {e}")
        extracted_text = ""

    # 打印到服务器控制台（调试用）
    print(f"\n{'='*60}")
    print(f"PDF 文件: {file.filename}")
    print(f"提取字符数: {len(extracted_text)}")
    print(f"文本预览:\n{extracted_text[:500]}")
    print(f"{'='*60}\n")

    # 自动为 PDF 建立 RAG 向量索引
    if extracted_text.strip():
        try:
            build_index_from_text(extracted_text, file.filename)
        except Exception as e:
            print(f"[RAG] 索引建立失败: {e}")

    return {
        "success": True,
        "filename": file.filename,
        "size": len(file_bytes),
        "text_length": len(extracted_text),
        "text_preview": extracted_text[:200],
        "message": f"文件 {file.filename} 上传成功",
    }
