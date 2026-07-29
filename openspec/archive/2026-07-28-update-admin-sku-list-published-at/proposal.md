## Why

管理端瓷砖 SKU 列表当前仅展示更新时间，运营无法在列表层快速区分 SKU 的发布时间与后续维护时间。新增发布时间列可以减少进入详情或编辑页确认的操作成本，并让新品巡检、发布节奏核对和问题沟通更直接。

## What Changes

- 在管理端瓷砖 SKU 列表中新增“发布时间”列，位置位于“更新时间”列之前。
- “发布时间”使用与“更新时间”一致的日期时间格式、空值占位和视觉层级。
- 新增并使用语义明确的 `tiles.published_at` 字段，不得直接复用更新时间或创建时间冒充发布时间。
- 管理端 SKU 列表响应补充 `published_at`；同步后端响应、Pydantic Schema、OpenAPI、Orval、接口文档和测试。
- 现有 `publish` 成功时刷新 `published_at`，恢复上架视为重新发布；`unpublish` 不清空数据库历史值，但非已上架状态响应返回 `published_at: null`。
- 保持现有分页、搜索、筛选、默认排序、加载态、空态、失败态和操作行为不变。
- 不新增发布时间筛选、排序、导出，不新增发布审批、定时发布或撤回流程，不影响店主 Web 或小程序。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `tile-sku-management`: 管理端 SKU 列表与筛选 API 需要支持列表展示发布时间列，并在必要时补充列表响应契约。

## Impact

```yaml
impact:
  backend: possible
  web: true
  miniapp: false
  admin: true
  database: possible
  storage: false
  api: possible
capabilities:
  new: []
  modified:
    - tile-sku-management
change_type: update
source_requirement: REQ-0079-admin-sku-list-published-at
```

- Web 管理端：SKU 列表列配置、时间格式渲染、空值展示、表格宽度与回归测试。
- 后端/API：补充列表项 `published_at` 与 publish/unpublish 响应语义，需同步响应 Schema 与 OpenAPI/Orval。
- 数据库：新增 `tiles.published_at` 字段和兼容迁移；历史已上架数据以 `updated_at` 回填，后续发布以 publish 成功时间为准。
- 测试：前端列表测试必需；后端/API/Orval 测试按契约变更触发。
