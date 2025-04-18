# DOCX-检查工具

这是一个基于 FastAPI 的文档检查工具，用于检查 DOCX 文件的格式和内容。

## 项目结构

```
.
└── backend/              # 后端代码
    ├── app/              # 应用代码
    │   ├── config.py     # 配置文件
    │   ├── models/       # 数据模型
    │   └── routers/      # API路由
    ├── main.py           # 应用入口点
    └── requirements.txt  # 依赖项
```

## 技术栈

- **后端**：FastAPI + Uvicorn
- **数据验证**：Pydantic

## 安装与运行

### 环境要求

- Python 3.7+

### 创建并激活虚拟环境

```bash
# 创建虚拟环境
cd backend
python3 -m venv venv

# 激活虚拟环境
## Windows
venv\Scripts\activate
## macOS/Linux
source venv/bin/activate
```

### 安装依赖

```bash
# 确保已激活虚拟环境
pip install -r requirements.txt
```

### 运行应用

```bash
# 确保已激活虚拟环境
python main.py
```

应用将在 http://localhost:8000 上运行，API 文档可在 http://localhost:8000/docs 访问。

## API 端点

- **GET /**: 欢迎信息
- **GET /api/hello**: 返回"你好，世界！"消息

## 开发

### 添加新路由

在 `backend/app/routers/` 目录中添加新的路由文件，并在 `api.py` 中引入。

### 添加新模型

在 `backend/app/models/` 目录中的 `schemas.py` 文件中添加新的数据模型
