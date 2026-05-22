"""
聊天路由
接收用户的提问，读取 PDF 上下文（或使用测试文本），调用 AI 返回回答
"""

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import UPLOAD_DIR
from app.services.ai import ask_ai
from app.services.pdf_service import extract_text
from app.services.rag_service import TEST_TEXT, split_text, build_index, search

router = APIRouter(prefix="/api/chat", tags=["chat"])

# 测试文本是否已建好索引
_test_index_ready = False


def _ensure_test_index():
    """确保测试文本的向量索引已建立（只执行一次）"""
    global _test_index_ready
    if not _test_index_ready:
        chunks = split_text(TEST_TEXT)
        build_index(chunks)
        _test_index_ready = True


class AskRequest(BaseModel):
    question: str
    filename: str = ""
    history: list[dict] = []
    use_test_text: bool = False  # 测试模式开关


@router.post("/ask")
def ask(request: AskRequest):
    """接收用户问题，获取上下文，调用 AI 回答"""

    # ---- 测试模式：使用写死在代码里的测试文本 ----
    if request.use_test_text:
        print(f"[CHAT] 收到问题: {request.question}")

        _ensure_test_index()
        retrieved, distances = search(request.question, top_k=3)
        context = "\n\n---\n\n".join(retrieved)

        print(f"[CHAT] 上下文长度: {len(context)} 字符, 切片数: {len(retrieved)}")

        answer = ask_ai(pdf_text=context, question=request.question, history=request.history)
        return {
            "answer": answer,
            "text_length": len(context),
            "source_chunks": len(retrieved),
        }

    # ---- 正式模式：从已上传 PDF 的 RAG 索引中检索 ----
    if not request.filename:
        return {"answer": "请先上传一份考研资料 PDF，我才能根据资料内容为您解答。"}

    file_path = os.path.join(UPLOAD_DIR, request.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"文件不存在: {request.filename}")

    print(f"[CHAT] 收到问题 (PDF模式): {request.question}")
    print(f"[CHAT] PDF 文件: {request.filename}")

    # 从 ChromaDB 中检索相关切片（以上传文件名作为集合名）
    try:
        retrieved, distances = search(
            request.question,
            top_k=3,
            collection_name=request.filename,
        )
    except Exception as e:
        # 如果索引不存在（比如旧文件没建索引），回退到全文读取
        print(f"[CHAT] RAG 检索失败，回退到全文模式: {e}")
        try:
            pdf_text = extract_text(file_path)
        except Exception as e2:
            raise HTTPException(status_code=500, detail=f"PDF 读取失败: {e2}")
        if not pdf_text.strip():
            return {"answer": "该 PDF 未能提取到文字内容，请确认文件包含可读文字。"}
        retrieved = [pdf_text]

    context = "\n\n---\n\n".join(retrieved)
    print(f"[CHAT] 上下文长度: {len(context)} 字符, 切片数: {len(retrieved)}")

    try:
        answer = ask_ai(pdf_text=context, question=request.question, history=request.history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 服务调用失败: {e}")

    return {
        "answer": answer,
        "text_length": len(context),
        "source_chunks": len(retrieved),
    }
