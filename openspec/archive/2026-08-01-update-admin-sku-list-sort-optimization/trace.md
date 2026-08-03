---
change_id: update-admin-sku-list-sort-optimization
source_requirement: REQ-0087-admin-sku-list-sort-optimization
change_type: update
status: applied
created_at: 2026-08-01 07:22:21
updated_at: 2026-08-01 08:05:03
owner: product
iteration: sprint-016
---

# Change Trace

## Source

- REQ: `REQ-0087-admin-sku-list-sort-optimization`
- REQ 状态：in_sprint
- 父需求：`REQ-0006-tile-sku-management`
- 相关需求：`REQ-0079-admin-sku-list-published-at`
- 相关缺陷：`BUG-0090-admin-sku-list-publish-sort-order`

## Impact

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: possible
capabilities:
  new: []
  modified:
    - tile-sku-management
change_type: update
strategy: tailwind-ds / existing-admin-list
```

## Requirement Readiness Report

| Item | Status |
|---|---|
| requirement.md | present |
| user-stories.md | present |
| business-flow.md | present |
| acceptance.md | present |
| trace.md | present |
| prototype/web | present |
| readiness | Ready |

## Knowledge Base

```yaml
cross_cutting_tags:
  - admin-list
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-015-retrospective.md
knowledge_base_gate: Pass
```

## Conflict Report

| Source | Finding | Resolution |
|---|---|---|
| prototype HTML | 未上架 SKU 样例排在已上架之前 | delta spec 改为未上架优先 |
| prototype context | 不新增排序控件，保持列表结构 | design D1 采用 existing-admin-list |
| acceptance.md | 32 条功能 AC + 6 条 AC-XCUT | tasks 覆盖排序、测试、横切验收 |
| current spec | 当前为已发布优先 | MODIFIED `管理端 SKU 列表与筛选 API` 替换排序契约 |

## PNG Checklist

- PNG Golden Reference：未提供，非阻塞。
- HTML/context 已提供排序样例；后续 `/opsx-apply` 可用 Playwright 或视检记录列表行顺序。

## Implementation Notes

```yaml
implemented_at: 2026-08-01 07:41:21
sorting_layer: backend_repository_sql_before_limit_offset
unpublished_group: "status != PUBLISHED"
published_group: "status = PUBLISHED"
order:
  - "status = PUBLISHED ? 1 : 0 ASC"
  - "unpublished created_at nulls last"
  - "unpublished created_at DESC"
  - "published published_at nulls last"
  - "published published_at DESC"
  - "id DESC"
api_contract_changed: false
database_changed: false
orval_required: false
docs_api_required: false
ui_structure_changed: true
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-015-retrospective.md
```

## Modify Notes

| 时间 | 反馈 | 调整 | 文档同步 |
|---|---|---|---|
| 2026-08-01 07:48:32 | SKU 被下架时，发布时间不要清空，仍然显示出来 | 后端查询不再对非 `PUBLISHED` 状态隐藏 `published_at`；下架响应、列表与详情继续返回历史发布时间；未上架分组排序仍按 `created_at DESC` | 已同步 delta spec、design、REQ acceptance、docs/03-api-index.md、Sprint release-note 与 acceptance-report |
| 2026-08-01 08:05:03 | SKU 列表页筛选区域没有占满，右侧仍有空白，需参照其他页面 | SKU 筛选区 CSS grid 改为 `1.35fr 1fr 1fr 1fr auto`，对应关键词、品牌、类目、状态、重置 5 个实际区域，移除多余预留列 | 已同步 delta spec、design、REQ acceptance 与 Sprint acceptance-report；API/DB/Orval 不涉及 |

## Validation

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-08-01 07:38:37 | `pnpm --dir src/web test -- TileSkuManagementPage.test.tsx` | PASS：59 files / 321 tests |
| 2026-08-01 07:40:00 | `uv run pytest src/backend/tests/test_admin_tile_skus.py` | PASS：27 tests |
| 2026-08-01 07:41:21 | `rg -n "page-summary|page-right|metric-label|metric-value|metric-desc|FixedAdminToast|fixed|AdminConfirmModal|window\\.confirm|AdminFilterSelect|SearchableSelect" ...` | PASS：SKU 页面保留分页 DOM 与指标卡测试；本 Change 未修改页面结构或 CSS；未发现 `window.confirm` |
| 2026-08-01 07:41:21 | `openspec validate update-admin-sku-list-sort-optimization --strict` | PASS |

## Change Log

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-01 08:05:03 | `/opsx-modify` | 验收返修：SKU 筛选区按实际控件数量铺满可用宽度，消除右侧空白 |
| 2026-08-01 07:48:32 | `/opsx-modify` | 验收返修：SKU 下架后继续返回并展示历史 `published_at` |
| 2026-08-01 07:41:21 | `/opsx-apply` | 实现管理端 SKU 列表未上架优先排序，补充后端与前端测试；API/DB/Orval 不变 |
| 2026-08-01 07:31:37 | `/sprint-propose` | 纳入 sprint-016 正式范围，等待 `/opsx-apply` |
| 2026-08-01 07:22:21 | `/req-opsx` | 从 REQ-0087 创建 OpenSpec Change，状态 proposed |
