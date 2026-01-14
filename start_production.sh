#!/bin/bash

# 生产环境启动脚本

echo "启动聊天助手应用（生产模式）..."

# 使用gunicorn启动，绑定到所有网络接口
# 使用单worker多线程模式，避免定时任务重复执行
gunicorn -w 1 \
  --threads 4 \
  -b 0.0.0.0:1342 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  wsgi:app
