## Context

`REQ-0087-admin-sku-list-sort-optimization` 已评审通过，目标是优化管理端 SKU 列表默认排序。现行 `tile-sku-management` 正式规格已经定义列表排序，但当前契约是“已发布 SKU 优先；已发布按 `published_at` 降序；未发布按 `created_at` 降序”。本需求要求改为“未上架优先”，因此需要通过 MODIFIED delta spec 替换排序契约。

目标页面是管理端 SKU 列表，命中 `admin-list` 横切标签。`acceptance.md` 已写入分页 DOM、指标卡、筛选下拉、fixed toast、DS confirm 与 `window.confirm` 的横切 AC。prototype/web 只说明排序后的列表结构，不要求新增排序控件或新页面视觉。

## Goals / Non-Goals

**Goals:**

- 将管理端 SKU 列表默认排序调整为未上架 SKU 优先。
- 保证未上架组内按 `created_at DESC`，已上架组内按 `published_at DESC`。
- 保证已下架 SKU 仍返回并展示最近一次发布成功时间。
- 保证 SKU 列表筛选区参照其他管理端列表页铺满 filter-card 可用宽度。
- 保证排序在搜索、筛选与分页前生效，避免只排序当前页。
- 保持现有管理端列表 UI、筛选、分页、加载态、空态、失败态和行操作。
- 补充后端/前端测试，覆盖排序契约与横切 AC 防回归点。

**Non-Goals:**

- 不新增显式排序控件。
- 不新增创建时间、发布时间或额外上架状态筛选项。
- 不调整 SKU 发布时间生成流程；下架只改变展示/响应是否保留历史发布时间，不清空历史 `published_at`。
- 不调整店主 Web、小程序或导出排序。
- 不新增数据库结构，除非实现阶段发现缺少必须字段且另行说明。

## Decisions

### D1. UI 策略：复用既有管理端列表与 Design System

采用 `tailwind-ds / existing-admin-list` 策略：本 Change 不做新页面 CSS port，不引入独立排序控件。实现应复用现有 SKU 列表页面、统一筛选下拉、分页 DOM 与 fixed toast 约束。prototype HTML 仅作为排序样例和 DOM 验收参考，优先级为 HTML > context.md > acceptance.md > ui-design.md > specs。

备选方案是新增“默认排序说明”或显式排序控件，但这会扩大 UI 行为面，并与 REQ 的 Out of Scope 冲突，因此不采用。

### D2. 排序实现优先放在后端分页前

若 `GET /api/v1/admin/tile-skus` 是后端分页接口，排序必须在数据库查询或 Repository 层完成后再分页，避免分页内排序导致跨页重复、漏项或顺序跳动。推荐排序逻辑：

```text
CASE WHEN status = 'PUBLISHED' THEN 1 ELSE 0 END ASC
未上架: created_at DESC
已上架: published_at DESC
稳定兜底: id DESC 或等价稳定字段
```

其中 `ASC` 使非 `PUBLISHED` 分组优先。具体 SQL/Repository 实现需兼容 SQLite 与 MySQL，避免拼接不可信 SQL。

如果现有前端一次性持有完整结果集再分页，则可前端排序，但必须在分页前排序，并通过测试覆盖完整结果集排序。当前风险更低的默认方案仍是后端分页前排序。

### D3. 未上架状态集合使用非 PUBLISHED

未上架分组按现有 SKU 状态枚举定义为 `status != PUBLISHED`，覆盖 `DRAFT`、`NEEDS_COMPLETION`、`DISABLED` 等非发布态。这样与现有数据模型兼容，不需要新增派生字段。若实现阶段发现存在特殊状态，应在实现说明中补充归属，但不得通过前端显示文案判断。

### D4. 既有发布时间语义保持不变

已上架组继续使用 `published_at` 作为主排序字段，不得使用 `updated_at` 或 `created_at` 替代。此决策与 `REQ-0079-admin-sku-list-published-at` 和现行 spec 的发布时间字段来源保持一致。

### D5. 下架后继续展示历史发布时间

验收返修确认：SKU 被下架后，“发布时间”仍应展示最近一次发布成功时间。后端不清空数据库历史 `published_at`，管理端列表、详情与下架响应也不得再因 `status != PUBLISHED` 将 `published_at` 派生为 `null`。该行为只影响管理端响应与展示，不改变未上架分组排序：已下架 SKU 仍按 `created_at DESC` 参与未上架组排序。

### D6. 筛选区按实际控件数量铺满

验收返修确认：SKU 列表筛选区右侧存在空白，原因是 CSS grid 预留了 6 列，但页面实际只有关键词、品牌、类目、状态与重置 5 个区域。SKU 页应参照品牌、类目、规格等管理端列表页，用实际控件数量定义列宽，避免额外空列。

## Conflict Resolution

| 来源 | 要求 | 处理 |
|---|---|---|
| `prototype/web/admin-sku-list-sort-optimization.html` | 未上架 SKU 在前，未上架按创建时间降序，已上架按发布时间降序 | 作为 UI/排序样例最高优先级输入，写入 delta spec |
| `prototype/web/context.md` | 不新增排序控件，保持分页、筛选、表格和操作列一致 | design D1 与 tasks 覆盖 |
| 验收返修反馈 | SKU 被下架时发布时间不要清空，仍然显示出来 | design D5 与 delta spec 改为下架后继续返回/展示历史 `published_at` |
| 验收返修反馈 | SKU 列表页筛选区域未占满，右侧有空白 | design D6 与 delta spec 改为按实际控件数量铺满 filter-card 宽度 |
| `acceptance.md` | AC-001 至 AC-032 与 6 条 AC-XCUT | tasks 与测试计划覆盖 |
| `ui-design.md` | 管理端列表页复用 AdminListPage / semantic token / DS 组件 | 不新增视觉体系，继续沿用 |
| `openspec/specs/tile-sku-management/spec.md` | 当前要求已发布 SKU 优先 | 与 REQ 冲突，使用 MODIFIED delta spec 改为未上架优先 |

## Risks / Trade-offs

- [Risk] 后端分页接口若只在前端当前页排序，会出现跨页顺序错乱。 → Mitigation: tasks 要求优先在后端分页前排序，并补充分页前排序测试。
- [Risk] `published_at` 为空的已上架历史数据可能造成顺序不稳定。 → Mitigation: delta spec 要求时间为空或重复时使用稳定兜底排序。
- [Risk] 改变默认排序会影响依赖旧“已发布优先”的运营习惯。 → Mitigation: 本需求已评审通过，且仅改变默认列表顺序，不改变筛选能力；用户仍可用状态筛选查看已上架 SKU。
- [Risk] 管理端横切 UI 组件回归。 → Mitigation: acceptance 的 AC-XCUT 覆盖分页 DOM、指标卡、筛选下拉、fixed toast、DS confirm 和 `window.confirm` 静态检查。

## Migration Plan

1. 更新管理端 SKU 列表排序实现，优先后端分页前排序。
2. 如接口契约发生变化，同步 Pydantic Schema、OpenAPI、Orval 与文档。
3. 更新前后端测试，覆盖默认排序、筛选分页与空值稳定性。
4. 视检管理端 SKU 列表，确认 UI 横切 AC 无回归。

## Open Questions

- 是否存在已上架但 `published_at` 为空的真实历史数据；若存在，实现阶段需确认置底还是依赖稳定兜底字段。
