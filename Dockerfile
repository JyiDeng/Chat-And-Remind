FROM python:3.11-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY . .

# 暴露端口
EXPOSE 1342

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动应用（使用gunicorn生产服务器）
# 使用单worker避免定时任务重复执行
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:1342", "--timeout", "120", "--threads", "4", "wsgi:app"]
