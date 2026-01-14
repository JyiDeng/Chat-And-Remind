# 聊天助手项目

这是一个基于Flask的简易聊天助手应用，集成了SiliconFlow API，具有定时任务功能。

## 功能特点

1. **聊天对话**：用户可以随时与聊天助手进行对话
2. **定时任务**：每15分钟自动触发一次，助手会主动发送提醒消息
3. **简易Web UI**：提供简洁的聊天界面，助手消息在左侧，用户消息在右侧
4. **消息持久化**：所有聊天记录保存在JSON文件中

## 项目结构

```
my_workflow/
├── app.py                 # Flask应用主文件
├── chat_service.py        # 聊天服务和历史管理
├── scheduler.py           # 定时任务配置
├── config.py              # 配置文件
├── requirements.txt       # Python依赖
├── Dockerfile             # Docker镜像配置
├── docker-compose.yml     # Docker Compose配置
├── .env.example           # 环境变量示例
├── .gitignore            # Git忽略文件
└── static/               # 静态文件
    ├── index.html        # 主页面
    ├── style.css         # 样式文件
    └── script.js         # 前端脚本
```

## 快速开始

### 方法一：本地运行

1. **安装依赖**

```bash
cd my_workflow
pip install -r requirements.txt
```

2. **配置API密钥**

复制 `.env.example` 为 `.env` 并填入你的SiliconFlow API密钥：

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API_KEY
```

3. **运行应用**

```bash
python app.py
```

4. **访问应用**

打开浏览器访问：http://localhost:1342

### 方法二：Docker运行

1. **配置环境变量**

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API_KEY
```

2. **构建并运行**

```bash
docker-compose up -d
```

3. **访问应用**

打开浏览器访问：http://localhost:1342

4. **查看日志**

```bash
docker-compose logs -f
```

5. **停止应用**

```bash
docker-compose down
```

## API接口

### 1. 发送消息

- **URL**: `/api/chat`
- **方法**: POST
- **请求体**:
```json
{
  "message": "用户消息内容"
}
```
- **响应**:
```json
{
  "success": true,
  "reply": "助手回复内容"
}
```

### 2. 获取历史记录

- **URL**: `/api/history`
- **方法**: GET
- **响应**:
```json
{
  "success": true,
  "messages": [
    {
      "role": "user",
      "content": "消息内容",
      "timestamp": "2026-01-14T10:30:00",
      "is_scheduled": false
    }
  ]
}
```

### 3. 健康检查

- **URL**: `/api/health`
- **方法**: GET
- **响应**:
```json
{
  "status": "ok",
  "scheduler_running": true
}
```

## 配置说明

在 `config.py` 中可以修改以下配置：

- `MODEL`: 使用的AI模型
- `SYSTEM_PROMPT`: 系统提示词
- `SCHEDULE_INTERVAL_MINUTES`: 定时任务间隔（分钟）
- `SCHEDULED_MESSAGE_PROMPT`: 定时任务的提示词

## 定时任务

定时任务使用cron表达式配置，默认每15分钟触发一次（在每小时的第0、15、30、45分钟）。

触发时，助手会根据配置的提示词生成消息并自动保存到聊天历史中。前端会每30秒自动刷新消息列表，以显示定时任务产生的消息。

## 技术栈

- **后端**: Flask + APScheduler
- **前端**: 原生HTML/CSS/JavaScript
- **API**: SiliconFlow Chat API
- **容器化**: Docker + Docker Compose

## 注意事项

1. 请确保API_KEY正确配置，否则无法调用聊天API
2. 聊天历史保存在 `chat_history.json` 文件中，请勿删除
3. Docker运行时，聊天历史文件会通过卷挂载持久化
4. 定时任务在后台运行，不会阻塞主应用

## 开发调试

启用Flask调试模式（仅用于开发环境）：

在 `app.py` 中修改最后一行：
```python
app.run(host='0.0.0.0', port=1342, debug=True)
```

## 许可证

MIT License
