---
created_at: 2026-07-04 22:30:20
updated_at: 2026-07-10 08:15:42
title: Sprint 005 发布说明
purpose: 记录 Sprint 005 交付能力与发布注意事项（初稿）
content: 基于 REQ-0029-admin-list-foundation-components、REQ-0030-api-docs-swagger-policy-checklist、BUG-0056-sprint-archive-incomplete-tasks-gate、BUG-0057-api-governance-tags-known-debt、BUG-0058-workflow-sync-check-time-drift-idempotency、BUG-0059-user-password-copy-not-working、BUG-0060-audit-log-request-id-copy-error 与 BUG-0061-change-password-policy-error-message-unclear
source: /sprint-propose REQ-0030；/sprint-propose REQ-0029 纳入 sprint-005；/sprint-propose BUG-0056 纳入 sprint-005；/sprint-propose BUG-0057 纳入 sprint-005；/sprint-propose BUG-0058 纳入 sprint-005；/sprint-propose BUG-0059 纳入 sprint-005；/sprint-propose BUG-0060 纳入 sprint-005；/sprint-propose BUG-0061 纳入 sprint-005
update_method: Sprint 完成或范围变更时更新
owner: 项目负责人
status: draft
---

# Sprint 005 发布说明

## 版本信息

| 字段 | 内容 |
|---|---|
| Sprint | sprint-005 |
| 关联需求 | REQ-0029-admin-list-foundation-components；REQ-0030-api-docs-swagger-policy-checklist |
| 关联 BUG | BUG-0056-sprint-archive-incomplete-tasks-gate；BUG-0057-api-governance-tags-known-debt；BUG-0058-workflow-sync-check-time-drift-idempotency；BUG-0059-user-password-copy-not-working；BUG-0060-audit-log-request-id-copy-error；BUG-0061-change-password-policy-error-message-unclear |
| 关联 Change | REQ-0029: `add-admin-list-foundation-components`；REQ-0030: `update-api-docs-swagger-policy-checklist`；BUG-0056: `fix-sprint-archive-incomplete-tasks-gate`；BUG-0057: `fix-api-governance-route-tags-known-debt`；BUG-0058: `fix-workflow-sync-check-time-drift-idempotency`；BUG-0059: `fix-user-password-copy-not-working`；BUG-0060: `fix-audit-log-request-id-copy-error`；BUG-0061: `fix-change-password-policy-error-message` |
| 计划周期 | 2026-07-04 22:30:20 ~ 2026-07-18 22:30:20 |

<!-- workflow-sync:release-status:start -->
| 发布状态 | **实现进行中（In progress）** |
<!-- workflow-sync:release-status:end -->

## 计划交付

### 管理端列表基础组件（MetricCard 与分页窗口工具）

- 新增管理端可复用 `MetricCard` / `MetricCardGrid` 或等价组件，稳定 `.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc` 与 `.summary-grid` DOM 契约。
- 将分页窗口算法沉淀到共享 Web/admin 工具层，默认最多展示 5 个页码，并补齐非法输入兜底。
- 首批选择 2–3 个管理端列表页接入，覆盖普通指标卡、danger / 异常描述与分页窗口。
- 在 `/design-system` 或等效管理端设计验收区展示正常、空值/loading、danger、2/3/4 卡布局和分页边界样例。
- 不修改后端分页 API、数据库结构、OpenAPI/Orval、小程序或店主 Web。

### 接口文档页 Swagger 代理与生产调试策略 checklist

- 将 Swagger Web 代理与生产 `Try It Out` 策略写入 API docs 相关 design / acceptance checklist。
- 固定检查 `/docs`、`/redoc`、`/openapi.json` 与 Swagger UI 依赖资源的同源代理策略。
- 要求 Vite dev proxy、Docker Web Nginx 与生产反向代理均有明确验证记录。
- 要求生产环境 Swagger 文档可见但在线调试禁用、隐藏或等价只读。
- 要求 Swagger 链接不得泄露 token、数据库 DSN、MinIO 凭据或真实环境变量。

### API governance route tags 历史债清理

- 统一后端 route tag 单一事实源，消除 router-level tag 与 decorator-level tag 双轨并存。
- 增强 `scripts/validate-api-standard.py`，校验最终 OpenAPI operation tags 的唯一性、重复项和 kebab-case 命名。
- 重新导出 OpenAPI，并按需同步 Orval 生成客户端。
- 确认 Swagger UI 与管理端接口文档不再因重复 tags 出现治理噪声。

### Sprint 归档未完成 tasks 硬门禁

- 新增 `/sprint-archive` 前置 readiness 校验，按 `sprint.yaml` 范围检查 active 与 archived Change 的 `tasks.md`。
- 默认阻断未完成 task、缺失 `tasks.md` 或缺失 Change 目录，返回非零退出码并列出 blocker。
- 将 readiness gate 写入 Codex skill 与命令文档，确保 Sprint close、issue promote 和目录迁移前先执行。
- 补充 pytest 覆盖 active 未完成、archived 未完成、缺失 tasks 与全部完成通过路径。

### workflow-sync check 时间漂移幂等性修复

- 稳定 archived Change 归档时间推导，不再使用可变 `updated_at` 作为归档事实。
- 确保 workflow-sync 在 Markdown 正文无变化时不刷新 `updated_at`。
- 补充时间漂移回归测试，覆盖 issue trace `updated_at` 晚于真实归档记录的场景。
- 验证连续执行 `python scripts/sync-workflow-status.py --check` 保持 no delta。

### 管理端一次性密码复制交互修复

- 修复创建用户成功后初始密码弹窗的「复制密码」可靠性。
- 修复重置密码成功后新随机密码弹窗的「复制密码」可靠性。
- 增加复制成功/失败反馈，避免管理员误判。
- 在 Clipboard API 不可用或写入失败时提供手动复制指引或选中文本兜底。
- 保持一次性密码关闭后不可再次查看，不新增明文密码持久化或查询入口。

### 管理端日志审计 request_id 复制交互修复

- 修复日志审计页点击复制 `request_id` 时可能报错或失败的问题。
- Clipboard API 可用时写入完整 `request_id`，而非短展示文本。
- 在 Clipboard API 不可用、权限拒绝或写入失败时提供手动复制指引或等价兜底。
- 复制成功、失败和兜底反馈保持 fixed toast 或等价固定层，不造成日志列表布局位移。
- 复制失败或兜底路径不得误报 `copy_request_id` 成功埋点。

### 管理端修改密码策略失败提示修复

- 修复修改密码时新密码策略失败只显示泛化文案的问题。
- 明确展示长度、大小写、数字、特殊字符、弱密码、同原密码等具体失败原因。
- 让修改密码弹窗的规则提示与当前有效密码策略保持一致。
- 保持后端密码策略强度，不因提示优化放宽校验。
- 若 API 错误响应增加结构化策略详情，需同步 OpenAPI、Orval、接口文档和测试。

## API 变更（计划）

- 默认不新增或修改业务 API 路径、请求参数、响应结构或错误码语义。
- REQ-0029 不涉及后端分页 API、OpenAPI 或 Orval。
- BUG-0056 不涉及业务 API、OpenAPI 或 Orval。
- BUG-0057 预计会调整 OpenAPI operation tags，属于契约元数据治理。
- 若 REQ-0030 Change 仅更新文档、测试 checklist 与治理规范，不需要执行 Orval。
- 若后续实现改变 `/api/v1/admin/api-docs` 响应字段或 OpenAPI 契约，必须同步 `docs/03-api-index.md`、OpenAPI 与 Orval。
- BUG-0058 不涉及业务 API 或 OpenAPI 契约变更。
- BUG-0059 不涉及用户管理 API 请求路径、响应字段、错误码或 OpenAPI 契约变更。
- BUG-0060 不涉及日志审计 API 请求路径、响应字段、错误码或 OpenAPI 契约变更。
- BUG-0061 可能涉及 `POST /api/v1/admin/profile/password` 错误响应表达增强；若新增结构化失败项，必须同步 OpenAPI、Orval 与 `docs/03-api-index.md`。

## 数据库变更（计划）

- 不涉及数据库结构变更。
- REQ-0029 不涉及数据库结构变更。
- BUG-0056 不涉及数据库结构变更。
- BUG-0059 不得将一次性明文密码持久化到数据库、日志、审计事件或长期文档。
- BUG-0060 不修改 `request_logs`、`usage_events`、`audit_logs` 表结构。
- BUG-0061 不涉及数据库结构变更，不得记录或持久化明文密码。

## 部署注意事项

- 若 Change 仅沉淀 checklist，不需要 Docker Compose 验证。
- REQ-0029 为 Web 管理端共享 UI 组件与测试，不需要 Docker Compose 验证；实现阶段需运行相关 Vitest / Web build 或等价校验。
- BUG-0056 为流程脚本与文档门禁，不需要 Docker Compose 验证。
- 若 Change 修改 `src/web/nginx.conf`、Vite proxy 或生产代理说明，必须验证 Web 同源 `/docs`、`/redoc`、`/openapi.json` 不进入 SPA fallback。
- 生产环境不得因 Web 代理调整而放开 Swagger `Try It Out`。

## 已知风险

- REQ-0029 追加后 Sprint 估算达到 29 SP / 21.0 人天，略超双人两周开发容量；若容量不足，首批页面至少完成 2 页闭环，第三页转后续推广。
- BUG-0057 修复 Change 已创建但尚未实现；Sprint apply 时必须执行 `/opsx-apply fix-api-governance-route-tags-known-debt`。
- BUG-0056 修复 Change 已归档；Sprint 整体 archive 前仍必须运行 readiness gate，确保所有 Sprint 范围 Change 的 tasks 均完成。
- BUG-0058 修复 Change 已创建但尚未实现；Sprint apply 时必须执行 `/opsx-apply fix-workflow-sync-check-time-drift-idempotency`。
- BUG-0059 修复 Change 已创建但尚未实现；Sprint apply 时必须执行 `/opsx-apply fix-user-password-copy-not-working`。
- BUG-0060 修复 Change 已创建但尚未实现；Sprint apply 时必须执行 `/opsx-apply fix-audit-log-request-id-copy-error`。
- BUG-0061 修复 Change 已创建但尚未实现；Sprint apply 时必须执行 `/opsx-apply fix-change-password-policy-error-message`。
- BUG-0059 涉及浏览器 Clipboard 权限差异，验收必须覆盖成功、失败和 API 不存在路径。
- BUG-0060 同样涉及浏览器 Clipboard 权限差异，验收必须覆盖成功、失败、API 不存在和 fixed toast 不位移。
- BUG-0061 可能牵涉前后端契约，需提前确认错误响应结构，避免前端再次硬编码失准。
- checklist 落点需在 design 中固定，否则可能在 API docs design、API governance 文档和知识库之间分散。

## 回滚说明

- 文档/checklist 类变更可通过回退对应 OpenSpec Change 与文档修改恢复。
- REQ-0029 可通过回退共享组件、分页工具迁移、首批页面接入和 `/design-system` 示例恢复；回退后必须确认已接入页面的原有指标卡和分页 DOM 不丢失。
- BUG-0056 可通过回退 `scripts/validate-sprint-archive-readiness.py`、对应测试与 `/sprint-archive` skill/命令文档恢复；但不建议移除该门禁，若误判应优先用 `--force` 并记录人工确认。
- 若后续涉及代理配置修改，回滚必须同时恢复 Web 代理配置并验证 `/api/`、`/media/`、`/openapi.json` 不回归。
- workflow-sync 工具链修复可通过回退对应脚本与测试修改恢复，并重新运行 `python scripts/sync-workflow-status.py --check` 确认衍生文档状态。
- BUG-0059 为 Web UI-only 修复，可回退 `ResetPasswordDialog` 相关改动与测试；回退后需重新人工验证创建用户/重置密码一次性密码交付链路。
- BUG-0060 为 Web UI-only 修复，可回退 `LogAuditPage` 复制函数和测试；回退后需保留通过日志详情手动复制 `request_id` 的临时规避说明。
- BUG-0061 若仅为 Web/UI 文案与规则展示修复，可回退前端组件与测试；若包含 API 错误响应结构调整，回滚必须同步恢复 OpenAPI、Orval 与接口文档。
