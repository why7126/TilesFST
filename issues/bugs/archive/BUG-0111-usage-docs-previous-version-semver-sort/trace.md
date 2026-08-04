---
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
status: done
lifecycle_stage: archive
severity: medium
priority: P2
created_at: 2026-08-03 23:11:28
updated_at: 2026-08-04 09:37:32
lifecycle:
  captured: 2026-08-03 23:11:28
  generated: 2026-08-04 08:18:44
  completed: 2026-08-04 08:20:02
  reviewed: 2026-08-04 08:23:49
  approved: 2026-08-04 08:23:49
  sprint_joined: null
  done: null
iteration: null
openspec_changes:
  - change_id: fix-usage-docs-previous-version-semver-sort
    type: fix
    status: archived
related_requirement: REQ-0088-versioned-product-usage-docs
related_bug: null
---

# BUG-0111 usage docs 前置版本候选使用字符串排序可能选错版本

```yaml
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
status: done
severity: medium
priority: P2
created_at: 2026-08-03 23:11:28
updated_at: 2026-08-04 08:37:23
lifecycle:
  captured: 2026-08-03 23:11:28
  generated: 2026-08-04 08:18:44
  completed: 2026-08-04 08:20:02
  reviewed: 2026-08-04 08:23:49
  approved: 2026-08-04 08:23:49
  sprint_joined: null
  done: null
iteration: null
openspec_changes:
  - change_id: fix-usage-docs-previous-version-semver-sort
    type: fix
    status: archived
related_requirement: REQ-0088-versioned-product-usage-docs
related_bug: null
```

## 摘要

`scripts/generate-usage-docs.py` 的 `previous_usage_docs_version()` 当前按字符串排序选择前一个已生成 usage docs 的版本。该方式在普通 `v0.3.x` 场景表现正常，但遇到 `v0.10.0` 与 `v0.9.0` 等 SemVer 版本时可能选错继承来源，进而影响新版本 usage docs 的完整页面集继承。

## 影响范围

- 发布使用文档生成脚本。
- `releases/vX.Y.Z/usage-docs/manifest.json` 的 `source_version`。
- `mintlify/docs/vX.Y.Z/` 与 `mintlify/docs/latest/` 投影来源。
- usage docs 完整页面集继承门禁。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-04 09:31:38 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-usage-docs-previous-version-semver-sort） |
| 2026-08-04 09:30:26 | /opsx-archive | Change `fix-usage-docs-previous-version-semver-sort` 已归档，状态同步完成。 |
| 2026-08-04 08:56:50 | /opsx-apply | Change `fix-usage-docs-previous-version-semver-sort` apply 完成，已 archive。 |
| 2026-08-04 08:28:22 | /bug-opsx | 创建 OpenSpec Change `fix-usage-docs-previous-version-semver-sort`。 |
| 2026-08-04 08:24:14 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-04 08:23:49 | /bug-review --approve | 评审通过，确认需要修复。 |
| 2026-08-04 08:20:02 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态曾推进为 review_ready，现已闭环。 |
| 2026-08-04 08:18:44 | /bug-generate | 生成 bug.md，完成初稿生成，现已闭环。 |
| 2026-08-03 23:11:28 | /capture | 记录 usage docs 前置版本候选 SemVer 排序缺陷。 |

- 2026-08-04 09:30:26 workflow-sync：状态同步为 done（Change archived）
