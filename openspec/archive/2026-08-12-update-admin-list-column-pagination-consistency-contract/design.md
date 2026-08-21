## 上下文

REQ-0112 已评审通过并纳入 `sprint-023`。需求来源于 sprint-022 复盘 T-002：Banner、日志审计、用户管理都触发列展示、换行、冻结列和分页细节返修。

相关事实源：

- `issues/requirements/archive/REQ-0112-admin-list-column-pagination-consistency-contract/`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/retrospectives/sprint-022-retrospective.md`
- `docs/standards/prototype-ui-acceptance.md`
- `rules/ui-design.md`

## 目标

- 把管理端列表页的列展示、分页和真实分页要求固化为 Design System / OpenSpec 契约。
- 让后续管理端列表新增或改造默认复用契约，而不是在页面内继续堆一次性样式。
- 为 Banner、日志审计、用户管理等代表页补齐前端测试与验收 gate。
- 明确 API / Orval 条件：只有分页接口契约变化时才同步生成物。

## 非目标

- 不一次性重构所有管理端列表。
- 不新增业务字段。
- 不新增数据库表或迁移。
- 不改变店主 Web 或微信小程序列表。
- 不制作独立 HTML 视觉原型；本 Change 以后续代表页面视觉证据验收。

## 决策

### D1 契约归属放在 Design System 与 knowledge-base

将列展示与分页契约写入 `design-system` spec，并同步更新 knowledge-base。这样后续 OpenSpec design 可以引用同一 gate，不需要每个 REQ 重新解释 nowrap、有效期例外和分页 DOM。

替代方案是只更新单页实现或只写 docs。该方案会继续依赖人工记忆，无法成为 `/opsx-apply` 与验收门禁。

### D2 首批代表页采用 Banner、日志审计、用户管理

用户管理是分页 DOM 基准，Banner 已有有效期例外、跳转对象和操作列返修经验，日志审计代表观测/审计类后端分页页面。三者能覆盖工作台式 CRUD、投放配置和观测日志三类高频列表。

若 apply 阶段发现某代表页缺少独立业务入口或当前实现已不适合本轮改造，应在 trace 中记录 N/A 理由，并至少保留一个有筛选、分页、操作列的代表页完成证据。

### D3 nowrap 默认，只有有效期类复合时间允许双行

表头和普通字段默认单行展示。有效期、投放周期等复合时间字段可双行展示，但需要固定列宽和稳定行高。任何新增换行例外必须在 Change trace 或验收记录中说明。

### D4 后端真实分页是契约，不接受前端切片替代

列表接口应由后端根据页码、每页条数、筛选、搜索和排序返回当前页数据与真实总数。前端全量拉取后切片不作为真实分页验收证据。若接口缺失分页字段，apply 阶段必须同步 Pydantic Schema、OpenAPI、Orval、API 文档和测试。

## UI Contract

| 项 | 合同 |
|---|---|
| 事实源优先级 | `prototype/web/context.md` > `acceptance.md` > `docs/knowledge-base/best-practices/admin-list-page-consistency.md` > `rules/ui-design.md` > 已归档 specs。当前没有 HTML/PNG 原型。 |
| 页面与入口 | 代表页为 Banner 管理、日志审计、用户管理；入口保持现有管理端导航和权限边界。 |
| 信息架构 | 保持管理端列表结构：标题/指标区、筛选区、表格、sticky 操作列、分页、fixed toast、DS confirm modal。 |
| 视觉 token | 使用 Design System semantic token、既有 admin list class 或 `AdminListPage` 等价模板；不得新增裸 Hex。 |
| 交互状态 | 覆盖 hover、focus、disabled、loading、横向滚动、筛选弹层打开、confirm modal 和 toast。 |
| 图标与文案 | 复用既有图标和按钮文案；危险操作继续走 DS confirm modal。 |
| Mock/API 边界 | 纯布局验证可用 mock 数据；真实分页必须通过真实 API 或测试替身验证请求参数、响应总数和页码边界。 |
| 权限规则 | 管理端列表权限沿用现有页面；本 Change 不放宽管理端与店主端边界。 |
| 一致性参照 | 用户管理分页 DOM 为基准；Banner 和日志审计为代表回归页。 |

## 冲突处理

- 若 `acceptance.md` 与 knowledge-base 都要求分页 DOM，对齐用户管理基准。
- 若某页面需要有效期双行展示，以 `prototype/web/context.md` 和 REQ-0112 的有效期例外为准。
- 若既有页面实现使用前端切片分页，而本 Change 要求真实分页，以本 Change 的 spec delta 为准；API/Orval 同步变为必须项。
- 若 existing specs 只约束字段语义 adapter，REQ-0112 不修改该语义范围，只补布局与分页契约。

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| 契约扩张为全量列表重构 | tasks 限定代表页和共享契约，新增页面治理另开 REQ/Change。 |
| 横向滚动和 sticky 操作列测试脆弱 | 优先测试 DOM/class/可达性，视觉证据用于人工验收补充。 |
| 日志审计分页 API 缺口扩大范围 | 若涉及 API，明确同步 Schema/OpenAPI/Orval；若超出容量，拆分后续 Change。 |
| knowledge-base 与 spec 漂移 | apply 阶段同步更新 knowledge-base，并在 trace 中记录引用。 |

## 验收与回滚

验收以 OpenSpec validate、语言校验、前端测试、后端/API 测试和代表页视觉证据组合完成。若实现引发回归，可先回滚页面级样式或 API 调用变更，但保留 spec / knowledge-base 契约，后续用修复 Change 收敛。

