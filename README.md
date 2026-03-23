<h1 align="center">Aether LLMOps 原生AI 应用开发平台</h1>

![GitHub stars](https://img.shields.io/github/stars/chyu-wissfi/aether-llmops-platform?style=social)
![GitHub forks](https://img.shields.io/github/forks/chyu-wissfi/aether-llmops-platform?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/chyu-wissfi/aether-llmops-platform?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/chyu-wissfi/aether-llmops-platform)
![GitHub language count](https://img.shields.io/github/languages/count/chyu-wissfi/aether-llmops-platform)
![GitHub top language](https://img.shields.io/github/languages/top/chyu-wissfi/aether-llmops-platform)
![GitHub last commit](https://img.shields.io/github/last-commit/chyu-wissfi/aether-llmops-platform?color=red)

## Aether LLMOps 项目服务架构设计

在整个Aether LLMOps项目中，我使用了多个服务，具体如下：

1. API：基于`Flask`和`LangChain`搭建的 `LLMOps API` 服务。
2. Web：基于`Vue.js`搭建的 `LLMOps`前端服务，一个静态`html`文件服务。
3. 数据库：`Postgres`数据库，用于存储`LLMOps`项目的数据信息。
4. 缓存：`Redis`缓存数据库，用于存储`Embeddings`缓存、`Celery`消息代理等信息。
5. 向量数据库：`Weaviate`向量数据库，用于存储`Embeddings`向量。
6. 任务队列：`Celery`任务队列，用于执行异步任务。
7. Nginx反向代理：反向代理连接`API`和`WEB`服务，实现域名访问 `LLMOps` 项目。

为了便于部署和管理，我将这些服务部署到`Docker`容器中，并使用`docker-compose`管理多个容
器，同时通过 `Nginx` 进行反向代理，连接 `API` 和 `web` 服务，项目整体服务架构设计图如下：

![docker-compose.jpg](./README/docker-compose.jpg)

## 快速开始

```bash
cd docker
docker-compose up -d
```

## 项目时间节点

```mermaid
gantt
    title LLMOps项目开发计划
    dateFormat  YYYY-MM-DD
    section 第一阶段
    需求分析              :2026-01-01, 14d
    架构设计              :2026-01-15, 16d
    基础框架搭建           :2026-01-31, 18d
    数据库表设计           :2026-01-31, 10d
    section 第二阶段
    核心模块开发&性能优化   :2026-02-18, 30d
    工作流引擎&知识库模块   :2026-02-18, 20d
    多LLM接入&安全性保障   :2026-02-18, 20d
    section 第三阶段
    发布渠道集成           :2026-03-17, 15d
    多模态插件             :2026-03-17, 15d
    第三方应用集成         :2026-03-17, 15d
    开放API开发           :2026-03-17, 15d
    section 第四阶段
    生产环境调优           :2026-04-02, 20d
    上线部署              :2026-04-22, 10d
```

## 附录

### 术语表

| 术语 | 定义                                            |
| ---- | ----------------------------------------------- |
| LLM  | Large Language Model，大语言模型                |
| RAG  | Retrieval-Augmented Generation，检索增强生成    |
| API  | Application Programming Interface，应用程序接口 |
| QPS  | Queries Per Second，每秒查询率                  |
| P99  | 99%的请求响应时间                               |

## 贡献

贡献是使开源社区成为学习、激励和创造的惊人之处。非常感谢您所做的任何贡献。如果您有任何建议或功能请求，请先开启一个议题讨论您想要改变的内容。

## 许可证

该项目根据 Apache-2.0 许可证的条款进行许可。详情请参见[LICENSE](LICENSE)文件。
