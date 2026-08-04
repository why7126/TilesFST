---
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
title: usage docs 前置版本候选使用字符串排序可能选错版本
status: done
severity: medium
priority: P2
source: "/capture"
captured_via: capture
classification_rationale: "已有 usage docs 继承逻辑要求选择前一个已生成使用文档版本，但当前实现使用字符串排序；在 v0.10.0 与 v0.9.0 等 SemVer 场景下可能偏离预期，属于既有治理脚本潜在缺陷。"
created_at: 2026-08-03 23:11:28
updated_at: 2026-08-04 09:31:30
related_requirement: REQ-0088-versioned-product-usage-docs
related_bug: null
iteration: null
openspec_changes: []
---

# BUG-0111 usage docs 前置版本候选使用字符串排序可能选错版本

## 原始描述

现在候选版本用的是字符串排序，不是严格 SemVer 排序。`v0.3.4`、`v0.3.5` 这类没问题，但未来如果出现 `v0.10.0` 和 `v0.9.0`，字符串排序可能选错。这块如果要更稳，适合后续提一个小的治理修正 Change，把 `previous_usage_docs_version()` 改成 SemVer 解析排序。

## 分类分析

| 字段 | 内容 |
|---|---|
| 类型倾向 | BUG |
| 判断依据 | `scripts/generate-usage-docs.py` 已实现前置 usage docs 版本选择，但排序方式可能不符合 SemVer 语义。 |
| 影响范围 | release usage docs 生成、Mintlify 投影、`usage-docs/manifest.json source_version`、发布文档继承完整性校验。 |
| 严重程度 | medium |
| 优先级 | P2 |

## 复现或验证要点

- 构造或测试存在 `releases/v0.9.0/usage-docs/` 与 `releases/v0.10.0/usage-docs/` 的候选集。
- 调用 `previous_usage_docs_version("v0.11.0")`，确认返回 SemVer 最大且小于当前版本的已生成 usage docs 版本。
- 确认缺失相邻版本 usage docs 时仍会继续向更早的已生成版本查找。
- 确认 prerelease 或带后缀版本的排序策略有明确规则，至少不破坏现有 `v0.3.x` 场景。

## 建议修复方向

- 将 `previous_usage_docs_version()` 从字符串排序改为 SemVer 解析排序。
- 增加覆盖 `v0.9.0`、`v0.10.0`、缺失相邻版本、当前版本排除的单元测试。
- 保持 `source_version` 与 validation 的完整页面集继承规则不变。
