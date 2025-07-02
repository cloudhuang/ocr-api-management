FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y build-essential cmake git wget unzip libgl1 libsm6 ffmpeg

# 清理缓存
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["flask", "--app", "src.api", "run", "--host", "0.0.0.0", "--port", "8000"]