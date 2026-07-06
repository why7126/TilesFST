---
created_at: 2026-07-04 22:30:20
updated_at: 2026-07-06 16:06:23
title: Sprint 005 发布说明
purpose: 记录 Sprint 005 交付能力与发布注意事项（初稿）
content: 基于 REQ-0030-api-docs-swagger-policy-checklist、BUG-0057-api-governance-tags-known-debt、BUG-0058-workflow-sync-check-time-drift-idempotency 与 BUG-0059-user-password-copy-not-working
source: /sprint-propose REQ-0030；/sprint-propose BUG-0057 纳入 sprint-005；/sprint-propose BUG-0058 纳入 sprint-005；/sprint-propose BUG-0059 纳入 sprint-005
update_method: Sprint 完成或范围变更时更新
owner: 项目负责人
status: draft
---

# Sprint 005 发布说明

## 版本信息

| 字段 | 内容 |
|---|---|
| Sprint | sprint-005 |
| 关联需求 | REQ-0030-api-docs-swagger-policy-checklist |
| 关联 BUG | BUG-0057-api-governance-tags-known-debt；BUG-0058-workflow-sync-check-time-drift-idempotency；BUG-0059-user-password-copy-not-working |
| 关联 Change | REQ-0030: `update-api-docs-swagger-policy-checklist`；BUG-0057: `fix-api-governance-route-tags-known-debt`；BUG-0058: `fix-workflow-sync-check-time-drift-idempotency`；BUG-0059: `fix-user-password-copy-not-working` |
| 计划周期 | 2026-07-04 22:30:20 ~ 2026-07-18 22:30:20 |

<!-- workflow-sync:release-status:start -->
| 发布状态 | **实现进行中（In progress）** |
<!-- workflow-sync:release-status:end -->

## 计划交付

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

## API 变更（计划）

- 默认不新增或修改业务 API 路径、请求参数、响应结构或错误码语义。
- BUG-0057 预计会调整 OpenAPI operation tags，属于契约元数据治理。
- 若 REQ-0030 Change 仅更新文档、测试 checklist 与治理规范，不需要执行 Orval。
- 若后续实现改变 `/api/v1/admin/api-docs` 响应字段或 OpenAPI 契约，必须同步 `docs/03-api-index.md`、OpenAPI 与 Orval。
- BUG-0058 不涉及业务 API 或 OpenAPI 契约变更。
- BUG-0059 不涉及用户管理 API 请求路径、响应字段、错误码或 OpenAPI 契约变更。

## 数据库变更（计划）

- 不涉及数据库结构变更。
- BUG-0059 不得将一次性明文密码持久化到数据库、日志、审计事件或长期文档。

## 部署注意事项

- 若 Change 仅沉淀 checklist，不需要 Docker Compose 验证。
- 若 Change 修改 `src/web/nginx.conf`、Vite proxy 或生产代理说明，必须验证 Web 同源 `/docs`、`/redoc`、`/openapi.json` 不进入 SPA fallback。
- 生产环境不得因 Web 代理调整而放开 Swagger `Try It Out`。

## 已知风险

- BUG-0057 修复 Change 已创建但尚未实现；Sprint apply 时必须执行 `/opsx-apply fix-api-governance-route-tags-known-debt`。
- BUG-0058 修复 Change 已创建但尚未实现；Sprint apply 时必须执行 `/opsx-apply fix-workflow-sync-check-time-drift-idempotency`。
- BUG-0059 修复 Change 已创建但尚未实现；Sprint apply 时必须执行 `/opsx-apply fix-user-password-copy-not-working`。
- BUG-0059 涉及浏览器 Clipboard 权限差异，验收必须覆盖成功、失败和 API 不存在路径。
- checklist 落点需在 design 中固定，否则可能在 API docs design、API governance 文档和知识库之间分散。

## 回滚说明

- 文档/checklist 类变更可通过回退对应 OpenSpec Change 与文档修改恢复。
- 若后续涉及代理配置修改，回滚必须同时恢复 Web 代理配置并验证 `/api/`、`/media/`、`/openapi.json` 不回归。
- workflow-sync 工具链修复可通过回退对应脚本与测试修改恢复，并重新运行 `python scripts/sync-workflow-status.py --check` 确认衍生文档状态。
- BUG-0059 为 Web UI-only 修复，可回退 `ResetPasswordDialog` 相关改动与测试；回退后需重新人工验证创建用户/重置密码一次性密码交付链路。
