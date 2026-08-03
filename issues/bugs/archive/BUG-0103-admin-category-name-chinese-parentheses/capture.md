---
bug_id: BUG-0103-admin-category-name-chinese-parentheses
status: done
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 09:14:11
severity_hint: medium
environment: admin-category
related_requirement: REQ-0005-tile-category-management
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 管理后台瓷砖类目名称输入能力已存在，当前英文括号可用但中文括号“（）”不可用，是既有输入校验或保存能力对合法业务字符支持不一致，属于 BUG。
---

# 现象

管理后台瓷砖类目名称支持输入英文括号，但不支持中文括号 `（`、`）`。

# 复现步骤

1. 登录管理后台。
2. 进入瓷砖类目管理。
3. 新建或编辑类目名称，输入包含中文括号的名称，例如 `墙砖（哑光）`。
4. 保存并观察校验提示或保存结果。

# 期望 vs 实际

- 期望：类目名称允许输入并保存中文括号 `（`、`）`，与英文括号支持逻辑一致。
- 实际：包含中文括号的类目名称无法通过校验或无法正常保存。

# 影响范围

- 管理后台瓷砖类目新增、编辑表单。
- 类目名称校验、保存与展示。

# 初步线索

- 需要检查前端表单校验、后端 Pydantic Schema 或数据库约束中对类目名称字符集的限制。
- 修复时应保持现有长度、必填、重复名等约束不被放宽。

# 建议验收或复现要点

- [ ] 类目名称可输入并保存中文括号 `（`、`）`。
- [ ] 英文括号仍可正常输入并保存。
- [ ] 非法字符、空名称、超长名称等既有校验保持有效。
- [ ] 类目树、列表和详情展示中文括号无乱码或截断。

# 附件

- 暂无。
