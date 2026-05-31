# AI 考研助手

基于 **RAG（检索增强生成）** 的智能考研学习平台。上传考研资料 PDF，AI 即能以考研辅导老师的身份，结合资料内容为你解答问题、梳理解题思路、制定复习策略。

## 系统架构

```
                    ┌─────────────┐
                    │   Vercel    │
                    │  (Frontend) │
                    │  Next.js    │
                    └──────┬──────┘
                           │  HTTPS
                           │  /api/*
                           ▼
                    ┌─────────────┐
                    │   Railway   │
                    │  (Backend)  │
                    │  FastAPI    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌─────────┐ ┌──────────┐ ┌───────────┐
        │ChromaDB │ │  PyPDF2  │ │ DeepSeek  │
        │向量检索  │ │ PDF 解析 │ │  Chat API │
        └─────────┘ └──────────┘ └───────────┘
```

### 请求流程

```
Browser                    Vercel                     Railway                    DeepSeek
  │                          │                          │                          │
  │  POST /api/chat/ask      │                          │                          │
  │────────────────────────►│                          │                          │
  │                          │  Proxy to Railway        │                          │
  │                          │────────────────────────►│                          │
  │                          │                          │  1. Query ChromaDB       │
  │                          │                          │  2. Retrieve Top‑3 docs  │
  │                          │                          │  3. Build prompt         │
  │                          │                          │                          │
  │                          │                          │  POST /chat/completions  │
  │                          │                          │────────────────────────►│
  │                          │                          │  ◄─────────────────────────│
  │                          │                          │  Streaming SSE / JSON    │
  │                          │                          │                          │
  │                          │  ◄─────────────────────────│                          │
  │  ◄────────────────────────│  JSON response           │                          │
  │                          │                          │                          │
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Next.js 16 + React 19 + Tailwind CSS 4 |
| 后端 | FastAPI (Python 3.11) |
| 向量数据库 | ChromaDB（持久化存储） |
| 大模型 | DeepSeek Chat API |
| PDF 解析 | PyPDF2 |
| 前端部署 | Vercel |
| 后端部署 | Railway |

## 功能展示

- **PDF 上传与解析** — 上传考研资料 PDF，自动提取全文文字内容
- **智能问答** — 基于 PDF 内容提问，AI 结合资料原文回答，标注信息来源（【来自资料】/【来自模型补充知识】）
- **RAG 检索增强** — 文本自动切片 → 向量化 → ChromaDB 存储 → 相似度检索
- **多轮对话** — 支持上下文连续对话，追问无需重复背景
- **测试模式** — 内置考研数学（高数）示例资料，无需上传文件即可体验
- **数学公式渲染** — 支持 KaTeX 渲染，AI 回答中的公式美观展示

## RAG 工作流程

```
用户上传 PDF
    │
    ▼
┌──────────────┐
│  PyPDF2 提取  │  提取 PDF 中的纯文本
│  文字内容     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  文本切片     │  按段落 + 重叠窗口，切成 400 字小块
│  (split_text) │  重叠 50 字保持上下文连续性
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  向量化       │  每个切片 → 2‑gram 哈希 → 256 维向量
│  (Embedding)  │  归一化处理，不依赖外部模型下载
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  ChromaDB     │  向量持久化存储，以 PDF 文件名为集合名
│  存储索引     │  支持多份资料独立检索
└──────┬───────┘
       │
       ▼  (用户提问时)
┌──────────────┐
│  相似度检索   │  问题向量化 → 与库中切片比对 → 返回 Top‑3
│  (search)     │  输出距离 + 相似度分数
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  DeepSeek     │  检索结果作为上下文 + 用户问题 + 历史对话
│  生成回答     │  → 结构化 prompt → 模型生成回答
└──────────────┘
```

### Embedding 方案说明

采用轻量级 **2-gram 哈希向量化**，不依赖任何外部嵌入模型（无需下载 HuggingFace 模型），原理如下：

1. 提取文本中每两个连续字符（2-gram）
2. 对每个 2-gram 做 MD5 哈希，映射到 256 维向量中的某个位置
3. 相似文本会产生更多相同的 2-gram，向量在高维空间中自然靠近

> 该方案适合课程演示和快速原型验证。生产环境可更换为 text2vec-large-chinese 或 OpenAI Embeddings 以获得语义级检索精度。

## 项目结构

```
ai-kaoyan-assistant/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py             # 应用入口，CORS 配置
│   │   ├── config.py           # 环境变量 & 路径常量
│   │   ├── db.py               # 内存存储（预留）
│   │   ├── routers/
│   │   │   ├── health.py       # GET /health 健康检查
│   │   │   ├── pdf.py          # POST /api/pdf/upload PDF 上传
│   │   │   └── chat.py         # POST /api/chat/ask 智能问答
│   │   ├── services/
│   │   │   ├── ai.py           # DeepSeek API 调用封装
│   │   │   ├── rag_service.py  # 文本切片 / 向量化 / 检索
│   │   │   └── pdf_service.py  # PDF 文件存储与文本提取
│   │   └── models/             # 数据模型（预留）
│   ├── .env.example            # 环境变量模板
│   ├── Procfile                # Railway 启动命令
│   └── requirements.txt        # Python 依赖
├── frontend/                   # Next.js 前端
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx        # 主页面
│   │   │   └── components/     # UI 组件
│   │   │       ├── ChatPanel.tsx       # 对话面板
│   │   │       ├── PdfUploadPanel.tsx  # PDF 上传面板
│   │   │       ├── MarkdownRenderer.tsx # Markdown 渲染
│   │   │       └── AiThinking.tsx      # 加载动画
│   │   └── lib/
│   │       └── api.ts          # API 请求封装
│   └── package.json
├── Dockerfile                  # Docker 构建（备用）
├── .dockerignore
├── .gitignore
└── README.md
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- DeepSeek API Key（[申请地址](https://platform.deepseek.com/)）

### 1. 启动后端

```bash
git clone https://github.com/SJYOUNG-QF/ai-kaoyan-assistant.git
cd ai-kaoyan-assistant/backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（复制模板后填入你的 API Key）
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY=sk-xxx

# 启动服务
uvicorn app.main:app --reload --port 8000
```

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 2. 启动前端

```bash
cd ai-kaoyan-assistant/frontend

# 安装依赖
npm install

# 配置 API 地址（创建 .env.local）
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local

# 启动开发服务器
npm run dev
```

访问 http://localhost:3000

### 测试 RAG 功能

无需上传 PDF，打开「测试模式」开关即可使用内置考研数学资料直接提问。

或通过 API：

```bash
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "什么是导数？", "use_test_text": true}'
```

## 部署

### 后端 — Railway

1. 将仓库推送到 GitHub
2. 在 [Railway](https://railway.app/) 中新建 Project → Deploy from GitHub
3. 设置 **Root Directory** 为 `backend/`
4. Railway 自动识别 `Procfile` 并启动服务
5. 配置环境变量（在 Railway Dashboard → Variables）：

| 变量 | 必填 | 说明 |
|------|------|------|
| `DEEPSEEK_API_KEY` | 是 | DeepSeek API 密钥 |
| `DEEPSEEK_BASE_URL` | 否 | API 地址，默认 `https://api.deepseek.com` |
| `FRONTEND_URL` | 是 | Vercel 前端地址，如 `https://xxx.vercel.app` |

### 前端 — Vercel

1. 在 [Vercel](https://vercel.com/) 中 Import 同一 GitHub 仓库
2. 设置 **Root Directory** 为 `frontend/`
3. Framework 自动检测为 Next.js
4. 配置环境变量（在 Vercel Dashboard → Environment Variables）：

| 变量 | 必填 | 说明 |
|------|------|------|
| `NEXT_PUBLIC_API_URL` | 是 | Railway 后端地址，如 `https://xxx.railway.app` |

> **注意**：Railway 免费计划有冷启动延迟，且 ChromaDB 数据存储在容器磁盘上，重启后会丢失。如需持久化，建议后续迁移至云存储 + 托管向量数据库。

### API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/api/pdf/upload` | 上传 PDF 文件 |
| POST | `/api/chat/ask` | 向 AI 提问（支持测试模式） |

## 页面截图
## 页面截图

| 首页 | 问答界面 |
|------|---------|
| <img src="docs/screenshots/home.png" width="400"> | <img src="docs/screenshots/chat.png" width="400"> |

| 资料上传 | AI 回答 |
|---------|---------|
| <img src="docs/screenshots/upload.png" width="400"> | <img src="docs/screenshots/answer.png" width="400"> |

## 后续优化方向

- [ ] **语义 Embedding** — 接入 text2vec-large-chinese 或 OpenAI Embeddings，提升检索精度
- [ ] **用户系统** — 登录注册，个人资料库隔离
- [ ] **多格式支持** — 支持 Word、Markdown、网页链接等资料导入
- [ ] **数据持久化** — 接入云存储（如 AWS S3）+ 托管向量数据库（如 Pinecone）
- [ ] **流式响应** — API 支持 SSE 流式输出，提升对话体验
- [ ] **错题本** — 自动识别用户薄弱知识点，生成针对性练习题
- [ ] **学习进度追踪** — 可视化各章节掌握程度
- [ ] **移动端适配** — 响应式布局 + PWA 支持

## 开源协议

MIT License

---

*Built with FastAPI & DeepSeek*
