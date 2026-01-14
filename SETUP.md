# 聊天助手项目（基于 Flask + Gunicorn + WSGI）

这是一个基于 Flask 的简易聊天助手应用，集成 SiliconFlow API，带定时任务（APScheduler）与生产级 WSGI 部署（Gunicorn）。

## 功能特点

1. 聊天对话：用户可与助手实时对话
2. 定时提醒：按 Cron 计划定期自动发送消息
3. 简易 Web UI：静态页面直出，开箱即用
4. 持久化：聊天历史保存在 JSON 文件
5. 生产部署：内置 `wsgi.py` 与 `start_production.sh`

## 项目结构

```
my_workflow/
├── app.py                 # Flask 应用主文件（开发直跑）
├── wsgi.py                # 生产入口（Gunicorn 使用：wsgi:app）
├── chat_service.py        # 调用 SiliconFlow API 与历史管理
├── scheduler.py           # 定时任务调度（APScheduler）
├── config.py              # 配置（API、模型、Cron 等）
├── chat_history.json      # 聊天历史数据
├── requirements.txt       # Python 依赖
├── start_production.sh    # 生产启动脚本（Gunicorn）
├── Dockerfile             # Docker 镜像配置（Gunicorn）
├── docker-compose.yml     # Docker Compose 配置
├── NETWORK_SETUP.md       # 公网访问/反向代理/HTTPS 指南
├── README.md              # 项目说明
├── .env.example           # 环境变量示例（复制为 .env）
├── .env                   # 本地环境变量（不提交）
└── static/                # 前端静态文件
    ├── index.html
    ├── style.css
    └── script.js
```

## 环境准备

1) Python 3.11+（或 Docker）
2) 安装依赖

```bash
cd my_workflow
pip install -r requirements.txt
```

3) 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，设置你的 SiliconFlow API_KEY
```

`.env` 关键项：

- `API_KEY`：SiliconFlow API 密钥

## 本地开发运行（Flask 自带服务器）

用于开发调试，包含热重载与简化日志：

```bash
python app.py
```

访问：http://localhost:1342

说明：开发模式直接在 `app.py` 中启动 APScheduler；生产模式统一由 `wsgi.py` 控制（避免多进程/多 Worker 重复执行）。

## 生产运行（Gunicorn + WSGI）

生产环境请使用 Gunicorn 运行 `wsgi:app`。项目已内置脚本并在 Docker 中默认启用。

推荐单 Worker（多线程）以确保定时任务只在一个进程内运行：

```bash
chmod +x start_production.sh
./start_production.sh
```

或直接执行命令：

```bash
gunicorn -w 1 --threads 4 -b 0.0.0.0:1342 --timeout 120 wsgi:app
```

关于定时任务与多 Worker：

- `wsgi.py` 内通过 `GUNICORN_WORKER_ID` 判断，仅在第一个 Worker 中启动调度器，避免重复执行。
- 若使用多个 Worker，确保调度器只在一个进程内启动；本项目默认通过单 Worker 保守处理。

## Docker 部署

使用 Compose 一键启动（已映射聊天历史为卷，持久化保存）：

```bash
docker-compose up -d
```

常用命令：

```bash
docker-compose logs -f
docker-compose down
```

访问：http://localhost:1342

## API 接口

1) 发送消息

- 路径：`/api/chat`
- 方法：POST
- 请求体：
```json
{ "message": "用户消息内容" }
```
- 响应：
```json
{ "success": true, "reply": "助手回复内容" }
```

2) 获取历史记录

- 路径：`/api/history`
- 方法：GET
- 响应：
```json
{
  "success": true,
  "messages": [
    { "role": "user", "content": "...", "timestamp": "...", "is_scheduled": false }
  ]
}
```

3) 健康检查

- 路径：`/api/health`
- 方法：GET
- 响应：
```json
{ "status": "ok", "scheduler_running": true }
```

## 配置说明（config.py）

- `API_KEY` / `API_URL` / `MODEL` / `SYSTEM_PROMPT`
- Cron：`CRON_MINUTE` `CRON_HOUR` `CRON_DAY` `CRON_MONTH` `CRON_DAY_OF_WEEK`
- `SCHEDULED_MESSAGE_PROMPT`：定时任务提示词
- `CHAT_HISTORY_FILE`：聊天记录文件路径

说明：当前 Cron 在 `config.py` 内以常量形式配置，如需通过环境变量控制，可按需改造为 `os.getenv` 读取。

## 公网访问/反向代理/HTTPS

如需公网访问、Nginx 反代、Systemd 服务与 HTTPS 配置，请参考 `NETWORK_SETUP.md`。

## 常见问题（FAQ）

1) 定时任务重复触发/多次执行？
- 使用单 Worker（`-w 1`），或确保仅一个进程启动调度器。
- 保持通过 `wsgi.py` 启动应用（Gunicorn 命令使用 `wsgi:app`）。

2) 无法调用 API？
- 检查 `.env` 中 `API_KEY` 是否正确；网络是否可访问 SiliconFlow。

3) 聊天记录未保存/丢失？
- 确认进程有写权限；Docker 下已将 `chat_history.json` 映射为卷。

## 开发提示

如需调试：

```python
# app.py 末尾（仅开发环境）：
app.run(host='0.0.0.0', port=1342, debug=True)
```

---

MIT License
