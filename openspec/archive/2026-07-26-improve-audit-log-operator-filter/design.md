## Context

`REQ-0070-audit-log-operator-filter` 已评审通过，目标是优化 Web 管理端 `/admin/logs` 的操作者筛选体验。当前日志列表已显示 `actor_name`，后端日志查询 API 已支持 `actor_user_id`，用户管理 API 已支持 `keyword` 查询 `username` 与 `display_name`，前端也已有 `SearchableSelect` 组件。

现状痛点是筛选区仍展示 User ID 输入框，管理员需要先从其他地方查 ID。需求要求界面按用户名称或账号搜索并单选操作者，但日志事实源和查询语义继续使用稳定的 `actor_user_id`。

### Requirement Readiness Report

| 项 | 结论 |
|---|---|
| status | approved |
| requirement.md | ready |
| user-stories.md | ready |
| business-flow.md | ready |
| acceptance.md | ready，含 25 条功能 AC 与 5 条 admin-list 横切 AC |
| prototype/web | ready，含 context 与 HTML 原型 |
| readiness | Ready |

### Impact

```yaml
impact:
  backend: conditional
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: conditional
capabilities:
  new: []
  modified:
    - product-usage-logging
    - web-client
```

### Conflict Report

优先级：HTML > prototype context > acceptance > ui-design > openspec/specs。

| 来源 | 结论 |
|---|---|
| `prototype/web/operator-filter.html` | 展示单选可搜索下拉；最终实现收敛为账号与用户名称两行，分页 DOM 使用 `.page-summary` + `.page-right`。 |
| `prototype/web/context.md` | 明确默认、展开、搜索中、无结果、失败、已选择状态，并要求复用 `SearchableSelect` 或同等 DS 组件。 |
| `acceptance.md` | 明确必须传 `actor_user_id`，不得把名称或账号作为日志过滤值。 |
| `rules/ui-design.md` | 管理端列表页优先复用 shared/ui、semantic token、列表骨架一致性。 |
| `openspec/specs/product-usage-logging` | 已要求页面展示操作者筛选，但未规定名称搜索下拉。 |
| `openspec/specs/web-client` | 已规定 `/admin/logs` 列表横切一致性和状态筛选下拉；可新增操作者筛选场景。 |

冲突处理：采用 HTML/context 中的交互意图，保留 acceptance 中的 `actor_user_id` 稳定过滤约束，并以 `web-client` 横切要求约束分页、toast、移动端和无 native dialog。

## Goals / Non-Goals

**Goals:**

- 将 `/admin/logs` 操作者筛选改为单选可搜索下拉。
- 候选项支持按用户名称和账号搜索，并以账号与用户名称两行区分同名用户。
- 日志查询继续传 `actor_user_id`，保持后端查询语义兼容。
- 候选加载、无结果、失败、清空、重置状态可用。
- 保持 admin-list 横切一致性：分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm`、移动端筛选区不溢出。
- 优先复用现有 `GET /api/v1/admin/users` 与 `SearchableSelect`，减少 API 和组件扩散。

**Non-Goals:**

- 不改写日志表中的 `actor_user_id` 事实源。
- 不按 `actor_name` 文本过滤日志。
- 不新增多选操作者筛选。
- 不扩展用户管理 CRUD 能力。
- 不新增数据库表或对象存储能力。
- 不创建独立审计操作者管理页面。

## Decisions

### D1. UI strategy: DS SearchableSelect reuse

采用 Design System / shared UI 复用策略：优先复用或小幅扩展 `SearchableSelect`，而不是 CSS Port 或全新控件。

理由：

- 需求是筛选控件交互替换，不是整页 Golden Reference 重做。
- 现有 `SearchableSelect` 已支持单选、搜索、下拉和空态，可减少重复实现。
- `rules/ui-design.md` 要求优先复用 `src/web/src/shared/ui/`，并使用 semantic token。

备选方案：

- CSS Port：适合从 HTML 原型完整移植页面视觉，但本需求只需要控件级行为，成本偏高。
- 新建业务控件：会增加维护面，并可能重复 shared UI 能力。

### D2. Filter semantics: display name selects, user id filters

前端下拉展示 `display_name || username`，选中后保存 `user.id`，日志查询继续传 `actor_user_id=user.id`。

理由：

- 用户名称可变且可能同名，不适合作为审计过滤事实源。
- 现有日志 API 已支持 `actor_user_id`，保留兼容可降低后端变更风险。
- 日志列表已通过 users join 显示 `actor_name`，筛选层无需改写历史记录。

### D3. Candidate source: reuse admin users API first

优先复用 `GET /api/v1/admin/users`：

```text
GET /api/v1/admin/users?page=1&page_size=20&keyword=<query>
```

前端将 `UserAdminItem` 映射为下拉候选项：

```text
value = id
label = display_name || username
description = username
```

如 apply 阶段确认 `SearchableSelect` 无法展示辅助文案，可小幅扩展 shared component option 结构，保持向后兼容。

新增轻量候选 API 仅在以下条件出现时启用：

- 用户列表 API 返回字段过多导致明显性能或隐私问题；
- 候选搜索需要与完整用户管理列表不同的权限边界；
- 需要包含已删除历史用户但用户管理列表默认不返回。

### D4. Error handling: separate candidate errors from log list errors

用户候选加载失败只影响操作者下拉，不应阻塞日志列表其他筛选。日志列表查询失败使用既有日志页错误反馈；候选失败使用控件内提示加 fixed toast 或等价固定反馈。

### D5. Cross-cutting validation

实现必须继承 `admin-list` 横切 AC：

- 分页 DOM 保持 `.page-summary` + `.page-right`。
- 指标卡 DOM 保持 `.metric-label` / `.metric-value` / `.metric-desc`。
- 候选错误、日志查询错误和复制反馈不得造成布局位移。
- 本期无危险操作，DS confirm 为 N/A；如新增危险操作必须使用 DS confirm。
- 不调用 `window.confirm`。

## Risks / Trade-offs

- [Risk] 复用用户列表 API 可能返回完整用户管理字段。→ Mitigation: 前端只使用候选所需字段；若数据暴露超出筛选需要，在 apply 阶段新增轻量候选 API 并同步 OpenAPI/Orval。
- [Risk] 同名用户误选。→ Mitigation: 候选项必须展示 username、role 或 status 等辅助信息；测试覆盖同名区分。
- [Risk] 搜索频繁触发用户列表请求。→ Mitigation: 复用 `SearchableSelect` 防抖机制或在日志页包装层增加防抖；限制 page_size。
- [Risk] 已删除历史操作者无法在候选列表中出现。→ Mitigation: design/apply 阶段确认用户列表状态过滤；若默认排除 deleted，需要在 UI/验收说明历史日志筛选限制，或新增候选 API 覆盖历史操作者。
- [Risk] 移动端筛选区溢出。→ Mitigation: 复用日志页现有 responsive filter grid，并补充 375px/390px 视口测试或截图验证。

## Migration Plan

1. 前端实现操作者候选搜索状态和选中用户状态。
2. 将日志查询参数从输入框字符串改为选中用户 `id`。
3. 补充候选搜索与日志查询交互测试。
4. 如未新增 API，仅运行前端测试与类型检查；如新增或修改 API，同步 OpenAPI、Orval、API 文档和后端测试。
5. 验证 `/admin/logs` 在桌面与移动端筛选区、分页、toast 无布局回归。

Rollback：保留日志 API `actor_user_id` 兼容，因此前端可回退到原输入框行为；无 DB rollback。

## Open Questions

- 现有用户列表 API 是否应包含 `deleted` 状态用户作为历史日志候选？apply 阶段需要用业务规则确认。
- `SearchableSelect` 是否需要扩展辅助文案、loading/error 显示？若扩展，应保持现有调用方兼容。
