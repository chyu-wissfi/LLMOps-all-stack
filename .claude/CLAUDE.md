# 个人偏好

## 沟通方式

- 使用中文回复
- 代码注释使用中文
- 解释简洁直接，不要过多铺垫

## 通用代码风格

- ./api/ 目录下的后端代码缩进使用 4 空格
- ./ui/ 目录下的前端代码缩进使用 2 空格
- 优先使用 async/await
- 变量命名使用 camelCase
- 常量命名使用 UPPER_SNAKE_CASE

## 我的常用工具

- 包管理器: conda
- 编辑器: TRAE CN
- 终端: Bash

# 项目：LLMOps平台全栈

在LLMOps目录下提交代码到Github命令为：

```bash
git add .
git commit -a -m "<描述信息，需要你决定>"
git push llmops
```

## 后端

### 技术栈

- Flask
- SQLAlchemy 连接 PostgreSQL
- LangGraph
- Redis
- Celery

### 后端：./api 的目录结构

```
api/
├── config/                     # 配置模块
│   ├── __init__.py
│   ├── config.py               # 配置加载逻辑
│   └── default_config.py       # 默认配置项
├── app/                        # 应用入口层
│   ├── __init__.py
│   └── http/                   # HTTP服务入口
│       ├── __init__.py
│       ├── app.py              # FastAPI 应用实例创建、中间件注册
│       └── module.py           # 依赖注入模块配置
├── internal/                   # 核心业务实现层
│   ├── core/                   # 核心组件（工作流、向量存储、文档处理等）
│   │   ├── agent/              # Agent 相关实现
│   │   │   ├── agent_builder.py
│   │   │   ├── agent_executor.py
│   │   │   └── conversation_agent.py
│   │   ├── builtin_apps/       # 内置应用实现
│   │   │   ├── chat/
│   │   │   ├── completion/
│   │   │   ├── dataset_qa/
│   │   │   └── workflow/
│   │   ├── file_extractor/     # 文件提取工具
│   │   ├── langchain_fix/      # LangChain 补丁/修复
│   │   ├── language_model/     # 语言模型封装
│   │   │   ├── base.py         # LLM 基类
│   │   │   ├── factory.py      # LLM 工厂
│   │   │   ├── openai.py       # OpenAI 模型封装
│   │   │   ├── anthropic.py    # Anthropic 模型封装
│   │   │   └── azure_openai.py # Azure OpenAI 模型封装
│   │   ├── memory/             # 对话记忆管理
│   │   ├── retrievers/         # 检索器实现
│   │   ├── tools/              # 工具集
│   │   │   ├── base_tool.py
│   │   │   ├── builtin_tools/
│   │   │   │   ├── search/
│   │   │   │   ├── calculator/
│   │   │   │   └── web_scraper/
│   │   │   └── api_tools/
│   │   ├── unstructured/       # 非结构化文档处理
│   │   │   ├── document_processor.py
│   │   │   └── nltk_data/      # NLTK 数据文件
│   │   │       ├── punkt/
│   │   │       │   └── ... (18种语言的 punkt 分词数据)
│   │   │       └── punkt_tab/
│   │   │           └── ... (22种语言的 punkt_tab 分词数据，包含 abbrev_types.txt、collocations.tab、ortho_context.tab等)
│   │   ├── vector_store/       # 向量数据库存储
│   │   └── workflow/           # 工作流引擎核心
│   │       ├── workflow.py                  # 工作流引擎主逻辑
│   │       ├── workflow_validate_rule.jpg   # 工作流验证规则图
│   │       ├── entities/                    # 工作流实体定义
│   │       │   ├── node_entity.py           # 节点实体
│   │       │   ├── edge_entity.py           # 边实体
│   │       │   ├── variable_entity.py       # 变量实体
│   │       │   └── workflow_entity.py       # 工作流实体
│   │       ├── nodes/                       # 工作流节点类型实现
│   │       │   ├── base_node.py             # 节点基类
│   │       │   ├── start/                   # 开始节点
│   │       │   ├── end/                     # 结束节点
│   │       │   ├── llm/                     # LLM 调用节点
│   │       │   ├── code/                    # 代码执行节点
│   │       │   ├── tool/                    # 工具调用节点
│   │       │   ├── http_request/            # HTTP 请求节点
│   │       │   ├── dataset_retrieval/       # 数据集检索节点
│   │       │   ├── template_transform/      # 模板转换节点
│   │       │   ├── question_classifier/     # 问题分类节点
│   │       │   └── iteration/               # 循环迭代节点
│   │       └── utils/                       # 工作流工具函数
│   ├── entity/                 # 实体定义
│   ├── exception/              # 自定义异常定义
│   ├── extension/              # 扩展模块
│   ├── handler/                # API 接口处理器（Controller层）
│   ├── lib/                    # 内部工具库
│   ├── middleware/             # HTTP 中间件
│   ├── migration/              # 数据库迁移（Alembic）
│   ├── model/                  # 数据库模型（DAO层）
│   ├── router/                 # 路由配置
│   ├── schema/                 # 请求/响应模型（Pydantic）
│   ├── server/                 # 服务启动配置
│   ├── service/                # 业务逻辑层（Service层）
│   └── task/                   # 异步任务模块
├── pkg/                        # 公共可复用组件
├── storage/                    # 存储相关模块
├── test/                       # 单元测试/集成测试
├── Dockerfile
├── requirements.txt
└── ...
```

### 详细文档

- 后端 API 文档见 `project-docs/api-document.md`
- 后端关系数据库表结构见 `api/docs/02.LLMOps数据库ER图.drawio`

## 前端

详细目录结构可以从记忆读取：/home/wissfi/.claude/projects/-home-wissfi-projects-LLMOps/memory

### 使用框架

- vue3
- vite 构建
- TypeScrip

### 目录结构

- docker/ - Docker 和 Nginx 配置
- src/assets/ - 图片、样式等资源
- src/components/ - 公共组件、图标
- src/config/ - 配置文件
- src/hooks/ - 自定义 Vue hooks
- src/models/ - TypeScript 类型定义
- src/router/ - 路由配置
- src/services/ - API 接口服务
- src/stores/ - Pinia 状态管理
- src/utils/ - 工具函数
- src/views/ - 页面视图（按功能模块划分：auth、space、store、web-apps等）
