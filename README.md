# AI 考研助手

基于 RAG 的智能考研学习平台。

支持：

✅ PDF 上传解析

✅ 向量知识库检索

✅ DeepSeek 问答

✅ SSE 流式输出

✅ 云端部署

在线体验：

https://ai-kaoyan-assistant.vercel.app
## 项目演示

![PDF上传及AI问答示例](docs/screenshots/upload.png)

## 技术亮点

### RAG 检索增强问答

使用 ChromaDB 构建向量知识库，通过 Top-K 检索为大模型提供上下文，提高回答准确率。

### 流式输出

基于 FastAPI + SSE 实现实时响应，提升交互体验。

### 前后端分离部署

Next.js + Vercel
FastAPI + Railway

### 技术栈
- **前端**：Next.js + TypeScript + Tailwind CSS
- **后端**：FastAPI + Python
- **AI / RAG**：ChromaDB + DeepSeek + PyPDF2
- **部署**：Vercel + Railway

## 我的贡献

项目独立开发完成：

- 前后端开发
- PDF解析
- RAG实现
- 向量数据库构建
- DeepSeek接入
- SSE流式输出
- 云端部署 
> 项目完整覆盖 PDF 解析 → 向量知识库 → RAG 问答 → 流式输出 → 前后端部署的全链路，实现了可在线体验的考研 AI 助手。
