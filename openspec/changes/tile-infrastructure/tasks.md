## 1. 环境配置

- [ ] 1.1 创建 .env.example 配置文件模板
- [ ] 1.2 配置 SQLite 数据库路径
- [ ] 1.3 配置 MinIO 连接信息（endpoint、access_key、secret_key、bucket）
- [ ] 1.4 配置 Redis 连接信息（用于缓存）

## 2. 数据库表结构

- [ ] 2.1 创建 Categories 表（类目）
- [ ] 2.2 创建 Brands 表（品牌）
- [ ] 2.3 创建 Products 表（商品）
- [ ] 2.4 创建 Employees 表（员工）
- [ ] 2.5 创建 Statistics 表（统计）
- [ ] 2.6 创建索引（category_id、brand_id、date 等）

## 3. 迁移管理

- [ ] 3.1 配置 Alembic 迁移工具
- [ ] 3.2 创建初始迁移脚本
- [ ] 3.3 编写回滚脚本

## 4. MinIO 配置

- [ ] 4.1 配置 MinIO 客户端连接
- [ ] 4.2 验证 MinIO 服务可访问
- [ ] 4.3 配置 bucket 和 prefix

## 5. 数据备份

- [ ] 5.1 制定 SQLite 备份策略
- [ ] 5.2 编写备份脚本
- [ ] 5.3 制定 MinIO 数据保留策略

## 6. 测试验证

- [ ] 6.1 验证数据库连接
- [ ] 6.2 验证 MinIO 连接
- [ ] 6.3 运行数据库迁移测试
- [ ] 6.4 测试数据读写