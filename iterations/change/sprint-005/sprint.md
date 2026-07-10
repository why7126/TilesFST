---
note: workflow-sync — workflow-sync 自动同步 — 7/8 Change archived；0 applied；1 进行中；Sprint `planning`
created_at: 2026-07-04 22:30:20
updated_at: 2026-07-10 08:50:39
title: Sprint 005 迭代说明
purpose: 记录 Sprint 005 目标、范围、Change、工作量与风险
content: 管理端列表基础组件（REQ-0029）、接口文档页 Swagger 策略 checklist（REQ-0030）、Sprint 归档未完成 tasks 门禁（BUG-0056）、API governance route tags 清理（BUG-0057）、workflow-sync check drift 修复（BUG-0058）、管理端一次性密码复制修复（BUG-0059）、日志审计 request_id 复制修复（BUG-0060）与修改密码安全策略错误提示修复（BUG-0061）
source: /sprint-propose REQ-0030；/sprint-propose REQ-0029 纳入 sprint-005；/sprint-propose BUG-0056 纳入 sprint-005；/sprint-propose BUG-0057 纳入 sprint-005；/sprint-propose BUG-0058 纳入 sprint-005；/sprint-propose BUG-0059 纳入 sprint-005；/sprint-propose BUG-0060 纳入 sprint-005；/sprint-propose BUG-0061 纳入 sprint-005
update_method: 迭代范围或状态变化时更新
owner: 项目负责人
status: planning
---

# Sprint 005

## Sprint 目标

本迭代聚焦 **API 文档治理、工作流治理补强、管理端列表基础组件与关键交互修复**，承接 Sprint 004 复盘行动项 A-001、A-003、A-006、A-004 与 A-005：一方面将 `/admin/api-docs` Swagger 入口经验沉淀为可复用的 OpenSpec design / acceptance / 文档治理门禁，并把 `MetricCard`、`MetricCardGrid` 与分页窗口工具抽象为管理端列表共享能力；另一方面补齐 `/sprint-archive` 未完成 tasks 硬门禁、清理 API governance route tags 历史债、修复 workflow-sync `--check` 时间漂移幂等性，并补入 BUG-0059 的一次性密码复制可靠性修复、BUG-0060 的日志审计 `request_id` 复制兜底修复与 BUG-0061 的修改密码策略提示修复，提升 OpenAPI 契约质量、校验脚本可信度、迭代归档审计稳定性和管理端关键排障/账号交互可用性。

正式纳入范围：

1. **REQ-0029-admin-list-foundation-components** — 管理端列表基础组件（MetricCard 与分页窗口工具）。
2. **REQ-0030-api-docs-swagger-policy-checklist** — 接口文档页 Swagger 代理与生产调试策略 checklist。
3. **BUG-0056-sprint-archive-incomplete-tasks-gate** — `/sprint-archive` 未完成 tasks 仍可归档。
4. **BUG-0057-api-governance-tags-known-debt** — API governance route tags 历史债清理未闭环。
5. **BUG-0058-workflow-sync-check-time-drift-idempotency** — workflow-sync `--check` 时间漂移幂等性不足。
6. **BUG-0059-user-password-copy-not-working** — 管理端创建用户/重置密码后一次性密码复制未生效。
7. **BUG-0060-audit-log-request-id-copy-error** — 日志审计页复制 `request_id` 时报错。
8. **BUG-0061-change-password-policy-error-message-unclear** — 修改密码新密码安全策略失败提示不清晰。

### REQ-0029-admin-list-foundation-components 要点

- **优先级**：P1
- **类型**：Web 管理端 / Design System / admin-list 基础组件
- **范围**：抽象 `MetricCard`、`MetricCardGrid` 与分页窗口工具，稳定 `.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`、`.summary-grid`、`.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap` DOM 契约。
- **不包含**：不重做完整 `AdminListPage`；不一次性重构全部管理端列表页；不修改后端分页 API、数据库、OpenAPI/Orval、小程序或店主端。
- **OpenSpec 状态**：已创建 Change `add-admin-list-foundation-components`，状态为 proposed；下一步执行 `/opsx-apply add-admin-list-foundation-components`。
- **验收重点**：首批接入 2–3 个页面，覆盖普通指标卡、danger/异常描述和分页窗口；`/design-system` 或等效验收区展示组件状态；补充 Vitest / Testing Library DOM 结构测试；使用 semantic token，禁止裸 Hex。

### REQ-0030-api-docs-swagger-policy-checklist 要点

- **优先级**：P2
- **类型**：API/docs governance / Web 代理策略 / 安全门禁
- **范围**：将 `/docs`、`/redoc`、`/openapi.json`、Swagger UI 依赖资源、Vite dev proxy、Docker Nginx、生产反向代理、生产 `Try It Out` 禁用/只读策略写入接口文档页模板 checklist。
- **不包含**：不重新设计 `/admin/api-docs` 页面；不新增业务 API；不改数据库；不开放生产 Swagger 在线调试；不新增店主 Web、小程序或未登录用户接口文档入口。
- **OpenSpec 状态**：已创建 Change `update-api-docs-swagger-policy-checklist`，状态为 proposed；下一步执行 `/opsx-apply update-api-docs-swagger-policy-checklist`。
- **验收重点**：后续 design/acceptance 固定包含 Swagger Web 代理与生产 Try It Out 策略；同源 `/docs` 不落入 SPA fallback；生产等价环境保持 `Try It Out` 禁用或只读；链接和文档不得泄露 token、DSN、MinIO 凭据或真实环境变量。

### BUG-0056-sprint-archive-incomplete-tasks-gate 要点

- **严重等级**：high
- **类型**：workflow / tooling / process-gate
- **现象**：`/sprint-archive` 应在归档前确认 Sprint 范围内所有 Change 的 `tasks.md` 均已完成，但当前流程缺少可执行硬门禁，可能遗漏未完成任务并继续归档。
- **根因**：归档流程依赖人工阅读 Archive Queue Report，未调用会返回非零退出码的前置校验脚本；`workflow_sync` 能统计 task 进度，但不是归档前阻断点。
- **修复范围**：新增 Sprint archive readiness 校验脚本，覆盖 active / archived change、未完成 task、缺失 `tasks.md`、缺失 Change 目录等 blocker；更新 `/sprint-archive` skill/命令文档并补 pytest。
- **OpenSpec 状态**：Change `fix-sprint-archive-incomplete-tasks-gate` 已归档至 `openspec/changes/archive/2026-07-09-fix-sprint-archive-incomplete-tasks-gate/`；已通过 readiness gate、pytest、OpenSpec strict 与目录结构校验。

### BUG-0057-api-governance-tags-known-debt 要点

- **严重等级**：medium
- **类型**：API governance / OpenAPI metadata / 工具链校验
- **现象**：`python scripts/validate-api-standard.py` 可通过，但最终 OpenAPI 仍存在 operation tags 重复或双轨并存，例如 `["admin-brands", "Admin Brands"]`、`["auth", "auth"]`。
- **根因**：`router.include_router(..., tags=[...])` 与 route decorator `tags=TAGS` 同时作为事实源，且现有 API 校验脚本只做源码级启发式检查，未校验最终 OpenAPI operation tags。
- **修复范围**：统一 route tag 单一事实源，规范 OpenAPI tag 命名，增强 `validate-api-standard.py` 对最终 OpenAPI tags 的校验，重新导出 OpenAPI 并按需同步 Orval。
- **OpenSpec 状态**：已创建 Change `fix-api-governance-route-tags-known-debt`，状态为 proposed；下一步执行 `/opsx-apply fix-api-governance-route-tags-known-debt`。

### BUG-0058-workflow-sync-check-time-drift-idempotency 要点

- **严重等级**：medium
- **类型**：workflow / tooling / document-metadata
- **现象**：执行 `python scripts/sync-workflow-status.py --check` 时，已归档 Sprint 的 Scope 表可能因 archived Change 时间字段漂移而反复报告 drift。
- **根因**：归档时间推导曾读取 issue trace 或 change trace frontmatter `updated_at`，且普通同步在正文无变化时也可能刷新 `updated_at`，导致可变文档维护时间污染归档事实。
- **修复范围**：稳定 archived Change 归档时间来源，避免读取可变 `updated_at`；确保 Markdown 正文无变化时不刷新 `updated_at`；补充时间漂移回归测试；验证连续 `workflow-sync --check` no delta。
- **OpenSpec 状态**：已创建 Change `fix-workflow-sync-check-time-drift-idempotency`，状态为 proposed；下一步执行 `/opsx-apply fix-workflow-sync-check-time-drift-idempotency`。

### BUG-0059-user-password-copy-not-working 要点

- **严重等级**：high
- **类型**：Web 管理端 / 用户管理 / modal interaction / Clipboard fallback
- **现象**：创建用户成功后的初始密码弹窗、重置密码成功后的新随机密码弹窗中，点击「复制密码」后无法可靠粘贴出弹窗展示的一次性密码，且缺少明确成功/失败反馈。
- **根因**：`ResetPasswordDialog` 直接调用 `navigator.clipboard.writeText(password)`，未判断 Clipboard API 可用性；失败路径被空 `catch` 吞掉；缺少手动复制 fallback 与组件级测试。
- **修复范围**：为一次性密码结果弹窗补充复制成功/失败反馈、Clipboard API 不可用或失败时的手动复制指引/选中文本兜底，并新增 `ResetPasswordDialog` 复制行为测试。
- **不包含**：不修改用户管理 API 请求/响应/错误码；不修改数据库 schema；不持久化一次性明文密码；不涉及店主 Web 或小程序。
- **OpenSpec 状态**：已创建 Change `fix-user-password-copy-not-working`，状态为 proposed；下一步执行 `/opsx-apply fix-user-password-copy-not-working`。

### BUG-0060-audit-log-request-id-copy-error 要点

- **严重等级**：medium
- **类型**：Web 管理端 / 日志审计 / Clipboard fallback / admin-list feedback
- **现象**：日志审计页列表中点击复制 `request_id` 时出现报错或复制失败提示，管理员无法稳定复制请求编号用于排障。
- **根因**：`LogAuditPage` 直接调用 `navigator.clipboard.writeText(value)`，未判断 Clipboard API 可用性，也缺少浏览器拒绝写入、非安全上下文或写入失败时的手动复制兜底；现有测试只覆盖成功 mock 路径。
- **修复范围**：补齐 `request_id` 复制成功、Clipboard API 不存在、`writeText` reject、空值防御和 fixed toast 反馈回归测试；失败或兜底路径不得误报 `copy_request_id` 成功埋点。
- **不包含**：不修改日志审计 API、数据库 schema、权限边界、OpenAPI/Orval、MinIO 或小程序。
- **OpenSpec 状态**：已创建 Change `fix-audit-log-request-id-copy-error`，状态为 proposed；下一步执行 `/opsx-apply fix-audit-log-request-id-copy-error`。

### BUG-0061-change-password-policy-error-message-unclear 要点

- **严重等级**：medium
- **类型**：Web 管理端 / 修改密码 / password policy / API error feedback
- **现象**：修改密码时新密码不满足安全策略，系统仅提示“新密码不符合安全策略”，没有说明长度、大小写、数字、特殊字符、弱密码或同原密码等具体失败原因。
- **根因**：后端 `validate_password_policy()` 将多类策略失败折叠为同一 `policy` 结果，`PasswordPolicyError` 只返回泛化 message；前端 `ChangePasswordModal` 仍展示静态旧规则，未同步当前有效密码策略。
- **修复范围**：补充后端策略失败详情或更具体错误表达，前端展示当前有效策略与具体失败项，新增后端/前端回归测试。
- **不包含**：不放宽密码策略；不绕过后端校验；不持久化明文密码；不涉及小程序、店主展示端、数据库 schema、MinIO 或 Docker Compose。
- **OpenSpec 状态**：已创建 Change `fix-change-password-policy-error-message`，状态为 proposed；下一步执行 `/opsx-apply fix-change-password-policy-error-message`。

## Scope

### 包含需求

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0029 | 管理端列表基础组件（MetricCard 与分页窗口工具） | P1 | done | archived `add-admin-list-foundation-components`（2026-07-10 08:29:59） |
| REQ-0030 | 接口文档页 Swagger 代理与生产调试策略 checklist | P2 | proposed | proposed `update-api-docs-swagger-policy-checklist` |
<!-- workflow-sync:scope-requirements:end -->

### 包含 BUG

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0056 | /sprint-archive 未完成 tasks 仍可归档 | high | done | archived `fix-sprint-archive-incomplete-tasks-gate`（2026-07-09 23:45:40） |
| BUG-0057 | API governance route tags 历史债清理未闭环 | medium | done | archived `fix-api-governance-route-tags-known-debt`（2026-07-10 00:07:56） |
| BUG-0058 | workflow-sync --check 时间漂移幂等性不足 | medium | done | archived `fix-workflow-sync-check-time-drift-idempotency`（2026-07-10 00:15:41） |
| BUG-0059 | 管理端一次性密码弹窗复制密码未生效 | high | done | archived `fix-user-password-copy-not-working`（2026-07-06 16:05:44） |
| BUG-0060 | 日志审计页复制 request_id 时报错 | medium | done | archived `fix-audit-log-request-id-copy-error`（2026-07-09 08:37:20） |
| BUG-0061 | 修改密码安全策略错误提示不清晰 | medium | done | archived `fix-change-password-policy-error-message`（2026-07-07 00:28:52） |
<!-- workflow-sync:scope-bugs:end -->

### 包含 Change

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-admin-list-foundation-components` | REQ-0029-admin-list-foundation-components | archived | archived `add-admin-list-foundation-components`（2026-07-10 08:29:59） |
| `fix-sprint-archive-incomplete-tasks-gate` | BUG-0056-sprint-archive-incomplete-tasks-gate | archived | archived `fix-sprint-archive-incomplete-tasks-gate`（2026-07-09 23:45:40） |
| `update-api-docs-swagger-policy-checklist` | REQ-0030-api-docs-swagger-policy-checklist | proposed | proposed `update-api-docs-swagger-policy-checklist` |
| `fix-api-governance-route-tags-known-debt` | BUG-0057-api-governance-tags-known-debt | archived | archived `fix-api-governance-route-tags-known-debt`（2026-07-10 00:07:56） |
| `fix-workflow-sync-check-time-drift-idempotency` | BUG-0058-workflow-sync-check-time-drift-idempotency | archived | archived `fix-workflow-sync-check-time-drift-idempotency`（2026-07-10 00:15:41） |
| `fix-user-password-copy-not-working` | REQ-0005-user-management | archived | archived `fix-user-password-copy-not-working`（2026-07-06 16:05:44） |
| `fix-audit-log-request-id-copy-error` | REQ-0024-product-usage-logging | archived | archived `fix-audit-log-request-id-copy-error`（2026-07-09 08:37:20） |
| `fix-change-password-policy-error-message` | REQ-0015-password-change | archived | archived `fix-change-password-policy-error-message`（2026-07-07 00:28:52） |
<!-- workflow-sync:scope-changes:end -->

### 延后项（待评审 / 未纳入本 Sprint）

| 项目 | 状态 | 延后原因 |
|---|---|---|
| A-002 AdminListPage 模板 | open | 需独立 REQ/评审后再纳入，避免 scope 膨胀 |
| A-007 统一 422 envelope 治理 | open | 已有 REQ-0031 captured，未评审，不得纳入正式范围 |
| A-008 acceptance-report 历史 sign-off 复核 | open | 人工 QA review 项，不纳入本 Sprint |

## 工作量估算

| 工作项 | SP | 人天 | 角色 | 说明 |
|---|---:|---:|---|---|
| REQ-0029 管理端列表基础组件 | 5 | 3.0 | 前端/测试 | `/opsx-apply` 后实现 `MetricCard`、`MetricCardGrid`、分页窗口共享工具、设计系统示例和首批 2–3 页接入 |
| OpenSpec Change 生成与设计 | 1 | 0.75 | 产品/架构 | `/req-opsx` 后补齐 proposal、design、tasks 与 specs delta |
| checklist 文档同步 | 1 | 0.75 | 前端/DevOps/文档 | 明确 API docs design 模板、`docs/03-api-index.md`、`docs/standards/api-governance.md` 同步策略 |
| 验证策略与测试/验收记录 | 1 | 0.5 | 测试/前端 | 覆盖本地、Docker、生产等价代理与 `Try It Out` 策略 |
| BUG-0056 Sprint archive readiness gate | 3 | 2.0 | 工具链/测试 | `/bug-opsx` 已创建并 apply，补齐归档前未完成 tasks 硬阻断脚本、命令文档与 pytest |
| BUG-0057 route tags 单一事实源与 OpenAPI 校验 | 3 | 3.0 | 后端/测试 | `/bug-opsx` 后修复 tags 双轨、补强校验脚本、同步 OpenAPI/Orval |
| BUG-0058 workflow-sync 时间漂移修复 | 3 | 2.0 | 工具链/测试 | `/bug-opsx` 后修复归档时间推导、Markdown touch 策略并补回归测试 |
| BUG-0059 一次性密码复制弹窗修复 | 2 | 1.5 | 前端/测试 | `/bug-opsx` 后修复 `ResetPasswordDialog` 复制反馈、fallback 与组件测试 |
| BUG-0060 日志审计 request_id 复制修复 | 2 | 1.0 | 前端/测试 | `/bug-opsx` 后修复 `LogAuditPage` 复制反馈、Clipboard fallback 与页面测试 |
| BUG-0061 修改密码策略失败提示修复 | 3 | 2.5 | 后端/前端/测试 | `/bug-opsx` 已创建 Change，后续修复策略失败详情、前端动态规则展示与回归测试 |
| fix_buffer | 6 | 4.0 | 全员 | 预留 31.6% SP，应对 API governance、workflow-sync、Web modal 与密码策略联动 |
| **合计** | **29** | **21.0** | — | 含 fix 缓冲；1 条 P1 Web 管理端组件 REQ + 1 条 P2 治理 REQ + 6 条治理/交互 BUG |

## 容量门禁

| 门禁 | 当前值 | 结论 |
|---|---:|---|
| add-* 主能力数 | 1 / 6 | Pass；`add-admin-list-foundation-components` 为 P1 横切组件能力 |
| fix 缓冲 | 6 / 29 SP = 20.7% | Warning；低于 30% 建议值，已在风险表记录，后续非阻断项不得继续追加 |
| 人天容量 | 21.0 / 约 20.0 开发人天 | Warning；REQ-0029 追加后略超双人两周开发容量，需优先完成已归档/已实现项收尾并冻结新增范围 |
| UI 横切复发风险 | 1 个管理端列表组件 REQ + 3 个管理端复制/弹窗/表单交互 fix | Warning；REQ-0029 与 BUG-0060 共同追加 `admin-list-page-consistency.md` gate |

## 里程碑

| 里程碑 | 目标日期 | 说明 |
|---|---|---|
| Sprint 规划完成 | 2026-07-04 22:30:20 | 四件套创建，REQ-0030 纳入正式范围 |
| REQ-0029 纳入 Sprint | 2026-07-10 08:15:42 | 已评审需求纳入 sprint-005 |
| REQ-0029 Change 创建 | 2026-07-10 08:09:52 | 已创建 `add-admin-list-foundation-components` |
| OpenSpec Change 创建 | 2026-07-05 07:55:25 | 已创建 `update-api-docs-swagger-policy-checklist` |
| BUG 修复 Change 创建 | 2026-07-05 07:52:26 | 已创建 `fix-api-governance-route-tags-known-debt` |
| BUG-0058 Change 创建 | 2026-07-05 15:09:02 | 已创建 `fix-workflow-sync-check-time-drift-idempotency` |
| BUG-0058 纳入 Sprint | 2026-07-05 14:34:26 | 已评审 BUG 纳入 sprint-005 |
| BUG-0059 纳入 Sprint | 2026-07-06 15:23:04 | 已评审 BUG 纳入 sprint-005 |
| BUG-0059 Change 创建 | 2026-07-06 15:33:45 | 已创建 `fix-user-password-copy-not-working` |
| BUG-0060 纳入 Sprint | 2026-07-09 08:28:01 | 已评审 BUG 纳入 sprint-005 |
| BUG-0060 Change 创建 | 2026-07-09 08:18:00 | 已创建 `fix-audit-log-request-id-copy-error` |
| BUG-0061 纳入 Sprint | 2026-07-06 23:54:41 | 已评审 BUG 纳入 sprint-005 |
| BUG-0061 Change 创建 | 2026-07-07 00:08:22 | 已创建 `fix-change-password-policy-error-message` |
| BUG-0056 纳入 Sprint | 2026-07-09 23:25:11 | 已评审 BUG 纳入 sprint-005 |
| BUG-0056 Change 创建 | 2026-07-04 15:04:22 | 已创建并应用 `fix-sprint-archive-incomplete-tasks-gate` |
| 文档与验收策略确认 | 2026-07-08 18:00:00 | 明确 checklist 落点和 smoke/测试方式 |
| Sprint 验收准备 | 2026-07-17 18:00:00 | 完成 tasks、trace、验收记录 |
| Sprint 计划结束 | 2026-07-18 22:30:20 | 可进入 `/sprint-archive` 前检查 |

## 风险

| 风险 | 等级 | 影响 | 缓解 |
|---|---|---|---|
| BUG-0057 Change 待实现 | medium | API tags 修复尚未落地，Sprint apply 前仍需排队执行 | 执行 `/opsx-apply fix-api-governance-route-tags-known-debt` |
| BUG-0058 Change 待实现 | medium | Change 已创建但修复尚未落地，Sprint apply 前仍需排队执行 | 执行 `/opsx-apply fix-workflow-sync-check-time-drift-idempotency` |
| BUG-0059 Change 待实现 | high | Change 已创建但修复尚未落地，复制可靠性缺陷仍存在 | 执行 `/opsx-apply fix-user-password-copy-not-working` |
| BUG-0060 Change 待实现 | medium | Change 已创建但修复尚未落地，日志审计 request_id 复制兜底仍存在缺口 | 执行 `/opsx-apply fix-audit-log-request-id-copy-error` |
| BUG-0061 Change 待实现 | medium | Change 已创建但修复尚未落地，密码策略失败提示仍不清晰 | 执行 `/opsx-apply fix-change-password-policy-error-message` |
| REQ-0029 Change 待实现 | medium | P1 管理端列表基础组件尚未落地，A-003 复盘行动项仍未闭环 | 执行 `/opsx-apply add-admin-list-foundation-components`，首批页面控制在 2–3 个 |
| 容量略超限 | high | REQ-0029 追加后估算 21.0 人天，高于 2 人两周约 20 人天基线 | 冻结后续新增范围；若实现阶段超时，保留 2 页最低闭环，第三页转后续推广 |
| fix 缓冲低于建议值 | medium | REQ-0029 追加后 fix_buffer 降至 20.7%，低于 30% 建议值 | 后续非 P0/P1 阻断项延后到下一 Sprint；实现阶段优先关闭已纳入 fix |
| BUG-0061 可能涉及 API 契约 | medium | 若返回结构化策略失败详情，需同步 OpenAPI、Orval、API 文档与测试 | 在 Change design 中明确响应结构；实现后运行 OpenAPI/Orval 同步 |
| 剪贴板权限与浏览器兼容 | medium | Clipboard API 在权限受限或非预期运行环境中可能失败，若无 fallback 会复发 | acceptance 必须覆盖 writeText 成功、失败与 API 不存在三类路径 |
| checklist 落点分散 | medium | design、API 文档、知识库重复或遗漏 | OpenSpec design 中固定事实源与同步对象 |
| 生产 Try It Out 策略被误解为可打开 | high | 可能放开生产在线调试 | acceptance 明确生产只读，security review 作为 tasks gate |
| scope 再次膨胀 | medium | 重蹈 sprint-004 多主线问题 | BUG-0059 以 2 SP 小修补入并同步增加 fix_buffer；其他 A-xxx 留延后项 |

## 知识库承接

| ID | 优先级 | 描述 | 本 Sprint 承接方式 |
|---|---|---|---|
| A-001 | P0 | 修复 `/sprint-archive` 前 tasks 未完成也可归档的问题 | **承接**；对应 BUG-0056 与 Change `fix-sprint-archive-incomplete-tasks-gate` |
| A-002 | P1 | 落地 `AdminListPage` / 管理端列表页契约 | 延后；需独立 approved REQ |
| A-003 | P1 | 抽象 `MetricCard` 与分页窗口工具 | **承接**；对应 REQ-0029 与 Change `add-admin-list-foundation-components` |
| A-004 | P1 | 清理 API governance 既有 route tags 失败 | **承接**；对应 BUG-0057 与 Change `fix-api-governance-route-tags-known-debt` |
| A-005 | P1 | 修复 workflow-sync `--check` 时间漂移幂等性 | **承接**；对应 BUG-0058 与 Change `fix-workflow-sync-check-time-drift-idempotency` |
| A-006 | P2 | 将 Swagger Web 代理和生产 Try It Out 策略写入接口文档页模板 checklist | **承接**；对应 REQ-0030 |
| A-007 | P2 | 将统一 422 envelope 设计扩展到所有管理端表单 API | 延后；REQ-0031 captured 但未评审 |
| A-008 | P2 | 复核 `acceptance-report.md` 历史待 sign-off 内容 | 延后；人工 QA review |

## 横切预防清单

本 Sprint 新增管理端列表基础组件能力但不新增完整 CRUD 列表页或媒体上传能力；REQ-0029 与 BUG-0060 触发 `admin-list` best-practice，BUG-0059 涉及管理端一次性密码结果弹窗交互修复，BUG-0061 涉及修改密码弹窗/表单错误提示修复，触发 `admin-modal` 与 `admin-form` best-practices 横切 AC。

本 Sprint 的专项预防清单来自 `docs/knowledge-base/retrospectives/sprint-004-retrospective.md`、`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` 与 `docs/knowledge-base/best-practices/admin-form-page-consistency.md`：

- [ ] API docs design MUST 声明 dev / Docker / production 代理路径。
- [ ] REQ-0029 MetricCard MUST 稳定输出 `.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`。
- [ ] REQ-0029 MetricCardGrid MUST 保留 `.summary-grid`，并覆盖 2、3、4 卡布局。
- [ ] REQ-0029 pagination-window MUST 默认最多 5 个页码，并覆盖首页附近、居中页、末页附近和非法输入。
- [ ] REQ-0029 first batch MUST 从 `TileSkuManagementPage`、`LogAuditPage`、`ApiDocsPage`、`BrandManagementPage` 中选择 2–3 个页面。
- [ ] REQ-0029 implementation MUST 使用 semantic token / 既有管理端 class 与 `cn()`，禁止新增裸 Hex。
- [ ] API docs design MUST 声明生产 `Try It Out` 禁用或只读策略。
- [ ] acceptance MUST 覆盖 `/docs` 不被 Web SPA fallback 接管。
- [ ] acceptance MUST 覆盖 Swagger 链接不泄露 token、DSN、MinIO 凭据或真实环境变量。
- [ ] API governance fix MUST 校验最终 OpenAPI operation tags，而不仅是源码 decorator 是否包含 `tags=`。
- [ ] API governance fix MUST 验证多 tag operation、重复 tag operation、非 kebab-case tag operation 均为 0。
- [ ] workflow-sync fix MUST 验证 archived Change 归档时间不读取 issue/change trace 的可变 `updated_at`。
- [ ] workflow-sync fix MUST 验证 Markdown 正文无变化时不刷新 frontmatter `updated_at`。
- [ ] workflow-sync fix MUST 连续运行 `python scripts/sync-workflow-status.py --check` 并保持 no delta。
- [ ] BUG-0056 archive readiness gate MUST 在 Sprint 内任一 Change `tasks.md` 存在 `- [ ]` 时返回非零退出码。
- [ ] BUG-0056 archive readiness gate MUST 覆盖 active 与 archived Change，不得因 Change 已归档而跳过未完成 tasks。
- [ ] BUG-0056 archive readiness gate MUST 在 `/sprint-archive` 默认流程中先于 Sprint close、issue promote 和目录迁移执行。
- [ ] BUG-0059 modal fix MUST 不引入 `modal-card` 与专属类双挂载，避免弹窗宽度 CSS 层叠回归。
- [ ] BUG-0059 modal fix MUST 保持关闭后不可再次查看的一次性密码风险提示清晰。
- [ ] BUG-0059 copy feedback MUST 不造成弹窗布局抖动，并在矮视口下保持滚动/关闭能力。
- [ ] BUG-0059 fallback MUST 不将一次性明文密码写入数据库、日志、审计事件或长期文档。
- [ ] BUG-0059 tests MUST 覆盖 Clipboard 成功、失败和不可用路径。
- [ ] BUG-0060 copy feedback MUST 使用 fixed toast 或等价固定层，不引起日志审计页 hero、表格、分页纵向位移。
- [ ] BUG-0060 fallback MUST 覆盖 Clipboard API 不存在、`writeText` reject、空 `request_id` 防御路径。
- [ ] BUG-0060 success telemetry MUST 仅在剪贴板写入成功后上报 `copy_request_id`，失败/兜底路径不得误报成功复制。
- [ ] BUG-0060 tests MUST 覆盖 `LogAuditPage` 列表渲染、复制成功、Clipboard 不可用、写入失败和详情/分页无回归。
- [ ] BUG-0061 fix MUST 明确密码策略事实源，前端展示规则与后端有效策略一致。
- [ ] BUG-0061 API error feedback MUST 指出具体失败项，且不得放宽后端密码策略。
- [ ] BUG-0061 tests MUST 覆盖长度不足、缺少大小写/数字/特殊字符、弱密码、同原密码和原密码错误无回归。

## 依赖

```text
sprint-005
├── REQ-0029-admin-list-foundation-components
    ├── parent: REQ-0028-admin-list-page-contract（已评审，未纳入本 Sprint）
    ├── related bug: BUG-0055-admin-list-layout-unification（已归档修复）
    ├── best-practice: admin-list-page-consistency
    └── change: add-admin-list-foundation-components（proposed）
├── REQ-0030-api-docs-swagger-policy-checklist
    ├── parent: REQ-0022-admin-api-docs-menu（已归档能力）
    ├── related: REQ-0023-api-docs-swagger-detail-link（已归档能力）
    ├── related bug: BUG-0051-api-docs-swagger-ui-link-wrong（已归档修复）
    └── change: update-api-docs-swagger-policy-checklist（proposed）
├── BUG-0056-sprint-archive-incomplete-tasks-gate
    ├── source: sprint-004 retrospective A-001
    ├── related capability: sprint-archive / workflow tooling
    └── change: fix-sprint-archive-incomplete-tasks-gate（archived）
├── BUG-0057-api-governance-tags-known-debt
    ├── source: sprint-004 retrospective A-004
    ├── related capability: api-governance
    └── change: fix-api-governance-route-tags-known-debt（proposed）
├── BUG-0058-workflow-sync-check-time-drift-idempotency
    ├── source: sprint-004 retrospective A-005
    ├── related capability: workflow-sync
    └── change: fix-workflow-sync-check-time-drift-idempotency（proposed）
└── BUG-0059-user-password-copy-not-working
    ├── parent: REQ-0005-user-management（已归档能力）
    ├── related capability: user-management / ResetPasswordDialog
    ├── best-practice: admin-modal-width-css-cascade
    └── change: fix-user-password-copy-not-working（proposed）
└── BUG-0060-audit-log-request-id-copy-error
    ├── parent: REQ-0024-product-usage-logging（已归档能力）
    ├── related capability: product-usage-logging / LogAuditPage
    ├── best-practice: admin-list-page-consistency
    └── change: fix-audit-log-request-id-copy-error（proposed）
└── BUG-0061-change-password-policy-error-message-unclear
    ├── parent: REQ-0015-password-change（已归档能力）
    ├── related capability: admin-password-change / ChangePasswordModal
    ├── best-practice: admin-modal-width-css-cascade, admin-form-page-consistency
    └── change: fix-change-password-policy-error-message（proposed）
```

## 发布计划

- 本 Sprint 暂不直接形成产品版本发布对象。
- REQ-0029 预计影响 Web 管理端共享 UI、`/design-system` 示例和首批列表页接入；不影响后端 API、数据库、OpenAPI/Orval、小程序或店主端。
- 若后续 Change 仅更新规范、文档和测试 checklist，可在迭代 release-note 中作为治理改进记录。
- BUG-0057 预计会更新 OpenAPI tags 与 Orval 生成物，发布说明需标注为 API 契约元数据治理，不改变业务请求/响应语义。
- BUG-0056 只影响 `/sprint-archive` 工作流脚本、命令文档与测试，不改变产品业务 API、数据库、Web UI、小程序或 Docker Compose。
- BUG-0058 预计只影响 workflow-sync 工具链和测试，不改变产品业务功能。
- BUG-0059 预计只影响 Web 管理端用户管理一次性密码弹窗复制交互，不改变 API、数据库或小程序。
- BUG-0060 预计只影响 Web 管理端日志审计页 `request_id` 复制交互，不改变 API、数据库、OpenAPI/Orval 或小程序。
- BUG-0061 预计影响 Web 管理端修改密码弹窗与密码策略失败反馈；若 API 错误响应增加结构化详情，发布说明需标注 OpenAPI/Orval 同步情况。
- 若涉及 Docker/Nginx 实际配置修改，必须补充 Docker Compose 验证记录，并在 release-note 中列为部署注意事项。

## 关联文档

| 文档 | 说明 |
|---|---|
| `issues/requirements/archive/REQ-0029-admin-list-foundation-components/` | 需求包事实源 |
| `issues/requirements/review/REQ-0030-api-docs-swagger-policy-checklist/` | 需求包事实源 |
| `issues/bugs/archive/BUG-0056-sprint-archive-incomplete-tasks-gate/` | BUG 包事实源 |
| `issues/bugs/archive/BUG-0057-api-governance-tags-known-debt/` | BUG 包事实源 |
| `issues/bugs/archive/BUG-0058-workflow-sync-check-time-drift-idempotency/` | BUG 包事实源 |
| `issues/bugs/archive/BUG-0059-user-password-copy-not-working/` | BUG 包事实源 |
| `issues/bugs/archive/BUG-0060-audit-log-request-id-copy-error/` | BUG 包事实源 |
| `issues/bugs/archive/BUG-0061-change-password-policy-error-message-unclear/` | BUG 包事实源 |
| `openspec/changes/fix-user-password-copy-not-working/` | BUG-0059 修复 Change |
| `openspec/changes/add-admin-list-foundation-components/` | REQ-0029 OpenSpec Change |
| `openspec/changes/archive/2026-07-09-fix-sprint-archive-incomplete-tasks-gate/` | BUG-0056 修复 Change 归档目录 |
| `openspec/changes/fix-workflow-sync-check-time-drift-idempotency/` | BUG-0058 修复 Change |
| `openspec/changes/fix-audit-log-request-id-copy-error/` | BUG-0060 修复 Change |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | BUG-0060 日志审计列表反馈横切预防 gate |
| `docs/knowledge-base/retrospectives/sprint-004-retrospective.md` | A-004 / A-005 / A-006 来源 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | BUG-0059 弹窗修复横切预防 gate |
| `docs/03-api-index.md` | 后续可能同步接口文档页说明 |
| `docs/standards/api-governance.md` | 后续可能同步 Swagger / Orval 治理 checklist |
| `src/web/nginx.conf` | Docker Web 代理检查对象 |

## 变更记录

| 时间 | 说明 |
|---|---|
| 2026-07-10 08:15:42 | `/sprint-propose` 续写 sprint-005，纳入 REQ-0029，承接 Sprint 004 A-003 |
| 2026-07-09 23:46:53 | `/opsx-archive` 归档 `fix-sprint-archive-incomplete-tasks-gate`，BUG-0056 迁入 archive |
| 2026-07-09 23:25:11 | `/sprint-propose` 续写 sprint-005，纳入 BUG-0056，承接 Sprint 004 A-001 归档 tasks gate |
| 2026-07-09 08:28:01 | `/sprint-propose` 续写 sprint-005，纳入 BUG-0060，增加日志审计 request_id 复制兜底修复范围 |
| 2026-07-06 23:54:41 | `/sprint-propose` 续写 sprint-005，纳入 BUG-0061，增加修改密码策略失败提示修复范围 |
| 2026-07-06 15:33:45 | `/bug-opsx` 创建 `fix-user-password-copy-not-working`，关联 BUG-0059 |
| 2026-07-06 15:23:04 | `/sprint-propose` 续写 sprint-005，纳入 BUG-0059，增加一次性密码弹窗复制修复范围 |
| 2026-07-05 15:09:02 | `/bug-opsx` 创建 `fix-workflow-sync-check-time-drift-idempotency`，关联 BUG-0058 |
| 2026-07-05 14:34:26 | `/sprint-propose` 续写 sprint-005，纳入 BUG-0058，承接 Sprint 004 A-005 |
| 2026-07-05 07:55:25 | `/req-opsx` 创建 `update-api-docs-swagger-policy-checklist`，关联 REQ-0030 |
| 2026-07-05 07:52:26 | `/bug-opsx` 创建 `fix-api-governance-route-tags-known-debt`，关联 BUG-0057 |
| 2026-07-04 22:42:09 | `/sprint-propose` 续写 sprint-005，纳入 BUG-0057，承接 Sprint 004 A-004 |
| 2026-07-04 22:30:20 | `/sprint-propose` 创建 sprint-005，纳入 REQ-0030 |
