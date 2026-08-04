---
change_id: fix-usage-docs-previous-version-semver-sort
type: fix
status: applied
source_bug: BUG-0111-usage-docs-previous-version-semver-sort
created_at: 2026-08-04 08:28:22
updated_at: 2026-08-04 08:56:25
sprint: sprint-019
---

# Change Trace

## 基本信息

```yaml
change_id: fix-usage-docs-previous-version-semver-sort
type: fix
status: applied
source_bug: BUG-0111-usage-docs-previous-version-semver-sort
related_requirement: REQ-0088-versioned-product-usage-docs
capabilities:
  - product-release-management
created_at: 2026-08-04 08:28:22
updated_at: 2026-08-04 08:56:25
sprint: sprint-019
```

## 来源

- BUG：`BUG-0111-usage-docs-previous-version-semver-sort`
- 父需求：`REQ-0088-versioned-product-usage-docs`
- 根因：usage docs 前置版本候选使用字符串排序，SemVer 位数变化时可能选错来源版本。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-04 08:28:22 | /bug-opsx | 从 BUG-0111 创建修复 Change。 |
| 2026-08-04 08:56:25 | /opsx-apply | 实现 usage docs 前置版本 SemVer 排序、manifest 过滤、回归测试与发布文档说明。 |

## 知识沉淀评估

本缺陷未造成已发布 usage docs 快照污染、线上事故或客户可见影响；长期治理点已沉淀到 `tests/test_release_validation.py` 回归测试和 `releases/README.md` 发布规则中，因此本次不新增 `docs/knowledge-base/incidents/` 条目。
