## Why

瓷砖信息管理平台需要一个统一的后端 API 服务，为小程序前端、Web前台、Web后台提供数据支撑。后端负责产品数据的存储和检索、员工认证、文件上传和存储、数据统计等核心能力。

## What Changes

- 新增 FastAPI 后端服务
- 实现产品模块：商品增删改查、上下架、多维筛选、全文搜索
- 实现类目模块：类目管理
- 实现品牌模块：品牌管理
- 实现文件模块：图片/视频上传、存储到 MinIO
- 实现员工模块：员工登录、角色认证、权限控制
- 实现统计模块：浏览量、收藏量、分享量统计

## Capabilities

### New Capabilities

- **product-api**: 产品相关 API
- **category-api**: 类目相关 API
- **brand-api**: 品牌相关 API
- **file-api**: 文件上传、存储、访问 API
- **auth-api**: 员工登录、认证、权限 API
- **statistics-api**: 运营统计 API

### Modified Capabilities

- 无

## Impact

- 新增 Python FastAPI 后端项目
- 使用 SQLite 存储业务数据
- 使用 MinIO 存储图片和视频（连接已部署的 MinIO 服务）
- 为所有前端应用提供 REST API 接口