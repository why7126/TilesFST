---
created_at: 2026-07-05 15:09:02
updated_at: 2026-07-05 15:09:02
---

# Design: workflow-sync check 时间漂移幂等性修复

## 背景

BUG-0058 的漂移集中在已归档 Change 渲染到 Sprint Scope 表时的时间字段。归档时间是事实时间，应该来自归档动作或归档目录；`updated_at` 是文档维护时间，会随同步、补字段或人工编辑变化，不能作为归档事实。

## Root Cause

- archived Change 归档时间推导允许读取 issue trace 或 change trace frontmatter `updated_at`。
- workflow-sync 写入 Markdown 时，在正文无变化或仅派生内容一致的情况下仍可能刷新 `updated_at`。
- 回归测试没有覆盖“可变文档维护时间晚于真实归档时间”的场景，导致 `--check` 幂等性缺口没有被自动捕获。

## Fix Strategy

### 归档时间事实源

归档时间解析顺序必须只使用稳定事实源：

1. trace/lifecycle 中明确记录的 archived / completed / done 时间。
2. 变更记录或归档记录中明确的归档动作时间。
3. `openspec/changes/archive/YYYY-MM-DD-*` 或等价归档目录日期作为兜底。

禁止将 issue trace 或 change trace frontmatter `updated_at` 作为 archived Change 的归档时间事实源。若只能读取到文档维护时间，渲染应降级为空或目录日期兜底，而不是引入漂移。

### Markdown 持久化幂等

`persist_markdown` 或等价写入辅助逻辑在写文件前应比较最终渲染内容：

- 当目标文件内容与渲染结果完全一致时，不写文件，不刷新 `updated_at`。
- 当需要补齐缺失的 `created_at` / `updated_at` 或正文确有变化时，才允许更新 `updated_at`。
- `--check` 模式只报告真实内容差异，不产生副作用。

### 回归测试

新增或更新 workflow-sync 专项测试：

- 构造 archived Change 的真实归档时间早于 issue/change trace `updated_at` 的 fixture，断言渲染结果使用稳定归档事实。
- 构造 Markdown 原文与渲染结果一致的场景，断言持久化函数不写文件且不刷新 `updated_at`。
- 连续执行 sync/check 路径，断言第二次 `--check` 无 delta。

## Compatibility

- API：无业务 API 变更；无请求、响应或错误码变更。
- Database：无 SQLite schema 或数据迁移变更。
- Web / 小程序 / 管理端：无运行时 UI 变更。
- Orval：无需执行。
- Docker Compose：无需验证；仅脚本与测试层变更。

## Validation

- `uv run pytest tests/test_workflow_sync_time_drift.py`
- `python scripts/sync-workflow-status.py --check`
- 再次执行 `python scripts/sync-workflow-status.py --check`，确认 no delta。
- `python scripts/validate-directory-structure.py`
