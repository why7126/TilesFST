---
bug_id: BUG-0103-admin-category-name-chinese-parentheses
acceptance_status: passed
created_at: 2026-08-03 08:22:14
updated_at: 2026-08-03 20:52:16
---

# 验收标准

## AC-001 中文括号类目名称可保存

- GIVEN 管理员登录管理后台并进入瓷砖类目管理
- WHEN 新建类目并输入名称 `墙砖（哑光）`
- THEN 类目应保存成功
- AND 类目树、列表和详情应完整显示 `墙砖（哑光）`

## AC-002 编辑类目名称支持中文括号

- GIVEN 已存在一个瓷砖类目
- WHEN 管理员编辑该类目名称为包含中文括号的文本，例如 `地砖（防滑）`
- THEN 保存应成功
- AND 刷新页面后名称仍应完整保留中文括号

## AC-003 英文括号能力不回退

- GIVEN 管理员新建或编辑瓷砖类目
- WHEN 类目名称包含英文括号，例如 `墙砖(哑光)`
- THEN 保存和展示仍应正常

## AC-004 既有基础校验保持有效

- GIVEN 管理员新建或编辑瓷砖类目
- WHEN 名称为空、超过长度限制、与同级类目重复，或包含仍不允许的非法字符
- THEN 系统应继续按既有规则拦截并给出明确提示
- AND 不应因为支持中文括号而放宽其他名称校验约束

## AC-005 前后端校验一致

- GIVEN 前端表单和后端接口均存在类目名称校验
- WHEN 提交包含中文括号的合法名称
- THEN 前端不应误拦截
- AND 后端不应返回名称字符非法类错误
- AND 若后端仍拒绝请求，前端应展示明确错误信息

## AC-006 回归范围覆盖

- SHOULD 覆盖管理后台类目新增、编辑、类目树展示、类目列表展示和详情读取。
- SHOULD 覆盖中文括号、英文括号、中文字符、数字、空名称、超长名称、重复名称和非法字符。
- SHOULD 补充或更新前端表单测试、后端类目接口测试或等价回归验证。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: fix-admin-category-name-chinese-parentheses
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

