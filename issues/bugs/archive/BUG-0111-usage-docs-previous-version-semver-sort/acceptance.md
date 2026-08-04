---
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
title: usage docs 前置版本候选使用字符串排序可能选错版本
acceptance_status: passed
created_at: 2026-08-04 08:20:02
updated_at: 2026-08-04 23:12:32
---

# Acceptance

## 回归验收项

| AC | 验收项 | 预期结果 |
|---|---|---|
| AC-001 | SemVer 数值排序 | 当候选版本包含 `v0.9.0` 与 `v0.10.0` 时，生成 `v0.11.0` 应选择 `v0.10.0` 作为 `source_version`。 |
| AC-002 | 跳过未生成版本 | 当相邻上一版本不存在 `usage-docs/` 时，应继续向更早已生成 usage docs 的版本查找。 |
| AC-003 | 排除当前版本 | 当前生成目标版本即使已有目录或同名候选，也不得被选为自己的 `source_version`。 |
| AC-004 | 完整页面集继承 | 新版本 `manifest.pages` 必须包含来源版本的全部页面，除非有明确授权的页面删除记录。 |
| AC-005 | 兼容现有场景 | 当前 `v0.3.x` 已生成 usage docs 的继承行为保持不变。 |

## 建议测试

- 针对 `previous_usage_docs_version()` 增加单元测试，使用临时 release 目录构造 `v0.9.0`、`v0.10.0`、`v0.11.0`。
- 针对 `generate_usage_docs()` 增加轻量集成测试，确认 `release.json usage_docs.source_version` 与 `usage-docs/manifest.json source_version` 一致。
- 保留 `validate-usage-docs.py` 对来源版本页面集合完整继承的校验。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-04 23:12:32
accepted_by: workflow-sync
source_change: fix-usage-docs-previous-version-semver-sort
source_sprint: null
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

