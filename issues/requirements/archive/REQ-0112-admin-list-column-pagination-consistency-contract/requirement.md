---
requirement_id: REQ-0112-admin-list-column-pagination-consistency-contract
title: 建立管理端列表页列展示与分页一致性契约
terminal: web-admin
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-12 14:26:16
updated_at: 2026-08-12 22:03:11
---

# REQ-0112 建立管理端列表页列展示与分页一致性契约

## 1. 需求背景

管理端列表页是后台运营的高频工作入口。近期 Banner、日志审计、用户管理等页面在列展示、文本换行、分页结构、冻结操作列和真实分页能力上反复返修，说明当前列表页一致性约束还停留在局部经验和单页修补层面。

项目已有 `REQ-0095-admin-list-field-display-adapter-checklist`，用于统一 image、name、fallback 等字段展示语义；也已有 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`，沉淀分页 DOM、toast、confirm、筛选下拉等历史经验。但这些资产尚未系统覆盖表格列宽、默认不换行、有效期例外、sticky 操作列、分页样式和后端真实分页契约。

本需求要求建立管理端列表页列展示与分页一致性契约，作为后续 Banner、日志审计、用户管理及新增管理端列表页的设计、开发、测试和验收基准，减少同类返修。

## 2. 目标用户

| 用户 | 核心诉求 |
|---|---|
| 后台运营 | 在不同管理端列表中稳定扫描数据、翻页和执行操作，不被换行、遮挡或分页差异打断。 |
| 后台管理员 | 管理用户、Banner、审计日志等对象时获得一致的表格布局、操作列和分页行为。 |
| 产品 / 设计 | 用统一契约描述管理端列表展示边界，减少每个页面重复补充视觉细节。 |
| 前端开发 | 明确表格列、分页组件、sticky 操作列和真实分页的实现约束，避免页面级临时样式。 |
| QA / 验收人员 | 有固定检查项覆盖换行、分页、横向滚动和接口分页，降低漏测。 |

## 3. 需求目标

- 建立管理端列表页列展示与分页一致性契约。
- 明确首批覆盖页面：Banner 管理、日志审计、用户管理；后续可扩展到品牌、证书、SKU、分类等管理端列表。
- 明确表格默认 nowrap 规则，以及有效期列允许双行展示的例外。
- 明确操作列冻结、横向滚动、窄屏可操作和叠层不遮挡要求。
- 统一分页 DOM、视觉样式、每页条数、总数展示和筛选后分页重置规则。
- 要求涉及分页的管理端列表使用后端真实分页，不以全量拉取后前端切片替代。
- 将契约沉淀到设计系统、前端测试和 `docs/knowledge-base`，作为后续 OpenSpec apply 前 gate。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 列展示契约 | 定义表头、普通文本、状态、时间、操作列的列宽、换行、截断和 tooltip 规则。 |
| nowrap 默认规则 | 除明确例外外，表头和单元格内容默认单行展示，不因长文案撑宽整表或撑高行高。 |
| 有效期例外 | 有效期、起止时间等复合时间字段可双行展示，但必须保持行高稳定、列宽固定、语义清晰。 |
| 冻结操作列 | 操作列在横向滚动、窄屏、hover/focus、禁用态、loading 态下保持可见和可操作。 |
| 分页样式契约 | 分页 DOM 与用户管理基准对齐：左侧 `page-summary`，右侧 `page-right` 页码与每页条数。 |
| 后端真实分页 | 首批覆盖页面必须确认列表 API 支持真实分页、总数返回和筛选条件下的页码边界。 |
| 首批页面 | Banner 管理、日志审计、用户管理。 |
| 测试要求 | 前端测试覆盖分页 DOM、nowrap/sticky 关键 class 或行为、筛选后分页重置和后端分页参数。 |
| 知识库沉淀 | 扩展管理端列表页一致性最佳实践，补齐本需求形成的列展示和分页 gate。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 重做所有管理端表格 | 本需求建立契约和首批代表页约束，不要求一次性重构全部列表。 |
| 新增业务字段 | 不新增 Banner、日志、用户等业务对象字段。 |
| 重建 Design System | 不推翻现有暗色旗舰风和语义 token，只补齐列表页契约。 |
| 店主 Web / 小程序 | 不覆盖公开 Web 展示端或微信小程序列表。 |
| 大规模 API 重构 | 仅要求涉及列表分页的接口满足真实分页契约；不改无关接口。 |
| 历史数据迁移 | 不涉及 SQLite/MySQL 表结构迁移和历史数据修复。 |

## 5. 核心概念

### 5.1 列展示一致性契约

列展示一致性契约指管理端列表页对列宽、换行、截断、tooltip、状态标签、时间字段和操作列布局的统一约束。它用于约束页面实际渲染，不替代字段语义 adapter。

### 5.2 nowrap 默认规则

nowrap 默认规则指表头和普通列表字段默认单行展示。长文本应通过固定列宽、截断、省略号、title tooltip 或等价可访问方式处理，不应撑开表格、挤压操作列或造成行高异常。

### 5.3 有效期例外

有效期例外指起始时间和结束时间组合展示时，可在同一单元格内双行呈现。该例外必须被显式声明，且不得泛化为所有时间、文本或备注字段都可换行。

### 5.4 后端真实分页

后端真实分页指列表接口接收页码、每页条数、筛选和搜索参数，由后端返回当前页数据、总数和分页边界信息。前端不得通过一次性拉取全量数据后本地切片来伪造分页。

## 6. 功能要求

### FR-001 契约归属与适用范围

- MUST 建立管理端列表页列展示与分页一致性契约。
- 契约 MUST 明确适用页面、适用字段类型、强制项、例外项和验证方式。
- 首批适用页面 MUST 包含 Banner 管理、日志审计和用户管理。
- SHOULD 标记品牌、证书、SKU、分类等已有管理端列表是否已符合契约或需后续治理。
- 契约 SHOULD 作为后续管理端列表新增或改造的 apply 前 gate。

### FR-002 nowrap 默认规则

- 表头文本 MUST 默认不换行。
- 除明确例外外，普通文本字段 MUST 默认单行展示。
- 长文本字段 MUST 使用固定宽度、最大宽度、截断、省略号、tooltip 或等价策略，避免撑宽整表。
- 空值、未知值和状态文案不得因兜底内容导致单元格换行或遮挡。
- 实现阶段 SHOULD 形成共享 class、组件 prop 或模板约束，避免每个页面重复手写 nowrap 样式。

### FR-003 有效期与复合时间例外

- 有效期列 MAY 使用起始时间和结束时间双行展示。
- 有效期例外 MUST 仅适用于有效期、投放周期或等价复合时间字段。
- 有效期双行展示 MUST 保持固定列宽和稳定行高，不得挤压操作列。
- 单个更新时间、创建时间、最后登录时间等普通时间字段 SHOULD 保持单行展示。
- 若某页面需要新增换行例外，MUST 在契约或 OpenSpec design 中说明原因和验证方式。

### FR-004 冻结操作列

- 管理端列表的操作列 MUST 在横向滚动时保持可见或有明确可访问的操作入口。
- sticky 操作列不得遮挡相邻列内容、分页区域、筛选弹层、确认弹窗或 toast。
- 操作列在窄屏、hover、focus、disabled、loading 和权限不足状态下 MUST 保持布局稳定。
- 危险操作继续使用 Design System confirm modal，不得引入 `window.confirm`。
- 操作成功/失败反馈继续使用 fixed toast，不得用文档流 notice 推挤表格。

### FR-005 分页 DOM 与视觉样式

- 分页 DOM MUST 与用户管理基准对齐：左侧 `page-summary`，右侧 `page-right` 页码与每页条数。
- 分页区域 MUST 位于表格卡片底部，不能被横向滚动条、sticky 操作列或加载态遮挡。
- 分页总数文案 MUST 使用真实总数，不得只显示当前页条数。
- 每页条数切换后 MUST 回到合理页码，避免显示空页或越界页。
- 搜索、筛选、排序条件变化后 SHOULD 重置到第一页，除非有明确产品理由保留当前页。

### FR-006 后端真实分页契约

- 首批覆盖页面的列表 API MUST 支持后端真实分页。
- 请求参数 SHOULD 至少包含页码、每页条数，并与搜索、筛选、排序参数共同生效。
- 响应 MUST 包含当前页数据和总数，或项目既有统一分页响应中的等价字段。
- 前端不得通过全量拉取后本地切片替代服务端分页。
- 筛选条件变化、页码越界、空结果、最后一页删除数据后，页面 MUST 有稳定的恢复策略。
- 如接口分页字段或响应结构变化，MUST 同步 Pydantic Schema、OpenAPI、Orval、API 文档和测试。

### FR-007 设计系统与知识库沉淀

- 契约 SHOULD 沉淀到 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 或继任文档。
- 若形成共享样式或组件约束，MUST 使用 Design System semantic token，不得新增裸 Hex。
- 如需新增设计系统 token、表格模板 prop 或 shared class，MUST 同步设计系统文档和示例页。
- 知识库 MUST 明确 REQ-0095 与本需求的分工：字段语义 adapter 与列表布局/分页契约分别治理。

### FR-008 前端测试与验收支撑

- 测试 MUST 覆盖分页 DOM 基准：`page-summary`、`page-right`、页码与每页条数。
- 测试 SHOULD 覆盖 nowrap 或等价单行展示约束，至少验证代表页面不会出现新增换行回退。
- 测试 SHOULD 覆盖 sticky 操作列存在性、横向滚动下操作入口可达性或关键 class。
- 测试 MUST 覆盖真实分页请求参数、总数展示和筛选后分页重置。
- 对无法自动化的视觉项，验收记录 MUST 包含代表页面、视口尺寸和人工验证结果。

## 7. UI / UE 约束

- 管理端继续遵守“工业石材 · 暗色旗舰风”和现有 Design System semantic token。
- 列表页应保持紧凑、可扫描，不新增说明卡片、营销式引导或装饰性区块。
- 表头、普通字段、状态标签、时间字段和操作按钮不得发生文本重叠。
- 横向滚动、sticky 操作列和分页区域应形成稳定布局，避免互相遮挡。
- 有效期双行展示应被视觉上识别为一个复合字段，而不是两个松散字段。
- 图标、状态标签、按钮和 tooltip 优先复用现有 DS 组件。

## 8. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite/MySQL | 通常不要求新增或修改表结构。 |
| Pydantic Schema | 若首批页面分页响应缺少统一分页字段，可能需要补齐响应 Schema。 |
| OpenAPI/Orval | 若 API 分页参数或响应结构变化，必须同步 OpenAPI 和 Orval；纯前端样式契约不需要。 |
| 管理端 Web | 需要落实列表页列展示、操作列、分页 DOM 和真实分页调用约束。 |
| 小程序 | 不涉及。 |
| 店主 Web | 不涉及。 |
| 测试 | 需要补充或更新前端测试；若涉及接口分页，需补充后端或 API 层测试。 |

## 9. 关联需求与现状参考

| 关联项 | 关系 |
|---|---|
| `REQ-0095-admin-list-field-display-adapter-checklist` | 已治理 image/name/fallback 字段展示语义，本需求不重复该范围。 |
| `REQ-0108-admin-banner-list-display-optimization` | Banner 列表已有有效期例外、分页 DOM 和 sticky 操作列相关验收经验。 |
| `REQ-0110-admin-user-contact-info-management` | 用户管理页是分页和表格布局基准页面之一。 |
| `REQ-0016-banner-management` | Banner 管理是首批覆盖页面。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 管理端列表页一致性最佳实践，应补齐本需求形成的契约。 |

## 10. 风险与待确认

| 风险 / 待确认 | 说明 |
|---|---|
| 首批页面边界 | Banner、日志审计、用户管理为建议首批范围；实现前需确认是否同步纳入品牌、证书、SKU。 |
| 日志审计分页现状 | 需确认日志审计接口当前是否已真实分页，若未支持会触发 API / Schema / Orval 工作。 |
| sticky 操作列视觉证据 | 冻结操作列需要横向滚动和窄屏验证，自动化与人工验收需组合。 |
| 有效期例外泛化风险 | 需要避免把有效期例外误用到备注、链接、名称等长文本字段。 |
| 测试稳定性 | computed style 和横向滚动类测试容易脆弱，需优先验证 DOM/class/行为契约。 |

## 11. 状态块

```yaml
requirement_id: REQ-0112-admin-list-column-pagination-consistency-contract
status: archived
priority: P1
readiness: Ready
parent_requirement: null
terminal: web-admin
target_clients:
  web_admin: included
  web_catalog: not_included
  wechat_miniapp: not_included
api_change_required: possible
database_change_required: false
orval_required: conditional
prototype_required: false
next_step: /sprint-propose --req REQ-0112-admin-list-column-pagination-consistency-contract
notes:
  - 本需求独立于 REQ-0095；REQ-0095 管字段语义 adapter，本需求管列表布局、操作列、分页样式与真实分页契约。
  - 首批建议覆盖 Banner 管理、日志审计和用户管理。
  - 若实现阶段改动分页 API 或响应结构，必须同步 OpenAPI、Orval、API 文档和测试。
  - 已写入 admin-list knowledge-base 横切 AC；后续 req-opsx design.md 必须引用 trace.md knowledge_base_refs。
```
