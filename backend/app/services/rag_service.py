"""
RAG 服务
负责文本切片、向量化存储和相似度检索
"""

import hashlib

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction

# ============================================================
# 测试数据：写死在代码里的考研数学资料
# 后面接上 PDF 后，这部分会被 PDF 提取的文本替换
# ============================================================

TEST_TEXT = """
第一章 函数与极限

1.1 函数的概念
函数是数学中最基本的概念之一。设x和y是两个变量，D是一个给定的数集。
如果对于D中的每一个数x，按照某种确定的规则f，变量y都有唯一确定的数值与之对应，
则称y是x的函数，记作y=f(x)。x称为自变量，y称为因变量。数集D称为函数的定义域。

1.2 函数的性质
单调性：如果对于区间I上的任意两点x1<x2，恒有f(x1)<f(x2)，则称f(x)在区间I上单调增加。
奇偶性：如果对于定义域内的任意x，都有f(-x)=f(x)，则称f(x)为偶函数；
如果f(-x)=-f(x)，则称f(x)为奇函数。
周期性：如果存在正数T，使得对于定义域内的任意x，都有f(x+T)=f(x)，则称f(x)为周期函数。

1.3 反函数
设函数y=f(x)的定义域为D，值域为W。如果对于W中的每一个y，在D中都有唯一的x使得f(x)=y，
则称x为y的反函数，记作x=f^{-1}(y)。

第二章 极限

2.1 极限的定义
设函数f(x)在点x0的某个去心邻域内有定义。如果当x无限趋近于x0时，
函数f(x)无限趋近于某个确定的常数A，则称A为函数f(x)当x→x0时的极限，
记作lim(x→x0) f(x) = A。

2.2 极限的四则运算法则
如果lim f(x)=A，lim g(x)=B，那么：
(1) lim[f(x)±g(x)] = A±B
(2) lim[f(x)·g(x)] = A·B
(3) lim[f(x)/g(x)] = A/B (B≠0)

2.3 两个重要极限
第一个重要极限：lim(x→0) sin(x)/x = 1
第二个重要极限：lim(x→∞) (1+1/x)^x = e

第三章 导数

3.1 导数的定义
设函数y=f(x)在点x0的某个邻域内有定义。当自变量x在x0处有增量Δx时，
函数取得增量Δy=f(x0+Δx)-f(x0)。如果极限
lim(Δx→0) Δy/Δx = lim(Δx→0) [f(x0+Δx)-f(x0)]/Δx
存在，则称函数f(x)在点x0处可导，此极限值称为f(x)在x0处的导数，
记作f'(x0)或dy/dx|x=x0。

3.2 基本求导公式
(1) (C)' = 0
(2) (x^n)' = nx^(n-1)
(3) (sin x)' = cos x
(4) (cos x)' = -sin x
(5) (e^x)' = e^x
(6) (ln x)' = 1/x

3.3 导数的应用
函数的单调性判定：如果在区间(a,b)内f'(x)>0，则f(x)在(a,b)内单调增加；
如果在区间(a,b)内f'(x)<0，则f(x)在(a,b)内单调减少。
函数的极值：设f(x)在x0处可导且f'(x0)=0。如果f''(x0)>0，则x0为极小值点；
如果f''(x0)<0，则x0为极大值点。

第四章 不定积分

4.1 原函数与不定积分
如果在区间I上，F'(x)=f(x)，则称F(x)为f(x)在区间I上的一个原函数。
f(x)在区间I上的全体原函数称为f(x)的不定积分，记作∫f(x)dx。
即∫f(x)dx = F(x) + C，其中C为任意常数。

4.2 基本积分公式
(1) ∫0dx = C
(2) ∫x^n dx = x^(n+1)/(n+1) + C (n≠-1)
(3) ∫(1/x)dx = ln|x| + C
(4) ∫e^x dx = e^x + C
(5) ∫sin x dx = -cos x + C
(6) ∫cos x dx = sin x + C

第五章 定积分

5.1 定积分的定义
设函数f(x)在区间[a,b]上有界。在[a,b]中任意插入n-1个分点，
将[a,b]分成n个小区间。在每个小区间上任取一点ξi，作和式Σf(ξi)Δxi。
当n→∞且最大小区间长度趋于零时，此和式的极限称为f(x)在[a,b]上的定积分，
记作∫[a,b] f(x)dx。

5.2 牛顿-莱布尼茨公式
如果F(x)是连续函数f(x)在区间[a,b]上的一个原函数，则：
∫[a,b] f(x)dx = F(b) - F(a)
这个公式揭示了定积分与不定积分之间的内在联系，是微积分基本定理的核心内容。
"""


# ============================================================
# 文本切片
# ============================================================

def split_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """将长文本按自然段切分成多个小块

    参数:
        text:       待切分的原始文本
        chunk_size: 每个切片的最大字符数
        overlap:    相邻切片之间的重叠字符数（保持上下文连续性）

    返回:
        切片列表
    """

    # 1. 先按空行分成自然段
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        # 2. 如果当前段加上新段落不超过限制，就拼进去
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += para + "\n\n"
        else:
            # 3. 超了：当前段存为一个切片，新段落开始下一个切片
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            # 重叠处理：取当前切片最后 overlap 个字符作为下一个切片的开头
            if overlap > 0 and chunks:
                prev_tail = chunks[-1][-overlap:] if len(chunks[-1]) > overlap else chunks[-1]
                current_chunk = prev_tail + "\n\n" + para + "\n\n"
            else:
                current_chunk = para + "\n\n"

    # 4. 处理最后一段
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


# ============================================================
# ChromaDB 向量存储
# ============================================================

# 存储路径（持久化到磁盘，重启后数据不丢失）
CHROMA_DB_DIR = "chroma_db"

class SimpleEmbedding(EmbeddingFunction):
    """轻量级 embedding，不依赖任何外部模型下载

    原理：
    将文本的每个 2-gram（两个连续字符）哈希后映射到向量的某个维度。
    相似文本会有更多相同的 2-gram，从而向量有更多重叠。
    这不是语义检索，但对「相同关键词」的匹配效果足够验证流程。
    """

    def __call__(self, input: Documents) -> list[list[float]]:
        dim = 256
        vectors = []
        for text in input:
            vec = [0.0] * dim
            # 提取所有 2-gram
            grams = [text[i : i + 2] for i in range(len(text) - 1)]
            for g in grams:
                # 对每个 2-gram 算哈希，映射到 0..dim-1 的维度
                idx = int(hashlib.md5(g.encode()).hexdigest(), 16) % dim
                vec[idx] += 1.0
            # 归一化，避免长文本天然有更大的向量
            norm = sum(v * v for v in vec) ** 0.5
            if norm > 0:
                vec = [v / norm for v in vec]
            vectors.append(vec)
        return vectors


# 使用自定义的轻量 embedding，无需下载任何模型
embedding_fn = SimpleEmbedding()

# 创建 ChromaDB 客户端（持久化模式）
_chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)


def build_index(chunks: list[str], collection_name: str = "study_materials"):
    """将文本切片向量化后存入 ChromaDB

    参数:
        chunks:          文本切片列表
        collection_name: 集合名称，相当于数据库中的"表"

    注意:
        如果集合已存在，会先删除再重建（每次上传新资料时覆盖旧数据）
    """

    # 删除旧集合（如果存在）
    try:
        _chroma_client.delete_collection(collection_name)
    except Exception:
        pass

    # 创建新集合，指定 embedding 函数
    collection = _chroma_client.create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
    )

    # 为每个切片生成唯一 ID，批量存入
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
    )

    print(f"[RAG] 已存入 {len(chunks)} 个切片到集合 '{collection_name}'")
    return collection


def search(query: str, top_k: int = 3, collection_name: str = "study_materials"):
    """根据用户问题检索最相关的文本切片

    返回:
        (documents, distances) 两个列表，distances 越小越相关
    """

    collection = _chroma_client.get_collection(
        name=collection_name,
        embedding_function=embedding_fn,
    )

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]

    # ---- 调试日志：检索结果 ----
    print(f"\n{'='*60}")
    print(f"[RAG] 检索查询: {query}")
    print(f"[RAG] Top-{top_k} 结果:")
    for i, (doc, dist) in enumerate(zip(documents, distances)):
        similarity = 1 - dist  # 距离转相似度（距离越小越相似）
        print(f"  [{i+1}] 距离={dist:.4f}  相似度={similarity:.4f}")
        print(f"      内容: {doc[:100]}...")
        print()
    print(f"{'='*60}\n")

    return documents, distances


def build_index_from_text(text: str, collection_name: str):
    """从原始文本一步完成切片+建索引

    参数:
        text:            原始文本（从 PDF 提取的全文）
        collection_name: ChromaDB 集合名（建议用 PDF 文件名）
    """
    chunks = split_text(text)
    build_index(chunks, collection_name)
    print(f"[RAG] 从文本建索引完成: '{collection_name}', 共 {len(chunks)} 个切片")


def index_test_data():
    """一键初始化：用测试文本建立索引（测试用）"""
    chunks = split_text(TEST_TEXT)
    build_index(chunks)
    print(f"[RAG] 测试索引建立完成，共 {len(chunks)} 个切片")
    return len(chunks)
