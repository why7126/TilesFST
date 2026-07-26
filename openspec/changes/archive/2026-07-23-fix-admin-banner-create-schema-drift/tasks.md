## 1. 生产证据与范围确认

- [x] 1.1 收集或复核 `BUG-0083` 对应生产请求 payload、响应 body、request_id 和后端日志，确认 500 的具体 SQL/运行时异常。
- [x] 1.2 对目标 MySQL 执行 schema drift 检查，记录 `banners` 缺失字段、额外字段、索引/外键状态和检查时间。
- [x] 1.3 确认生产后端镜像与 Web bundle 版本，排除前后端版本不一致导致的 payload 漂移。

## 2. MySQL 兼容迁移

- [x] 2.1 扩展 `src/backend/app/db/mysql_migrations.py`，对既有 `banners` 表逐列检查并幂等补齐创建/编辑接口写入字段。
- [x] 2.2 字段定义与 `src/backend/app/db/schema.mysql.sql` 保持兼容，至少覆盖 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark`。
- [x] 2.3 保持或补齐必要索引；外键添加前检查脏数据，存在脏数据时记录跳过原因和计数。
- [x] 2.4 确保 MySQL 兼容迁移仅在 MySQL backend 执行，不影响 SQLite 本地/demo 路径。

## 3. Banner 保存链路回归

- [x] 3.1 回归 `POST /api/v1/admin/banners` 创建 `jump_type=BRAND_DETAIL` Banner，确认 HTTP 200、统一 envelope 和 `brand_id` 回显。
- [x] 3.2 回归 `PUT /api/v1/admin/banners/{id}` 编辑品牌类型 Banner，确认品牌、图片来源、排序、有效期和备注不丢失。
- [x] 3.3 回归 `image_source=brand_logo` 与 `image_source=custom_upload` 两种图片来源。
- [x] 3.4 回归品牌不存在、品牌未启用、品牌无 Logo、Logo key 不匹配、标题重复等失败场景，确认返回 4xx 业务错误且不裸 500。

## 4. 测试与文档

- [x] 4.1 更新 `tests/test_mysql_migrations.py`，覆盖旧 MySQL `banners` 表缺失多个创建字段时的幂等补齐。
- [x] 4.2 更新 `tests/test_mysql_schema_drift.py` 或相关脚本测试，确保 drift 检查能报告 `banners` 缺列。
- [x] 4.3 运行 `src/backend/tests/test_admin_banners.py`，确保品牌类型 Banner 新增、编辑和失败场景不回归。
- [x] 4.4 同步 `docs/04-database-design.md`、`docs/02-deployment.md`；若新增错误码或 API schema 变化，同步 `docs/03-api-index.md`、`docs/standards/error-codes.md`、OpenAPI 和 Orval。

## 5. 发布与验收

- [x] 5.1 记录生产执行前备份、迁移命令、执行结果和回滚边界，避免提交真实 DSN、密钥或客户数据。
- [x] 5.2 提供目标 MySQL schema drift 检查通过证据，证明 `banners` 无阻塞缺列。
- [x] 5.3 提供生产或等价环境品牌类型 Banner 创建成功 smoke 证据。
- [x] 5.4 运行 `openspec validate --change fix-admin-banner-create-schema-drift --strict` 并修复问题。
- [x] 5.5 修复完成后评估是否需要沉淀 `docs/knowledge-base/incidents/`；若无复用价值，在实现输出中说明。
