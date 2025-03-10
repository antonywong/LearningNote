FROM python:3.9-slim
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建数据存储目录
RUN mkdir -p /data /tdx

VOLUME /data /tdx

CMD ["python", "main.py"]