# Python 基础入门

欢迎来到 Python 的世界！这份文档会帮助你从零开始理解项目中的代码。

---

## 写在前面：编程是什么？

编程就是**给计算机下命令**，让它帮你做事。

就像你告诉朋友：
> "帮我买一杯咖啡，要热的，加糖"

编程就是用代码告诉计算机：
> "帮我发送一条消息，发给 @BotFather，内容是 /start"

---

## 一、Python 是什么？

Python 是一种**编程语言**，就像汉语、英语是人类语言一样。

| 对比 | 人类语言 | 编程语言 |
|------|----------|----------|
| 用途 | 人与人交流 | 人与计算机交流 |
| 例子 | 汉语、英语 | Python、JavaScript |
| 特点 | 有歧义 | 必须精确 |

### 为什么选 Python？

```
其他语言写循环：
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

Python 写循环：
for i in range(10):
    print(i)
```

Python 更简洁，更像人说话！

### 怎么运行 Python？

```bash
# 方法1：直接运行文件
python hello.py

# 方法2：进入交互模式（像计算器一样）
python
>>> print("Hello")
Hello
>>> 1 + 1
2
>>> exit()    # 退出
```

---

## 二、变量 —— 给数据起名字

### 什么是变量？

想象你有很多盒子，每个盒子装一样东西。为了方便找，你在盒子上贴了标签。

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    name     │    │     age     │    │    city     │
│   "小明"    │    │     18      │    │   "北京"    │
└─────────────┘    └─────────────┘    └─────────────┘
```

这就是变量：**变量名 = 标签，变量值 = 盒子里的东西**。

### 创建变量

```python
# 创建变量：名字 = 值
name = "小明"
age = 18
is_student = True

# 使用变量：用名字找值
print(name)        # 小明
print(age)         # 18
```

**重要：** `=` 不是"等于"，是"赋值"！把右边的东西放进左边的盒子里。

```python
x = 5        # 把 5 放进叫 x 的盒子
x = x + 1    # 把 x 盒子的值取出来，加1，再放回去
print(x)     # 6
```

### 变量命名规则

```python
# ✅ 正确的名字
user_name = "张三"      # 用下划线连接（推荐）
userName = "李四"       # 驼峰命名
age1 = 20              # 可以有数字
_private = "秘密"       # 下划线开头表示"私有的"

# ❌ 错误的名字
1name = "错误"          # 不能数字开头
user-name = "错误"      # 减号会被当成减法
my name = "错误"        # 不能有空格
class = "错误"          # 不能用 Python 关键字
```

### 命名建议

```python
# 好的名字：见名知意
user_age = 18
total_price = 99.9
is_logged_in = True

# 不好的名字：看不懂
a = 18
x = 99.9
flag = True
```

### 变量可以改变类型

```python
x = 10          # x 是整数
x = "hello"     # x 变成字符串（Python 允许，但不推荐）
```

---

## 三、数据类型 —— 数据的种类

就像超市里不同商品放不同货架，不同数据有不同类型。

### 1. 字符串（str）—— 文字

用引号包起来的就是字符串。

```python
# 单引号、双引号都可以
name = '小明'
city = "北京"

# 三引号：多行文字
poem = '''
床前明月光，
疑是地上霜。
'''

# 为什么需要引号？
# 没有引号，Python 会把它当成变量名
name = 小明      # ❌ 错误：小明是谁？
name = "小明"    # ✅ 正确：这是一个文字
```

#### 字符串常用操作

```python
# 拼接
first = "Hello"
last = "World"
full = first + " " + last
print(full)           # Hello World

# 重复
line = "-" * 20
print(line)           # --------------------

# 长度
print(len("小明"))     # 2（两个汉字）

# 包含判断
text = "我喜欢Python"
print("Python" in text)    # True
print("Java" in text)      # False

# 取出单个字符
text = "Python"
print(text[0])        # P（第1个）
print(text[-1])       # n（最后1个）

# 取出部分（切片）
text = "Python"
print(text[0:3])      # Pyt（第1到第3个，不含第4个）
print(text[:3])       # Pyt（从头取3个）
print(text[3:])       # hon（从第4个取到最后）
```

#### 字符串格式化

```python
name = "小明"
age = 18

# 方法1：f-string（推荐，Python 3.6+）
message = f"我叫{name}，今年{age}岁"
print(message)        # 我叫小明，今年18岁

# 方法2：format()
message = "我叫{}，今年{}岁".format(name, age)

# 方法3：百分号（老写法）
message = "我叫%s，今年%d岁" % (name, age)
```

**f-string 进阶：**

```python
price = 19.999
count = 5

print(f"单价：{price:.2f}元")      # 保留2位小数：单价：20.00元
print(f"数量：{count:03d}")         # 补零到3位：数量：005
print(f"总价：{price * count}元")   # 可以计算：总价：99.995元
```

**什么时候用字符串？**
- 名字、地址、描述
- 消息内容
- API 密钥、Token
- 文件路径

---

### 2. 整数（int）—— 整数

没有小数点的数字。

```python
age = 18
count = 100
temperature = -10      # 可以是负数
big_number = 1_000_000 # 可以用下划线分隔，更易读（Python 3.6+）
```

#### 整数运算

```python
a = 10
b = 3

print(a + b)     # 13（加）
print(a - b)     # 7（减）
print(a * b)     # 30（乘）
print(a / b)     # 3.333...（除，结果是浮点数）
print(a // b)    # 3（整除，只取整数部分）
print(a % b)     # 1（取余数，10除以3余1）
print(a ** b)    # 100（幂运算，10的3次方）
```

**整除和取余的妙用：**

```python
# 分离分钟和秒
total_seconds = 125
minutes = total_seconds // 60    # 2（分钟）
seconds = total_seconds % 60     # 5（剩余秒数）
print(f"{minutes}分{seconds}秒")  # 2分5秒

# 判断奇偶
num = 7
if num % 2 == 0:
    print("偶数")
else:
    print("奇数")
```

**什么时候用整数？**
- 年龄、数量、次数
- ID（用户ID、消息ID）
- 排名、分数
- 索引位置

---

### 3. 浮点数（float）—— 小数

有小数点的数字。

```python
price = 99.9
pi = 3.14159265358979
temp = -0.5
scientific = 1.5e10    # 科学计数法：15000000000.0
```

**浮点数的坑：**

```python
# 计算机存储小数有精度问题
print(0.1 + 0.2)    # 0.30000000000000004（不是精确的0.3）

# 解决方法：用 round() 四舍五入
result = 0.1 + 0.2
print(round(result, 2))    # 0.3（保留2位小数）
```

**什么时候用浮点数？**
- 价格、金额
- 温度、速度
- 比例、百分比
- 科学计算

---

### 4. 布尔值（bool）—— 真或假

只有两个值：`True`（真）和 `False`（假）。

```python
is_adult = True
has_license = False

# 注意：首字母必须大写！
true   # ❌ 错误
True   # ✅ 正确
```

#### 布尔运算

```python
# 与（and）：两个都真才真
print(True and True)    # True
print(True and False)   # False

# 或（or）：有一个真就真
print(True or False)    # True
print(False or False)   # False

# 非（not）：取反
print(not True)         # False
print(not False)        # True
```

#### 什么算"真"？

```python
# 这些都是 False
bool(0)         # False
bool(0.0)       # False
bool("")        # False（空字符串）
bool([])        # False（空列表）
bool({})        # False（空字典）
bool(None)      # False

# 其他的都是 True
bool(1)         # True
bool(-1)        # True
bool("hello")   # True
bool([0])       # True（列表有元素）
```

**什么时候用布尔值？**
- 开关状态（开/关、是/否）
- 条件判断
- 验证结果（成功/失败）

---

### 5. None —— 空值

表示"什么都没有"或"不存在"。

```python
result = None      # 还没有结果

# 常见用途：
# 1. 函数没有返回值时
def greet():
    print("Hello")
    # 没有 return，默认返回 None

# 2. 表示"无"的状态
user = get_user(999)    # 用户不存在时返回 None
if user is None:
    print("用户不存在")

# 3. 作为默认值
def search(query, limit=None):
    if limit is None:
        limit = 10    # 默认查询10条
```

**None vs 0 vs 空字符串：**

```python
# 它们不一样！
value1 = None       # 没有值
value2 = 0          # 值是0
value3 = ""         # 值是空字符串

# 判断是否是 None
if value is None:           # ✅ 推荐
if value == None:           # ❌ 不推荐
```

---

### 类型转换

```python
# 字符串转数字
num_str = "123"
num = int(num_str)          # 123（整数）
num = float("3.14")         # 3.14（浮点数）

# 数字转字符串
age = 18
age_str = str(age)          # "18"

# 布尔转换
bool(1)         # True
bool(0)         # False
bool("")        # False
bool("hello")   # True

# 查看类型
x = 123
print(type(x))              # <class 'int'>
print(type(x).__name__)     # 'int'
```

---

## 四、列表（List）—— 有序的盒子们

### 什么是列表？

列表就是**一排有顺序的盒子**，每个盒子里放一样东西。

```
索引:     0       1       2       3
       ┌───────┬───────┬───────┬───────┐
       │ "苹果" │ "香蕉" │ "橙子" │ "葡萄" │
       └───────┴───────┴───────┴───────┘
索引:    -4      -3      -2      -1
```

- **索引从 0 开始**（第一个是0，不是1）
- **负数索引**从后往前数（-1是最后一个）

### 创建列表

```python
# 创建列表
fruits = ["苹果", "香蕉", "橙子"]
numbers = [1, 2, 3, 4, 5]
mixed = ["小明", 18, True, 99.9]    # 可以放不同类型

# 空列表
empty1 = []
empty2 = list()

# 创建相同元素的列表
zeros = [0] * 5       # [0, 0, 0, 0, 0]
```

### 访问元素

```python
fruits = ["苹果", "香蕉", "橙子", "葡萄"]

# 用索引取元素
print(fruits[0])      # 苹果（第1个）
print(fruits[2])      # 橙子（第3个）
print(fruits[-1])     # 葡萄（最后1个）
print(fruits[-2])     # 橙子（倒数第2个）

# 索引超出范围会报错
print(fruits[10])     # IndexError: list index out of range
```

### 切片 —— 取出一部分

```python
fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]

# 语法：列表[开始:结束]（不包含结束位置）
print(fruits[1:3])    # ["香蕉", "橙子"]（索引1到2）
print(fruits[:3])     # ["苹果", "香蕉", "橙子"]（从头取3个）
print(fruits[2:])     # ["橙子", "葡萄", "西瓜"]（从索引2到最后）
print(fruits[::2])    # ["苹果", "橙子", "西瓜"]（每隔1个取1个）
print(fruits[::-1])   # ["西瓜", "葡萄", "橙子", "香蕉", "苹果"]（反转）

# 切片不会报错，超出范围会自动调整
print(fruits[2:100])  # ["橙子", "葡萄", "西瓜"]
```

### 修改列表

```python
fruits = ["苹果", "香蕉", "橙子"]

# 修改元素
fruits[0] = "西瓜"
print(fruits)         # ["西瓜", "香蕉", "橙子"]

# 添加元素
fruits.append("葡萄")           # 加到最后
print(fruits)         # ["西瓜", "香蕉", "橙子", "葡萄"]

fruits.insert(1, "草莓")         # 插入到位置1
print(fruits)         # ["西瓜", "草莓", "香蕉", "橙子", "葡萄"]

# 删除元素
fruits.remove("香蕉")            # 删除指定值
print(fruits)         # ["西瓜", "草莓", "橙子", "葡萄"]

del fruits[0]                    # 删除指定位置
print(fruits)         # ["草莓", "橙子", "葡萄"]

last = fruits.pop()              # 删除并返回最后一个
print(last)           # 葡萄
print(fruits)         # ["草莓", "橙子"]

item = fruits.pop(0)             # 删除并返回指定位置
print(item)           # 草莓
```

### 列表常用操作

```python
fruits = ["苹果", "香蕉", "橙子", "香蕉"]

# 长度
print(len(fruits))              # 4

# 查找
print("苹果" in fruits)          # True
print("西瓜" in fruits)          # False
print(fruits.index("香蕉"))      # 1（第一个香蕉的位置）
print(fruits.count("香蕉"))      # 2（香蕉出现2次）

# 排序
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()                  # 排序（修改原列表）
print(numbers)        # [1, 1, 2, 3, 4, 5, 6, 9]

numbers.reverse()               # 反转
print(numbers)        # [6, 9, 5, 4, 3, 2, 1, 1]

# 排序不修改原列表
numbers = [3, 1, 4, 1, 5]
sorted_numbers = sorted(numbers)
print(numbers)        # [3, 1, 4, 1, 5]（不变）
print(sorted_numbers) # [1, 1, 3, 4, 5]

# 清空
fruits.clear()
print(fruits)         # []
```

### 列表合并

```python
list1 = [1, 2, 3]
list2 = [4, 5, 6]

# 用 + 合并
combined = list1 + list2
print(combined)       # [1, 2, 3, 4, 5, 6]

# 用 extend
list1.extend(list2)
print(list1)          # [1, 2, 3, 4, 5, 6]

# 用 append（注意区别！）
list1 = [1, 2, 3]
list1.append(list2)
print(list1)          # [1, 2, 3, [4, 5, 6]]（整个列表作为一个元素）
```

### 列表推导式 —— 快速创建列表

```python
# 传统写法
squares = []
for i in range(5):
    squares.append(i ** 2)
print(squares)        # [0, 1, 4, 9, 16]

# 列表推导式
squares = [i ** 2 for i in range(5)]
print(squares)        # [0, 1, 4, 9, 16]

# 带条件
evens = [i for i in range(10) if i % 2 == 0]
print(evens)          # [0, 2, 4, 6, 8]

# 带条件表达式
labels = ["偶数" if i % 2 == 0 else "奇数" for i in range(5)]
print(labels)         # ["偶数", "奇数", "偶数", "奇数", "偶数"]
```

**什么时候用列表？**
- 存储一组数据
- 需要保持顺序
- 需要频繁增删
- 存储消息列表、用户列表等

---

## 五、字典（Dict）—— 用名字找值

### 什么是字典？

列表用**编号**找东西，字典用**名字**找东西。

就像电话簿：
```
姓名        电话
─────────────────
小明    →  138xxxx
小红    →  139xxxx
小刚    →  137xxxx
```

用名字（键）就能找到电话（值）。

### 创建字典

```python
# 创建字典：{键: 值, 键: 值, ...}
person = {
    "name": "小明",
    "age": 18,
    "city": "北京"
}

# 空字典
empty1 = {}
empty2 = dict()

# 从列表创建
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = dict(zip(keys, values))
print(d)              # {"a": 1, "b": 2, "c": 3}
```

### 访问值

```python
person = {"name": "小明", "age": 18, "city": "北京"}

# 用键访问
print(person["name"])           # 小明
print(person["age"])            # 18

# 键不存在会报错！
print(person["phone"])          # KeyError: 'phone'

# 用 get() 更安全
print(person.get("name"))       # 小明
print(person.get("phone"))      # None（不存在返回 None）
print(person.get("phone", "无")) # 无（指定默认值）
```

### 修改字典

```python
person = {"name": "小明", "age": 18}

# 添加/修改
person["city"] = "北京"          # 添加新键值对
person["age"] = 19              # 修改已有值
print(person)
# {"name": "小明", "age": 19, "city": "北京"}

# 删除
del person["city"]
print(person)         # {"name": "小明", "age": 19}

age = person.pop("age")          # 删除并返回值
print(age)            # 19
print(person)         # {"name": "小明"}

# 更新（合并另一个字典）
person = {"name": "小明", "age": 18}
extra = {"city": "北京", "job": "学生"}
person.update(extra)
print(person)
# {"name": "小明", "age": 18, "city": "北京", "job": "学生"}
```

### 遍历字典

```python
person = {"name": "小明", "age": 18, "city": "北京"}

# 遍历键
for key in person:
    print(key)
# name, age, city

# 遍历键（更明确）
for key in person.keys():
    print(key)

# 遍历值
for value in person.values():
    print(value)
# 小明, 18, 北京

# 遍历键值对（最常用）
for key, value in person.items():
    print(f"{key}: {value}")
# name: 小明
# age: 18
# city: 北京
```

### 字典推导式

```python
# 传统写法
squares = {}
for i in range(5):
    squares[i] = i ** 2
print(squares)        # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 字典推导式
squares = {i: i ** 2 for i in range(5)}
print(squares)        # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 带条件
even_squares = {i: i ** 2 for i in range(10) if i % 2 == 0}
print(even_squares)   # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

### 嵌套字典

```python
# 字典里套字典
users = {
    "user1": {
        "name": "小明",
        "age": 18
    },
    "user2": {
        "name": "小红",
        "age": 20
    }
}

print(users["user1"]["name"])    # 小明

# 字典里套列表
person = {
    "name": "小明",
    "hobbies": ["游泳", "阅读", "游戏"]
}
print(person["hobbies"][0])      # 游泳

# 列表里套字典
students = [
    {"name": "小明", "score": 90},
    {"name": "小红", "score": 85},
    {"name": "小刚", "score": 95}
]
print(students[0]["name"])       # 小明
```

**什么时候用字典？**
- 存储配置信息
- API 返回的 JSON 数据
- 需要用名字快速查找
- 存储实体信息（用户、商品等）

---

## 六、条件判断 —— 让程序做决定

### if 语句

让程序根据条件选择执行不同的代码。

```python
age = 18

if age >= 18:
    print("成年人")
```

**语法要点：**
1. `if` 后面跟条件，末尾有冒号 `:`
2. 条件成立执行的代码要**缩进**（4个空格）
3. 条件的结果必须是布尔值（True/False）

### if-else

```python
age = 15

if age >= 18:
    print("成年人")
else:
    print("未成年")
```

### if-elif-else

多条件判断。

```python
score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

**注意：** `elif` 是 `else if` 的缩写，Python 只有 `elif`。

### 比较运算符

| 符号 | 含义 | 示例 | 结果 |
|------|------|------|------|
| `==` | 等于 | `1 == 1` | True |
| `!=` | 不等于 | `1 != 2` | True |
| `>` | 大于 | `2 > 1` | True |
| `<` | 小于 | `1 < 2` | True |
| `>=` | 大于等于 | `2 >= 2` | True |
| `<=` | 小于等于 | `1 <= 2` | True |

**重要：** `==` 是比较，`=` 是赋值！

```python
a = 5       # 赋值：把5给a
a == 5      # 比较：a等于5吗？（True）
```

### 逻辑运算符

```python
age = 25
has_license = True

# and：两个都真才真
if age >= 18 and has_license:
    print("可以开车")

# or：有一个真就真
day = "周六"
if day == "周六" or day == "周日":
    print("周末")

# not：取反
is_member = False
if not is_member:
    print("请先注册")
```

### 常用判断技巧

```python
# 判断是否在范围内
age = 25
if 18 <= age <= 60:          # 链式比较
    print("工作年龄")

# 判断列表是否为空
items = []
if items:                     # 有元素为True
    print("列表不为空")
else:
    print("列表为空")

# 判断列表是否包含元素
fruits = ["苹果", "香蕉"]
if "苹果" in fruits:
    print("有苹果")

# 判断字典是否包含键
person = {"name": "小明"}
if "name" in person:
    print("有name键")

# 判断是否为空值
result = None
if result is None:
    print("没有结果")
```

### 三元表达式

简写的 if-else。

```python
age = 20

# 传统写法
if age >= 18:
    status = "成年"
else:
    status = "未成年"

# 三元表达式
status = "成年" if age >= 18 else "未成年"

# 在打印中使用
print(f"状态：{'成年' if age >= 18 else '未成年'}")
```

---

## 七、循环 —— 重复做事

### for 循环

遍历一个序列，对每个元素做同样的事。

```python
fruits = ["苹果", "香蕉", "橙子"]

for fruit in fruits:
    print(f"我喜欢{fruit}")

# 输出：
# 我喜欢苹果
# 我喜欢香蕉
# 我喜欢橙子
```

**执行过程：**

```
第1次循环：fruit = "苹果" → 打印 "我喜欢苹果"
第2次循环：fruit = "香蕉" → 打印 "我喜欢香蕉"
第3次循环：fruit = "橙子" → 打印 "我喜欢橙子"
循环结束
```

### range() 函数

生成一个数字序列。

```python
# range(n)：0 到 n-1
for i in range(5):
    print(i)
# 0, 1, 2, 3, 4

# range(start, stop)：start 到 stop-1
for i in range(2, 5):
    print(i)
# 2, 3, 4

# range(start, stop, step)：步长
for i in range(0, 10, 2):
    print(i)
# 0, 2, 4, 6, 8

# 倒序
for i in range(5, 0, -1):
    print(i)
# 5, 4, 3, 2, 1
```

### 常用循环技巧

```python
# 遍历索引
fruits = ["苹果", "香蕉", "橙子"]
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")
# 0: 苹果
# 1: 香蕉
# 2: 橙子

# 同时获取索引和值（推荐）
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# 从指定索引开始
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")
# 1: 苹果
# 2: 香蕉
# 3: 橙子

# 同时遍历多个列表
names = ["小明", "小红", "小刚"]
ages = [18, 20, 19]
for name, age in zip(names, ages):
    print(f"{name}: {age}岁")
# 小明: 18岁
# 小红: 20岁
# 小刚: 19岁

# 遍历字典
person = {"name": "小明", "age": 18}
for key, value in person.items():
    print(f"{key}: {value}")
```

### while 循环

条件为真时一直执行。

```python
count = 0
while count < 5:
    print(count)
    count += 1
# 0, 1, 2, 3, 4

# 死循环（需要用 break 退出）
while True:
    answer = input("输入q退出：")
    if answer == "q":
        break
```

### break 和 continue

```python
# break：跳出整个循环
for i in range(10):
    if i == 5:
        break           # 到5就停止
    print(i)
# 0, 1, 2, 3, 4

# continue：跳过本次，继续下一次
for i in range(5):
    if i == 2:
        continue        # 跳过2
    print(i)
# 0, 1, 3, 4
```

### for-else 和 while-else

循环正常结束（没有 break）时执行 else。

```python
# 查找元素
fruits = ["苹果", "香蕉", "橙子"]
target = "西瓜"

for fruit in fruits:
    if fruit == target:
        print(f"找到{target}")
        break
else:
    print(f"没找到{target}")
# 输出：没找到西瓜
```

### 循环嵌套

```python
# 打印九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end=" ")
    print()  # 换行

# 输出：
# 1×1=1
# 1×2=2 2×2=4
# 1×3=3 2×3=6 3×3=9
# ...
```

---

## 八、函数 —— 封装代码块

### 什么是函数？

函数是一段**可重复使用**的代码，给它一个名字，随时可以调用。

就像菜谱：
- 菜谱名 = 函数名
- 材料 = 参数
- 菜 = 返回值

```python
# 定义函数
def greet():
    print("你好！")

# 调用函数
greet()      # 你好！
greet()      # 你好！
```

### 参数

把数据传给函数。

```python
def greet(name):
    print(f"你好，{name}！")

greet("小明")     # 你好，小明！
greet("小红")     # 你好，小红！
```

### 多个参数

```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)    # 8

# 按位置传参
add(3, 5)        # a=3, b=5

# 按关键字传参
add(a=3, b=5)    # 明确指定
add(b=5, a=3)    # 顺序不重要
```

### 返回值

函数执行完返回结果。

```python
def add(a, b):
    return a + b       # 返回计算结果

result = add(3, 5)
print(result)          # 8

# 没有返回值的函数
def say_hello():
    print("Hello")

x = say_hello()        # 打印 Hello
print(x)               # None

# 返回多个值（实际是元组）
def get_info():
    name = "小明"
    age = 18
    return name, age

n, a = get_info()      # 解包
print(n)               # 小明
print(a)               # 18
```

### 默认参数

```python
def greet(name, greeting="你好"):
    print(f"{greeting}，{name}！")

greet("小明")                    # 你好，小明！
greet("小明", "早上好")           # 早上好，小明！
greet("小明", greeting="晚上好")  # 晚上好，小明！
```

### 可变参数

```python
# *args：接收任意数量的位置参数
def add_all(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

print(add_all(1, 2, 3))        # 6
print(add_all(1, 2, 3, 4, 5))  # 15

# **kwargs：接收任意数量的关键字参数
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="小明", age=18, city="北京")
# name: 小明
# age: 18
# city: 北京
```

### 变量作用域

```python
# 全局变量
total = 100

def add(n):
    # 局部变量
    local = 10
    return total + n + local

print(add(5))      # 115
# print(local)     # 报错！局部变量外部不可见

# 修改全局变量
count = 0

def increment():
    global count    # 声明使用全局变量
    count += 1

increment()
print(count)        # 1
```

### 函数作为参数

```python
def apply(func, value):
    return func(value)

def double(x):
    return x * 2

result = apply(double, 5)
print(result)       # 10

# 使用 lambda（匿名函数）
result = apply(lambda x: x * 2, 5)
print(result)       # 10
```

### 常用内置函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `len()` | 长度 | `len([1,2,3])` → 3 |
| `max()` | 最大值 | `max(1, 5, 3)` → 5 |
| `min()` | 最小值 | `min(1, 5, 3)` → 1 |
| `sum()` | 求和 | `sum([1,2,3])` → 6 |
| `abs()` | 绝对值 | `abs(-5)` → 5 |
| `round()` | 四舍五入 | `round(3.5)` → 4 |
| `sorted()` | 排序 | `sorted([3,1,2])` → [1,2,3] |
| `reversed()` | 反转 | `list(reversed([1,2,3]))` → [3,2,1] |
| `any()` | 任一为真 | `any([False, True])` → True |
| `all()` | 全部为真 | `all([True, False])` → False |

---

## 九、模块 —— 使用外部代码

### 什么是模块？

模块就是一个 `.py` 文件，里面有别人写好的代码。

### 导入方式

```python
# 导入整个模块
import math
print(math.sqrt(16))    # 4.0

# 导入并起别名
import math as m
print(m.pi)             # 3.14159...

# 从模块导入特定内容
from math import sqrt, pi
print(sqrt(16))         # 4.0
print(pi)               # 3.14159...

# 导入所有（不推荐）
from math import *
```

### 常用内置模块

```python
# os：操作系统
import os
print(os.getcwd())              # 当前目录
print(os.listdir())             # 目录内容
os.makedirs("new_dir")          # 创建目录

# sys：Python 解释器
import sys
print(sys.version)              # Python 版本
print(sys.path)                 # 模块搜索路径

# datetime：日期时间
from datetime import datetime
now = datetime.now()
print(now)                      # 2026-03-29 12:00:00
print(now.strftime("%Y-%m-%d")) # 2026-03-29

# json：JSON 处理
import json
data = {"name": "小明", "age": 18}
json_str = json.dumps(data)     # 转成 JSON 字符串
data2 = json.loads(json_str)    # 解析 JSON

# random：随机数
import random
print(random.randint(1, 10))    # 1-10 随机整数
print(random.choice([1,2,3]))   # 随机选择一个
random.shuffle([1,2,3])         # 打乱顺序

# time：时间
import time
print(time.time())              # 时间戳
time.sleep(2)                   # 等待2秒
```

### 第三方模块

```bash
# 安装
pip install telethon

# 指定版本
pip install telethon==1.34.0

# 从文件安装
pip install -r requirements.txt

# 卸载
pip uninstall telethon

# 查看已安装
pip list
```

```python
# 使用第三方模块
from telethon import TelegramClient

client = TelegramClient(session, api_id, api_hash)
```

---

## 十、异常处理 —— 处理错误

### 什么是异常？

程序运行出错时会"抛出异常"，如果不处理，程序会崩溃。

```python
# 不处理异常
result = 10 / 0
# ZeroDivisionError: division by zero
# 程序崩溃！
```

### try-except

捕获并处理异常。

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除数不能为0")
# 程序继续运行，不崩溃
```

### 多个异常

```python
try:
    num = int(input("请输入数字："))
    result = 10 / num
except ValueError:
    print("输入的不是数字")
except ZeroDivisionError:
    print("不能输入0")
```

### 捕获异常信息

```python
try:
    result = 10 / 0
except Exception as e:
    print(f"出错了：{e}")
    print(f"错误类型：{type(e).__name__}")
# 出错了：division by zero
# 错误类型：ZeroDivisionError
```

### else 和 finally

```python
try:
    num = int(input("请输入数字："))
except ValueError:
    print("输入错误")
else:
    # 没有异常时执行
    print(f"你输入了 {num}")
finally:
    # 无论是否有异常都执行
    print("程序结束")
```

### 主动抛出异常

```python
def set_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(e)    # 年龄不能为负数
```

---

## 十一、类和对象 —— 面向对象编程

### 什么是类？什么是对象？

- **类**：图纸、模板、设计图
- **对象**：根据图纸造出来的东西

```
类 = 汽车设计图
对象 = 具体的一辆汽车

类 = Dog
对象 = 你家的狗、我家的狗
```

### 定义类

```python
class Dog:
    # 类属性（所有实例共享）
    species = "狗"

    # 构造函数（创建对象时调用）
    def __init__(self, name, age):
        # 实例属性（每个实例独有）
        self.name = name
        self.age = age

    # 实例方法
    def bark(self):
        print(f"{self.name}：汪汪汪！")

    def info(self):
        print(f"{self.name}，{self.age}岁，是{self.species}")

# 创建对象
my_dog = Dog("旺财", 3)
your_dog = Dog("来福", 2)

# 访问属性
print(my_dog.name)       # 旺财
print(your_dog.age)      # 2

# 调用方法
my_dog.bark()            # 旺财：汪汪汪！
my_dog.info()            # 旺财，3岁，是狗
```

### `self` 是什么？

`self` 代表**对象自己**。

```python
class Person:
    def __init__(self, name):
        self.name = name    # self.name = 这个对象的name属性

    def say_hello(self):
        print(f"我是{self.name}")

p1 = Person("小明")
p1.say_hello()    # 我是小明（self 是 p1）

p2 = Person("小红")
p2.say_hello()    # 我是小红（self 是 p2）
```

### 类属性 vs 实例属性

```python
class Dog:
    # 类属性
    species = "狗"
    count = 0

    def __init__(self, name):
        # 实例属性
        self.name = name
        Dog.count += 1      # 每创建一个对象，count+1

d1 = Dog("旺财")
d2 = Dog("来福")

print(d1.name)      # 旺财（实例属性）
print(d2.name)      # 来福（实例属性）
print(Dog.species)  # 狗（类属性）
print(Dog.count)    # 2（创建了2个对象）
```

### 继承

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name}在吃东西")

# Dog 继承 Animal
class Dog(Animal):
    def bark(self):
        print(f"{self.name}：汪汪汪！")

# Cat 继承 Animal
class Cat(Animal):
    def bark(self):
        print(f"{self.name}：喵喵喵！")

dog = Dog("旺财")
dog.eat()       # 旺财在吃东西（继承自 Animal）
dog.bark()      # 旺财：汪汪汪！（Dog 自己的方法）

cat = Cat("咪咪")
cat.eat()       # 咪咪在吃东西
cat.bark()      # 咪咪：喵喵喵！
```

### 特殊方法

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 打印时的显示
    def __str__(self):
        return f"({self.x}, {self.y})"

    # 加法
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    # 长度
    def __len__(self):
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

p1 = Point(3, 4)
p2 = Point(1, 2)

print(p1)           # (3, 4)（调用 __str__）
print(p1 + p2)      # (4, 6)（调用 __add__）
print(len(p1))      # 5（调用 __len__）
```

---

## 十二、异步编程 —— async/await

### 同步 vs 异步

```python
# 同步：一件一件做
做饭()      # 等30分钟
洗衣服()    # 等20分钟
扫地()      # 等10分钟
# 总共：60分钟

# 异步：同时开始
await 做饭()     # 开始
await 洗衣服()   # 开始（不用等饭做好）
await 扫地()     # 开始
# 总共：30分钟（最长的那个）
```

### async def

定义异步函数。

```python
import asyncio

# 普通函数
def normal_func():
    return "结果"

# 异步函数
async def async_func():
    await asyncio.sleep(1)
    return "结果"
```

### await

等待异步操作完成，只能在 `async def` 内使用。

```python
import asyncio

async def fetch_data():
    print("开始获取...")
    await asyncio.sleep(2)    # 等待2秒（模拟网络请求）
    print("获取完成！")
    return "数据"

async def main():
    result = await fetch_data()
    print(f"结果是：{result}")

# 运行异步函数
asyncio.run(main())
```

### 并发执行

```python
import asyncio

async def task(name, seconds):
    print(f"{name} 开始，需要 {seconds} 秒")
    await asyncio.sleep(seconds)
    print(f"{name} 完成！")
    return f"{name}的结果"

async def main():
    # 串行执行（一个一个来）
    # await task("A", 2)
    # await task("B", 1)
    # await task("C", 3)
    # 总共：6秒

    # 并发执行（同时开始）
    results = await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3)
    )
    # 总共：3秒（最长的那个）
    print(results)

asyncio.run(main())

# 输出：
# A 开始，需要 2 秒
# B 开始，需要 1 秒
# C 开始，需要 3 秒
# B 完成！
# A 完成！
# C 完成！
# ['A的结果', 'B的结果', 'C的结果']
```

### 异步上下文管理器

```python
import asyncio

class AsyncTimer:
    async def __aenter__(self):
        self.start = asyncio.get_event_loop().time()
        return self

    async def __aexit__(self, *args):
        elapsed = asyncio.get_event_loop().time() - self.start
        print(f"耗时：{elapsed:.2f}秒")

async def main():
    async with AsyncTimer():
        await asyncio.sleep(1)

asyncio.run(main())    # 耗时：1.00秒
```

---

## 十三、文件操作

### 读取文件

```python
# 读取全部
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)

# 按行读取
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())    # strip() 去除换行符

# 读取所有行到列表
with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
```

### 写入文件

```python
# 覆盖写入
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.write("World\n")

# 追加写入
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("新的一行\n")

# 写入多行
lines = ["第一行\n", "第二行\n", "第三行\n"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)
```

### 文件模式

| 模式 | 说明 |
|------|------|
| `r` | 读取（默认） |
| `w` | 写入（覆盖） |
| `a` | 追加 |
| `x` | 创建（文件存在则报错） |
| `b` | 二进制模式 |
| `+` | 读写模式 |

```python
# 二进制文件
with open("image.png", "rb") as f:
    data = f.read()

with open("copy.png", "wb") as f:
    f.write(data)
```

---

## 十四、实用技巧汇总

### 字符串处理

```python
# 分割
text = "苹果,香蕉,橙子"
fruits = text.split(",")    # ["苹果", "香蕉", "橙子"]

# 连接
fruits = ["苹果", "香蕉", "橙子"]
text = ",".join(fruits)     # "苹果,香蕉,橙子"

# 去除空白
text = "  hello  "
print(text.strip())         # "hello"（两边）
print(text.lstrip())        # "hello  "（左边）
print(text.rstrip())        # "  hello"（右边）

# 替换
text = "I like Java"
print(text.replace("Java", "Python"))  # "I like Python"

# 大小写
text = "Hello World"
print(text.lower())         # "hello world"
print(text.upper())         # "HELLO WORLD"
print(text.title())         # "Hello World"

# 判断开头结尾
filename = "test.py"
print(filename.endswith(".py"))  # True
print(filename.startswith("test"))  # True
```

### 列表技巧

```python
# 统计
numbers = [1, 2, 3, 2, 4, 2, 5]
print(numbers.count(2))     # 3（2出现3次）

# 查找
print(numbers.index(3))     # 2（3在索引2）

# 去重（保留顺序）
unique = list(dict.fromkeys(numbers))
print(unique)               # [1, 2, 3, 4, 5]

# 扁平化
nested = [[1, 2], [3, 4], [5]]
flat = [x for sub in nested for x in sub]
print(flat)                 # [1, 2, 3, 4, 5]

# 分组
from itertools import batched
data = [1, 2, 3, 4, 5, 6, 7]
groups = list(batched(data, 3))
print(groups)               # [(1, 2, 3), (4, 5, 6), (7,)]
```

### 字典技巧

```python
# 默认值
from collections import defaultdict
word_count = defaultdict(int)
words = ["apple", "banana", "apple", "orange"]
for word in words:
    word_count[word] += 1
print(dict(word_count))     # {'apple': 2, 'banana': 1, 'orange': 1}

# 有序字典
from collections import OrderedDict
od = OrderedDict()
od['a'] = 1
od['b'] = 2
print(od)                   # OrderedDict([('a', 1), ('b', 2)])

# 合并字典（Python 3.9+）
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
merged = d1 | d2
print(merged)               # {'a': 1, 'b': 3, 'c': 4}
```

### 解包技巧

```python
# 列表解包
a, b, c = [1, 2, 3]
print(a, b, c)              # 1 2 3

# 扩展解包
first, *middle, last = [1, 2, 3, 4, 5]
print(first)                # 1
print(middle)               # [2, 3, 4]
print(last)                 # 5

# 交换变量
a, b = 1, 2
a, b = b, a
print(a, b)                 # 2 1

# 忽略值
a, _, c = [1, 2, 3]         # _ 是占位符，表示不关心这个值
```

### 链式调用

```python
# 判断非空
name = None
result = name or "默认名"
print(result)               # 默认名

# 判断范围
age = 25
if 18 <= age <= 60:
    print("工作年龄")

# 安全调用
person = {"name": "小明"}
city = person.get("address", {}).get("city", "未知")
print(city)                 # 未知
```

---

## 十五、代码风格指南

### 缩进

- 使用 **4 个空格**，不用 Tab
- 同一代码块必须对齐

```python
# 正确
if True:
    print("Hello")
    print("World")

# 错误
if True:
    print("Hello")
  print("World")    # 缩进不一致
```

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量/函数 | 小写+下划线 | `user_name`, `get_data()` |
| 常量 | 大写+下划线 | `MAX_SIZE`, `API_KEY` |
| 类 | 驼峰命名 | `TelegramBot`, `UserInfo` |
| 私有属性 | 下划线开头 | `_client`, `_instance` |
| 私有属性（强） | 双下划线开头 | `__password` |

### 注释

```python
# 单行注释

"""
多行注释
用于函数或类的说明
"""

def calculate(x, y):
    """
    计算两个数的和

    Args:
        x: 第一个数
        y: 第二个数

    Returns:
        两数之和
    """
    return x + y
```

### 空行

```python
import os

# 导入和代码之间空两行


def func1():
    pass


def func2():
    # 函数内逻辑块之间空一行
    data = load_data()

    result = process(data)

    return result


# 类之间空两行
class MyClass:
    def method1(self):
        pass

    def method2(self):
        pass
```

---

## 十六、快速参考卡

### 数据类型

```python
str     "hello"         # 字符串
int     123             # 整数
float   3.14            # 浮点数
bool    True / False    # 布尔值
list    [1, 2, 3]       # 列表
dict    {"a": 1}        # 字典
tuple   (1, 2, 3)       # 元组（不可变列表）
set     {1, 2, 3}       # 集合（不重复）
None    None            # 空值
```

### 运算符

```python
# 算术
+  -  *  /  //  %  **

# 比较
==  !=  >  <  >=  <=

# 逻辑
and  or  not

# 成员
in  not in

# 身份
is  is not
```

### 常用函数

```python
print()      # 打印
input()      # 输入
len()        # 长度
type()       # 类型
int()        # 转整数
str()        # 转字符串
list()       # 转列表
dict()       # 转字典
range()      # 数字序列
enumerate()  # 带索引遍历
zip()        # 并行遍历
sorted()     # 排序
reversed()   # 反转
sum()        # 求和
max()        # 最大值
min()        # 最小值
any()        # 任一为真
all()        # 全部为真
```

### 格式化字符串

```python
name = "小明"
age = 18

# f-string
f"姓名：{name}"
f"年龄：{age}"
f"明年：{age + 1}岁"
f"价格：{99.9:.2f}元"
f"编号：{5:03d}"
```

---

## 下一步

恭喜你学完了 Python 基础！现在可以开始阅读项目代码了：

```
推荐学习顺序：

00_Python基础入门.md     ← 你在这里
        ↓
01_config_py讲解.md      配置文件（最简单）
        ↓
02_login_py讲解.md       登录工具（异步编程）
        ↓
03_bot_sender_py讲解.md  核心类（类和对象）
        ↓
04_api_server_py讲解.md  API服务（综合应用）
```

祝你学习顺利！
