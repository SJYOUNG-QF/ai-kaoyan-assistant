# AI 考研助手

> 基于 RAG（Retrieval-Augmented Generation）的智能考研学习平台

用户上传考研 PDF 资料后，系统自动解析文档、构建知识库，并结合大模型实现资料问答、知识点整理与学习规划辅助。

在线体验： [ai-kaoyan-assistant.vercel.app](https://ai-kaoyan-assistant.vercel.app)
---

## 项目亮点

### 📚 RAG 知识库问答

- 支持上传考研 PDF 教材与笔记
- 使用 PyPDF2 解析文档内容
- 基于 ChromaDB 构建向量知识库
- 检索相关内容后发送给大模型生成回答

> 解决了大模型无法理解用户私有学习资料的问题。

### ⚡ 流式对话体验

- FastAPI + SSE 实现流式输出
- AI 回答逐字返回
- 接近 ChatGPT 的交互体验

> 相比传统等待完整响应，用户体验明显提升。

### ☁️ 前后端分离部署

| 层级 | 技术 | 平台 |
|------|------|------|
| 前端 | Next.js | Vercel |
| 后端 | FastAPI | Railway |

> 实现低成本云端部署与自动化发布。

---

## 技术架构

```mermaid
graph TD
    A[用户浏览器 / Next.js (Vercel)] -->|HTTPS| B[FastAPI (Railway)]
    B --> C[PyPDF2 解析文本]
    B --> D[ChromaDB 向量检索]
    B --> E[DeepSeek API 推理]
    C --> F[构建知识库]
    D --> G[检索 Top-3 文档]
    E --> H[流式/最终回答]
    F --> D
    G --> E

---

## 技术栈

**Frontend**
- Next.js
- TypeScript
- Tailwind CSS

**Backend**
- FastAPI
- Python

**AI / RAG**
- DeepSeek API
- ChromaDB
- PyPDF2

**Deploy**
- Vercel
- Railway

---

## 我的工作

项目由本人独立完成，负责：

- 系统架构设计
- RAG 知识库搭建
- PDF 解析流程开发
- 向量检索实现
- AI 对话模块开发
- 前后端部署上线

---

## 项目难点

### 1. 大模型幻觉问题

直接把用户问题发送给模型时，经常出现脱离资料内容的回答。

**解决方案：**
- 引入 RAG 架构
- 优先检索知识库内容
- 将检索结果作为上下文提供给模型

→ 提高回答与资料内容的一致性。

### 2. PDF 内容质量差

不同教材排版差异较大。

**解决方案：**
- 增加文本清洗
- 去除页码与无效字符
- 优化分块策略

→ 提升检索质量。

---

## 后续规划

- [ ] OCR 扫描版 PDF 支持
- [ ] 多文档知识库
- [ ] 学习进度管理
- [ ] 知识点自动总结
- [ ] 题目生成与错题本
