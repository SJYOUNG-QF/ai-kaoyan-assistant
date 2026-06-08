# AI 考研助手

> 基于 RAG（Retrieval-Augmented Generation）的智能考研学习平台

用户上传考研 PDF 资料后，系统自动解析文档、构建知识库，并结合大模型实现资料问答、知识点整理与学习规划辅助。

### 在线体验

[ai-kaoyan-assistant.vercel.app](https://ai-kaoyan-assistant.vercel.app)

---

## 项目截图

### 首页

![首页](docs/screenshots/home.png)

### PDF 上传成功页面

![上传](docs/screenshots/upload.png)

### 测试模式提问 & 回答页面

![测试模式提问](docs/screenshots/chat.png)

### 回答示例

![回答示例](docs/screenshots/answer.png)

---

## 项目亮点

### 📚 RAG 知识库问答

- 支持上传考研 PDF 教材与学习笔记
- 使用 PyPDF2 自动解析文档内容
- 基于 ChromaDB 构建向量知识库
- Top-K 相似度检索获取上下文
- 检索结果与用户问题共同发送给大模型生成回答

解决了大模型无法理解用户私有学习资料的问题，降低幻觉回答概率。

---

### ⚡ 流式对话体验

- FastAPI + SSE 实现流式响应
- AI 回答实时返回
- 接近 ChatGPT 的交互体验

相比等待完整结果后统一返回，显著提升用户体验。

---

### ☁️ 前后端分离部署

| 模块 | 技术 |
|--------|--------|
| 前端 | Next.js |
| 后端 | FastAPI |
| 数据库 | ChromaDB |
| AI 服务 | DeepSeek API |
| 部署 | Vercel + Railway |

实现低成本云端部署与自动化发布。

---

## 系统架构

```text
┌─────────────────────────┐
│       用户浏览器         │
└──────────┬──────────────┘
           │ HTTPS
           ▼
┌─────────────────────────┐
│ Next.js (Vercel)        │
│ 前端界面与文件上传       │
└──────────┬──────────────┘
           │ API 调用
           ▼
┌─────────────────────────┐
│ FastAPI (Railway)       │
│ 后端服务                │
└──────────┬──────────────┘
           │
     ┌─────┼─────┐
     │     │     │
     ▼     ▼     ▼

 PDF解析  向量检索  DeepSeek
 PyPDF2  ChromaDB   API

     │
     ▼

 构建知识库

     │
     ▼

 Top-K 检索

     │
     ▼

 AI生成回答

     │
     ▼

 SSE流式返回
```

---

## 技术栈

### Frontend

- Next.js
- TypeScript
- Tailwind CSS

### Backend

- FastAPI
- Python

### AI / RAG

- DeepSeek API
- ChromaDB
- PyPDF2

### Deploy

- Vercel
- Railway

---

## 我的工作

项目由本人独立开发完成，负责：

- 系统整体架构设计
- 前后端开发
- PDF 文档解析模块
- ChromaDB 向量知识库构建
- RAG 检索增强问答实现
- DeepSeek API 集成
- SSE 流式输出实现
- Vercel + Railway 云部署

---

## 项目难点

### 1. 大模型幻觉问题

直接将用户问题发送给大模型时，经常出现脱离资料内容的回答。

**解决方案：**

- 引入 RAG 检索增强生成架构
- 优先从知识库检索相关内容
- 将检索结果作为上下文提供给模型

提高回答与用户资料的一致性和可信度。

---

### 2. PDF 文本质量不稳定

不同教材、讲义和笔记格式差异较大。

**解决方案：**

- 增加文本清洗流程
- 去除页码和无效字符
- 优化文本分块策略

提升向量检索准确率。

---

### 3. AI 响应等待时间较长

传统请求需要等待完整结果生成后返回。

**解决方案：**

- 使用 FastAPI + SSE
- 实现流式输出
- 实时返回生成内容

提升交互流畅度。

---

## 后续规划

- [ ] OCR 扫描版 PDF 支持
- [ ] 多文档知识库
- [ ] 学习进度管理
- [ ] 知识点自动总结
- [ ] AI 出题功能
- [ ] 错题本系统

---

## 本地运行

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动后端

```bash
uvicorn main:app --reload
```

### 启动前端

```bash
npm install
npm run dev
```

---

## 项目价值

完整覆盖 PDF 文档解析 → 向量数据库构建 → RAG 检索增强生成 → LLM 调用 → SSE 流式输出 → 前后端分离部署的全链路，实现了可在线体验的考研 AI 助手。
