# bot_sender.py 讲解

这个文件包含核心功能类 `TelegramBotSender`，负责发送消息。

---

## 原始代码

```python
import asyncio
from typing import Dict, Any, List, Union
from telethon import TelegramClient
from telethon.sessions import StringSession

from config import API_ID, API_HASH, PROXY


class TelegramBotSender:
    _instance = None

    def __new__(cls, session_string: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session_string = session_string
            cls._instance._client = None
            cls._instance._loop = None
        return cls._instance

    @property
    def client(self):
        if self._client is None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._client = TelegramClient(
                StringSession(self.session_string),
                API_ID,
                API_HASH,
                proxy=PROXY,
                loop=self._loop
            )
        return self._client

    async def connect(self):
        if not self.client.is_connected():
            await self.client.connect()

    async def send_message(
        self,
        target: str,
        text: str
    ) -> Dict[str, Any]:
        """向单个机器人/用户发送消息"""
        await self.connect()

        try:
            entity = await self.client.get_entity(target)
            message = await self.client.send_message(entity, text)

            return {
                "success": True,
                "message_id": message.id,
                "target": target,
                "text": text,
                "timestamp": str(message.date)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "target": target,
                "text": text
            }

    async def send_batch(
        self,
        messages: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """批量发送消息到多个目标"""

        Args:
            messages: [{"target": "@bot1", "text": "hello"}, {"target": "@bot2", "text": "hi"}]

        Returns:
            每条消息的发送结果列表

        await self.connect()
        results = []

        for msg in messages:
            result = await self.send_message(msg["target"], msg["text"])
            results.append(result)

        return results

    async def get_bot_response(
        self,
        target: str,
        text: str,
        timeout: float = 10.0
    ) -> Dict[str, Any]:
        """发送消息并等待回复"""
        await self.connect()

        try:
            entity = await self.client.get_entity(target)
            sent_msg = await self.client.send_message(entity, text)

            response = None
            async for message in self.client.iter_messages(
                entity,
                limit=10,
                min_id=sent_msg.id
            ):
                sender = message.sender
                if sender and sender.bot:
                    response = message
                    break

            if response:
                return {
                    "success": True,
                    "sent_message": text,
                    "response": response.text,
                    "response_id": response.id,
                    "target": target
                }
            else:
                return {
                    "success": True,
                    "sent_message": text,
                    "response": None,
                    "message": "未收到回复",
                    "target": target
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "target": target,
                "text": text
            }

    async def get_dialogs(self, limit: int = 20):
        """获取对话列表"""
        await self.connect()

        dialogs = []
        async for dialog in self.client.iter_dialogs(limit=limit):
            entity = dialog.entity
            dialogs.append({
                "name": dialog.name,
                "id": dialog.id,
                "username": getattr(entity, 'username', None),
                "is_bot": getattr(entity, 'bot', False),
                "unread_count": dialog.unread_count
            })

        return dialogs

    async def get_me(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        await self.connect()
        me = await self.client.get_me()
        return {
            "id": me.id,
            "first_name": me.first_name,
            "last_name": me.last_name,
            "username": me.username,
            "phone": me.phone
        }
```

---

## 第一部分：导入

```python
import asyncio
from typing import Dict, Any, List, Union
from telethon import TelegramClient
from telethon.sessions import StringSession

from config import API_ID, API_HASH, PROXY
```

| 导入 | 说明 |
|------|------|
| `asyncio` | 异步编程模块 |
| `typing` | 类型提示（帮助 IDE 和开发者理解代码） |
| `TelegramClient` | Telegram 客户端类 |
| `StringSession` | 字符串形式的会话 |
| `config` | 配置文件中的变量 |

**类型提示是什么？**

```python
from typing import Dict, Any, List

# 表示：参数是字符串列表，返回值是字典
def process(items: List[str]) -> Dict[str, Any]:
    ...
```

类型提示让代码更清晰，但 Python 不会强制检查。

---

## 第二部分：类定义和单例模式

### 类的基本结构

```python
class TelegramBotSender:
    _instance = None  # 类变量

    def __new__(cls, session_string: str):  # 特殊方法
        ...

    @property  # 装饰器
    def client(self):  # 实例方法
        ...

    async def send_message(self, target: str, text: str):  # 普通方法
        ...
```

### 类变量 vs 实例变量

```python
class Dog:
    species = "狗"        # 类变量，所有实例共享

    def __init__(self, name):
        self.name = name  # 实例变量，每个实例独有

dog1 = Dog("旺财")
dog2 = Dog("来福")

print(dog1.species)  # "狗"
print(dog2.species)  # "狗"
print(dog1.name)     # "旺财"
print(dog2.name)     # "来福"
```

---

### 单例模式详解

```python
class TelegramBotSender:
    _instance = None  # 类变量，存储唯一实例

    def __new__(cls, session_string: str):
        if cls._instance is None:           # 如果还没有实例
            cls._instance = super().__new__(cls)  # 创建实例
            cls._instance.session_string = session_string
            cls._instance._client = None
            cls._instance._loop = None
        return cls._instance  # 返回唯一实例
```

**什么是单例模式？**

单例模式确保一个类只有一个实例。

```
第一次创建 → 新建实例 → 保存到 _instance
第二次创建 → 发现已存在 → 返回已有实例
第三次创建 → 发现已存在 → 返回已有实例
```

**`__new__` vs `__init__`**

| 方法 | 作用 | 调用时机 |
|------|------|----------|
| `__new__` | 创建对象 | 先调用 |
| `__init__` | 初始化对象 | 后调用 |

```python
# 普通 __init__
class Person:
    def __init__(self, name):
        self.name = name

p = Person("张三")  # 先 __new__ 创建对象，再 __init__ 初始化
```

**为什么用单例？**

Telegram 客户端只需要一个连接，多个实例会浪费资源或导致冲突。

---

### @property 装饰器

```python
@property
def client(self):
    if self._client is None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._client = TelegramClient(
            StringSession(self.session_string),
            API_ID,
            API_HASH,
            proxy=PROXY,
            loop=self._loop
        )
    return self._client
```

**`@property` 是什么？**

把方法变成属性访问，更简洁。

```python
# 没有 @property
sender = TelegramBotSender(session)
client = sender.client()  # 需要加括号

# 有 @property
client = sender.client    # 像访问属性一样
```

**惰性加载（懒加载）：**

```python
if self._client is None:  # 只有第一次访问时才创建
    self._client = TelegramClient(...)
return self._client
```

- 第一次访问 `client` 时才创建 TelegramClient
- 之后直接返回已创建的实例
- 节省资源，只在需要时才创建

---

## 第三部分：方法详解

### connect 方法

```python
async def connect(self):
    if not self.client.is_connected():
        await self.client.connect()
```

**逻辑：**
1. 检查是否已连接
2. 如果没连接，才进行连接

这是"懒连接"模式：只在需要时才连接。

---

### send_message 方法

```python
async def send_message(
    self,
    target: str,
    text: str
) -> Dict[str, Any]:
    """向单个机器人/用户发送消息"""
    await self.connect()

    try:
        entity = await self.client.get_entity(target)
        message = await self.client.send_message(entity, text)

        return {
            "success": True,
            "message_id": message.id,
            "target": target,
            "text": text,
            "timestamp": str(message.date)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "target": target,
            "text": text
        }
```

**流程：**
```
连接服务器
    ↓
获取目标实体（用户/群组/频道）
    ↓
发送消息
    ↓
返回成功结果
    ↓
（如果出错）捕获异常，返回失败结果
```

**返回值设计：**

无论成功还是失败，都返回字典，包含 `success` 字段：

```python
# 成功
{"success": True, "message_id": 123, ...}

# 失败
{"success": False, "error": "错误信息", ...}
```

这种设计让调用者很容易判断结果。

---

### send_batch 方法

```python
async def send_batch(
    self,
    messages: List[Dict[str, str]]
) -> List[Dict[str, Any]]:
    """批量发送消息到多个目标"""
    await self.connect()
    results = []

    for msg in messages:
        result = await self.send_message(msg["target"], msg["text"])
        results.append(result)

    return results
```

**拆解：**
1. `messages` 是一个列表，每个元素是 `{"target": "...", "text": "..."}`
2. 用 `for` 循环遍历每个消息
3. 调用 `send_message` 发送
4. 把结果追加到 `results` 列表
5. 返回所有结果

**示例：**
```python
messages = [
    {"target": "@BotFather", "text": "hello"},
    {"target": "@userbot", "text": "hi"}
]

results = await sender.send_batch(messages)
# [{"success": True, ...}, {"success": True, ...}]
```

---

### get_bot_response 方法

```python
async def get_bot_response(
    self,
    target: str,
    text: str,
    timeout: float = 10.0
) -> Dict[str, Any]:
    """发送消息并等待回复"""
    await self.connect()

    try:
        entity = await self.client.get_entity(target)
        sent_msg = await self.client.send_message(entity, text)

        response = None
        async for message in self.client.iter_messages(
            entity,
            limit=10,
            min_id=sent_msg.id
        ):
            sender = message.sender
            if sender and sender.bot:
                response = message
                break
        ...
```

**`async for` 是什么？**

异步迭代器，用于遍历异步数据流。

```python
# 普通 for
for item in items:
    ...

# 异步 for（用于异步生成器）
async for item in async_items:
    ...
```

**`iter_messages` 参数：**
- `limit=10` - 最多获取 10 条消息
- `min_id=sent_msg.id` - 只获取 ID 比发送消息大的（即之后的）

**查找回复的逻辑：**
```
发送消息
    ↓
获取之后的消息
    ↓
遍历这些消息
    ↓
找到第一条来自机器人的消息
    ↓
返回这个回复
```

---

### get_dialogs 方法

```python
async def get_dialogs(self, limit: int = 20):
    """获取对话列表"""
    await self.connect()

    dialogs = []
    async for dialog in self.client.iter_dialogs(limit=limit):
        entity = dialog.entity
        dialogs.append({
            "name": dialog.name,
            "id": dialog.id,
            "username": getattr(entity, 'username', None),
            "is_bot": getattr(entity, 'bot', False),
            "unread_count": dialog.unread_count
        })

    return dialogs
```

**`getattr()` 函数：**

安全地获取对象属性，如果不存在则返回默认值。

```python
# 等价于 entity.username，但如果属性不存在不会报错
username = getattr(entity, 'username', None)

# 相当于：
try:
    username = entity.username
except AttributeError:
    username = None
```

---

### get_me 方法

```python
async def get_me(self) -> Dict[str, Any]:
    """获取当前用户信息"""
    await self.connect()
    me = await self.client.get_me()
    return {
        "id": me.id,
        "first_name": me.first_name,
        "last_name": me.last_name,
        "username": me.username,
        "phone": me.phone
    }
```

- `get_me()` 是 Telethon 提供的方法
- 返回当前登录用户的信息
- 我们把它转成字典返回

---

## 关键知识点总结

| 概念 | 语法 | 说明 |
|------|------|------|
| 类定义 | `class Name:` | 定义一个类 |
| `__new__` | `def __new__(cls, ...)` | 控制实例创建 |
| 单例模式 | `_instance` 类变量 | 确保只有一个实例 |
| `@property` | 装饰器 | 把方法变成属性 |
| 惰性加载 | `if self._x is None` | 延迟创建资源 |
| 类型提示 | `-> Dict[str, Any]` | 说明返回类型 |
| 异步方法 | `async def` | 可以使用 await |
| `getattr()` | `getattr(obj, 'attr', default)` | 安全获取属性 |

---

## 练习

1. 理解单例模式：为什么 Telegram 客户端需要单例？
2. 理解 `@property`：它有什么好处？
3. 尝试添加一个新方法 `get_chat_history(target, limit=10)`
