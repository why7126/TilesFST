---
change_id: fix-miniapp-sku-detail-brand-card-route
type: fix
status: archived
created_at: 2026-07-21 15:01:23
updated_at: 2026-07-22 09:01:56
source_bug: BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search
related_requirement: REQ-0044-miniapp-sku-detail-page
iteration: sprint-010
---

# Change Trace

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| BUG | `BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search` | 生产环境小程序商品详情页品牌卡片误跳搜索页 |
| 关联需求 | `REQ-0044-miniapp-sku-detail-page` | SKU 详情页已交付能力，当前修复品牌入口路径偏差 |

## 状态

```yaml
change_id: fix-miniapp-sku-detail-brand-card-route
type: fix
status: archived
source_bug: BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search
related_requirement: REQ-0044-miniapp-sku-detail-page
iteration: sprint-010
tasks:
  total: 11
  completed: 11
```

## 验收证据

| 时间 | 类型 | 证据 |
|---|---|---|
| 2026-07-21 22:55:44 | 后端回归 | `uv run pytest tests/test_miniapp_home.py` 通过 29 项；SKU 详情接口断言 `data.brand.brand_entry_path == "/pages/brand-detail/index?brandId=1"`，品牌列表页入口仍为品牌详情页 |
| 2026-07-21 22:55:44 | 小程序静态回归 | `uv run pytest tests/test_miniapp_static.py` 通过 27 项；SKU 详情页仍注册并使用 `brand-card`，`app.json` 仍注册 `pages/brand-detail/index` |

## 影响评估

- API 字段名、Pydantic Schema、接口路径和统一响应结构未变化，仅修正既有字段取值。
- 不影响数据库、Web 管理端、媒体上传、MinIO 或 Docker 配置。
- 不需要 OpenAPI / Orval；无需更新 `docs/03-api-index.md`。
- 本缺陷为单点路径契约修复，无新增复用性事故模式，暂不新增 `docs/knowledge-base/incidents/`。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 09:01:56 | /opsx-archive | Change 已归档到 `openspec/changes/archive/2026-07-22-fix-miniapp-sku-detail-brand-card-route/`，delta spec 已合并 |
| 2026-07-21 22:55:44 | /opsx-apply | 修正 SKU 详情品牌入口路径并完成后端与小程序静态回归 |
| 2026-07-21 15:22:32 | /sprint-propose | 纳入 sprint-010 正式范围 |
| 2026-07-21 15:01:23 | /bug-opsx | 从 BUG-0078 创建 OpenSpec fix Change |
