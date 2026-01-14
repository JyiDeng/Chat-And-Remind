# 公网访问配置指南

## 方案一：云服务器部署（推荐）

### 1. 云服务器配置

如果你使用的是阿里云、腾讯云、AWS等云服务器：

**a. 安全组规则配置**
- 登录云服务控制台
- 找到你的实例的安全组设置
- 添加入站规则：
  - 协议：TCP
  - 端口：1342
  - 源地址：0.0.0.0/0 (允许所有IP访问) 或指定IP段

**b. 防火墙配置**
```bash
# Ubuntu/Debian
sudo ufw allow 1342/tcp
sudo ufw reload

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=1342/tcp
sudo firewall-cmd --reload
```

### 2. 使用生产级服务器

**停止当前的开发服务器**（按Ctrl+C），然后使用Gunicorn：

```bash
# 安装依赖（如果还没安装）
pip install -r requirements.txt

# 给启动脚本添加执行权限
chmod +x start_production.sh

# 启动生产服务器
./start_production.sh
```

或者直接使用命令：
```bash
gunicorn -w 4 -b 0.0.0.0:1342 --timeout 120 wsgi:app
```

### 3. 访问应用

假设你的云服务器公网IP是 `123.45.67.89`，在浏览器中访问：
```
http://123.45.67.89:1342
```

---

## 方案二：使用Nginx反向代理（更推荐）

### 1. 安装Nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

### 2. 配置Nginx

创建配置文件 `/etc/nginx/sites-available/chat-assistant`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 或者使用你的公网IP

    location / {
        proxy_pass http://127.0.0.1:1342;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/chat-assistant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. 开放80端口

```bash
# 安全组：添加80端口规则

# 防火墙
sudo ufw allow 80/tcp
sudo ufw reload
```

### 4. 访问应用

使用80端口（默认HTTP端口）访问：
```
http://your-domain.com
或
http://123.45.67.89
```

---

## 方案三：Docker部署

使用Docker Compose部署更简单：

### 1. 修改docker-compose.yml

已经配置好了端口映射 `1342:1342`，直接使用：

```bash
docker-compose up -d
```

### 2. 访问应用

```
http://your-public-ip:1342
```

---

## 方案四：使用内网穿透（本地开发）

如果你在本地网络环境，可以使用内网穿透工具：

### 选项1：使用frp

1. 下载frp客户端
2. 配置frpc.ini
3. 启动客户端

### 选项2：使用ngrok

```bash
# 安装ngrok
brew install ngrok  # macOS

# 启动穿透
ngrok http 1342
```

会得到一个公网URL，例如：`https://abc123.ngrok.io`

### 选项3：使用Cloudflare Tunnel

```bash
# 安装cloudflared
brew install cloudflare/cloudflare/cloudflared

# 登录
cloudflared tunnel login

# 创建隧道
cloudflared tunnel create chat-assistant

# 运行隧道
cloudflared tunnel run --url http://localhost:1342 chat-assistant
```

---

## 使用Systemd服务（生产环境推荐）

创建服务文件 `/etc/systemd/system/chat-assistant.service`:

```ini
[Unit]
Description=Chat Assistant Application
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/my_workflow
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:1342 wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable chat-assistant
sudo systemctl start chat-assistant
sudo systemctl status chat-assistant
```

---

## HTTPS配置（可选但推荐）

使用Let's Encrypt免费SSL证书：

```bash
# 安装certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书并自动配置Nginx
sudo certbot --nginx -d your-domain.com

# 证书会自动续期
```

---

## 安全建议

1. **使用环境变量**：不要在代码中硬编码API密钥
2. **限制访问源**：在安全组中只允许需要的IP访问
3. **使用HTTPS**：保护数据传输安全
4. **设置速率限制**：防止API滥用
5. **定期更新依赖**：修复安全漏洞
6. **使用防火墙**：只开放必要的端口
7. **监控日志**：及时发现异常访问

---

## 快速开始（推荐方案）

**如果你在云服务器上**：

1. 开放1342端口
2. 停止开发服务器（Ctrl+C）
3. 运行生产服务器：
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:1342 wsgi:app
   ```
4. 访问：`http://你的公网IP:1342`

**如果你在本地开发**：

使用ngrok最简单：
```bash
ngrok http 1342
```
