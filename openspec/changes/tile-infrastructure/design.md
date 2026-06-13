## Context

本项目是瓷砖信息管理平台的数据存储基础设施，包括 SQLite 数据库和 MinIO 对象存储。

技术约束：
- SQLite 作为关系数据库
- 连接已部署的 MinIO 服务（不负责部署）
- 配置通过环境变量注入

## Goals / Non-Goals

**Goals:**
- 设计并创建业务数据表结构
- 配置 SQLite 数据库连接
- 配置 MinIO 对象存储连接
- 实现数据迁移机制
- 实现备份策略

**Non-Goals:**
- 不部署 MinIO 服务
- 不负责生产环境运维

## Decisions

### 1. SQLite 配置

**决策：使用 SQLAlchemy ORM + WAL 模式**

- 启用 WAL 模式提高并发性能
- 使用 Alembic 管理数据库迁移
- 敏感配置通过环境变量注入

### 2. MinIO 配置

**决策：连接已部署的 MinIO 服务**

- 不创建新的 bucket，使用已有的 bucket
- 配置预签名 URL 访问策略
- 对象 key 生成规则：prefix + uuid + 后缀

### 3. 环境配置

**决策：使用 .env 文件管理配置**

- 开发环境：本地 SQLite + 本地 MinIO
- 生产环境：云端 SQLite + 腾讯 COS（未来可迁移）

### 4. 数据表设计

```
┌─────────────┐     ┌─────────────┐
│ categories  │     │   brands    │
├─────────────┤     ├─────────────┤
│ id          │     │ id          │
│ name        │     │ name        │
│ parent_id   │     │ logo_url    │
│ sort_order  │     │ created_at  │
│ created_at  │     └─────────────┘
└─────────────┘            │
                           │
┌─────────────┐            │
│  products   │◀───────────┤
├─────────────┤            │
│ id          │            │
│ name        │            │
│ category_id │────────────┤
│ brand_id    │            │
│ size        │            │
│ price       │            │
│ images      │            │
│ video_url   │            │
│ description │            │
│ is_active   │            │
│ created_at  │            │
└─────────────┘            │
                           │
┌─────────────┐            │
│ employees   │            │
├─────────────┤            │
│ id          │            │
│ username    │            │
│ password    │            │
│ role        │            │
│ created_at  │            │
└─────────────┘            │
                           │
┌─────────────┐            │
│ statistics  │◀───────────┘
├─────────────┤
│ id          │
│ product_id  │
│ type        │ (view/favorite/share)
│ count       │
│ date        │
└─────────────┘
```

## Risks / Trade-offs

| 风险 | 描述 | 缓解方案 |
|-----|------|----------|
| SQLite 并发 | 并发写入可能产生锁 | 使用 WAL 模式，减小事务粒度 |
| MinIO 不可用 | MinIO 服务不可用 | 实现重试机制，记录日志 |
| 数据丢失 | 数据库损坏 | 定期备份 |