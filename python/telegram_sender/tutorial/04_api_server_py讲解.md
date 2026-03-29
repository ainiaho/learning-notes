# api_server.py 讲解

这是项目的核心文件，提供 REST API 服务。

---

## 原始代码（分段讲解）

### 第一部分：导入和初始化

```python
from quart import Quart, request, jsonify
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import uuid

from bot_sender import TelegramBotSender
from config import SESSION_STRING

app = Quart(__name__)

# 初始化 sender 和调度器
sender = TelegramBotSender(SESSION_STRING)
scheduler = AsyncIOScheduler()

# 存储定时任务
scheduled_jobs = {}
```

**导入说明：**

| 模块 | 说明 |
|------|------|
| `quart` | 异步 Web 框架（类似 Flask，但支持异步） |
| `apscheduler` | 定时任务调度器 |
| `datetime` | 日期时间处理 |
| `uuid` | 生成唯一 ID |

**Quart vs Flask：**

| 特性 | Flask | Quart |
|------|-------|-------|
| 异步支持 | 否 | 是 |
| 语法 | 相同 | 相同 |
| 性能 | 普通 | 高并发更好 |

**初始化流程：**
```
创建 Quart 应用实例
    ↓
创建 TelegramBotSender 实例
    ↓
创建调度器实例
    ↓
创建空字典存储定时任务
```

---

### 第二部分：生命周期钩子

```python
@app.before_serving
async def startup():
    """服务启动前初始化"""
    scheduler.start()
    print("调度器已启动")


@app.after_serving
async def shutdown():
    """服务关闭时清理"""
    scheduler.shutdown()
    print("调度器已关闭")
```

**什么是钩子（Hook）？**

钩子是在特定时机自动执行的函数。

```
服务器启动 ────→ 执行 before_serving
                  ↓
              服务运行中...
                  ↓
服务器关闭 ────→ 执行 after_serving
```

**装饰器语法：**

```python
@app.before_serving
async def startup():
    ...
```

等价于：

```python
async def startup():
    ...

startup = app.before_serving(startup)
```

装饰器把函数"注册"到特定事件上。

---

### 第三部分：路由基础

#### 什么是路由？

路由就是把 URL 和函数对应起来。

```
GET /health ────→ health() 函数
POST /send   ────→ send_message() 函数
```

#### 健康检查路由

```python
@app.route("/health", methods=["GET"])
async def health():
    """健康检查"""
    try:
        me = await sender.get_me()
        return jsonify({"status": "ok", "user": me})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
```

**拆解：**

- `@app.route("/health", methods=["GET"])` - 注册路由
- `async def health():` - 异步处理函数
- `jsonify(...)` - 把字典转成 JSON 响应
- `500` - HTTP 状态码（服务器错误）

**HTTP 状态码：**

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 客户端错误 |
| 404 | 未找到 |
| 500 | 服务器错误 |

---

### 第四部分：发送消息路由

```python
@app.route("/send", methods=["POST"])
async def send_message():
    """发送消息给单个目标

    Body:
    {
        "target": "@BotUsername",
        "text": "/start"
    }
    """
    data = await request.get_json()

    if not data:
        return jsonify({"error": "缺少请求体"}), 400

    target = data.get("target") or data.get("bot")  # 兼容旧参数
    text = data.get("text")

    if not target or not text:
        return jsonify({"error": "缺少 target 或 text 参数"}), 400

    result = await sender.send_message(target, text)

    if result["success"]:
        return jsonify(result)
    else:
        return jsonify(result), 500
```

**获取请求体：**

```python
data = await request.get_json()
# data = {"target": "@BotFather", "text": "/start"}
```

**参数获取：**

```python
target = data.get("target") or data.get("bot")
# 如果 target 不存在，尝试用 bot（兼容旧版本）
```

**`data.get()` vs `data["key"]`：**

```python
# 用 get，键不存在返回 None，不报错
data.get("target")  # 返回 None 或值

# 用方括号，键不存在会报错
data["target"]  # 可能抛出 KeyError
```

**返回响应：**

```python
# 成功，返回 200（默认）
return jsonify(result)

# 失败，返回 500
return jsonify(result), 500
```

---

### 第五部分：批量发送路由

```python
@app.route("/send-batch", methods=["POST"])
async def send_batch():
    """批量发送消息"""
    data = await request.get_json()

    if not data:
        return jsonify({"error": "缺少请求体"}), 400

    messages = data.get("messages")

    if not messages or not isinstance(messages, list):
        return jsonify({"error": "缺少 messages 数组参数"}), 400

    results = await sender.send_batch(messages)
    success_count = sum(1 for r in results if r["success"])

    return jsonify({
        "total": len(messages),
        "success": success_count,
        "failed": len(messages) - success_count,
        "results": results
    })
```

**`isinstance()` 函数：**

检查变量类型。

```python
isinstance([1, 2, 3], list)  # True
isinstance("hello", list)    # False
isinstance(123, int)         # True
```

**列表推导式统计：**

```python
success_count = sum(1 for r in results if r["success"])
```

等价于：

```python
count = 0
for r in results:
    if r["success"]:
        count += 1
success_count = count
```

---

### 第六部分：发送并等待回复

```python
@app.route("/send-and-wait", methods=["POST"])
async def send_and_wait():
    """发送消息并等待回复"""
    data = await request.get_json()

    if not data:
        return jsonify({"error": "缺少请求体"}), 400

    target = data.get("target") or data.get("bot")
    text = data.get("text")
    timeout = data.get("timeout", 10.0)  # 默认 10 秒

    if not target or not text:
        return jsonify({"error": "缺少 target 或 text 参数"}), 400

    result = await sender.get_bot_response(target, text, timeout)

    return jsonify(result)
```

**默认参数：**

```python
timeout = data.get("timeout", 10.0)
# 如果 timeout 不存在，使用默认值 10.0
```

---

### 第七部分：定时任务 - 创建

```python
@app.route("/schedule", methods=["POST"])
async def schedule_message():
    """创建定时发送任务"""
    data = await request.get_json()

    # ... 参数验证 ...

    job_id = str(uuid.uuid4())[:8]  # 生成 8 位 ID
    schedule_type = schedule.get("type", "once")

    # 创建触发器
    if schedule_type == "once":
        dt_str = schedule.get("datetime")
        run_date = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        trigger = DateTrigger(run_date=run_date)

    elif schedule_type == "interval":
        interval = schedule.get("interval")
        trigger = IntervalTrigger(seconds=interval)

    elif schedule_type == "cron":
        cron_expr = schedule.get("cron")
        trigger = CronTrigger.from_crontab(cron_expr)

    # 添加任务
    job = scheduler.add_job(
        sender.send_message,   # 要执行的函数
        trigger=trigger,       # 触发器
        args=[target, text],   # 传递给函数的参数
        id=job_id,
        name=f"Send to {target}"
    )

    # 保存任务信息
    scheduled_jobs[job_id] = {
        "job_id": job_id,
        "target": target,
        "text": text,
        "schedule_type": schedule_type,
        "next_run": str(job.next_run_time),
        "status": "active"
    }

    return jsonify({
        "success": True,
        "job_id": job_id,
        "next_run": str(job.next_run_time)
    })
```

**UUID 生成：**

```python
import uuid

uuid.uuid4()          # 生成完整 UUID
# 'd3ec5b21-a957-4b8f-9c2d-123456789abc'

str(uuid.uuid4())[:8] # 取前 8 位
# 'd3ec5b21'
```

**日期解析：**

```python
from datetime import datetime

dt_str = "2026-03-29 15:30:00"
run_date = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

# 格式说明：
# %Y - 年（4位）
# %m - 月（01-12）
# %d - 日（01-31）
# %H - 小时（00-23）
# %M - 分钟（00-59）
# %S - 秒（00-59）
```

**调度器添加任务：**

```python
job = scheduler.add_job(
    func,           # 要执行的函数
    trigger,        # 触发器（决定何时执行）
    args=[...],     # 位置参数
    kwargs={...},   # 关键字参数
    id="job_id"     # 任务 ID
)
```

---

### 第八部分：定时任务 - 查询和删除

#### 查询任务列表

```python
@app.route("/schedule/list", methods=["GET"])
async def list_scheduled():
    """获取所有定时任务"""
    return jsonify({
        "jobs": list(scheduled_jobs.values()),
        "total": len(scheduled_jobs)
    })
```

**字典转列表：**

```python
scheduled_jobs = {
    "abc1": {"job_id": "abc1", "target": "@BotFather", ...},
    "def2": {"job_id": "def2", "target": "@user", ...}
}

list(scheduled_jobs.values())
# [{"job_id": "abc1", ...}, {"job_id": "def2", ...}]
```

#### 删除任务

```python
@app.route("/schedule/<job_id>", methods=["DELETE"])
async def cancel_scheduled(job_id):
    """取消定时任务"""
    if job_id not in scheduled_jobs:
        return jsonify({"error": "任务不存在"}), 404

    scheduler.remove_job(job_id)
    scheduled_jobs[job_id]["status"] = "cancelled"
    del scheduled_jobs[job_id]

    return jsonify({"success": True, "message": f"任务 {job_id} 已取消"})
```

**URL 参数：**

```python
@app.route("/schedule/<job_id>", methods=["DELETE"])
#                              ↑
#                    URL 中的动态参数

# 请求：DELETE /schedule/abc123
# job_id = "abc123"
```

**字典操作：**

```python
# 检查键是否存在
if job_id in scheduled_jobs:

# 删除键值对
del scheduled_jobs[job_id]
```

---

### 第九部分：其他路由

```python
@app.route("/dialogs", methods=["GET"])
async def get_dialogs():
    """获取对话列表"""
    limit = request.args.get("limit", 20, type=int)
    dialogs = await sender.get_dialogs(limit)
    return jsonify({"dialogs": dialogs})


@app.route("/me", methods=["GET"])
async def get_me():
    """获取当前用户信息"""
    me = await sender.get_me()
    return jsonify(me)
```

**查询参数：**

```python
# URL: /dialogs?limit=10

limit = request.args.get("limit", 20, type=int)
#                               ↑     ↑
#                            默认值  类型转换
```

---

### 第十部分：启动服务

```python
if __name__ == "__main__":
    print("启动 Telegram Bot Sender API...")
    print()
    print("接口文档:")
    print("  消息发送:")
    print("    POST /send           - 发送单条消息")
    print("    POST /send-batch     - 批量发送消息")
    print("    POST /send-and-wait  - 发送并等待回复")
    print()
    # ... 更多打印 ...

    app.run(host="0.0.0.0", port=5000, debug=False)
```

**`app.run()` 参数：**

| 参数 | 说明 |
|------|------|
| `host` | 监听地址，`0.0.0.0` 表示所有网卡 |
| `port` | 端口号 |
| `debug` | 调试模式，True 会自动重载代码 |

---

## 完整架构图

```
┌─────────────────────────────────────────────────────┐
│                    API Server                        │
│                   (api_server.py)                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │   Routes     │  │  Scheduler   │                 │
│  │  (路由层)    │  │  (调度器)    │                 │
│  └──────┬───────┘  └──────┬───────┘                 │
│         │                 │                          │
│         └────────┬────────┘                          │
│                  ↓                                   │
│  ┌───────────────────────────┐                      │
│  │    TelegramBotSender      │                      │
│  │     (bot_sender.py)       │                      │
│  └─────────────┬─────────────┘                      │
│                ↓                                     │
│  ┌───────────────────────────┐                      │
│  │     TelegramClient        │                      │
│  │      (telethon)           │                      │
│  └───────────────────────────┘                      │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 关键知识点总结

| 概念 | 语法 | 说明 |
|------|------|------|
| 路由装饰器 | `@app.route("/path")` | 注册 URL 路由 |
| 异步视图 | `async def handler():` | 异步处理请求 |
| 获取 JSON | `await request.get_json()` | 解析请求体 |
| 返回 JSON | `jsonify(data)` | 转换为 JSON 响应 |
| URL 参数 | `@app.route("/<id>")` | 获取动态 URL 部分 |
| 查询参数 | `request.args.get("key")` | 获取 URL `?key=value` |
| 生命周期钩子 | `@app.before_serving` | 服务启动/关闭时执行 |
| 调度器 | `scheduler.add_job()` | 添加定时任务 |

---

## REST API 设计原则

这个 API 遵循 RESTful 设计：

| 操作 | HTTP 方法 | URL |
|------|-----------|-----|
| 发送消息 | POST | /send |
| 查询任务 | GET | /schedule/list |
| 删除任务 | DELETE | /schedule/{id} |

**状态码使用：**

- `200` - 成功
- `400` - 客户端参数错误
- `404` - 资源不存在
- `500` - 服务器内部错误

---

## 练习

1. 添加一个新的路由 `GET /status`，返回服务状态
2. 思考：为什么消息发送用 POST 而不是 GET？
3. 尝试添加一个批量取消任务的接口
