---
change_id: fix-admin-category-name-chinese-parentheses
source_bug: BUG-0103-admin-category-name-chinese-parentheses
acceptance_status: not_started
created_at: 2026-08-03 08:32:46
updated_at: 2026-08-03 08:32:46
---

# Acceptance

- AC-001：管理后台新增类目时，名称 `墙砖（哑光）` 可保存并完整展示。
- AC-002：管理后台编辑类目时，名称 `地砖（防滑）` 可保存，刷新后仍完整保留中文括号。
- AC-003：包含英文括号的类目名称仍可正常保存和展示。
- AC-004：空名称、超长名称、同层级重复名称、换行、制表符和不可见控制字符仍被拒绝。
- AC-005：前端表单校验与后端接口校验对中文括号保持一致。
- AC-006：类目树、列表、详情和选择器展示中文括号名称时不乱码、不截断、不撑破布局。

## 验收结果回填

```yaml
acceptance_status: not_started
accepted_at: null
accepted_by: null
source_sprint: null
evidence: []
failed_items: []
notes: 待 opsx-apply 和后续验收回填。
```
