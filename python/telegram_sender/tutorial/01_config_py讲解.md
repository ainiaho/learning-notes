# config.py 讲解

这是项目中最简单的文件，用来存储配置信息。

---

## 原始代码

```python
# Telegram API 凭证（从 https://my.telegram.org 获取）
API_ID = 31630651
API_HASH = "be85c71fb7ec7ffbed31328bb99f683f"
PHONE = "+18149001586"

# 如果有两步验证密码
PASSWORD = ""  # 可选

# Session String（运行 login.py 后获取）
SESSION_STRING = "1BVtsOHEBu5-j2XpfOYXoo9eMT0Km4-..."

# 代理设置（如需要）
PROXY = None
# PROXY = ("socks5", "127.0.0.1", 1080)  # 取消注释并配置代理
```

---

## 逐行讲解

### 第 1 行：注释
```python
# Telegram API 凭证（从 https://my.telegram.org 获取）
```

- `#` 开头的是**注释**，程序不会执行
- 注释用来解释代码的作用
- 中文注释完全没问题

---

### 第 2 行：整数变量
```python
API_ID = 31630651
```

**拆解：**
- `API_ID` 是变量名
- `=` 是赋值符号（不是"等于"的意思）
- `31630651` 是一个**整数**类型的值

**命名规范：**
- Python 推荐用**全大写**命名常量
- 用**下划线**分隔单词：`API_ID`、`MAX_SIZE`

---

### 第 3 行：字符串变量
```python
API_HASH = "be85c71fb7ec7ffbed31328bb99f683f"
```

**拆解：**
- `API_HASH` 是变量名
- `"..."` 双引号表示这是一个**字符串**（文本）
- 单引号 `'...'` 效果相同

---

### 第 4 行：字符串变量
```python
PHONE = "+18149001586"
```

电话号码用字符串存储，因为：
- 可能包含 `+` 号
- 不需要进行数学运算

---

### 第 7 行：空字符串
```python
PASSWORD = ""  # 可选
```

- `""` 是**空字符串**（长度为0）
- `# 可选` 是行内注释
- 如果没有两步验证密码，就保持为空

---

### 第 10 行：很长的字符串
```python
SESSION_STRING = "1BVtsOHEBu5-j2XpfOYXoo9eMT0Km4-..."
```

这是登录后获取的会话凭证，是一个很长的字符串。
- 它包含了你的登录状态
- 相当于"记住密码"功能
- 有了它就不需要每次都输入验证码

---

### 第 13 行：None 值
```python
PROXY = None
```

- `None` 是 Python 的**空值**，表示"什么都没有"
- 类似其他语言的 `null` 或 `nil`
- 这里表示不使用代理

---

### 第 14 行：注释掉的代码
```python
# PROXY = ("socks5", "127.0.0.1", 1080)  # 取消注释并配置代理
```

- 这行被 `#` 注释掉了，不会执行
- 如果需要代理，删掉开头的 `#` 就可以启用
- `("socks5", "127.0.0.1", 1080)` 是一个**元组**（不可修改的列表）

---

## 这里的数据类型汇总

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `API_ID` | int | 整数，API ID |
| `API_HASH` | str | 字符串，API 密钥 |
| `PHONE` | str | 字符串，手机号 |
| `PASSWORD` | str | 字符串，可为空 |
| `SESSION_STRING` | str | 字符串，会话凭证 |
| `PROXY` | None 或 tuple | 空值或元组 |

---

## 如何在其他文件中使用？

其他文件通过 `import` 导入这些变量：

```python
from config import API_ID, API_HASH, PHONE
```

这样就可以使用 `config.py` 中定义的变量了。

---

## 练习

1. 创建一个新变量 `BOT_USERNAME = "@BotFather"`
2. 试着打印这些变量：
   ```python
   print(API_ID)
   print(f"手机号是: {PHONE}")
   ```

---

## 安全提示

真实项目中，敏感信息不应该直接写在代码里。更好的做法：

```python
import os

# 从环境变量读取
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
```

这样可以避免把密码泄露到代码仓库中。
