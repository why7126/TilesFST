---
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
title: usage docs 前置版本候选使用字符串排序可能选错版本
review_status: approved
reviewed_at: 2026-08-04 08:23:49
reviewed_by: operator
created_at: 2026-08-04 08:23:49
updated_at: 2026-08-04 08:23:49
---

# Review

## 评审结论

确认修复，状态批准为 `approved`。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 现有实现使用字符串排序，SemVer 位数变化时可能选择错误来源版本。 |
| 严重等级合理 | 通过 | `medium` 合理；影响发布治理和 usage docs 继承可信度，不影响运行时业务功能。 |
| 回归验收明确 | 通过 | acceptance 已覆盖 SemVer 排序、跳过未生成版本、排除当前版本、完整页面集继承和现有场景兼容。 |
| 是否需 hotfix 路径 | 不需要 | 当前版本尚未进入 `v0.10.0` 等高风险区间，可按普通治理修复进入 Sprint。 |

## 后续动作

- 可执行 `/bug-opsx BUG-0111` 创建 OpenSpec 修复 Change。
- 修复 Change 进入 Sprint 后再执行实现。
