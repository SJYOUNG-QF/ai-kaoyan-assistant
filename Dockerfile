FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装 ChromaDB 可能需要的编译依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ .

# 创建上传和数据库目录
RUN mkdir -p uploads chroma_db

# 告诉 Koyeb 这个服务监听哪个端口
EXPOSE 8000

# 启动命令：Koyeb 会通过 PORT 环境变量告诉我们应该监听哪个端口
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
