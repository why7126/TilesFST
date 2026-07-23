## Why

管理端类目新增 / 编辑弹窗仍沿用旧规则，要求运营填写类目编码，并允许 1-30 字符类目名称。REQ-0067 已评审通过，明确类目编码应由系统生成，类目名称需要短、规范且同层级唯一，以降低运营维护成本并提升类目主数据质量。

## What Changes

- **BREAKING:** 管理端类目创建 API 不再要求前端提交 `code`；后端在创建时生成 `CAT-` 前缀唯一编码。
- 管理端类目新增 / 编辑弹窗不展示可填写的类目编码字段。
- 类目名称收敛为最多 10 个字符，仅允许中文、英文和数字。
- 类目名称在同一 `parent_id` 层级下必须唯一；编辑自身不误判重复。
- 上级类目、类目名称、排序权重必须有必填标识与字段级校验。
- 保留 `tile_categories.code` 作为唯一内部编码字段；默认不做数据库结构变更或历史数据清理。
- 同步 OpenAPI、Orval、错误码文档与前后端测试。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `tile-category-management`: 调整类目数据模型约束、创建/更新 API、编码生成、名称校验、同层级唯一和错误码契约。
- `web-client`: 调整管理端类目新增 / 编辑弹窗字段、必填标识、字段级错误展示和 admin-modal 横切验收。

## Impact

- 后端：类目创建 / 更新 Schema、业务校验、编码生成、同层级名称查重、错误码和测试。
- API：`POST /api/v1/admin/tile-categories` 请求契约移除必填 `code`；响应继续返回 `code`。
- Web 管理端：`CategoryFormModal` 字段、必填标识、本地校验、payload、错误映射和组件测试。
- Orval：创建请求类型变化后必须重新生成并更新调用方。
- 数据库：保留 `tile_categories.code UNIQUE NOT NULL`；默认不新增迁移。
- 小程序 / 店主端：不直接修改页面逻辑，只消费更规范的类目主数据。
- 存储：不涉及对象存储或媒体上传策略变化。
