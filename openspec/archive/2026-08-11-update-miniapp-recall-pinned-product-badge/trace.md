---
change_id: update-miniapp-recall-pinned-product-badge
status: applied
type: update
source_requirement: REQ-0104-miniapp-recall-pinned-product-badge
sprint: sprint-022
created_at: 2026-08-08 09:36:33
updated_at: 2026-08-11 23:18:40
---

# Change 追踪

## 基本信息

```yaml
change_id: update-miniapp-recall-pinned-product-badge
status: applied
type: update
source_requirement: REQ-0104-miniapp-recall-pinned-product-badge
source_requirement_status: in_sprint
sprint: sprint-022
affected_capabilities:
  - miniapp-product-list-page
  - miniapp-search
impact:
  backend: true
  api: true
  miniapp: true
  web: false
  admin: false
  database: false
  storage: false
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-product-list-sorting.md
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-11 23:18:40 | `/opsx-archive` | 归档后规格一致性复核：修正 `REQ-0103` 遗留“小程序无置顶标识 / 搜索结果无置顶标识”场景为非应用入口或未标记置顶结果不展示，避免与 `REQ-0104` 的实际生效置顶标识规则冲突。 |
| 2026-08-11 23:15:40 | `/opsx-archive` | 归档前验收补证：用户确认已通过小程序体验/开发者工具验收；REQ acceptance 回填 passed，原型一致性以既有商品卡片角标区域和手动小程序验收结论闭环。 |
| 2026-08-08 10:25:00 | `/opsx-apply` | 实现 `REQ-0104`：API 商品卡片新增 `is_recall_pinned`，仅普通商品列表与完整搜索 SKU 结果在当前入口实际应用召回置顶时返回 true；小程序商品卡片以“置顶 > 新品 > 热销 > 下架”优先级复用现有角标区域展示。 |
| 2026-08-08 10:25:00 | `./scripts/generate-openapi-client.sh` | 同步 OpenAPI 与 Orval 生成物；Web 端生成类型新增 `MiniappProductCard.is_recall_pinned`。 |
| 2026-08-08 10:25:00 | `uv run pytest ...` | 通过小程序商品列表、搜索 SKU 结果、新品/热销边界与商品卡片静态契约 focused tests；加载更多仍沿用服务端顺序与分页结果，不做端侧跨页重排。 |
| 2026-08-08 10:25:00 | `python scripts/validate-openspec-language.py` | OpenSpec 文档语言校验通过；持续引用 `docs/knowledge-base/best-practices/miniapp-product-list-sorting.md`。 |
| 2026-08-08 09:36:33 | `/req-opsx` | 从 REQ-0104 创建 OpenSpec Change，状态为 proposed。 |
