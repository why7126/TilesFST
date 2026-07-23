---
created_at: 2026-07-21 15:28:51
updated_at: 2026-07-21 23:00:44
---

## 1. 生产失败证据与根因确认

- [x] 1.1 收集或复核生产保存接口 URL、HTTP 状态码、响应 JSON、请求 payload 和后端日志。
- [x] 1.2 检查生产 MySQL `banners` 表结构，确认 `brand_id`、`image_source`、`jump_type`、`sku_gallery_asset_id` 等 Banner 关键字段是否与 baseline 一致。
- [x] 1.3 区分 schema drift 与业务校验失败：若响应为 `30052` 或等价业务错误，核对品牌状态、Logo object key 和图片来源；若响应为 500/SQL 缺列，按数据库漂移修复。

## 2. 数据库修复

- [x] 2.1 增加 MySQL 幂等迁移或 schema drift 修复逻辑，补齐既有 `banners.brand_id` 字段。
- [x] 2.2 保持 SQLite schema、SQLite migration、MySQL schema 与数据库文档中 Banner 关键字段语义一致。
- [x] 2.3 评估并补齐支持 `display_client`、`position`、`status`、`brand_id` 查询/约束的索引或外键；若生产脏数据导致无法加外键，在实现记录中说明取舍。
- [x] 2.4 记录生产执行前备份、迁移命令、执行结果和回滚边界。

## 3. Banner 保存链路修复

- [x] 3.1 回归 `POST /api/v1/admin/banners` 创建 `jump_type=BRAND_DETAIL` Banner，确认 `brand_id` 持久化。
- [x] 3.2 回归 `PUT /api/v1/admin/banners/{id}` 编辑品牌详情 Banner，确认品牌、图片来源、排序、有效期和备注可保存。
- [x] 3.3 覆盖 `image_source=brand_logo` 时 object key 必须匹配品牌 `logo_object_key`。
- [x] 3.4 覆盖 `image_source=custom_upload` 时保存使用后端授权上传返回的 Banner object key。
- [x] 3.5 确保品牌不存在、品牌未启用、品牌无 Logo、Logo key 不匹配、标题重复等失败场景返回统一错误 envelope 和稳定错误码/信息。
- [x] 3.6 确保数据库漂移错误不会向管理端暴露原始 SQL、DSN、MinIO 凭据或内部堆栈。

## 4. 展示与管理端一致性

- [x] 4.1 保存成功后，管理端列表、详情和编辑弹窗应回显同一品牌详情 Banner 配置。
- [x] 4.2 小程序首页轮播和品牌列表页轮播公开查询应继续按 position 分流读取已上线且有效期内 Banner。
- [x] 4.3 回归非品牌跳转类型 Banner 保存不受影响。

## 5. 测试与文档

- [x] 5.1 新增或更新后端 Banner API 测试，覆盖品牌详情 Banner 新增、编辑、`brand_logo`、`custom_upload` 和失败场景。
- [x] 5.2 新增 MySQL schema drift/迁移验证，至少证明既有缺 `brand_id` 的 `banners` 表可被安全补齐，默认 SQLite pytest 不依赖本机 MySQL。
- [x] 5.3 若新增或调整错误码，同步 `docs/standards/error-codes.md`。
- [x] 5.4 若 API schema 变化，同步 OpenAPI、Orval、`docs/03-api-index.md` 和相关测试；若无 schema 变化，在实现输出中说明不需要 Orval。
- [x] 5.5 更新 `BUG-0075` trace、Change trace 与验收证据。
- [x] 5.6 修复完成后评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若无复用价值，在验收输出中说明不新增知识库条目。
