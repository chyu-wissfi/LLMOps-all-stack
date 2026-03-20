# AetherLLMOps

![GitHub stars](https://img.shields.io/github/stars/chyu-wissfi/LLMOps-all-stack?style=social)
![GitHub forks](https://img.shields.io/github/forks/chyu-wissfi/LLMOps-all-stack?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/chyu-wissfi/LLMOps-all-stack?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/chyu-wissfi/LLMOps-all-stack)
![GitHub language count](https://img.shields.io/github/languages/count/chyu-wissfi/LLMOps-all-stack)
![GitHub top language](https://img.shields.io/github/languages/top/chyu-wissfi/LLMOps-all-stack)
![GitHub last commit](https://img.shields.io/github/last-commit/chyu-wissfi/LLMOps-all-stack?color=red)

目前README.md文件正在更新中，还比较粗糙，项目整体框架完善后会整体更新整理一次
一些模块的技术文档和这个项目的API文档会随时更新，可以在LLMOps项目技术文档中查看到

## AetherLLMOps 架构

待更新

## 起动后端项目

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 配置环境变量
   - 复制`.env.example`文件为`.env`
   - 填写 OpenAI API 密钥和其他必要的配置

```bash
cp .env.example .env
```

3. 启动项目

```bash
python -m flask run
```

## 项目前端架构与基础框架选择

### 项目前端架构

LLMOps 项目的前端部分包含了 视图层、编译层、代码层和数据层 4 个部分。

1. 视图层 ：涵盖浏览器和业务模块，主要功能是将用户选择的 web 资源，通过解析网页源文件进行显示，并展示出不同的模块。
2. 编译层 ：编译层分析项目结构，根据入口文件找到 JavaScript 模块及其它浏览器不能直接运行的拓展语言（如 TypeScript、SCSS 等），通过 Vite 将源代码编译成适合浏览器使用的格式。
3. 代码层 ：在代码层，每个独立的可视或可交互区域都视为一个组件，并将所需的各种资源集中在组件目录下维护。Vue-router 用于页面路径和组件的映射，Pinia 集中管理应用状态，UI 组件库提高界面设计效率，util 文件夹则管理全局工具。
4. 数据层 ：数据层包括 Service 模块，负责业务逻辑的独立性和重用性；Network 模块，查看网络请求的内容；以及 Api 模块，通过 fetch 请求从后端接口获取所需数据。
   项目技术架构图如下：
   ![前端技术架构图](README/前端技术架构图.png)

### 项目技术选型

选定一个前端框架时，我考虑的因素有：

- 框架是否能满足大部分应用的需求？如果不能，那么需要使用哪个框架？
- 框架是否有丰富的组件库？如果没有，我的团队和组织是否有独立开发的能力？
- 框架的社区支持怎样？在遇到问题时能否快速方便地找到人解答？
- 框架的替换成本如何？假如我的新项目将使用 B 框架，那么我还需要额外学习什么内容？
  目前市面上的三大前端框架 Angular、React、Vue，为什么选择 Vue 作为最基础的框架？

1. React ：React 只是一个 View 层的框架，为了完成一个完整的应用，还需要使用 路由库、执行单向流库、webAPI 调用库、测试库、依赖管理、编译构建配置 等，要搭建一个完整的 React 功能，需要做大量的额外工作，需要单独学习 JSX 模板语法。
2. Angular ：一个大而全的框架，提供了开发应用所需的脚手架，包含测试、运行服务、打包等部分，但是上手成本高，框架限制高，对新手不友好，国内企业使用得比较少，并且于 2022 年已经停止维护。
3. Vue ：对于没有 Angular 和 React 经验的团队来说，Vue 是一个非常好的选择。Vue 借鉴了 Angular 和 React 的一些思想，在其基础上开发了一套更易上手的框架。Vue 的开发者尤雨溪是中国人，框架本身提供了 大量丰富的中文文档 ，这也为 Vue 的发展和使用带来巨大的优势。
   ![前端技术选型](README/前端技术选型.png)

## 贡献

贡献是使开源社区成为学习、激励和创造的惊人之处。非常感谢您所做的任何贡献。如果您有任何建议或功能请求，请先开启一个议题讨论您想要改变的内容。

## 许可证

该项目根据 Apache-2.0 许可证的条款进行许可。详情请参见[LICENSE](LICENSE)文件。
