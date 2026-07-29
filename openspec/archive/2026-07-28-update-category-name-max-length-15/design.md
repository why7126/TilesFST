## Context

REQ-0077 已评审通过，要求将类目名称输入长度上限从 10 个字符放宽为 15 个字符。正式 `tile-category-management` spec 当前只定义数据模型 `name` 最大 30 字符，未把管理端业务输入上限 10 或 15 写入规格，因此本变更需要把 15 字符业务规则补入正式能力，并消除实现、测试、OpenAPI 或文档中可能残留的 10 字符假设。

关联文档：

- `issues/requirements/archive/REQ-0077-category-name-max-length-15/requirement.md`
- `issues/requirements/archive/REQ-0077-category-name-max-length-15/acceptance.md`
- `issues/requirements/archive/REQ-0077-category-name-max-length-15/prototype/web/category-name-max-length-15.html`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`

## Goals / Non-Goals

**Goals:**

- 后端创建 / 更新类目接口接受 1-15 字符名称，拒绝 16 字符及以上名称。
- Web 管理端新增 / 编辑弹窗使用同样的 15 字符校验与错误提示。
- OpenAPI / Orval / docs / tests 与新的长度约束一致。
- 回归管理端类目树、类目列表、小程序分类页和 Web 展示端分类入口在 15 字符名称下布局稳定。
- 保留 admin-list 与 admin-modal 横切 AC，避免分页、toast、confirm 和弹窗 CSS cascade 回归。

**Non-Goals:**

- 不改变类目名称字符集，仍沿用中文、英文、数字规则。
- 不改变同层级名称唯一规则。
- 不改变类目编码自动生成、编码唯一、层级上限、排序权重、启停和删除规则。
- 不做历史类目数据清洗、批量重命名或迁移。
- 不新增类目别名、多语言名称、简称、SEO 名称或展示名称字段。

## Conflict Resolution

原型与验收优先级：HTML > PNG > `prototype-context.md` > `acceptance.md` > `rules/ui-design.md` > `openspec/specs`。

| 来源 | 结论 |
|---|---|
| HTML 原型 `category-name-max-length-15.html` | 明确展示 15 字符可保存、16 字符错误态、类目树和列表展示样例；作为 UI 语义最高参考。 |
| PNG | 尚未导出，非阻塞；后续实现可按 HTML 原型截图补证据。 |
| `prototype-context.md` | 明确实现阶段复用 `CategoryFormModal`、管理端列表模板、FixedAdminToast、AdminConfirmModal。 |
| `acceptance.md` | 功能 AC 与横切 AC 完整，作为测试矩阵来源。 |
| `rules/ui-design.md` | 要求 semantic token、DS 组件复用、字段级错误定位和管理端 modal best-practice。 |
| `openspec/specs/tile-category-management/spec.md` | 当前数据模型最大 30 字符与本需求不冲突；本变更新增业务输入上限 15。 |

## Decisions

### D1 UI 策略：Design System 增量调整

采用 DS 增量调整，不做 CSS Port。原因是本需求只调整现有 `CategoryFormModal` 的校验、提示和回归样例，不需要新视觉或页面结构。实现时应复用现有表单、弹窗、列表、toast 和 confirm 组件，并保持 semantic token。

备选：按 HTML 原型重新 port CSS。未采用，因为 HTML 只用于表达验收语义，直接 port 会增加样式分叉风险。

### D2 字符计数边界：用户可见字符

前端和后端均按用户可见字符执行 15 字符上限。实现时可沿用现有字符计数工具或在服务层明确同等语义，中文、英文、数字均按 1 个字符计数。

备选：按数据库字节或 Unicode code unit 计数。未采用，因为会导致中文名称体验不一致，也不符合 REQ-0077。

### D3 数据库策略：先确认约束，再决定是否迁移

正式 spec 的数据模型允许 `name` 最大 30 字符，因此 15 字符输入上限理论上不需要数据库结构变更。实现阶段仍必须检查 SQLite schema、MySQL migration、Pydantic Schema 和测试夹具是否残留 10 字符限制；只有发现真实 DB 约束小于 15 时才纳入 migration。

### D4 API / Orval 策略：后端事实源驱动

后端 Schema 或业务校验是长度规则事实源，OpenAPI 从后端导出，Orval 从 OpenAPI 生成。前端不得手写重复接口类型；若 OpenAPI 体现 `maxLength`，必须重新生成 Orval 并更新调用方测试。

## Risks / Trade-offs

- [Risk] 代码中存在多个 10 字符常量，漏改会造成前后端行为不一致。→ Mitigation：使用 targeted `rg` 搜索 `10`、`max_length=10`、`maxLength: 10`、旧错误文案，并用后端/前端测试覆盖 15/16 字符边界。
- [Risk] 数据库字段实际已足够长，但测试夹具仍以 10 字符作为业务规则。→ Mitigation：同步测试 helper 和最小合法 payload，避免 fixture/schema drift。
- [Risk] 15 字符名称在类目树、列表或小程序分类入口导致布局拥挤。→ Mitigation：使用 15 字符中文与英文数字样例做管理端、小程序和 Web 展示回归；允许既有截断/tooltip，但不得重叠或撑破。
- [Risk] 弹窗小改动触发 CSS cascade 回归。→ Mitigation：执行 admin-modal 横切 AC，确认 TSX 不同时挂载 `modal-card` 与专属类，并验收 computed width 与矮视口滚动。

## Migration Plan

1. 检查现有 SQLite schema、MySQL migration 和模型字段长度。
2. 若字段上限大于等于 15，记录无需 DB migration。
3. 若字段上限小于 15，新增迁移将字段放宽到至少 15，并同步 `docs/04-database-design.md`。
4. 回滚时仅恢复应用层上限；若执行过 DB 放宽迁移，不应自动收窄字段以避免截断已保存数据。

## Validation

- 后端 pytest：类目创建 / 更新 15 字符成功，16 字符失败；非法字符、空名称、同层级重复不回归。
- 前端 Vitest/Testing Library：`CategoryFormModal` 15 字符不报错，16 字符显示「类目名称最多 15 个字符」。
- OpenAPI / Orval：导出 schema 后重新生成客户端，确认 `maxLength` 为 15 或调用侧测试与后端约束一致。
- UI 回归：管理端类目树、列表、分页、fixed toast、confirm modal、弹窗 computed width、矮视口滚动。
- 小程序 / Web 展示端：15 字符类目名称样例不重叠、不撑破容器。
