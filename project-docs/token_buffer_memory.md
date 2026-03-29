# TokenBufferMemory 技术文档

## 1. 代码功能概述

`TokenBuoken` 数量限制和消息条数限制双重约束，从数据库中检索并裁剪历史对话`fferMemory` 是一个基于 Token 计数的对话缓冲记忆组件，用于在 LLMOps 平台中管理会话历史消息。该组件实现了**短期记忆机制**，通过 T，为 LLM 提供合适的上下文窗口。

### 核心功能

| 功能         | 描述                       |
| ---------- | ------------------------ |
| 历史消息检索     | 从数据库查询指定会话的历史消息          |
| Token 计数裁剪 | 根据 Token 限制智能裁剪消息列表      |
| 消息格式转换     | 将数据库消息转换为 LangChain 消息格式 |
| 文本格式输出     | 支持将历史消息转换为文本提示格式         |

### 应用场景

- 对话机器人上下文管理
- 多轮对话历史记忆
- RAG 系统中的对话上下文构建
- Agent 会话状态维护

***

## 2. 核心算法与实现原理

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    TokenBufferMemory                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │     db      │  │ conversation │  │  model_instance   │   │
│  │ (SQLAlchemy)│  │(Conversation)│  │(BaseLanguageModel)│   │
│  └─────────────┘  └──────────────┘  └───────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                      核心方法                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        get_history_prompt_messages()                 │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐   │   │
│  │  │会话校验  │-→│消息查询   │-→│格式转换  │-→│Token裁剪│   │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         get_history_prompt_text()                    │   │
│  │  ┌─────────────────┐  ┌─────────────────────────┐    │   │
│  │  │获取历史消息列表    │-→│转换为文本格式字符串        │    │   │
│  │  └─────────────────┘  └─────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 消息检索策略

```
数据库消息表 (按时间倒序)
┌────────────────────────────────────────────────────┐
│ id │ conversation_id │ query │ answer │ created_at │
├────┼─────────────────┼───────┼────────┼────────────┤
│ 10 │       1         │  Q5   │  A5    │  12:00     │  ← 最新
│  9 │       1         │  Q4   │  A4    │  11:50     │
│  8 │       1         │  Q3   │  A3    │  11:40     │
│  ......                                            │
│  1 │       1         │  Q1   │  A1    │  10:00     │  ← 最早
└────────────────────────────────────────────────────┘
                    ↓
        按时间倒序查询 + LIMIT 限制
                    ↓
        reversed() 反转为正序
                    ↓
┌─────────────────────────────────────────────────────┐
│  Q1→A1 → Q2→A2 → Q3→A3 → ... → Qn→An                │
└─────────────────────────────────────────────────────┘
```

### 2.3 Token 裁剪算法

使用 LangChain 的 `trim_messages` 函数实现智能裁剪：

```
原始消息列表 (超出 Token 限制)
┌─────────────────────────────────────────────────────┐
│ Human: Q1 (100 tokens)                              │
│ AI: A1 (200 tokens)                                 │
│ Human: Q2 (150 tokens)                              │
│ AI: A2 (300 tokens)                                 │
│ Human: Q3 (120 tokens)                              │
│ AI: A3 (250 tokens)                                 │
│ ...                                                 │
│ Human: Qn (130 tokens)                              │
│ AI: An (280 tokens)                                 │
└─────────────────────────────────────────────────────┘
                    ↓
        trim_messages() 策略裁剪
        - strategy: "last" (保留最新消息)
        - start_on: "human" (以人类消息开始)
        - end_on: "ai" (以 AI 消息结束)
                    ↓
裁剪后消息列表 (符合 Token 限制)
┌─────────────────────────────────────────────────────┐
│ Human: Q(n-2) (130 tokens)                          │
│ AI: A(n-2) (260 tokens)                             │
│ Human: Q(n-1) (140 tokens)                          │
│ AI: A(n-1) (270 tokens)                             │
│ Human: Qn (130 tokens)                              │
│ AI: An (280 tokens)                                 │
└─────────────────────────────────────────────────────┘
```

### 2.4 消息状态过滤

只检索以下状态的消息：

| 状态      | 枚举值       | 说明        |
| ------- | --------- | --------- |
| NORMAL  | `normal`  | 正常完成的消息   |
| STOP    | `stop`    | 用户手动停止的消息 |
| TIMEOUT | `timeout` | 响应超时的消息   |

**排除条件：**

- `answer` 为空字符串
- `is_deleted` 为 True（软删除）
- 状态为 `ERROR` 的消息

***

## 3. 类与方法详细说明

### 3.1 类定义

```python
@dataclass
class TokenBufferMemory:
    """基于token计数的缓冲记忆组件"""
    db: SQLAlchemy              # 数据库实例
    conversation: Conversation  # 会话模型
    model_instance: BaseLanguageModel  # LLM大语言模型
```

### 3.2 依赖关系

```
TokenBufferMemory
    ├── SQLAlchemy (pkg.sqlalchemy)
    │       └── 数据库会话管理
    ├── Conversation (internal.model)
    │       └── 会话数据模型
    ├── Message (internal.model)
    │       └── 消息数据模型
    ├── BaseLanguageModel (internal.core.language_model.entities)
    │       ├── 继承自 LCBaseLanguageModel
    │       ├── 提供 token 计数能力
    │       └── 提供 convert_to_human_message() 方法
    └── LangChain Core
            ├── trim_messages() - 消息裁剪
            ├── get_buffer_string() - 消息转文本
            ├── AnyMessage - 消息类型
            └── AIMessage - AI 消息类型
```

### 3.3 方法详解

#### 3.3.1 `get_history_prompt_messages()`

**功能：** 获取符合 Token 限制的历史消息列表（LangChain 消息格式）

**签名：**

```python
def get_history_prompt_messages(
    self,
    max_token_limit: int = 2000,
    message_limit: int = 10,
) -> list[AnyMessage]
```

**执行流程：**

```python
# Step 1: 会话存在性校验
if self.conversation is None:
    return []

# Step 2: 数据库查询
messages = self.db.session.query(Message).filter(
    Message.conversation_id == self.conversation.id,
    Message.answer != "",
    Message.is_deleted == False,
    Message.status.in_([MessageStatus.NORMAL, MessageStatus.STOP, MessageStatus.TIMEOUT]),
).order_by(desc("created_at")).limit(message_limit).all()

# Step 3: 时间顺序反转
messages = list(reversed(messages))

# Step 4: 转换为 LangChain 消息格式
prompt_messages = []
for message in messages:
    prompt_messages.extend([
        self.model_instance.convert_to_human_message(message.query, message.image_urls),
        AIMessage(content=message.answer),
    ])

# Step 5: Token 裁剪
return trim_messages(
    messages=prompt_messages,
    max_tokens=max_token_limit,
    token_counter=self.model_instance,
    strategy="last",
    start_on="human",
    end_on="ai",
)
```

**返回值：** `list[AnyMessage]` - LangChain 消息列表

***

#### 3.3.2 `get_history_prompt_text()`

**功能：** 获取历史消息的文本格式（用于文本生成模型）

**签名：**

```python
def get_history_prompt_text(
    self,
    human_prefix: str = "Human",
    ai_prefix: str = "AI",
    max_token_limit: int = 2000,
    message_limit: int = 10,
) -> str
```

**执行流程：**

```python
# Step 1: 获取历史消息列表
messages = self.get_history_prompt_messages(max_token_limit, message_limit)

# Step 2: 转换为文本格式
return get_buffer_string(messages, human_prefix, ai_prefix)
```

**输出示例：**

```
Human: 你好，请介绍一下自己
AI: 你好！我是一个AI助手，可以帮助你解答各种问题。
Human: 你能做什么？
AI: 我可以回答问题、提供建议、协助写作等。
```

**返回值：** `str` - 格式化的对话历史文本

***

## 4. 参数说明

### 4.1 类属性参数

| 参数               | 类型                | 必填 | 说明                   |
| ---------------- | ----------------- | -- | -------------------- |
| `db`             | SQLAlchemy        | 是  | 数据库实例，用于查询消息记录       |
| `conversation`   | Conversation      | 是  | 会话模型实例，可为 None       |
| `model_instance` | BaseLanguageModel | 是  | LLM 实例，提供 Token 计数能力 |

### 4.2 方法参数

#### `get_history_prompt_messages()`

| 参数                | 类型  | 默认值  | 说明            |
| ----------------- | --- | ---- | ------------- |
| `max_token_limit` | int | 2000 | 最大 Token 数量限制 |
| `message_limit`   | int | 10   | 最大消息条数限制      |

#### `get_history_prompt_text()`

| 参数                | 类型  | 默认值     | 说明            |
| ----------------- | --- | ------- | ------------- |
| `human_prefix`    | str | "Human" | 人类消息前缀标识      |
| `ai_prefix`       | str | "AI"    | AI 消息前缀标识     |
| `max_token_limit` | int | 2000    | 最大 Token 数量限制 |
| `message_limit`   | int | 10      | 最大消息条数限制      |

### 4.3 trim\_messages 参数说明

| 参数              | 值               | 说明                   |
| --------------- | --------------- | -------------------- |
| `strategy`      | "last"          | 保留最新的消息              |
| `start_on`      | "human"         | 确保消息列表以人类消息开始        |
| `end_on`        | "ai"            | 确保消息列表以 AI 消息结束      |
| `token_counter` | model\_instance | 使用 LLM 实例进行 Token 计数 |

***

## 5. 使用示例

### 5.1 基本使用

```python
from internal.core.memory.token_buffer_memory import TokenBufferMemory
from internal.model import Conversation
from pkg.sqlalchemy import SQLAlchemy

# 初始化数据库和模型
db = SQLAlchemy()
conversation = db.session.query(Conversation).filter_by(id=1).first()
model_instance = get_llm_instance("gpt-4")

# 创建记忆组件
memory = TokenBufferMemory(
    db=db,
    conversation=conversation,
    model_instance=model_instance
)

# 获取历史消息列表
history_messages = memory.get_history_prompt_messages(
    max_token_limit=4000,
    message_limit=20
)

# 构建完整提示
from langchain_core.messages import HumanMessage
full_messages = history_messages + [HumanMessage(content="请继续上面的对话")]
response = model_instance.invoke(full_messages)
```

### 5.2 获取文本格式历史

```python
# 获取文本格式的历史对话
history_text = memory.get_history_prompt_text(
    human_prefix="用户",
    ai_prefix="助手",
    max_token_limit=2000,
    message_limit=10
)

print(history_text)
# 输出:
# 用户: 你好
# 助手: 你好！有什么可以帮助你的吗？
# 用户: 请介绍一下 Python
# 助手: Python 是一种高级编程语言...
```

### 5.3 在 Agent 中使用

```python
from langchain.agents import AgentExecutor

def build_agent_with_memory(conversation_id: int):
    # 获取会话
    conversation = db.session.query(Conversation).get(conversation_id)

    # 创建记忆组件
    memory = TokenBufferMemory(
        db=db,
        conversation=conversation,
        model_instance=llm
    )

    # 获取历史上下文
    history = memory.get_history_prompt_messages()

    # 构建 Agent
    agent = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=history
    )

    return agent
```

### 5.4 处理空会话

```python
# 当 conversation 为 None 时
memory = TokenBufferMemory(
    db=db,
    conversation=None,
    model_instance=model_instance
)

messages = memory.get_history_prompt_messages()
# 返回: []
```

***

## 6. 潜在优化点

### 6.1 性能优化

| 优化点      | 当前实现                    | 优化建议             |
| -------- | ----------------------- | ---------------- |
| 数据库查询    | 每次调用都查询                 | 添加缓存层，短期缓存历史消息   |
| 消息反转     | Python list(reversed()) | 在 SQL 中使用 ASC 排序 |
| Token 计数 | 每次重新计算                  | 缓存已计算的消息 Token 数 |

### 6.2 功能增强建议

```python
# 建议 1: 添加缓存机制
@dataclass
class TokenBufferMemory:
    _cache: dict = field(default_factory=dict)
    _cache_ttl: int = 300  # 5分钟缓存

    def get_history_prompt_messages(self, ...):
        cache_key = f"{self.conversation.id}_{max_token_limit}_{message_limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        # ... 原有逻辑
        self._cache[cache_key] = result
        return result

# 建议 2: 支持异步查询
async def get_history_prompt_messages_async(self, ...):
    messages = await self.db.session.execute(
        select(Message).where(...).order_by(desc("created_at")).limit(message_limit)
    )
    # ...

# 建议 3: 添加消息摘要支持
def get_summary_if_exceeds_limit(
    self,
    max_token_limit: int,
    summary_threshold: float = 0.8
) -> list[AnyMessage]:
    """当历史消息超过阈值时，生成摘要压缩上下文"""
    pass
```

### 6.3 代码改进建议

```python
# 当前代码
messages = self.db.session.query(Message).filter(
    Message.conversation_id == self.conversation.id,
    Message.answer != "",
    Message.is_deleted == False,
    Message.status.in_([MessageStatus.NORMAL, MessageStatus.STOP, MessageStatus.TIMEOUT]),
).order_by(desc("created_at")).limit(message_limit).all()
messages = list(reversed(messages))

# 建议改进：直接使用 ASC 排序，避免反转
messages = self.db.session.query(Message).filter(
    Message.conversation_id == self.conversation.id,
    Message.answer != "",
    Message.is_deleted == False,
    Message.status.in_([MessageStatus.NORMAL, MessageStatus.STOP, MessageStatus.TIMEOUT]),
).order_by(asc("created_at")).limit(message_limit).all()
```

***

## 7. 注意事项

### 7.1 使用注意

1. **会话为空处理**：当 `conversation` 为 `None` 时，方法会返回空列表，调用方需处理此情况
2. **Token 计数准确性**：依赖 `model_instance` 的 Token 计数能力，不同模型的计数结果可能不同
3. **消息状态过滤**：只会检索 `NORMAL`、`STOP`、`TIMEOUT` 状态的消息，错误消息会被排除
4. **图片消息处理**：`convert_to_human_message()` 方法会根据模型是否支持图片输入决定消息格式

### 7.2 数据库依赖

```python
# Message 模型必需字段
class Message:
    id: int
    conversation_id: int
    query: str              # 用户问题
    answer: str             # AI 回答
    image_urls: list[str]   # 图片 URL 列表
    is_deleted: bool        # 软删除标记
    status: MessageStatus   # 消息状态
    created_at: datetime    # 创建时间
```

### 7.3 线程安全

- `TokenBufferMemory` 本身不是线程安全的
- 如需在多线程环境使用，建议每个线程创建独立实例
- 数据库会话 (`db.session`) 需要注意线程隔离

### 7.4 内存管理

- 大量历史消息可能导致内存占用较高
- 建议合理设置 `message_limit` 参数
- 对于长对话场景，考虑使用摘要记忆替代

***

## 8. 相关组件

| 组件                | 路径                                                      | 说明     |
| ----------------- | ------------------------------------------------------- | ------ |
| BaseLanguageModel | `internal/core/language_model/entities/model_entity.py` | 语言模型基类 |
| MessageStatus     | `internal/entity/conversation_entity.py`                | 消息状态枚举 |
| Conversation      | `internal/model/conversation.py`                        | 会话数据模型 |
| Message           | `internal/model/`                                       | 消息数据模型 |
| SQLAlchemy        | `pkg/sqlalchemy/sqlalchemy.py`                          | 数据库工具类 |

***

## 10. 参考资料

- [LangChain Memory Documentation](https://python.langchain.com/docs/modules/memory/)
- [LangChain trim\_messages API](https://api.python.langchain.com/en/latest/messages/langchain_core.messages.utils.trim_messages.html)
- [LangChain get\_buffer\_string API](https://api.python.langchain.com/en/latest/messages/langchain_core.messages.utils.get_buffer_string.html)

