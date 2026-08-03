---
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
status: captured
severity: medium
priority: P2
created_at: 2026-08-03 23:11:28
updated_at: 2026-08-03 23:11:28
lifecycle:
  captured: 2026-08-03 23:11:28
  generated: null
  completed: null
  reviewed: null
  approved: null
  in_sprint: null
  done: null
iteration: null
openspec_changes: []
related_requirement: REQ-0088-versioned-product-usage-docs
related_bug: null
---

# BUG-0111 usage docs 前置版本候选使用字符串排序可能选错版本

```yaml
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
status: captured
severity: medium
priority: P2
created_at: 2026-08-03 23:11:28
updated_at: 2026-08-03 23:11:28
lifecycle:
  captured: 2026-08-03 23:11:28
  generated: null
  completed: null
  reviewed: null
  approved: null
  in_sprint: null
  done: null
iteration: null
openspec_changes: []
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
| 2026-08-03 23:11:28 | /capture | 记录 usage docs 前置版本候选 SemVer 排序缺陷。 |
