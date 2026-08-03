## Why

BUG-0095 指出管理端类目树右侧计数显示为商品数量，而用户期望该位置显示下一层级类目数量。该问题会让后台运营误判类目层级结构，尤其在维护一级、二级类目时，商品数量与子类目数量混用会干扰类目梳理和数据排查。

现有正式 spec 明确 `GET /api/v1/admin/tile-categories/tree` 节点包含 `sku_count`，但没有把直接子类目数量字段及管理端展示口径写成稳定契约。后端已具备直接子类目数量字段，问题收敛到管理端类目树组件当前绑定了商品数量计数字段。

## What Changes

- 明确管理端类目树 API 节点必须同时区分 `sku_count` 与 `children_count`。
- 明确 `sku_count` 只表达商品/SKU 数量，不得用于类目树节点右侧的下级类目数量展示。
- 修正 Web 管理端类目树节点右侧计数绑定，普通节点显示直接子类目数量，叶子节点显示 `0`。
- 明确“全部类目”入口右侧数字显示顶层类目数量，不显示商品总数。
- 补充前端组件/页面回归测试；若接口契约或 OpenAPI 缺失 `children_count`，同步 API、OpenAPI、Orval、接口文档和后端测试。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `tile-category-management`: 管理端类目树 API 必须提供直接子类目数量字段，并明确 `sku_count` 与类目数量的语义边界。
- `web-client`: 管理端类目树右侧计数必须展示下一层级类目数量，“全部类目”入口展示顶层类目数量。

## Impact

- 影响范围：管理后台 Web 的类目树组件与类目管理页面。
- 可能影响 API 响应契约、OpenAPI、Orval 和接口文档，取决于当前 `children_count` 是否已在 OpenAPI 中暴露。
- 不影响数据库结构、权限、MinIO、媒体上传、小程序和 Docker Compose。
- 需要补充或更新管理端类目树前端测试；若 API 契约补齐，则需要补充后端接口测试。

## Rollback Plan

如修复导致类目树计数展示异常或筛选联动回归，可回退前端字段绑定改动，恢复页面可用性；但不得把商品数量继续定义为类目树右侧计数的长期口径。若新增或同步 `children_count` 契约引发兼容问题，应保留 `sku_count` 既有语义不变，并只回滚新增字段消费逻辑。
