FROM python:3.14-slim

WORKDIR /app

# 系统依赖（pymupdf 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Poetry
RUN pip install --no-cache-dir poetry==2.1.2

# 先复制依赖文件，利用 Docker 缓存层
COPY pyproject.toml poetry.lock ./

# 安装 Python 依赖（不安装项目本身）
RUN poetry install --no-dev --no-root && \
    poetry run pip cache purge

# 复制源码
COPY src/ ./src/

# ChromaDB 数据持久化目录
RUN mkdir -p /app/chroma_data

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
