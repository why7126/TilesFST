## Context

REQ-0082 已评审通过，要求将管理后台瓷砖类目名称规则由“最多 15 个字符，只能包含中文、英文和数字”调整为“最多 15 个字符，允许中文、英文、数字和特殊字符”。正式 `tile-category-management` spec 已包含“类目名称输入长度上限”，其中仍表述为不改变既有字符集；本变更需要修改该规格，使字符集放宽成为正式能力。

关联文档：

- `issues/requirements/archive/REQ-0082-admin-category-name-special-characters/requirement.md`
- `issues/requirements/archive/REQ-0082-admin-category-name-special-characters/acceptance.md`
- `issues/requirements/archive/REQ-0082-admin-category-name-special-characters/prototype/web/admin-category-name-special-characters.html`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/retrospectives/sprint-013-retrospective.md`

## Goals / Non-Goals

**Goals:**

- 后端创建 / 更新类目接口接受包含合法特殊字符、长度不超过 15 个用户可见字符的名称。
- 后端拒绝空名称、16 字符名称、换行、制表符和不可见控制字符。
- Web 管理端新增 / 编辑弹窗使用同样的字符集与长度校验，并提供字段级错误提示。
- OpenAPI / Orval / docs / tests 与新的字符集约束一致。
- 回归管理端类目树、列表、选择器、小程序分类页和 Web 展示端分类入口在特殊字符名称下布局稳定。
- 保留 admin-list 与 admin-modal 横切 AC，避免分页、toast、confirm 和弹窗 CSS cascade 回归。

**Non-Goals:**

- 不调整类目名称最多 15 个字符的长度上限。
- 不改变同层级名称唯一规则。
- 不改变类目编码自动生成、编码唯一、层级上限、排序权重、启停和删除规则。
- 不做历史类目数据清洗、批量重命名或迁移。
- 不新增类目别名、多语言名称、简称、SEO 名称或展示名称字段。

## Conflict Resolution

原型与验收优先级：HTML > PNG > `prototype-context.md` > `acceptance.md` > `rules/ui-design.md` > `openspec/specs`。

| 来源 | 结论 |
|---|---|
| HTML 原型 `admin-category-name-special-characters.html` | 明确展示特殊字符合法样例、非法控制字符错误态、类目树和列表展示样例；作为 UI 语义最高参考。 |
| PNG | 尚未导出，非阻塞；后续实现可按 HTML 原型或实际页面补截图证据。 |
| `prototype-context.md` | 明确实现阶段复用现有类目管理页、类目新增 / 编辑弹窗、列表和类目树。 |
| `acceptance.md` | 功能 AC 与 7 条横切 AC 完整，作为测试矩阵来源。 |
| `rules/ui-design.md` | 要求 semantic token、DS 组件复用、字段级错误定位和管理端 modal/list best-practice。 |
| `openspec/specs/tile-category-management/spec.md` | 当前“类目名称输入长度上限”保留 15 字符上限，但旧描述“不改变既有字符集”与本需求冲突；delta spec 使用 MODIFIED 消化。 |

## Decisions

### D1 UI 策略：Design System 增量调整

采用 DS 增量调整，不做 CSS Port。原因是本需求只调整现有类目表单的校验、提示和回归样例，不需要新视觉或页面结构。实现时应复用现有表单、弹窗、列表、toast 和 confirm 组件，并保持 semantic token。

备选：按 HTML 原型重新 port CSS。未采用，因为 HTML 只用于表达验收语义，直接 port 会增加样式分叉风险。

### D2 字符集策略：允许常见可见业务符号，禁止控制字符

前端和后端统一采用“允许中文、英文、数字和常见可见特殊字符；禁止换行、制表符、不可见控制字符和仅空白输入”的策略。常见业务符号至少包含 `-`、`_`、`/`、`&`、`()`、`·`、`.`、`+`、`#`、`:`、`，`、`、`。如果实现采用更广义的可见符号判断，也必须明确禁止控制字符并保持测试覆盖。

备选：允许所有字符。未采用，因为换行、控制字符会破坏列表、树、日志和输入安全边界。

### D3 数据库策略：先确认约束，再决定是否迁移

正式 spec 的数据模型允许 `name` 最大 30 字符，业务需求只放宽应用层字符集，因此理论上不需要数据库结构变更。实现阶段仍必须检查 SQLite schema、MySQL migration、CHECK 约束、触发器和测试夹具是否残留“中文、英文和数字”限制；只有发现真实 DB 约束限制旧字符集时才纳入 migration。

### D4 API / Orval 策略：后端事实源驱动

后端 Schema 或业务校验是名称规则事实源，OpenAPI 从后端导出，Orval 从 OpenAPI 生成。前端不得手写重复接口类型；若 OpenAPI 体现 `pattern`、`maxLength` 或字段描述，必须重新生成 Orval 并更新调用方测试。

### D5 类目树策略：默认折叠并分离展开与筛选

管理端左侧类目树默认只显示一级类目，二级及以下类目默认收起。有子级的类目前置 `+/-` 控件用于展开 / 收起；点击 `+/-` 仅改变树展开状态，不触发类目筛选。点击类目名称或节点主体仍用于筛选对应类目。该策略用于降低特殊字符名称在多级树中同时展示时的拥挤风险，并保持层级识别稳定。

## Risks / Trade-offs

- [Risk] 前端接受特殊字符但后端仍按旧正则拒绝。→ Mitigation：后端和前端测试均覆盖 `岩板-大规格`、`仿古砖/客厅`、`600x1200(亮面)`、`A+B#系列`。
- [Risk] 过度放宽字符集导致换行或控制字符进入类目树、列表、日志。→ Mitigation：明确禁止换行、制表符、不可见控制字符和仅空白输入。
- [Risk] OpenAPI / Orval 或测试 fixture 仍保留旧字符集说明。→ Mitigation：搜索旧文案和 schema pattern，重新生成 OpenAPI / Orval 并同步测试 helper。
- [Risk] 特殊字符名称在列表、树或小程序分类入口导致布局异常。→ Mitigation：执行管理端、小程序和 Web 展示端布局回归；允许既有截断 / tooltip，但不得重叠或撑破。
- [Risk] 类目树多级节点默认展开导致特殊字符名称拥挤，或点击展开控件误触发筛选。→ Mitigation：类目树默认仅显示一级类目，使用独立 `+/-` 控件控制展开 / 收起，并以组件测试覆盖点击分离。
- [Risk] 弹窗小改动触发 CSS cascade 回归。→ Mitigation：执行 admin-modal 横切 AC，确认 TSX 不同时挂载 `modal-card` 与专属类，并验收 computed width 与矮视口滚动。

## Migration Plan

1. 检查现有 SQLite schema、MySQL migration、模型字段、CHECK 约束和触发器。
2. 若字段和约束已支持特殊字符，记录无需 DB migration。
3. 若存在旧字符集 DB 约束，新增迁移放宽为允许常见可见业务符号并禁止控制字符，同时同步 `docs/04-database-design.md`。
4. 回滚时恢复应用层校验；如果执行过 DB 约束放宽，不应自动收窄已保存数据以避免破坏线上数据。

## Validation

- 后端 pytest：类目创建 / 更新特殊字符成功，16 字符失败；空名称、控制字符、同层级重复不回归。
- 前端 Vitest / Testing Library：`CategoryFormModal` 特殊字符不报错，16 字符和控制字符显示字段级错误。
- OpenAPI / Orval：导出 schema 后重新生成客户端，确认字段描述、pattern 或约束不保留旧字符集。
- UI 回归：管理端类目树、列表、分页、fixed toast、confirm modal、弹窗 computed width、矮视口滚动；类目树需覆盖默认仅显示一级类目、`+/-` 展开 / 收起和点击分离。
- 小程序 / Web 展示端：特殊字符类目名称样例不重叠、不撑破容器。
