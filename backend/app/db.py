"""
简单的内存存储模块
Phase 1: 把 PDF 文本存在内存字典里，不做向量检索
后面可以升级为 ChromaDB / PostgreSQL
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PdfDocument:
    """代表一个已上传的 PDF 文档"""
    id: str
    filename: str
    content: str          # PDF 提取出的纯文本
    page_count: int
    uploaded_at: str = field(default_factory=lambda: datetime.now().isoformat())


# 内存存储: key = 文档ID, value = PdfDocument
_documents: dict[str, PdfDocument] = {}


def save_document(doc: PdfDocument):
    """保存文档到内存"""
    _documents[doc.id] = doc


def get_document(doc_id: str) -> PdfDocument | None:
    """按 ID 获取文档"""
    return _documents.get(doc_id)


def get_all_documents() -> list[PdfDocument]:
    """获取所有文档列表"""
    return list(_documents.values())


def delete_document(doc_id: str) -> bool:
    """删除文档"""
    if doc_id in _documents:
        del _documents[doc_id]
        return True
    return False
