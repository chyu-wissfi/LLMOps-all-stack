# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

LLMOps平台全栈项目，包含前端(Vue3 + Vite + TypeScript)和后端(Flask + SQLAlchemy + LangGraph)。

## 常用命令

### 前端开发 (./ui/)

```bash
cd ui

# 安装依赖
npm install

# 开发服务器
npm run dev

# 生产构建
npm run build

# 运行测试
npm run test:unit

# 代码格式化
npm run format

# 代码检查
npm run lint
```

### 后端开发 (./api/)

```bash
cd api

# 创建conda环境
conda create -n llmops python=3.11
conda activate llmops

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 运行开发服务器 (自动重载)
python app.py

# 或使用gunicorn
python -m gunicorn app:app -c gunicorn.conf.py

# 运行测试
pytest

# 运行单个测试
pytest test/path/to/test_file.py::test_function -v

# 代码格式化
black .
isort .

# 运行pre-commit
pre-commit run --all-files
```

### 数据库操作

```bash
cd api

# 数据库迁移
alembic revision --autogenerate -m "migration message"
alembic upgrade head
alembic downgrade -1
```

### Docker开发

```bash
# 启动所有服务
docker-compose -f docker/docker-compose.yml up -d

# 查看日志
docker-compose -f docker/docker-compose.yml logs -f

# 停止服务
docker-compose -f docker/docker-compose.yml down
```

## 代码规范

### 缩进规范
- **后端代码** (./api/): 4空格缩进
- **前端代码** (./ui/): 2空格缩进

### 命名规范
- 变量: camelCase
- 常量: UPPER_SNAKE_CASE
- 类名: PascalCase
- 文件名: snake_case (后端), camelCase (前端)

### 注释规范
- 代码注释使用**中文**
- 复杂逻辑必须添加注释

### 异步代码
- 优先使用 async/await
- 避免嵌套回调

## 架构说明

### 前端架构 (Vue3 + Vite)

```
src/
├── components/     # 公共组件
├── views/          # 页面视图
│   ├── auth/       # 认证相关
│   ├── space/      # 工作空间(apps, datasets, workflows, tools)
│   ├── store/      # 商店
│   └── web-apps/   # Web应用
├── services/       # API服务层
├── stores/         # Pinia状态管理
├── models/         # TypeScript类型定义
├── router/         # 路由配置
├── hooks/          # 自定义Vue hooks
└── utils/          # 工具函数
```

### 后端架构 (Flask)

```
api/
├── app/            # 应用入口层
│   └── http/       # HTTP服务入口
├── internal/       # 核心业务实现层
│   ├── core/       # 核心组件
│   │   ├── agent/          # Agent实现
│   │   ├── builtin_apps/   # 内置应用
│   │   ├── language_model/ # 语言模型封装
│   │   ├── tools/          # 工具集
│   │   ├── vector_store/   # 向量存储
│   │   └── workflow/       # 工作流引擎
│   ├── entity/     # 实体定义
│   ├── handler/    # API处理器(Controller)
│   ├── middleware/ # HTTP中间件
│   ├── model/      # 数据库模型(DAO)
│   ├── schema/     # 请求/响应模型(Pydantic)
│   └── service/    # 业务逻辑层
├── config/         # 配置模块
├── migration/      # 数据库迁移
├── pkg/            # 公共可复用组件
└── test/           # 测试
```

### 核心模块说明

**工作流引擎** (`internal/core/workflow/`)
- 支持多种节点类型: start, end, llm, code, tool, http_request, dataset_retrieval, template_transform, question_classifier, iteration
- 实体定义: node_entity, edge_entity, variable_entity, workflow_entity

**语言模型** (`internal/core/language_model/`)
- 支持多厂商: OpenAI, Anthropic, Azure OpenAI
- 基类: base.py, 工厂: factory.py

**工具系统** (`internal/core/tools/`)
- 内置工具: search, calculator, web_scraper
- API工具: api_tools/

## 环境配置

### 必需环境变量

后端 `.env`:
```
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/llmops

# Redis
REDIS_URL=redis://localhost:6379/0

# LLM API Keys
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
AZURE_OPENAI_API_KEY=

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

### 服务依赖

- PostgreSQL 14+
- Redis 6+
- Python 3.11+
- Node.js 18+

## 提交代码到Github

```bash
git add .
git commit -a -m "<描述信息>"
git push llmops
```

## 参考资料

- 后端API文档: `project-docs/api-document.md`
- 数据库ER图: `api/docs/02.LLMOps数据库ER图.drawio`
- 需求文档: `project-docs/requirement-document.md`
