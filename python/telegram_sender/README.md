# Telegram Bot Sender API

个人账户向机器人/用户自动发送消息的 API 服务。

## 快速开始

### 1. 安装依赖

```bash
cd /home/kali/workspace/telegram_sender
pip install -r requirements.txt
```

### 2. 配置

编辑 `config.py`：

```python
API_ID = 31630651
API_HASH = "be85c71fb7ec7ffbed31328bb99f683f"
PHONE = "+18149001586"
SESSION_STRING = "你的session字符串"
```

### 3. 首次登录获取 Session

```bash
python login.py
```

按提示输入验证码，将输出的 `SESSION_STRING` 保存到 `config.py`。

### 4. 启动服务

```bash
python api_server.py
```

服务地址：`http://localhost:5000`

---

## API 接口

### 基础接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /health | 健康检查 |
| GET | /me | 获取当前用户信息 |
| GET | /dialogs | 获取对话列表 |

### 消息发送

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /send | 发送单条消息 |
| POST | /send-batch | 批量发送消息 |
| POST | /send-and-wait | 发送并等待回复 |

### 定时任务

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /schedule | 创建定时任务 |
| POST | /schedule-batch | 批量创建定时任务 |
| GET | /schedule/list | 获取任务列表 |
| DELETE | /schedule/{job_id} | 取消任务 |

---

## 详细说明

### 1. 发送单条消息

**POST** `/send`

请求体：
```json
{
    "target": "@BotFather",
    "text": "/start"
}
```

响应：
```json
{
    "success": true,
    "message_id": 123,
    "target": "@BotFather",
    "text": "/start",
    "timestamp": "2026-03-29 12:00:00"
}
```

### 2. 批量发送消息

**POST** `/send-batch`

请求体：
```json
{
    "messages": [
        {"target": "@BotFather", "text": "/start"},
        {"target": "@userbot", "text": "hello"},
        {"target": "123456789", "text": "用户ID也可以"}
    ]
}
```

响应：
```json
{
    "total": 3,
    "success": 3,
    "failed": 0,
    "results": [
        {"success": true, "target": "@BotFather", "text": "/start", ...},
        {"success": true, "target": "@userbot", "text": "hello", ...},
        {"success": true, "target": "123456789", "text": "用户ID也可以", ...}
    ]
}
```

### 3. 发送并等待回复

**POST** `/send-and-wait`

请求体：
```json
{
    "target": "@BotFather",
    "text": "/mybots",
    "timeout": 10
}
```

响应：
```json
{
    "success": true,
    "sent_message": "/mybots",
    "response": "BotFather的回复内容...",
    "response_id": 456,
    "target": "@BotFather"
}
```

---

## 定时任务

### 定时类型

| type | 说明 | 参数 |
|------|------|------|
| once | 一次执行 | datetime: "YYYY-MM-DD HH:MM:SS" |
| interval | 间隔重复 | interval: 秒数 |
| cron | Cron表达式 | cron: "分 时 日 月 周" |

### 4. 创建定时任务

**POST** `/schedule`

#### 一次执行

```json
{
    "target": "@BotFather",
    "text": "定时消息",
    "schedule": {
        "type": "once",
        "datetime": "2026-03-29 15:30:00"
    }
}
```

#### 间隔重复

每 60 秒发送一次：
```json
{
    "target": "@BotFather",
    "text": "每分钟发送",
    "schedule": {
        "type": "interval",
        "interval": 60
    }
}
```

#### Cron 表达式

每天 9:00 发送：
```json
{
    "target": "@BotFather",
    "text": "早上好",
    "schedule": {
        "type": "cron",
        "cron": "0 9 * * *"
    }
}
```

Cron 表达式示例：

| 表达式 | 说明 |
|--------|------|
| `0 9 * * *` | 每天 9:00 |
| `30 18 * * *` | 每天 18:30 |
| `0 9,18 * * *` | 每天 9:00 和 18:00 |
| `0 9 * * 1-5` | 周一到周五 9:00 |
| `0 */2 * * *` | 每 2 小时 |

响应：
```json
{
    "success": true,
    "job_id": "a1b2c3d4",
    "next_run": "2026-03-29 15:30:00+00:00"
}
```

### 5. 批量定时任务

**POST** `/schedule-batch`

请求体：
```json
{
    "messages": [
        {"target": "@bot1", "text": "消息1"},
        {"target": "@bot2", "text": "消息2"}
    ],
    "schedule": {
        "type": "once",
        "datetime": "2026-03-29 16:00:00"
    }
}
```

### 6. 查看定时任务列表

**GET** `/schedule/list`

响应：
```json
{
    "jobs": [
        {
            "job_id": "a1b2c3d4",
            "target": "@BotFather",
            "text": "定时消息",
            "schedule_type": "once",
            "next_run": "2026-03-29 15:30:00+00:00",
            "status": "active"
        }
    ],
    "total": 1
}
```

### 7. 取消定时任务

**DELETE** `/schedule/{job_id}`

响应：
```json
{
    "success": true,
    "message": "任务 a1b2c3d4 已取消"
}
```

---

## 其他接口

### 健康检查

**GET** `/health`

响应：
```json
{
    "status": "ok",
    "user": {
        "id": 123456789,
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "phone": "18149001586"
    }
}
```

### 获取用户信息

**GET** `/me`

### 获取对话列表

**GET** `/dialogs?limit=20`

响应：
```json
{
    "dialogs": [
        {
            "name": "BotFather",
            "id": 93372553,
            "username": "BotFather",
            "is_bot": true,
            "unread_count": 0
        }
    ]
}
```

---

## Target 参数说明

| 格式 | 示例 | 说明 |
|------|------|------|
| 用户名 | `@BotFather` | 带 @ 的用户名 |
| 用户ID | `123456789` | 数字ID |
| 群组 | `groupname` | 群组用户名 |
| 频道 | `channelname` | 频道用户名 |

---

## 使用示例

### curl

```bash
# 发送消息
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"target": "@BotFather", "text": "/start"}'

# 批量发送
curl -X POST http://localhost:5000/send-batch \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"target": "@bot1", "text": "hello"}, {"target": "@bot2", "text": "hi"}]}'

# 定时任务
curl -X POST http://localhost:5000/schedule \
  -H "Content-Type: application/json" \
  -d '{"target": "@BotFather", "text": "定时消息", "schedule": {"type": "once", "datetime": "2026-03-29 15:30:00"}}'

# 查看任务
curl http://localhost:5000/schedule/list

# 取消任务
curl -X DELETE http://localhost:5000/schedule/a1b2c3d4
```

### Python

```python
import requests

API_URL = "http://localhost:5000"

# 发送消息
resp = requests.post(f"{API_URL}/send", json={
    "target": "@BotFather",
    "text": "/start"
})
print(resp.json())

# 批量发送
resp = requests.post(f"{API_URL}/send-batch", json={
    "messages": [
        {"target": "@bot1", "text": "hello"},
        {"target": "@bot2", "text": "hi"}
    ]
})
print(resp.json())

# 创建定时任务
resp = requests.post(f"{API_URL}/schedule", json={
    "target": "@BotFather",
    "text": "定时消息",
    "schedule": {
        "type": "once",
        "datetime": "2026-03-29 15:30:00"
    }
})
print(resp.json())
```

---

## 文件结构

```
telegram_sender/
├── config.py          # 配置文件
├── login.py           # 登录工具
├── bot_sender.py      # 核心功能类
├── api_server.py      # API 服务
├── requirements.txt   # 依赖
└── README.md          # 文档
```

## 获取 API 凭证

1. 访问 https://my.telegram.org
2. 输入手机号获取验证码
3. 点击 API Development tools
4. 创建应用获取 `api_id` 和 `api_hash`

## 注意事项

- 首次运行需要登录获取 Session
- Session 有效期较长，无需重复登录
- 避免频繁发送消息，防止账号限制
- 定时任务在服务重启后需要重新创建
