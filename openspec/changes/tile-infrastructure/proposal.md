## Why

瓷砖信息管理平台需要可靠的数据存储基础设施，包括关系数据库（SQLite）存储业务数据，对象存储（MinIO）存储图片和视频文件。本项目连接已部署的 MinIO 服务，不负责 MinIO 的部署和运维。

## What Changes

- 配置 SQLite 数据库连接
- 设计并创建业务数据表（商品、类目、品牌、员工、统计）
- 配置 MinIO 对象存储连接
- 配置数据备份策略
- 配置开发/测试/生产环境切换

## Capabilities

### New Capabilities

- **database**: SQLite 数据库配置和表结构
- **object-storage**: MinIO 对象存储配置和操作接口
- **migration**: 数据库迁移管理
- **backup**: 数据备份策略

### Modified Capabilities

- 无

## Impact

- 为 tile-api-backend 提供数据存储支撑
- 所有业务数据存储在 SQLite
- 所有图片和视频存储在 MinIO