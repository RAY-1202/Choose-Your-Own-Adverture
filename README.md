# Choose Your Own Adventure - 互动故事生成器

## 项目介绍

这是一个基于大语言模型（LLM）的全栈互动冒险故事生成器。用户输入一个故事主题，后端通过豆包（Doubao）大模型自动生成具有**多分支路径**和**多结局**的冒险故事树，前端以交互式 UI 呈现故事内容，玩家通过做出选择来推动剧情发展，最终到达不同的结局（胜利或失败）。

### 核心功能

- 🎭 **主题自定义**：用户可输入任意主题（奇幻、科幻、悬疑等），由 AI 生成对应风格的冒险故事
- 🌳 **分支叙事**：每个故事节点提供 2-3 个选项，构成 3-4 层深度的故事树结构
- 🏆 **多结局体验**：包含胜利结局和失败结局，鼓励玩家反复探索不同路径
- ⚡ **异步生成**：采用后台任务 + 轮询机制（Job），故事生成过程不阻塞用户操作
- 🔄 **重玩与新建**：支持重新开始当前故事或生成全新故事
- 🍪 **会话管理**：通过 Cookie 自动关联用户与其生成的故事

## 技术栈

### 后端

| 技术 | 说明 |
|------|------|
| **Python 3.12+** | 运行环境 |
| **FastAPI** | 高性能异步 Web 框架，提供 RESTful API |
| **Uvicorn** | ASGI 服务器 |
| **SQLAlchemy** | ORM 框架，管理故事、节点、任务等数据模型 |
| **LangChain + LangChain-OpenAI** | LLM 应用框架，对接豆包（Doubao）大模型 API |
| **Pydantic / Pydantic-Settings** | 数据校验与配置管理 |
| **python-dotenv** | 环境变量加载 |
| **psycopg2-binary** | PostgreSQL 数据库驱动 |

### 前端

| 技术 | 说明 |
|------|------|
| **React 19** | UI 框架 |
| **Vite 6** | 前端构建工具，支持热更新 |
| **React Router v7** | 客户端路由管理 |
| **Axios** | HTTP 请求库，与后端 API 通信 |

### 数据库

| 技术 | 说明 |
|------|------|
| **SQLite** | 本地开发数据库 |
| **PostgreSQL** | 生产环境数据库（通过 SQLAlchemy 兼容切换） |

## 项目结构

```
Choose-Your-Own-Adventure/
├── README.md                    # 项目总说明文档
├── backend/                     # 后端服务
│   ├── main.py                  # FastAPI 应用入口
│   ├── requirements.txt         # Python 依赖
│   ├── pyproject.toml           # 项目配置
│   ├── core/                    # 核心业务逻辑
│   │   ├── config.py            # 应用配置（环境变量加载）
│   │   ├── models.py            # LLM 响应的 Pydantic 数据模型
│   │   ├── prompts.py           # LLM 提示词模板
│   │   └── story_generator.py   # 故事生成器（调用 LLM + 递归构建故事树）
│   ├── db/
│   │   └── database.py          # 数据库连接与会话管理
│   ├── models/                  # SQLAlchemy 数据库模型
│   │   ├── story.py             # Story 和 StoryNode 模型
│   │   └── job.py               # StoryJob 异步任务模型
│   ├── routers/                 # API 路由
│   │   ├── story.py             # 故事相关接口（创建、查询）
│   │   └── job.py               # 任务状态查询接口
│   └── schemas/                 # Pydantic 请求/响应模式
│       ├── story.py             # 故事相关 Schema
│       └── job.py               # 任务相关 Schema
└── frontend/                    # 前端应用
    ├── package.json             # Node.js 依赖
    ├── vite.config.js           # Vite 配置（含开发代理）
    ├── index.html               # HTML 入口
    └── src/
        ├── App.jsx              # 应用根组件与路由配置
        ├── util.js              # API 地址等工具常量
        └── components/
            ├── ThemeInput.jsx       # 主题输入组件
            ├── StoryGenerator.jsx   # 故事生成流程控制组件
            ├── LoadingStatus.jsx    # 加载状态展示组件
            ├── StoryLoader.jsx      # 故事数据加载组件
            └── StoryGame.jsx        # 故事交互游戏组件
```

## 快速开始

### 环境要求

- Python >= 3.12
- Node.js >= 18

### 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（在 backend 目录下创建 .env 文件）
# DATABASE_URL=sqlite:///./test.db
# OPENAI_API_KEY=your_api_key
# OPENAI_API_BASE=https://ark.cn-beijing.volces.com/api/v3
# ALLOWED_ORIGINS=http://localhost:5173

# 启动服务
python main.py
```

服务启动后可访问：
- API 文档：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173 即可开始体验互动故事。

