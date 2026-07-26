---
created_at: 2026-07-05 15:09:02
updated_at: 2026-07-05 15:09:02
---

# Change: fix-workflow-sync-check-time-drift-idempotency

## Why

BUG-0058 记录了 `workflow-sync --check` 在已归档 Sprint Scope 表中出现时间漂移的问题。漂移来自 archived Change 归档时间与文档维护时间混用：同步过程刷新 issue trace 或 change trace 的 `updated_at` 后，后续 `--check` 可能把该可变时间误判为归档事实，导致无业务变化也报告 drift。

该问题会降低 `python scripts/sync-workflow-status.py --check` 的可信度，并影响 Sprint 归档审计、CI 校验和人工验收判断。

## What Changes

- 稳定 archived Change 的归档时间推导，禁止使用 issue trace 或 change trace frontmatter `updated_at` 作为归档事实源。
- 调整 workflow-sync Markdown 持久化策略：渲染结果与原文一致时，不仅不写文件，也不得刷新 frontmatter `updated_at`。
- 增加时间漂移回归测试，覆盖可变 `updated_at` 晚于真实归档事实、以及无正文变化时 `persist_markdown` 不 touch 的场景。
- 验证连续执行 `workflow-sync --check` 保持 no delta。

## Capabilities

- Modified: `testing`

## Impact

- 影响脚本：`scripts/sync-workflow-status.py` 及其 workflow-sync 辅助模块。
- 影响测试：新增或更新 workflow-sync 时间漂移回归测试。
- 不影响后端业务 API、请求/响应结构、错误码或 OpenAPI 契约。
- 不影响 SQLite 表结构、Pydantic Schema、Web 管理端、店主 Web 或小程序。
- 不需要执行 Orval。
- 不需要 Docker Compose 验证。

## Rollback Plan

- 若修复导致 workflow-sync 状态推导异常，回退本 Change 对 workflow-sync 脚本及测试的修改。
- 回退后重新运行 `python scripts/sync-workflow-status.py --check`，确认衍生文档与回退后的脚本行为一致。
- 若已写入 Sprint 或 BUG trace 的派生字段出现不一致，重新执行对应 workflow-sync 事件同步恢复。
